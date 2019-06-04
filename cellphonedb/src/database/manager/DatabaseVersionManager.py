import io
import json
import os
import zipfile
from distutils.dir_util import copy_tree
from distutils.file_util import copy_file
from distutils.version import LooseVersion
from typing import Union

import requests

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cellphonedb_app import core_dir
from cellphonedb.src.app.cpdb_app import create_app
from cellphonedb.src.exceptions.NoReleasesException import NoReleasesException
from cellphonedb.src.local_launchers.local_collector_launcher import LocalCollectorLauncher

cpdb_releases = '~/.cpdb/releases'
database_file = 'cellphone.db'


def _ensure_core_version_in_user_dbs():
    with open(os.path.join(core_dir, 'metadata.json')) as metadata_file:
        metadata = json.load(metadata_file)
        core_version = metadata.get('database_version', 'core')

        user_databases_prefix = os.path.expanduser(cpdb_releases)
        dest_folder = os.path.join(user_databases_prefix, core_version)
        database_file_location = os.path.join(dest_folder, database_file)

        if os.path.isfile(database_file_location):
            return

        os.makedirs(dest_folder, exist_ok=True)

        copy_file(os.path.join(core_dir, database_file), dest_folder)
        copy_tree(os.path.join(core_dir, 'data'), dest_folder)


def find_database_for(value: str) -> str:
    file_candidate = os.path.expanduser(value)

    if os.path.exists(file_candidate):
        # todo: warning is perhaps not appropriate, logger doesn't allow info at this point
        app_logger.warning('User selected database `{}` is available, using it'.format(file_candidate))
        return file_candidate

    _ensure_core_version_in_user_dbs()
    user_databases_prefix = os.path.expanduser(cpdb_releases)

    if not os.path.isdir(user_databases_prefix):
        app_logger.error('No downloaded databases found, run the `tools download_database` command from the cli first')
        # todo: should we abort in this case?
        exit(1)

    if value == 'latest' or not value:
        available = list_local_versions()
        latest_available = available[-1]
        app_logger.warning('Latest dowloaded version is `{}`, using it'.format(latest_available))
        value = latest_available

    downloaded_candidate = os.path.join(user_databases_prefix, value, database_file)
    valid_database = os.path.exists(downloaded_candidate)

    if valid_database:
        # todo: warning is perhaps not appropriate, logger doesn't allow info at this point
        app_logger.warning('User selected downloaded database `{}` is available, using it'.format(value))
    else:
        app_logger.warning('User selected database `{}` not available, trying to download it'.format(value))
        download_database(value)
        return find_database_for(value)

    return downloaded_candidate


def collect_database(database, output_path):
    database_file_path = os.path.join(output_path, database)

    app = create_app(verbose=True, database_file=database_file_path, collecting=True)
    app.database_manager.database.drop_everything()
    app.database_manager.database.create_all()

    getattr(LocalCollectorLauncher(database_file_path), 'all')(None)


def download_database(version):
    try:
        if not version or version == 'latest':
            latest_release = _latest_release()

            version = latest_release['tag']
            zip_to_download = latest_release['url']
        else:
            releases = _list_releases()

            if version not in releases:
                app_logger.error('Unavailable version selected')
                app_logger.error('Available versions are: {}'.format(', '.join(releases.keys())))
                exit(1)

            zip_to_download = releases[version]['url']

        print('Downloading {} release of database'.format(version))

        output_folder = os.path.expanduser('{}/{}'.format(cpdb_releases, version))
        os.makedirs(output_folder, exist_ok=True)

        zip_response = requests.get(zip_to_download)
        with zipfile.ZipFile(io.BytesIO(zip_response.content)) as thezip:
            root_folder = thezip.namelist()[0]
            for name in thezip.namelist():
                if name.endswith('/'):
                    continue

                file_folder = os.path.dirname(name)
                file_name = os.path.basename(name)

                dest_folder = os.path.realpath(os.path.join(output_folder, os.path.relpath(file_folder, root_folder)))
                dest_file = os.path.join(dest_folder, file_name)
                os.makedirs(dest_folder, exist_ok=True)

                with thezip.open(name) as zf:
                    with open(dest_file, 'wb') as fw:
                        fw.write(zf.read())

    except NoReleasesException:
        print('There are no versions available (or connection could not be made to server to retrieve them)')
        exit(1)


def list_local_versions():
    releases_folder = os.path.expanduser(cpdb_releases)

    return sorted(os.listdir(releases_folder), key=LooseVersion)


def list_remote_database_versions():
    try:
        releases: dict = _list_releases()

        for idx, (_, version) in enumerate(releases.items()):
            note = ' *latest' if idx == 0 else ''
            print('version {}{}: released: {}, url: {}'.format(version['tag'], note, version['date'], version['link']))

    except NoReleasesException:
        print('There are no versions available (or connection could not be made to server to retrieve them)')
        exit(1)


def list_local_database_versions():
    releases: list = list_local_versions()

    if not releases:
        print('There are no versions available')
        exit(1)

    for idx, version in enumerate(reversed(releases)):
        note = ' *latest' if idx == 0 else ''
        print('version {}{}'.format(version, note))


def _list_releases():
    try:
        releases = _github_query('releases')

        if not releases:
            raise NoReleasesException()

        return _format_releases(*releases)

    except requests.exceptions.ConnectionError:
        raise NoReleasesException()


def _latest_release():
    try:
        latest_release = _github_query('latest')

        if not latest_release:
            raise NoReleasesException()

        return _format_release(latest_release)

    except requests.exceptions.ConnectionError:
        raise NoReleasesException()


def _github_query(kind) -> Union[dict, list]:
    queries = {
        'releases': 'https://api.github.com/repos/{}/{}/releases'.format('ydevs', 'cpdb-data'),
        'latest': 'https://api.github.com/repos/{}/{}/releases/latest'.format('ydevs', 'cpdb-data')
    }

    query = queries[kind]

    response = requests.get(query, headers={'Accept': 'application/vnd.github.v3+json'})

    if response.status_code != 200:
        raise NoReleasesException()

    return response.json()


def _format_releases(*releases) -> dict:
    return {item['tag_name']: _format_release(item) for item in releases}


def _format_release(item) -> dict:
    return {'url': item['zipball_url'],
            'tag': item['tag_name'],
            'date': item['published_at'],
            'link': item['html_url']}
