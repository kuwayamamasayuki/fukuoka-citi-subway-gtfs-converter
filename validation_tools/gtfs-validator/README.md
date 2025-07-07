# GTFS Validator - 公式検証ツール

MobilityDataが開発した公式GTFS検証ツール

## セットアップ

### JARファイルのダウンロード

```bash
# 最新版のダウンロード
wget https://github.com/MobilityData/gtfs-validator/releases/latest/download/gtfs-validator-4.2.0_cli.jar
```

### 必要な環境
- Java 11以上

## 使用方法

### 基本的な検証

```bash
# GTFSデータの検証
java -jar gtfs-validator-4.2.0_cli.jar \
  -i ../../gtfs_output \
  -o validation_results
```

### 詳細オプション

```bash
# 詳細な検証（全ルール適用）
java -jar gtfs-validator-4.2.0_cli.jar \
  -i ../../gtfs_output \
  -o validation_results \
  --validation_report_name fukuoka_subway_validation \
  --html_report \
  --json_report
```

## 出力ファイル

### HTMLレポート
- `validation_results/report.html` - 視覚的な検証レポート

### JSONレポート
- `validation_results/report.json` - 機械可読な検証結果

### 検証内容

1. **必須ファイル・フィールドの確認**
2. **データ整合性チェック**
3. **地理的妥当性の検証**
4. **時刻表の論理チェック**
5. **GTFS仕様準拠の確認**

## 検証ルール

- **エラー**: GTFS仕様違反
- **警告**: 推奨事項の未実装
- **情報**: データ品質の改善提案

## 自動検証スクリプト

```bash
# 定期的な検証の実行
./validate_fukuoka_gtfs.sh
```
