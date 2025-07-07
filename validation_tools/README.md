# GTFS検証・可視化ツール

福岡市地下鉄のGTFSデータを検証・可視化するための各種ツールを設定しています。

## 利用可能なツール

### 1. transitfeed
Googleが開発したGTFS検証ツール
- **用途**: GTFS仕様準拠の検証
- **フォルダ**: `transitfeed/`

### 2. gtfs-to-html
GTFSデータからHTMLタイムテーブルを生成
- **用途**: 時刻表のHTML可視化
- **フォルダ**: `gtfs-to-html/`

### 3. OpenTripPlanner (OTP)
マルチモーダル経路検索エンジン
- **用途**: 経路検索・地図可視化
- **フォルダ**: `opentripplanner/`

### 4. static-GTFS-manager
GTFSデータの編集・管理ツール
- **用途**: GTFSデータの編集・管理
- **フォルダ**: `static-gtfs-manager/`

### 5. GTFS Validator
MobilityDataが開発した公式検証ツール
- **用途**: 包括的なGTFS検証
- **フォルダ**: `gtfs-validator/`

### 6. gtfs-kit
PythonベースのGTFS分析ツール
- **用途**: データ分析・統計
- **フォルダ**: `gtfs-kit/`

## 使用方法

各ツールのフォルダに移動して、それぞれのREADMEファイルの指示に従ってください。

## GTFSデータの場所

検証・可視化対象のGTFSデータ: `../gtfs_output/`
