# static-GTFS-manager - GTFS編集ツール

GTFSデータの編集・管理のためのWebベースツール

## セットアップ

### Dockerを使用する場合（推奨）

```bash
# Dockerイメージの取得と起動
docker run -d -p 9000:9000 \
  -v $(pwd)/../../gtfs_output:/gtfs \
  --name gtfs-manager \
  conveyal/gtfs-editor
```

### 手動セットアップ

```bash
# リポジトリのクローン
git clone https://github.com/conveyal/static-gtfs-manager.git
cd static-gtfs-manager

# 依存関係のインストール
npm install

# 設定ファイルの作成
cp config/default.yml.tmp config/default.yml

# サーバーの起動
npm start
```

## 使用方法

### Webインターフェース

ブラウザで http://localhost:9000 にアクセス

### 主な機能

1. **GTFSデータのインポート**
   - 既存のGTFSファイルを読み込み

2. **路線・駅の編集**
   - 地図上での駅位置調整
   - 路線情報の編集

3. **時刻表の編集**
   - 視覚的な時刻表編集
   - 運行パターンの調整

4. **検証機能**
   - リアルタイムでの検証
   - エラー・警告の表示

5. **エクスポート**
   - 編集後のGTFSファイル出力

## 福岡市地下鉄での活用

- 駅座標の微調整
- 新駅追加時の編集
- ダイヤ改正時の時刻表更新
- 運行パターンの変更
