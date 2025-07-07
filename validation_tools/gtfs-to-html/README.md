# gtfs-to-html - HTML時刻表生成

GTFSデータから美しいHTML時刻表を生成

## セットアップ

```bash
# Node.js環境でのインストール
npm install gtfs-to-html

# または、グローバルインストール
npm install -g gtfs-to-html
```

## 使用方法

### 基本的な使用方法

```bash
# HTML時刻表の生成
gtfs-to-html --configPath=config.json
```

### 設定ファイル

`config.json` で出力設定をカスタマイズできます。

## 出力

- `html/` フォルダに各路線・方向別のHTML時刻表が生成されます
- `index.html` で全体のインデックスページが作成されます

## 特徴

- レスポンシブデザイン
- 路線別・方向別の時刻表
- 駅間の所要時間表示
- モバイル対応
