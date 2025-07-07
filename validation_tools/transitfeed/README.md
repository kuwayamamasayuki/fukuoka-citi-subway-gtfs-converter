# transitfeed - GTFS検証ツール

GoogleのtransitfeedライブラリによるGTFS検証

## セットアップ

```bash
# Python仮想環境の作成（推奨）
python -m venv venv
source venv/bin/activate

# transitfeedのインストール
pip install transitfeed
```

## 使用方法

### 基本的な検証

```bash
# GTFSデータの検証
feedvalidator.py ../../gtfs_output/

# 詳細レポートの生成
feedvalidator.py --output=validation_report.html ../../gtfs_output/
```

### 検証スクリプト

```bash
# 自動検証スクリプトの実行
python validate_fukuoka_gtfs.py
```

## 出力ファイル

- `validation_report.html` - 詳細な検証レポート
- `validation_summary.txt` - 検証結果サマリー
