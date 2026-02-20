#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('../../code/')
import os

from cti import *

# セッションの開始
session = get_session(os.getenv('CTI_SERVER_URI', 'ctip://localhost:8099/'),{
    'user'  :'user',
    'password'  :'kappa'
})
try:
    print(session.get_server_info('http://www.cssj.jp/ns/ctip/version'))
finally:
    session.close()
