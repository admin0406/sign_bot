# *--conding:utf-8--*
import linecache
import random
import sys
import time
import os


def add_in(user):
    f = open('list', 'r')
    l = f.read()
    if user is None:
        return '报名未成功，请设置username!'
    else:
        if l.find('%s' % user) == -1:
            f = open('list', 'a+')
            r = user
            f.write(user)
            f.write('\n')
            f.close()
            sf = open('adminlist', 'a+')
            s = ' | '
            localtime = time.strftime("%m-%d|%H:%M:%S", time.localtime())
            rr = localtime + s + r
            print(sf, rr)
            sf.close()
            return '成功参加抽奖~'
        else:
            return '你已经参加了哦~请耐心等待开奖吧！'


def get_lottery():
    count = -1
    for count, line in enumerate(open("list", 'r')):
        pass
    count += 1
    if count == 0:
        return 0, '还没人参加抽奖，不能开奖额'
    else:
        with open('list') as f:
            l = f.read().splitlines()
            r = random.sample(l, 1)
            a = ''.join(r)
            rr = '我抽中了： @%s' % a
    return 1, rr


def read_list(un):
    s = os.path.getsize('list')
    if s < 3096:
        with open('list', 'r') as f:
            rr = f.read()
            return rr
    else:
        f = open('list', 'r')
        l = f.read()
        if l.find('%s' % un) == -1:
            return u'由于telegram限制，我无法提供完整的名单 \n\n 但您   未参与   抽奖'
        else:
            return u'由于telegram限制，我无法提供完整的名单 \n\n 但您   已参与   抽奖'


def del_list():
    f = open('list', 'w')
    f.close()

    return '名单已清空~'
