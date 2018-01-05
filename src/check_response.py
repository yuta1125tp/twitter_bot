#coding:utf-8
"""check response func"""

import json

def check_response(response, logger=None):
    """APIからの反応をチェックする"""
    if response.status_code == 200:
        if logger is not None:
            logger.info('OK ({})'.format(response.status_code))
        return True
    else:
        response_j = json.loads(response.text)
        if logger is not None:
            logger.info('error ({}) : {}'.format(response.status_code, response_j))
        return False
