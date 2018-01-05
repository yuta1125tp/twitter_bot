#-*-coding:utf-8-*-
"""get time stamp string"""

from datetime import datetime as dt

def _get_dt_now():
    return dt.now()

def get_date_stamp(dtnow=None):
    """year month date（年月日）"""
    if dtnow is None:
        dtnow = _get_dt_now()
    return dtnow.strftime('%Y%m%d')

def get_time_stamp(dtnow=None, b_with_millisec=False):
    """hour minute second（時分秒）"""
    if dtnow is None:
        dtnow = _get_dt_now()
    if b_with_millisec:
        return dtnow.strftime('%H%M%S') + "%03d" % (dtnow.microsecond // 1000)
    else:
        return dtnow.strftime('%H%M%S')

def get_datetime_stamp(dtnow=None):
    """年月日時分秒ミリ秒の17桁の文字列を返す"""
    if dtnow is None:
        dtnow = _get_dt_now()
    return get_date_stamp(dtnow)+get_time_stamp(dtnow, b_with_millisec=True)

if __name__ == "__main__":
    """main func"""
    print("{}_{}".format(get_date_stamp(), get_time_stamp()))
