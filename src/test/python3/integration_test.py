#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import socket
import sys
sys.path.append('../../code/')

from cti import get_session
from cti.builder import *
from cti.results import *
from cti.session import IllegalStateError

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
OUT_DIR = os.path.join(BASE_DIR, 'out')

SERVER_URI = os.environ.get('CTI_SERVER_URI', 'ctip://localhost:8099/')
USER = os.environ.get('CTI_TEST_USER', os.environ.get('CTI_USER', 'user'))
PASSWORD = os.environ.get('CTI_TEST_PASSWORD', os.environ.get('CTI_PASSWORD', 'kappa'))


def data_path(name):
    return os.path.join(DATA_DIR, name)


def session_option():
    return {
        'user': USER,
        'password': PASSWORD
    }


def parse_host_port():
    uri = SERVER_URI
    host = 'localhost'
    port = 8099
    m = re.match(r'^ctips?://([^:/]+):([0-9]+)/?$', uri)
    if m:
        host = m.group(1)
        port = int(m.group(2))
        return host, port
    m = re.match(r'^ctips?://([^:/]+)/?$', uri)
    if m:
        host = m.group(1)
    return host, port


def server_available():
    host, port = parse_host_port()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        return sock.connect_ex((host, port)) == 0
    finally:
        sock.close()


def assert_pdf(path):
    with open(path, 'rb') as fp:
        header = fp.read(4)
    assert header == b'%PDF'


def transcode_local_html(session, output_file, with_css=True):
    if output_file:
        session.set_output_as_file(output_file)

    if with_css:
        with open(data_path('test.css'), 'rb') as fp:
            out = session.resource('test.css')
            out.write(fp.read())
            out.close()

    with open(data_path('test.html'), 'rb') as fp:
        out = session.transcode()
        try:
            out.write(fp.read())
        finally:
            out.close()


def run_auth_failure():
    try:
        get_session(SERVER_URI, {
            'user': 'invalid-user',
            'password': 'invalid-password'
        })
        raise AssertionError('認証失敗時に例外が発生していません')
    except IllegalStateError:
        pass


def run_server_info():
    with get_session(SERVER_URI, session_option()) as session:
        info = session.get_server_info('http://www.cssj.jp/ns/ctip/version')
        assert info is not None and len(info) > 0


def run_output_file():
    output = os.path.join(OUT_DIR, 'python3-output-file.pdf')
    if os.path.exists(output):
        os.remove(output)
    with get_session(SERVER_URI, session_option()) as session:
        transcode_local_html(session, output)
    assert_pdf(output)


def run_output_directory():
    output_dir = os.path.join(OUT_DIR, 'output-dir')
    if os.path.exists(output_dir):
        for name in os.listdir(output_dir):
            path = os.path.join(output_dir, name)
            if os.path.isfile(path):
                os.remove(path)
    else:
        os.makedirs(output_dir, exist_ok=True)

    with get_session(SERVER_URI, session_option()) as session:
        session.property('output.type', 'image/jpeg')
        session.set_output_as_directory(output_dir, '', '.jpg')
        transcode_local_html(session, None)

    jpgs = [p for p in os.listdir(output_dir) if p.lower().endswith('.jpg')]
    assert len(jpgs) > 0


def run_progress():
    progress = []
    with get_session(SERVER_URI, session_option()) as session:
        session.set_results(SingleResult(NullBuilder()))
        session.set_progress_func(lambda length, read: progress.append((length, read)))
        session.property('input.include', 'https://www.w3.org/**')
        session.transcode_server('https://www.w3.org/TR/xslt-10/')
    assert len(progress) > 0
    assert all((item is not None and item[1] is not None) for item in progress)


def run_resolver():
    resolved = {'called': False}

    def resolver(uri, resource):
        if uri == 'test.css':
            resolved['called'] = True
            out = resource.found()
            with open(data_path('test.css'), 'rb') as fp:
                out.write(fp.read())
            out.close()

    output = os.path.join(OUT_DIR, 'python3-resolver.pdf')
    if os.path.exists(output):
        os.remove(output)
    with get_session(SERVER_URI, session_option()) as session:
        session.set_resolver_func(resolver)
        session.set_output_as_file(output)
        with open(data_path('test.html'), 'rb') as fp:
            out = session.transcode()
            try:
                out.write(fp.read())
            finally:
                out.close()
    assert resolved['called']
    assert_pdf(output)


def run_reset():
    out1 = os.path.join(OUT_DIR, 'python3-reset-1.pdf')
    out2 = os.path.join(OUT_DIR, 'python3-reset-2.pdf')
    for p in (out1, out2):
        if os.path.exists(p):
            os.remove(p)

    with get_session(SERVER_URI, session_option()) as session:
        transcode_local_html(session, out1)
        session.reset()
        transcode_local_html(session, out2)
    assert_pdf(out1)
    assert_pdf(out2)


if __name__ == '__main__':
    if not server_available():
        print('CTI サーバーに接続できないため、テストをスキップします。')
        sys.exit(0)

    os.makedirs(OUT_DIR, exist_ok=True)
    run_auth_failure()
    run_server_info()
    run_output_file()
    run_output_directory()
    run_progress()
    run_resolver()
    run_reset()
    print('Python3 統合テスト: すべて成功しました。')
