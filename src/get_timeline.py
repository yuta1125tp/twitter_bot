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


def get_user_timeline(session, user_id, count=200, path_to_dump='database/timeline'):
    """フレンドのリストを取得する
    user_id:
    count:一度に取得するつぶやきの数"""
    datetime_stamp = get_datetime_stamp()
    func_name = sys._getframe().f_code.co_name
    func_target = func_name.lstrip("get_")

    # タイムライン情報取得用のURL
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    timeline = []
    ret_j = [{'id':-1}]
    json_output_idx = 0

    while True:
        params = {
            'user_id':user_id,
            'cursor':-1,
            'count':count,
            'skip_status':False,
            'include_user_entities':False}
        if ret_j[0].get('id', -1)>0:
            params['max_id']=ret_j[-1].get('id', -1) - 1 # 同じIDを指定すると前回の最後と今回の最初が重複する


        # リプライを除く
        # params["exclude_replies"] = True

        # ここまでのつぶやきを取得する（新しい側の区切り）
        #params["max_id"] = -1
        # ここからのつぶやきを取得する（古い側の区切り）
        #params["since_id"] = -1

        logger.info(params)
        # APIへリクエストを送る
        ret = session.get(url, params=params)
        logger.info(dir(ret))
        logger.info(ret.text)

        # レスポンスを確認
        if not check_response(ret):
            raise RuntimeError(f'failed @ {func_target}')
        else:
            ret_j = json.loads(ret.text)

        logger.info(json.dumps(ret_j, indent=4, sort_keys=True))

        output_dirname = os.path.join(path_to_dump, str(user_id))
        output_json_filename = "{}_{}.json".format(datetime_stamp, json_output_idx)
        os.makedirs(output_dirname, exist_ok=True)

        json.dump(ret_j, open(os.path.join(output_dirname, output_json_filename), "w"), indent=2)
        json_output_idx += 1
        if len(ret_j)==0:
            break
        timeline.extend(ret_j)
    return timeline


# def get_timeline_list(session, user_id, path_to_dump='database'):
#     """フォロワーのIDのリストを取得する"""
#     func_name = sys._getframe().f_code.co_name
#     func_target = func_name.lstrip("get_")

#     # 友人情報取得用のURL
#     url = "https://api.twitter.com/1.1/followers/ids.json"

#     ret_j = {'next_cursor':-1}
#     json_output_idx = 0
#     id_list = []

#     while True:
#         if ret_j.get('next_cursor', -1) == 0:
#             break
#         logger.info(f'{json_output_idx}')

#         params = {
#             'cursor':ret_j.get('next_cursor', -1),
#             'user_id':user_id
#             }

#         # APIへリクエストを送る
#         ret = session.get(url, params=params)
#         logger.info(dir(ret))
#         logger.info(ret.text)

#         # レスポンスを確認
#         if not check_response(ret, logger):
#             raise RuntimeError(f'failed @ {func_target}')

#         ret_j = json.loads(ret.text)

#         output_dirname = os.path.join(path_to_dump, str(user_id))
#         output_json_filename = "{}_{}.json".format(get_datetime_stamp(), json_output_idx)

#         os.makedirs(output_dirname, exist_ok=True)

#         logger.info(json.dumps(ret_j, indent=4, sort_keys=True))
#         json.dump(ret_j, open(os.path.join(output_dirname, output_json_filename), "w"), indent=2)
#         json_output_idx += 1
        
#         _id_list = ret_j["ids"]

#         id_list.extend(_id_list)

#     return id_list

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

    # target_screen_name = 'kawa1125tp'
    # user_id = screen_name_to_user_id(sess, target_screen_name)
    
    user_id = 87714006
    logger.info(user_id)
    get_user_timeline(sess, user_id)

if __name__ == "__main__":
    main()
