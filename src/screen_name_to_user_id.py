import json

from check_response import check_response

def screen_name_to_user_id(session, screen_name):
    """ユーザー情報を照会する
    APIをたたいて、screen_name->user_idの変換をする
    user_id -> screen_nameも可能
    https://dev.twitter.com/rest/reference/get/users/lookup
    https://api.twitter.com/1.1/users/lookup.json
    """

    # 友人情報取得用のURL
    url = "https://api.twitter.com/1.1/users/lookup.json"

    params = {
        # 'user_id':user_id,
        'screen_name':screen_name,
        }
    # APIへリクエストを送る
    ret = session.get(url, params=params)

    # レスポンスを確認
    check_response(ret)

    ret_j = json.loads(ret.text)
    
    return ret_j[0]["id"] # return ret_j[0]['screen_name']
    

