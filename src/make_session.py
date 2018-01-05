#coding:utf-8
"""make a OAuth1Session instance"""


from requests_oauthlib import OAuth1Session

def make_session(consumer_key, consumer_secret, access_token, access_token_secret):
    """make a session"""
    return OAuth1Session(consumer_key, consumer_secret, access_token, access_token_secret)
