# CTI Driver for Python 2

Copper PDF 文書変換サーバーに接続するためのPython 2ドライバ（レガシー版）

> **注意:** これはPython 2向けのレガシー版です。Python 3をお使いの場合は [cti.python](../cti.python/) をご利用ください。

## 動作要件

- Python 2.4.3以降

## インストール

`src/code/cti/` ディレクトリをプロジェクトにコピーするか、`PYTHONPATH` に追加してください。

```bash
export PYTHONPATH=/path/to/cti.python2/src/code:$PYTHONPATH
```

## 基本的な使い方

```python
from cti import get_session

session = get_session('ctip://localhost:8099/', {
    'user': 'user',
    'password': 'kappa'
})

try:
    # 出力先をファイルに設定
    session.set_output_as_file('output.pdf')

    # CSSリソースを送信
    out = session.resource('test.css')
    with open('data/test.css', 'rb') as f:
        out.write(f.read())
    out.close()

    # HTML文書を変換
    out = session.transcode()
    with open('data/test.html', 'rb') as f:
        out.write(f.read())
    out.close()
finally:
    session.close()
```

## API概要

`Session` オブジェクトの主なメソッドは以下の通りです。

| メソッド | 説明 |
|---|---|
| `get_session(uri, params)` | セッションを取得します |
| `session.close()` | セッションを閉じます |
| `session.set_output_as_file(path)` | 出力先をファイルに設定します |
| `session.set_output_as_bytes()` | 出力先をバイト列に設定します |
| `session.resource(uri)` | リソースを送信するためのストリームを返します |
| `session.transcode()` | 文書を変換するためのストリームを返します |
| `session.set_property(name, value)` | プロパティを設定します |
| `session.get_property(name)` | プロパティを取得します |
| `session.set_source_resolver(resolver)` | ソースリゾルバを設定します |

詳細は[オンラインマニュアル](http://dl.cssj.jp/docs/copper/3.0/html/3425_ctip2_python.html)を参照してください。

## テストの実行方法

このドライバは Python 2 向けのレガシー版です。ユニットテストは実施対象外で、配布時点で
`ant dist` が通ることを確認する運用とします。

```bash
ant dist
```

## ドキュメント生成方法

Ant の `doc` ターゲットを使用してドキュメントを生成できます。内部的に `pydoc3` を使用しています。

```bash
ant doc
```

## ライセンス

Apache License 2.0

Copyright (c) 2013 Zamasoft

## 変更履歴

### v2.0.0 (2013/5/31)

- 最初のリリース
