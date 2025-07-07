# gtfs-kit - Python GTFS分析ツール

PythonベースのGTFS分析・統計ツール

## セットアップ

```bash
# Python仮想環境の作成
python -m venv venv
source venv/bin/activate

# gtfs-kitのインストール
pip install gtfs-kit
```

## 使用方法

### 基本的な分析

```python
import gtfs_kit as gk

# GTFSデータの読み込み
feed = gk.read_feed("../../gtfs_output", dist_units='km')

# 基本統計の表示
print(feed.describe())
```

### 分析スクリプト

```bash
# 福岡市地下鉄の分析実行
python analyze_fukuoka_gtfs.py
```

## 主な機能

### 1. データ統計
- 路線数、駅数、トリップ数
- 運行頻度分析
- 距離・時間統計

### 2. 地理的分析
- 駅間距離の計算
- サービスエリアの可視化
- 路線図の生成

### 3. 時刻表分析
- 運行間隔の分析
- ピーク時間の特定
- サービス品質指標

### 4. 可視化
- 路線図の生成
- 運行頻度マップ
- 時刻表グラフ

## 出力例

- `route_map.html` - インタラクティブ路線図
- `frequency_analysis.png` - 運行頻度グラフ
- `statistics_report.txt` - 統計レポート
