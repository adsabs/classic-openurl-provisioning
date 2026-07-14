import argparse
import logging.config

import config as base_config

try:
    import local_config
except ImportError:
    local_config = None

from openurl.tasks import export_openurl_db, update_openurl_db

ACTIONS = {
    'updatedb': update_openurl_db,
    'exportdb': export_openurl_db,
}


def load_config():
    """
    Build the effective configuration dict from config.py, optionally
    overridden by local_config.py
    :return: dict of configuration values
    """
    conf = {key: getattr(base_config, key) for key in dir(base_config) if key.isupper()}
    if local_config is not None:
        conf.update({key: getattr(local_config, key) for key in dir(local_config) if key.isupper()})
    return conf


def main():
    parser = argparse.ArgumentParser(description='Institute OpenURL database utility')
    parser.add_argument('action', choices=sorted(ACTIONS.keys()), help='Action to perform')
    args = parser.parse_args()

    config = load_config()
    logging.config.dictConfig(config['INSTITUTE_LOGGING'])

    ACTIONS[args.action](config)


if __name__ == '__main__':
    main()
