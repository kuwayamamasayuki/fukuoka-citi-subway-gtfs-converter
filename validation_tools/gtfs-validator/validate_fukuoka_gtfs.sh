#!/bin/bash


echo "福岡市地下鉄GTFSデータの検証を開始..."

mkdir -p validation_results

java -jar gtfs-validator-4.2.0_cli.jar \
  -i ../../gtfs_output \
  -o validation_results \
  --validation_report_name fukuoka_subway_validation_$(date +%Y%m%d_%H%M%S) \
  --html_report \
  --json_report

echo "検証完了。結果は validation_results/ フォルダを確認してください。"
echo "HTMLレポート: validation_results/report.html"
echo "JSONレポート: validation_results/report.json"
