#coding:utf-8
"""load timeline.json files"""

import os
import json
import configparser

from utils.my_logging import my_get_logger

config = configparser.ConfigParser()
config.read('config/common.ini')
path_to_dump_timeline = config['path to dump']['timeline']

def load_timeline_user_id(user_id, logger=None):
    dirname = os.path.join(path_to_dump_timeline, str(user_id))
    if not os.path.exists(dirname):
        if logger is not None:
            logger.info(f'can not find dirname : {dirname}')
        return False
    timeline = []
    json_filenames = [elm for elm in sorted(os.listdir(dirname), key=lambda x:int(os.path.splitext(x)[0].split('_')[-1])) if elm.endswith('.json')]
    if logger is not None:
        logger.info(f'json_filenames : {json_filenames}')
    for json_filename in json_filenames:
        _timeline = load_timeline_json(os.path.join(dirname, json_filename))
        timeline.extend(_timeline)
    return timeline

def load_timeline_json(json_filename):
    """ load timeline json file
    json_filename: str : path to json file which contains timeline infomation
    return : list : timeline info
    """
    if os.path.exists(json_filename):
        timeline = json.load(open(json_filename))
    else:
        timeline = []
    return timeline

def main():
    """main func."""
    logger = my_get_logger(__name__, os.path.basename(__file__)+'.log')
    user_id = 87714006
    timeline = load_timeline_user_id(user_id, logger)
    logger.info(json.dumps(timeline, indent=2, sort_keys=True))

if __name__ == "__main__":
    main()
