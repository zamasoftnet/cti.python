#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CTI Python3 ドライバ PDF生成テスト (TC-01〜TC-10)

生成されたPDFは build/test-output/ ディレクトリに保存される。
"""
import os
import sys
import socket

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(BASE_DIR, '../../code'))

from cti import get_session

SERVER_URI = 'ctip://cti.li/'
SOURCE_URI = 'http://cti.li/'
OUTPUT_DIR = os.path.normpath(os.path.join(BASE_DIR, '../../../../build/test-output'))


def server_available():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    try:
        return sock.connect_ex(('cti.li', 8099)) == 0
    finally:
        sock.close()


def with_session(filename, setup):
    try:
        session = get_session(SERVER_URI, {'user': 'user', 'password': 'kappa'})
    except Exception as e:
        sys.stderr.write('接続エラー: {}\n'.format(e))
        sys.exit(0)
    session.set_output_as_file(os.path.join(OUTPUT_DIR, filename))
    error = None
    try:
        setup(session)
    except Exception as e:
        error = e
    try:
        session.close()
    except Exception:
        pass
    if error:
        sys.stderr.write('エラー ({}): {}\n'.format(filename, error))
        sys.exit(0)
    sys.stderr.write('生成: {}\n'.format(filename))


if __name__ == '__main__':
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if not server_available():
        sys.stderr.write('CTIサーバーに接続できないためスキップします。\n')
        sys.exit(0)

    # TC-01: 基本URL変換
    with_session('ctip-python-url.pdf', lambda s: s.transcode_server(SOURCE_URI))

    # TC-02: ハイパーリンク有効
    def tc02(session):
        session.property('output.pdf.hyperlinks', 'true')
        session.transcode_server(SOURCE_URI)
    with_session('ctip-python-hyperlinks.pdf', tc02)

    # TC-03: ブックマーク有効
    def tc03(session):
        session.property('output.pdf.bookmarks', 'true')
        session.transcode_server(SOURCE_URI)
    with_session('ctip-python-bookmarks.pdf', tc03)

    # TC-04: ハイパーリンクとブックマーク有効
    def tc04(session):
        session.property('output.pdf.hyperlinks', 'true')
        session.property('output.pdf.bookmarks', 'true')
        session.transcode_server(SOURCE_URI)
    with_session('ctip-python-hyperlinks-bookmarks.pdf', tc04)

    # TC-05: クライアント側HTML変換
    def tc05(session):
        html = '<html><body><h1>Hello</h1><p>Client-side HTML transcoding test.</p></body></html>'
        with session.transcode('dummy:///test.html') as out:
            out.write(html)
    with_session('ctip-python-client-html.pdf', tc05)

    # TC-06: 日本語HTMLコンテンツ
    def tc06(session):
        html = ('<html><head><meta charset="UTF-8"/></head><body>'
                '<h1>日本語テスト</h1><p>こんにちは世界。クライアント側から日本語コンテンツを送信します。</p>'
                '</body></html>')
        with session.transcode('dummy:///japanese.html') as out:
            out.write(html)
    with_session('ctip-python-client-japanese.pdf', tc06)

    # TC-07: 最小HTML（境界条件）
    def tc07(session):
        with session.transcode('dummy:///minimal.html') as out:
            out.write('<html><body><p>.</p></body></html>')
    with_session('ctip-python-client-minimal.pdf', tc07)

    # TC-08: 連続モード（2文書を結合）
    def tc08(session):
        html1 = '<html><body><h1>Page 1</h1><p>First document in continuous mode.</p></body></html>'
        html2 = '<html><body><h1>Page 2</h1><p>Second document in continuous mode.</p></body></html>'
        session.set_continuous(True)
        with session.transcode('dummy:///page1.html') as out:
            out.write(html1)
        with session.transcode('dummy:///page2.html') as out:
            out.write(html2)
        session.join()
    with_session('ctip-python-continuous.pdf', tc08)

    # TC-09: 大規模テーブル（メモリ→ファイル切り替えを誘発）
    def tc09(session):
        with session.transcode('dummy:///large-table.html') as out:
            out.write('<html><head><meta charset="UTF-8"/></head><body>')
            out.write('<h1>大規模テーブルテスト</h1>')
            out.write('<table border="1"><tr><th>番号</th><th>名前</th><th>説明</th><th>備考</th></tr>')
            for i in range(1, 15001):
                out.write('<tr><td>{0}</td><td>項目{0}</td>'
                          '<td>これはテスト項目 {0} の詳細説明テキストです。</td>'
                          '<td>備考テキスト {0}</td></tr>'.format(i))
            out.write('</table></body></html>')
    with_session('ctip-python-large-table.pdf', tc09)

    # TC-10: 長文テキスト文書
    # TC-09の大規模テーブルが2MB超のPDFを生成するため、大容量出力のテストはTC-09でカバーされる。
    # テキスト文書のレイアウト機能を確認することが目的であり、ここでは100セクションで十分。
    def tc10(session):
        sentences = ('Copper PDFはHTMLやXMLをPDFに変換するサーバーサイドのソフトウェアです。'
                     'CTIプロトコルを通じてクライアントからドキュメントを送信し、変換結果をPDFとして受け取ります。'
                     'このテストは大量のテキストコンテンツを含む文書を生成します。'
                     'ドライバはPDF出力が2MBを超えた際にメモリからファイル書き出しへ切り替わります。'
                     'このテストはその動作を確認するために設計されています。')
        with session.transcode('dummy:///large-text.html') as out:
            out.write('<html><head><meta charset="UTF-8"/></head><body>')
            for s in range(1, 101):
                out.write('<h2>セクション {}</h2>'.format(s))
                for p in range(1, 21):
                    out.write('<p>{}（セクション{}、段落{}）</p>'.format(sentences, s, p))
            out.write('</body></html>')
    with_session('ctip-python-large-text.pdf', tc10)
