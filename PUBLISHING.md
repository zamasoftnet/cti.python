# リリース手順

## リリース方法

`python3/pyproject.toml` の `version` を更新し、バージョンタグを push します。

```bash
git tag v3.0.1
git push origin v3.0.1
```

GitHub Actions が以下を自動実行します：

1. pydoc によるAPIドキュメント生成
2. GitHub Releases にアーカイブを公開（`cti-python-{VERSION}.zip` / `.tar.gz`）
3. GitHub Pages にドキュメントをデプロイ

## PyPI への公開（手動）

```bash
cd python3
pip install build twine
python -m build
twine upload dist/*
```

PyPI アカウントと API トークンが必要です（https://pypi.org/）。

## ドキュメント

- **GitHub Pages**: https://zamasoftnet.github.io/cti.python/
- リリース時に自動更新
