#coding:utf-8
"""tweet func"""

import argparse
import configparser

import os
import json

from logging import getLogger

from make_session import make_session
from check_response import check_response

from utils.my_logging import my_get_logger
from utils.time_stamp import get_datetime_stamp


def tweet(session, text):
    """tweet a text"""

    # ツイート投稿用のURL
    url = "https://api.twitter.com/1.1/statuses/update.json"

    # ツイート本文
    params = {"status": text}

    # APIへリクエストを送る
    return session.post(url, params=params)

def main():
    """main func."""
    logger = my_get_logger(__name__, os.path.basename(__file__)+'.log')

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('config', type=str, help='acount config file')
    arg_parser.add_argument('--mode', type=str, default='tweet', choices=['tweet'])
    args = arg_parser.parse_args()
    config = configparser.ConfigParser()
    config.read(args.config)
    
    logger.info("args")
    logger.info(args)
    logger.info("config.sections()")
    logger.info(config.sections())
    logger.info("config['API Keys'].items()")
    logger.info(dict(config['API Keys'].items()))

    sess = make_session(**dict(config['API Keys'].items()))

    text = 'this is a test @ {}'.format(get_datetime_stamp())
    
    logger.info(f'tweet : \"{text}\"')

    ret = tweet(sess, text)

    # レスポンスを確認
    print(check_response(ret, logger))


if __name__ == "__main__":
    main()
