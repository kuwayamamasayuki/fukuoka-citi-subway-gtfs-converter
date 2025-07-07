# OpenTripPlanner (OTP) - 経路検索エンジン

福岡市地下鉄の経路検索・地図可視化

## セットアップ

### 必要な環境
- Java 11以上
- 8GB以上のRAM（推奨）

### OTPのダウンロード

```bash
# OTP JARファイルのダウンロード
wget https://repo1.maven.org/maven2/org/opentripplanner/otp/2.4.0/otp-2.4.0-shaded.jar
```

### OpenStreetMapデータの準備

```bash
# 福岡市周辺のOSMデータをダウンロード
wget https://download.geofabrik.de/asia/japan/kyushu-latest.osm.pbf
```

## 使用方法

### グラフの構築

```bash
# GTFSとOSMデータからグラフを構築
java -Xmx8G -jar otp-2.4.0-shaded.jar --build --save .
```

### サーバーの起動

```bash
# OTPサーバーの起動
java -Xmx4G -jar otp-2.4.0-shaded.jar --load .
```

### Webインターフェース

ブラウザで http://localhost:8080 にアクセス

## 機能

- インタラクティブな地図表示
- 経路検索（電車・徒歩・自転車）
- 等時線マップ
- リアルタイム情報対応（設定時）
- API経由でのデータアクセス

## API例

```bash
# 経路検索API
curl "http://localhost:8080/otp/routers/default/plan?fromPlace=33.5904,130.4017&toPlace=33.6061,130.4181&mode=TRANSIT,WALK"
```
