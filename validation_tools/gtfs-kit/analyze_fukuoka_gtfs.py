#!/usr/bin/env python3
"""
福岡市地下鉄GTFSデータの分析スクリプト (gtfs-kit使用)
"""
import gtfs_kit as gk
import pandas as pd
import matplotlib.pyplot as plt
import folium
from datetime import datetime

def analyze_fukuoka_gtfs():
    """福岡市地下鉄GTFSデータの包括的分析"""
    
    print("福岡市地下鉄GTFSデータの分析を開始...")
    
    gtfs_path = "../../gtfs_output"
    feed = gk.read_feed(gtfs_path, dist_units='km')
    
    print("\n=== 基本統計 ===")
    description = feed.describe()
    print(description)
    
    with open("statistics_report.txt", "w", encoding="utf-8") as f:
        f.write("福岡市地下鉄GTFS分析レポート\n")
        f.write("=" * 40 + "\n")
        f.write(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("基本統計:\n")
        f.write(str(description))
        f.write("\n\n")
    
    print("\n=== 路線別統計 ===")
    routes_stats = feed.routes.groupby('route_id').size()
    print("路線数:", len(feed.routes))
    print("路線別詳細:")
    for route_id, route_info in feed.routes.iterrows():
        print(f"  {route_info['route_short_name']}: {route_info['route_long_name']}")
    
    print("\n=== 駅統計 ===")
    print("総駅数:", len(feed.stops))
    print("駅一覧:")
    for stop_id, stop_info in feed.stops.iterrows():
        print(f"  {stop_info['stop_name']} ({stop_info['stop_lat']:.4f}, {stop_info['stop_lon']:.4f})")
    
    print("\n=== 運行統計 ===")
    print("総トリップ数:", len(feed.trips))
    
    service_stats = feed.trips.groupby('service_id').size()
    print("サービス別トリップ数:")
    for service_id, count in service_stats.items():
        print(f"  {service_id}: {count}トリップ")
    
    print("\n=== 運行頻度分析 ===")
    try:
        frequencies = gk.compute_trip_stats(feed, '20240701')  # 平日の例
        print("運行頻度統計:")
        print(frequencies.describe())
    except Exception as e:
        print(f"運行頻度分析でエラー: {e}")
    
    print("\n=== 路線図生成 ===")
    try:
        center_lat = feed.stops['stop_lat'].mean()
        center_lon = feed.stops['stop_lon'].mean()
        
        m = folium.Map(location=[center_lat, center_lon], zoom_start=12)
        
        for stop_id, stop in feed.stops.iterrows():
            folium.Marker(
                [stop['stop_lat'], stop['stop_lon']],
                popup=stop['stop_name'],
                tooltip=stop['stop_name']
            ).add_to(m)
        
        m.save("route_map.html")
        print("路線図を route_map.html に保存しました")
        
    except Exception as e:
        print(f"路線図生成でエラー: {e}")
    
    with open("statistics_report.txt", "a", encoding="utf-8") as f:
        f.write("路線別統計:\n")
        for route_id, route_info in feed.routes.iterrows():
            f.write(f"  {route_info['route_short_name']}: {route_info['route_long_name']}\n")
        f.write(f"\n総駅数: {len(feed.stops)}\n")
        f.write(f"総トリップ数: {len(feed.trips)}\n")
        f.write("\nサービス別トリップ数:\n")
        for service_id, count in service_stats.items():
            f.write(f"  {service_id}: {count}トリップ\n")
    
    print("\n分析完了！")
    print("- 統計レポート: statistics_report.txt")
    print("- 路線図: route_map.html")

if __name__ == "__main__":
    analyze_fukuoka_gtfs()
