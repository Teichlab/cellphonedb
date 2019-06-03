import io
import os
import zipfile
from typing import Union

import requests

from cellphonedb.src.app.app_logger import app_logger
from cellphonedb.src.app.cpdb_app import create_app
from cellphonedb.src.exceptions.NoReleasesException import NoReleasesException
from cellphonedb.src.local_launchers.local_collector_launcher import LocalCollectorLauncher


def collect_database(database, output_path):
    database_file = os.path.join(output_path, database)

    app = create_app(verbose=True, database_file=database_file, collecting=True)
    app.database_manager.database.drop_everything()
    app.database_manager.database.create_all()

    getattr(LocalCollectorLauncher(database_file), 'all')(None)


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

        output_folder = os.path.expanduser('~/.cpdb/releases/{}'.format(version))
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


def list_database_versions():
    try:
        releases: dict = _list_releases()

        for idx, (_, version) in enumerate(releases.items()):
            note = ' *latest' if idx == 0 else ''
            print('version {}{}: released: {}, url: {}'.format(version['tag'], note, version['date'], version['link']))

    except NoReleasesException:
        print('There are no versions available (or connection could not be made to server to retrieve them)')
        exit(1)


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
