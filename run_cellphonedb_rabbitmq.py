import os
import io
import json
import time

import pandas as pd

import boto3
import pika

from cellphonedb.app import app_config
from cellphonedb.core.CellphonedbSqlalchemy import CellphonedbSqlalchemy
from cellphonedb.app.app_logger import app_logger

try:
    s3_access_key = os.environ['S3_ACCESS_KEY']
    s3_secret_key = os.environ['S3_SECRET_KEY']
    s3_bucket_name = os.environ['S3_BUCKET_NAME']
    s3_endpoint = os.environ['S3_ENDPOINT']
    rabbit_host = os.environ['RABBIT_HOST']
    rabbit_port = os.environ['RABBIT_PORT']
    jobs_queue_name = os.environ['RABBIT_JOB_QUEUE']
    result_queue_name = os.environ['RABBIT_RESULT_QUEUE']


except KeyError as e:
    app_logger.error('ENVIRONMENT VARIABLE {} not defined. Please set it'.format(e))
    exit(1)

config = app_config.AppConfig()
app = CellphonedbSqlalchemy(config.get_cellphone_core_config())

s3_resource = boto3.resource('s3', aws_access_key_id=s3_access_key,
                             aws_secret_access_key=s3_secret_key,
                             endpoint_url=s3_endpoint)
s3_client = boto3.client('s3', aws_access_key_id=s3_access_key,
                         aws_secret_access_key=s3_secret_key,
                         endpoint_url=s3_endpoint)


def read_data_from_s3(filename: str, s3_bucket_name: str):
    object = s3_client.get_object(Bucket=s3_bucket_name, Key=filename)
    bytestream = io.BytesIO(object['Body'].read())
    return pd.read_csv(bytestream, sep='\t', encoding='utf-8', index_col=0)


def write_data_in_s3(data: pd.DataFrame, filename: str):
    result_buffer = io.StringIO()
    data.to_csv(result_buffer, index=False, sep='\t')
    result_buffer.seek(0)

    encoding = result_buffer
    s3_client.put_object(Body=encoding.getvalue().encode('utf-8'), Bucket=s3_bucket_name, Key=filename)


def process_job(method, properties, body) -> dict:
    metadata = json.loads(body.decode('utf-8'))

    meta = read_data_from_s3(metadata['file_meta'], s3_bucket_name)
    counts = read_data_from_s3(metadata['file_counts'], s3_bucket_name)
    counts = counts.astype(dtype=pd.np.float64, copy=False)

    pvalues_simple, means_simple, significant_means_simple, means_pvalues_simple, deconvoluted_simple = \
        app.method.cluster_statistical_analysis_launcher(meta,
                                                         counts,
                                                         threshold=float(metadata['threshold'] / 100),
                                                         iterations=int(metadata['iterations']),
                                                         debug_seed=-1,
                                                         threads=4)

    job_id = metadata['job_id']
    response = {
        'job_id': job_id,
        'files': {
            'pvalues_simple': 'pvalues_simple_{}.txt'.format(job_id),
            'means_simple': 'means_simple_{}.txt'.format(job_id),
            'significant_means_simple': 'significant_means_simple_{}.txt'.format(job_id),
            'means_pvalues_simple': 'means_pvalues_simple_{}.txt'.format(job_id),
            'deconvoluted_simple': 'deconvoluted_simple_{}.txt'.format(job_id),
        },
        'success': True
    }

    write_data_in_s3(pvalues_simple, response['files']['pvalues_simple'])
    write_data_in_s3(means_simple, response['files']['means_simple'])
    write_data_in_s3(significant_means_simple, response['files']['significant_means_simple'])
    write_data_in_s3(means_pvalues_simple, response['files']['means_pvalues_simple'])
    write_data_in_s3(deconvoluted_simple, response['files']['deconvoluted_simple'])

    return response


credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=rabbit_host,
    port=rabbit_port,
    virtual_host='/',
    credentials=credentials
))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

while True:
    job = channel.basic_get(queue=jobs_queue_name, no_ack=True)

    if all(job):
        try:
            job_response = process_job(*job)
            channel.basic_publish(exchange='', routing_key=result_queue_name, body=json.dumps(job_response))
            app_logger.info('JOB %s PROCESSED' % job_response['job_id'])
        except Exception as e:
            error_response = {
                'job_id': json.loads(job[2].decode('utf-8'))['job_id'],
                'success': False,
                'error': {
                    'id': 'unknown_error',
                    'message': 'mensage '
                }
            }
            app_logger.error('[-] ERROR DURING PROCESSING JOB %s' % error_response['job_id'])
            channel.basic_publish(exchange='', routing_key=result_queue_name, body=json.dumps(error_response))
            app_logger.error(e)

    else:
        app_logger.info('Empty queue')

    time.sleep(2)
