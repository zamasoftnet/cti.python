# CTI Driver for Python

Copper PDF 文書変換サーバーに接続するためのPython 3ドライバです。

- バージョン: 3.0.0
- オンラインマニュアル: http://dl.cssj.jp/docs/copper/3.0/html/3425_ctip2_python.html

## 動作要件

- Python 3以降

## インストール

`src/code/cti/` ディレクトリをプロジェクトにコピーするか、`PYTHONPATH` に追加してください。

```
export PYTHONPATH=/path/to/cti.python3/src/code:$PYTHONPATH
```

## 基本的な使い方

以下は、Copper PDFサーバーに接続してHTML文書をPDFに変換する基本的な例です。

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
    with session.resource('test.css') as out:
        with open('data/test.css', 'rb') as f:
            out.write(f.read())

    # HTML文書を変換
    with session.transcode() as out:
        with open('data/test.html', 'rb') as f:
            out.write(f.read())
finally:
    session.close()
```

コンテキストマネージャを使うと、セッションの終了処理を自動化できます。

```python
from cti import get_session

with get_session('ctip://localhost:8099/', {'user': 'user', 'password': 'kappa'}) as session:
    session.set_output_as_file('output.pdf')
    with session.transcode() as out:
        with open('data/test.html', 'rb') as f:
            out.write(f.read())
```

## API概要

Sessionオブジェクトの主なメソッドは以下の通りです。

| メソッド | 説明 |
|---|---|
| `set_output_as_file` | 出力先をファイルに設定します |
| `set_output_as_directory` | 出力先をディレクトリに設定します |
| `set_output_as_stream` | 出力先をストリームに設定します |
| `set_results` | 変換結果の出力先を設定します |
| `set_message_func` | メッセージハンドラ関数を設定します |
| `set_progress_func` | 進捗ハンドラ関数を設定します |
| `set_resolver_func` | リソースリゾルバ関数を設定します |
| `property` | サーバーのプロパティを設定します |
| `resource` | リソースを送信します |
| `transcode` | 文書を変換します |
| `transcode_server` | サーバー側の文書を変換します |
| `set_continuous` | 連続変換モードを設定します |
| `join` | 連続変換の完了を待機します |
| `reset` | セッションの状態をリセットします |
| `abort` | 処理を中断します |
| `close` | セッションを閉じます |
| `get_server_info` | サーバー情報を取得します |

## テストの実行方法

このドライバは実運用対象で、接続先サーバーが利用可能な環境でテストを実行してください。

```bash
python3 src/test/python3/*.py
```

## ドキュメント生成方法

ドキュメントを生成するには、`ant` の `doc` ターゲットを使用してください。内部的に `pydoc3` が使われます。

```bash
ant doc
```

## ライセンス

Copyright (c) 2013-2025 Zamasoft

Apache License 2.0 の下で公開されています。詳細は LICENSE ファイルを参照してください。

## 変更履歴

### v3.0.0 (2025/07/18)

- Python 3 に対応

### v2.0.0 (2013/05/31)

- 最初のリリース
