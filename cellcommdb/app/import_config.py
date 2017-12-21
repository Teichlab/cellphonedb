import os
import yaml


def _load_yaml(yaml_name):
    with open(yaml_name, 'r') as stream:
        try:
            return yaml.load(stream)
        except yaml.YAMLError as exec:
            print(exec)


def _merge_configs(config_base, new_config):
    config = {**config_base, **new_config}
    for key in config_base:
        if isinstance(config_base[key], dict) and key in new_config:
            config[key] = _merge_configs(config_base[key], new_config[key])

    return config


def _load_config(environment: str, load_defaults) -> dict:
    config = {}
    if load_defaults:
        config = _load_yaml('cellcommdb/config/{}.yml'.format('base_config'))
    if environment:
        custom_config = _load_yaml('cellcommdb/config/{}.yml'.format(environment))
        config = _merge_configs(config, custom_config)

    return config


def _build_sqlalchemy_database_uri(database_config):
    return '{}://{}:{}@{}:{}/{}'.format(database_config['adapter'], database_config['user'],
                                        database_config['password'], database_config['host'],
                                        database_config['port'], database_config['db_name'])


def flask_config(environment, support, load_defaults):
    if support == 'yaml':
        flask_config = _flask_config_from_yaml(environment, load_defaults)
    elif support == 'environment_vars':
        flask_config = _flask_config_from_environment_vars(load_defaults)
    else:
        raise Exception('Non valid support defined {yaml,environment_vars}')

    return flask_config


def _flask_config_from_environment_vars(load_defaults):
    flask_config = {}
    if load_defaults:
        flask_config = _flask_config_from_yaml(None, load_defaults)

    config_keys = ['SECRET_KEY', 'SQLALCHEMY_DATABASE_URI', 'API_PREFIX', 'DEBUG', 'SQLALCHEMY_TRACK_MODIFICATIONS']

    for config_key in config_keys:
        if os.environ.get(config_key):
            flask_config[config_key] = os.environ.get(config_key)
    return flask_config


def _flask_config_from_yaml(environment, load_defaults):
    config = _load_config(environment, load_defaults)

    flask_config = {
        'SECRET_KEY': config['flask']['secret_key'],
        'SQLALCHEMY_DATABASE_URI': _build_sqlalchemy_database_uri(config['database']),
        'API_PREFIX': config['api']['prefix'],
        'DEBUG': config['flask']['secret_key'],
        'SQLALCHEMY_TRACK_MODIFICATIONS': config['flask']['sqlalchemy_track_modifications']
    }
    return flask_config
