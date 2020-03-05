#!/usr/bin/env python3

import io
import json
import os
import sys
import tempfile
import time
import traceback
from distutils.util import strtobool
from functools import wraps
from logging import INFO
from typing import Callable

import boto3
import pandas as pd
import pika

from cellphonedb.src.app import cpdb_app
from cellphonedb.src.core.exceptions.AllCountsFilteredException import AllCountsFilteredException
from cellphonedb.src.core.exceptions.EmptyResultException import EmptyResultException
from cellphonedb.src.core.exceptions.ThresholdValueException import ThresholdValueException
from cellphonedb.src.core.utils.subsampler import Subsampler
from cellphonedb.src.database.manager.DatabaseVersionManager import list_local_versions, find_database_for
from cellphonedb.src.exceptions.ParseCountsException import ParseCountsException
from cellphonedb.src.exceptions.ParseMetaException import ParseMetaException
from cellphonedb.src.exceptions.PlotException import PlotException
from cellphonedb.src.exceptions.ReadFileException import ReadFileException
from cellphonedb.src.plotters.r_plotter import dot_plot, heatmaps_plot
from cellphonedb.utils import utils
from rabbit_logger import RabbitAdapter, RabbitLogger

rabbit_logger = RabbitLogger()

try:
    s3_access_key = os.environ['S3_ACCESS_KEY']
    s3_secret_key = os.environ['S3_SECRET_KEY']
    s3_bucket_name = os.environ['S3_BUCKET_NAME']
    s3_endpoint = os.environ['S3_ENDPOINT']
    rabbit_host = os.environ['RABBIT_HOST']
    rabbit_port = os.environ['RABBIT_PORT']
    rabbit_user = os.environ['RABBIT_USER']
    rabbit_password = os.environ['RABBIT_PASSWORD']
    jobs_queue_name = os.environ['RABBIT_JOB_QUEUE']
    result_queue_name = os.environ['RABBIT_RESULT_QUEUE']
    queue_type = os.environ['QUEUE_TYPE']


except KeyError as e:
    rabbit_logger.error('ENVIRONMENT VARIABLE {} not defined. Please set it'.format(e))
    exit(1)

verbose = bool(strtobool(os.getenv('VERBOSE', 'true')))

if verbose:
    rabbit_logger.setLevel(INFO)


def logger_for_job(job_id):
    return RabbitAdapter.logger_for(rabbit_logger, job_id)


def _track_success(f) -> Callable:
    @wraps(f)
    def wrapper(*args, **kwargs):
        logger = kwargs.get('logger', rabbit_logger)

        logger.info('calling {} method'.format(f.__name__))
        result = f(*args, **kwargs)
        logger.info('successfully called {} method'.format(f.__name__))
        return result

    return wrapper


def create_rabbit_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(
        host=rabbit_host,
        port=rabbit_port,
        virtual_host='/',
        credentials=credentials
    ))


s3_resource = boto3.resource('s3', aws_access_key_id=s3_access_key,
                             aws_secret_access_key=s3_secret_key,
                             endpoint_url=s3_endpoint)

s3_client = boto3.client('s3', aws_access_key_id=s3_access_key,
                         aws_secret_access_key=s3_secret_key,
                         endpoint_url=s3_endpoint)


def read_data_from_s3(filename: str, s3_bucket_name: str, index_column_first: bool):
    s3_object = s3_client.get_object(Bucket=s3_bucket_name, Key=filename)
    return utils.read_data_from_s3_object(s3_object, filename, index_column_first=index_column_first)


def write_data_in_s3(data: pd.DataFrame, filename: str):
    result_buffer = io.StringIO()
    data.to_csv(result_buffer, index=False, sep='\t')
    result_buffer.seek(0)

    # TODO: Find more elegant solution (connexion closes after timeout)
    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key,
                             aws_secret_access_key=s3_secret_key,
                             endpoint_url=s3_endpoint)

    s3_client.put_object(Body=result_buffer.getvalue().encode('utf-8'), Bucket=s3_bucket_name, Key=filename)


def write_image_to_s3(path: str, filename: str):
    _io = open(path, 'rb')

    # TODO: Find more elegant solution (connexion closes after timeout)
    s3_client = boto3.client('s3', aws_access_key_id=s3_access_key,
                             aws_secret_access_key=s3_secret_key,
                             endpoint_url=s3_endpoint)

    s3_client.put_object(Body=_io, Bucket=s3_bucket_name, Key=filename)


@_track_success
def dot_plot_results(means: str, pvalues: str, rows: str, columns: str, job_id: str):
    with tempfile.TemporaryDirectory() as output_path:
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(means)[-1]) as means_file:
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(pvalues)[-1]) as pvalues_file:
                with tempfile.NamedTemporaryFile() as rows_file:
                    with tempfile.NamedTemporaryFile() as columns_file:
                        _from_s3_to_temp(means, means_file)
                        _from_s3_to_temp(pvalues, pvalues_file)
                        _from_s3_to_temp(rows, rows_file)
                        _from_s3_to_temp(columns, columns_file)

                        output_name = 'plot__{}.png'.format(job_id)

                        dot_plot(means_path=means_file.name,
                                 pvalues_path=pvalues_file.name,
                                 output_path=output_path,
                                 output_name=output_name,
                                 rows=rows_file.name,
                                 columns=columns_file.name)

                        output_file = os.path.join(output_path, output_name)

                        if not os.path.exists(output_file):
                            raise PlotException('Could not generate output file for plot of type dot_plot')

                        response = {
                            'job_id': job_id,
                            'files': {
                                'plot': output_name,
                            },
                            'success': True
                        }

                        write_image_to_s3(output_file, output_name)

                        return response


@_track_success
def heatmaps_plot_results(meta: str, pvalues: str, pvalue: float, job_id: str):
    with tempfile.TemporaryDirectory() as output_path:
        with tempfile.NamedTemporaryFile(suffix=os.path.splitext(pvalues)[-1]) as pvalues_file:
            with tempfile.NamedTemporaryFile(suffix=os.path.splitext(meta)[-1]) as meta_file:
                _from_s3_to_temp(pvalues, pvalues_file)
                _from_s3_to_temp(meta, meta_file)

                count_name = 'plot_count__{}.png'.format(job_id)
                count_log_name = 'plot_count_log__{}.png'.format(job_id)

                count_network_name = 'count_network__{}.txt'.format(job_id)
                interactions_count_name = 'interactions_count__{}.txt'.format(job_id)

                heatmaps_plot(meta_file=meta_file.name,
                              pvalues_file=pvalues_file.name,
                              output_path=output_path,
                              count_name=count_name,
                              log_name=count_log_name,
                              count_network_filename=count_network_name,
                              interaction_count_filename=interactions_count_name,
                              pvalue=pvalue)

                output_count_file = os.path.join(output_path, count_name)
                output_count_log_file = os.path.join(output_path, count_log_name)
                output_count_network_file = os.path.join(output_path, count_network_name)
                output_interactions_count_file = os.path.join(output_path, interactions_count_name)

                if not os.path.exists(output_count_file) \
                        or not os.path.exists(output_count_log_file) \
                        or not os.path.exists(output_count_network_file) \
                        or not os.path.exists(output_interactions_count_file):
                    raise PlotException('Could not generate output file for plot of type heatmap_plot')

                response = {
                    'job_id': job_id,
                    'files': {
                        'count_plot': count_name,
                        'count_log_plot': count_log_name,
                        'count_network': count_network_name,
                        'interactions_sum': interactions_count_name,
                    },
                    'success': True
                }

                write_image_to_s3(output_count_file, count_name)
                write_image_to_s3(output_count_log_file, count_log_name)
                write_image_to_s3(output_count_network_file, count_network_name)
                write_image_to_s3(output_interactions_count_file, interactions_count_name)

                return response


def _from_s3_to_temp(key, file):
    data = s3_client.get_object(Bucket=s3_bucket_name, Key=key)
    file.write(data['Body'].read())
    file.seek(0)

    return file


@_track_success
def process_plot(method, properties, body, logger) -> dict:
    metadata = json.loads(body.decode('utf-8'))
    job_id = metadata['job_id']
    logger.info('New Plot Queued')

    plot_type = metadata.get('type', None)

    if plot_type == 'dot_plot':
        return dot_plot_results(metadata.get('file_means'),
                                metadata.get('file_pvalues'),
                                metadata.get('file_rows', None),
                                metadata.get('file_columns', None),
                                job_id
                                )

    if plot_type == 'heatmaps_plot':
        return heatmaps_plot_results(metadata.get('file_meta'),
                                     metadata.get('file_pvalues'),
                                     metadata.get('pvalue', 0.05),
                                     job_id
                                     )

    return {
        'job_id': job_id,
        'success': False,
        'error': {
            'id': 'UnknownPlotType',
            'message': 'Given plot type does not exist: {}'.format(plot_type)
        }
    }


@_track_success
def process_method(method, properties, body, logger) -> dict:
    metadata = json.loads(body.decode('utf-8'))
    job_id = metadata['job_id']
    logger.info('New Job Queued')
    meta = read_data_from_s3(metadata['file_meta'], s3_bucket_name, index_column_first=False)
    counts = read_data_from_s3(metadata['file_counts'], s3_bucket_name, index_column_first=True)

    subsampler = Subsampler(bool(metadata['log']),
                            int(metadata['num_pc']),
                            int(metadata['num_cells']) if metadata.get('num_cells', False) else None
                            ) if metadata.get('subsampling', False) else None

    database_version = metadata.get('database_version', 'latest')

    if database_version not in list_local_versions() + ['latest']:
        database_version = 'latest'

    app = cpdb_app.create_app(verbose=verbose, database_file=find_database_for(database_version))

    if metadata['iterations']:
        response = statistical_analysis(app, meta, counts, job_id, metadata, subsampler)
    else:
        response = non_statistical_analysis(app, meta, counts, job_id, metadata, subsampler)

    return response


@_track_success
def statistical_analysis(app, meta, counts, job_id, metadata, subsampler):
    pvalues, means, significant_means, deconvoluted = \
        app.method.cpdb_statistical_analysis_launcher(meta,
                                                      counts,
                                                      counts_data=metadata.get('counts_data', 'ensembl'),
                                                      threshold=float(metadata['threshold']),
                                                      iterations=int(metadata['iterations']),
                                                      debug_seed=-1,
                                                      threads=4,
                                                      result_precision=int(metadata['result_precision']),
                                                      pvalue=float(metadata.get('pvalue', 0.05)),
                                                      subsampler=subsampler,
                                                      )
    response = {
        'job_id': job_id,
        'files': {
            'pvalues': 'pvalues_simple_{}.txt'.format(job_id),
            'means': 'means_simple_{}.txt'.format(job_id),
            'significant_means': 'significant_means_simple_{}.txt'.format(job_id),
            'deconvoluted': 'deconvoluted_simple_{}.txt'.format(job_id),
        },
        'success': True
    }
    write_data_in_s3(pvalues, response['files']['pvalues'])
    write_data_in_s3(means, response['files']['means'])
    write_data_in_s3(significant_means, response['files']['significant_means'])
    write_data_in_s3(deconvoluted, response['files']['deconvoluted'])
    return response


@_track_success
def non_statistical_analysis(app, meta, counts, job_id, metadata, subsampler):
    means, significant_means, deconvoluted = \
        app.method.cpdb_method_analysis_launcher(meta,
                                                 counts,
                                                 counts_data=metadata.get('counts_data', 'ensembl'),
                                                 threshold=float(metadata['threshold']),
                                                 result_precision=int(metadata['result_precision']),
                                                 subsampler=subsampler,
                                                 )
    response = {
        'job_id': job_id,
        'files': {
            'means': 'means_simple_{}.txt'.format(job_id),
            'significant_means': 'significant_means_{}.txt'.format(job_id),
            'deconvoluted': 'deconvoluted_simple_{}.txt'.format(job_id),
        },
        'success': True
    }
    write_data_in_s3(means, response['files']['means'])
    write_data_in_s3(significant_means, response['files']['significant_means'])
    write_data_in_s3(deconvoluted, response['files']['deconvoluted'])
    return response


consume_more_jobs = True

credentials = pika.PlainCredentials(rabbit_user, rabbit_password)
connection = create_rabbit_connection()
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

jobs_runned = 0

while jobs_runned < 3 and consume_more_jobs:
    job = channel.basic_get(queue=jobs_queue_name, no_ack=True)

    if all(job):
        job_id = json.loads(job[2].decode('utf-8'))['job_id']
        job_logger = logger_for_job(job_id)
        try:
            if queue_type == 'plot':
                job_response = process_plot(*job, logger=job_logger)
            elif queue_type == 'method':
                job_response = process_method(*job, logger=job_logger)
            else:
                raise Exception('Unknown queue type')

            # TODO: Find more elegant solution
            connection = create_rabbit_connection()
            channel = connection.channel()
            channel.basic_qos(prefetch_count=1)

            channel.basic_publish(exchange='', routing_key=result_queue_name, body=json.dumps(job_response))
            job_logger.info('JOB PROCESSED')
        except (ReadFileException, ParseMetaException, ParseCountsException, ThresholdValueException,
                AllCountsFilteredException, EmptyResultException, PlotException) as e:
            error_response = {
                'job_id': job_id,
                'success': False,
                'error': {
                    'id': str(e),
                    'message': (' {}.'.format(e.description) if hasattr(e, 'description') and e.description else '') +
                               (' {}.'.format(e.hint) if hasattr(e, 'hint') and e.hint else '')

                }
            }
            print(traceback.print_exc(file=sys.stdout))
            job_logger.error('[-] ERROR DURING PROCESSING JOB')
            if connection.is_closed:
                connection = create_rabbit_connection()
                channel = connection.channel()
                channel.basic_qos(prefetch_count=1)
            channel.basic_publish(exchange='', routing_key=result_queue_name, body=json.dumps(error_response))
            job_logger.error(e)
        except Exception as e:
            error_response = {
                'job_id': job_id,
                'success': False,
                'error': {
                    'id': 'unknown_error',
                    'message': ''
                }
            }
            print(traceback.print_exc(file=sys.stdout))
            job_logger.error('[-] ERROR DURING PROCESSING JOB')
            if connection.is_closed:
                connection = create_rabbit_connection()
                channel = connection.channel()
                channel.basic_qos(prefetch_count=1)
            channel.basic_publish(exchange='', routing_key=result_queue_name, body=json.dumps(error_response))
            job_logger.error(e)

        jobs_runned += 1

    else:
        rabbit_logger.debug('Empty queue')

    time.sleep(1)
