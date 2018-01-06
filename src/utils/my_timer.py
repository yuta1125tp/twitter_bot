# coding:utf-8
"""時間計測をするクラス"""

import time
from collections import OrderedDict


class MyTimer(object):
    """時間計測のためのクラス"""

    def __init__(self):
        self._index = 0
        self._name_time_dict = OrderedDict()

    def start(self, name=""):
        """計測開始の関数"""
        start = time.time()
        if name == "":
            name = "timer_{}".format(self._index)
            self._index += 1
        self._name_time_dict[name] = start

    def end(self, name=""):
        """計測の終わりの関数
        計測結果の秒数をfloatで返す"""
        end = time.time()
        if len(self._name_time_dict.keys()) == 0:
            print("no timer was set.")
            return -1
        if name == "":
            name = list(self._name_time_dict)[-1]#.keys()[-1]
        if not name in self._name_time_dict:
            print("specified key does not exist. : {name}".format(name=name))
            return -1
        process = end - self._name_time_dict[name]
        hour = int(process / 3600)
        process -= hour * 3600
        minu = int(process / 60)
        process -= minu * 60
        sec = int(process)
        msec = int((process - sec) * 1000)
        msg = "MyTimer : {name:<20} :{hour:>4}:{min:0>2}:{sec:0>2}.{msec:0<3}".format(
            name=name,
            hour=hour,
            min=minu,
            sec=sec,
            msec=msec)
        print(msg)
        del self._name_time_dict[name]
        return process


def main():
    """main func."""
    myTimer = MyTimer()
    myTimer.start()
    myTimer.start("test func1")
    time.sleep(4)
    s = 0
    for i in range(5000000):
        pass

    myTimer.start("test func2")
    for i in range(1000000):
        s += i
    myTimer.end()
    myTimer.end("test func1")
    for i in range(1000000):
        s += i
    myTimer.end()


if __name__ == "__main__":
    main()
