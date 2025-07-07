# 福岡市地下鉄 GTFS変換システム

福岡市交通局の時刻表ExcelファイルからGTFS（General Transit Feed Specification）データを生成するシステムです。

## 概要

このシステムは以下の機能を提供します：

- 福岡市地下鉄の時刻表ExcelファイルからGTFSデータを自動生成
- OpenStreetMapから駅座標を自動取得
- 3つの運行パターン（平日・金曜・土休日）に対応
- 空港線・箱崎線間の直通運転を適切に処理
- 将来のダイヤ改正に対応した再現性のあるスクリプト

## 必要なファイル

### 入力ファイル
- `kukohakozaki_timetable.xlsx` - 空港線・箱崎線時刻表
- `nanakuma_timetable.xlsx` - 七隈線時刻表

### 生成されるGTFSファイル
- `agency.txt` - 交通事業者情報
- `routes.txt` - 路線情報
- `stops.txt` - 駅情報
- `calendar.txt` - 運行日情報
- `trips.txt` - 運行情報
- `stop_times.txt` - 時刻表データ

## セットアップ

### 1. 依存関係のインストール

```bash
pip install -r requirements.txt
```

### 2. 時刻表ファイルの配置

福岡市交通局の公式サイトから最新の時刻表Excelファイルをダウンロードし、プロジェクトディレクトリに配置してください：

- https://subway.city.fukuoka.lg.jp/subway/about/data/kukohakozaki_timetable.xlsx
- https://subway.city.fukuoka.lg.jp/subway/about/data/nanakuma_timetable.xlsx

## 使用方法

### 基本的な使用方法

```bash
python convert_to_gtfs.py
```

### オプション指定

```bash
python convert_to_gtfs.py \
  --kuko-hakozaki kukohakozaki_timetable.xlsx \
  --nanakuma nanakuma_timetable.xlsx \
  --output-dir gtfs_output
```

### 生成されたGTFSファイルの検証

```bash
python validate_gtfs.py gtfs_output
```

## データ仕様と前提条件

### 運行パターン

1. **平日** - 月曜日〜木曜日
2. **金曜** - 金曜日
3. **土休日** - 土曜日・日曜日・祝日

### 到着時刻の扱い

**重要な前提条件**: Excelファイルには出発時刻のみが記載されており、到着時刻は記載されていません。GTFSでは到着時刻が必須項目のため、本システムでは **到着時刻 = 出発時刻** として処理しています。

この前提条件により、駅での停車時間は0分として扱われます。実際の運行では各駅で短時間の停車がありますが、正確な到着時刻データが入手できないため、この簡略化を採用しています。

### 直通運転の扱い

- **空港線・箱崎線間の直通運転**: 適切に処理されます
- **JR九州筑肥線との相互乗り入れ**: 対象外（JR側のGTFSデータが必要）
- **西鉄貝塚線との連絡**: 直通運転ではないため対象外

### 駅座標

駅の緯度・経度座標はOpenStreetMapから自動取得されます。OpenStreetMapにデータが存在しない駅については、手動で座標を設定しています。

## ファイル構成

```
fukuoka_gtfs/
├── convert_to_gtfs.py          # メイン変換スクリプト
├── gtfs_generator.py           # GTFS生成クラス
├── excel_parser.py             # Excel解析クラス
├── station_coordinates.py      # 駅座標取得
├── validate_gtfs.py            # GTFS検証スクリプト
├── requirements.txt            # 依存関係
├── README.md                   # このファイル
├── kukohakozaki_timetable.xlsx # 空港線・箱崎線時刻表
├── nanakuma_timetable.xlsx     # 七隈線時刻表
└── gtfs_output/               # 生成されるGTFSファイル
    ├── agency.txt
    ├── routes.txt
    ├── stops.txt
    ├── calendar.txt
    ├── trips.txt
    └── stop_times.txt
```

## 将来のダイヤ改正への対応

### 1. 時刻表ファイルの更新

新しい時刻表Excelファイルを同じファイル名で置き換えてください：

```bash
# 新しいファイルをダウンロード
wget "https://subway.city.fukuoka.lg.jp/subway/about/data/kukohakozaki_timetable.xlsx" -O kukohakozaki_timetable.xlsx
wget "https://subway.city.fukuoka.lg.jp/subway/about/data/nanakuma_timetable.xlsx" -O nanakuma_timetable.xlsx

# 変換実行
python convert_to_gtfs.py

# 検証
python validate_gtfs.py gtfs_output
```

### 2. 新駅追加への対応

新駅が追加された場合は、以下のファイルを更新してください：

1. `station_coordinates.py` の `manual_mappings` に新駅の座標を追加
2. `excel_parser.py` の `_normalize_station_name` メソッドに新駅の名前マッピングを追加

### 3. 運行パターン変更への対応

運行パターンが変更された場合は、`gtfs_generator.py` の `generate_calendar` メソッドを更新してください。

## トラブルシューティング

### OpenStreetMap接続エラー

```bash
# 手動で駅座標を確認
python station_coordinates.py
```

### Excel解析エラー

```bash
# Excel構造を確認
python analyze_excel.py
```

### GTFS検証エラー

```bash
# 詳細な検証を実行
python validate_gtfs.py gtfs_output
```

## 技術仕様

### 対応路線

- **空港線** (Airport Line): 姪浜 ⇔ 福岡空港
- **箱崎線** (Hakozaki Line): 中洲川端 ⇔ 貝塚
- **七隈線** (Nanakuma Line): 橋本 ⇔ 博多

### GTFS仕様準拠

生成されるGTFSファイルは[Google Transit GTFS仕様](https://developers.google.com/transit/gtfs/reference)に準拠しています。

### 座標系

駅座標はWGS84測地系（EPSG:4326）で記録されています。

## 制限事項

1. **到着時刻**: 出発時刻と同一として処理（実際の停車時間は考慮されません）
2. **JR筑肥線**: 相互乗り入れ区間は含まれません
3. **西鉄貝塚線**: 連絡のみで直通運転ではないため含まれません
4. **リアルタイム情報**: 静的な時刻表データのみ対応

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 作成者

- 作成者: @kuwayamamasayuki
- Devin実行URL: https://app.devin.ai/sessions/c457364503ed434bab8bb48460a57f16

## 貢献

バグ報告や機能改善の提案は、GitHubのIssueまたはPull Requestでお願いします。
