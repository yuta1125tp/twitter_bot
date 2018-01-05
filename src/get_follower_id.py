import sys
import os
import json
import argparse
import configparser

from make_session import make_session

from check_response import check_response
from screen_name_to_user_id import screen_name_to_user_id

from utils.my_logging import my_get_logger
from utils.time_stamp import get_datetime_stamp

logger = my_get_logger(__name__, os.path.basename(__file__)+'.log')

def get_follower_id_list(session, user_id, path_to_dump='database/follower_id'):
    """フォロワーのIDのリストを取得する"""
    datetime_stamp = get_datetime_stamp()
    func_name = sys._getframe().f_code.co_name
    func_target = func_name.lstrip("get_")

    # 友人情報取得用のURL
    url = "https://api.twitter.com/1.1/followers/ids.json"

    ret_j = {'next_cursor':-1}
    json_output_idx = 0
    id_list = []

    while True:
        if ret_j.get('next_cursor', -1) == 0:
            break
        logger.info(f'{json_output_idx}')

        params = {
            'cursor':ret_j.get('next_cursor', -1),
            'user_id':user_id
            }

        # APIへリクエストを送る
        ret = session.get(url, params=params)
        logger.info(dir(ret))
        logger.info(ret.text)

        # レスポンスを確認
        if not check_response(ret, logger):
            raise RuntimeError(f'failed @ {func_target}')

        ret_j = json.loads(ret.text)

        output_dirname = os.path.join(path_to_dump, str(user_id))
        output_json_filename = "{}_{}.json".format(datetime_stamp, json_output_idx)

        os.makedirs(output_dirname, exist_ok=True)

        logger.info(json.dumps(ret_j, indent=4, sort_keys=True))
        json.dump(ret_j, open(os.path.join(output_dirname, output_json_filename), "w"), indent=2)
        json_output_idx += 1
        
        _id_list = ret_j["ids"]

        id_list.extend(_id_list)

    return id_list

def main():
    """main func."""
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

    target_screen_name = 'kawa1125tp'
    user_id = screen_name_to_user_id(sess, target_screen_name)

    
    logger.info(user_id)

    get_follower_id_list(sess, user_id)

if __name__ == "__main__":
    main()
