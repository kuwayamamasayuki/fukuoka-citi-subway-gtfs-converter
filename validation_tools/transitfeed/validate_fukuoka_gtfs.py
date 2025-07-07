#!/usr/bin/env python3
"""
福岡市地下鉄GTFSデータの検証スクリプト (transitfeed使用)
"""
import os
import sys
import transitfeed

def validate_gtfs():
    """GTFSデータを検証"""
    gtfs_path = "../../gtfs_output"
    
    if not os.path.exists(gtfs_path):
        print(f"エラー: GTFSデータが見つかりません: {gtfs_path}")
        return False
    
    print("福岡市地下鉄GTFSデータの検証を開始...")
    
    loader = transitfeed.Loader(gtfs_path)
    schedule = loader.Load()
    
    accumulator = transitfeed.ProblemAccumulator()
    schedule.Validate(accumulator)
    
    problems = accumulator.GetProblems()
    
    print(f"\n検証完了: {len(problems)}件の問題が検出されました")
    
    errors = [p for p in problems if p.GetType() == transitfeed.TYPE_ERROR]
    warnings = [p for p in problems if p.GetType() == transitfeed.TYPE_WARNING]
    
    print(f"エラー: {len(errors)}件")
    print(f"警告: {len(warnings)}件")
    
    with open("validation_summary.txt", "w", encoding="utf-8") as f:
        f.write("福岡市地下鉄GTFS検証レポート\n")
        f.write("=" * 40 + "\n\n")
        f.write(f"総問題数: {len(problems)}\n")
        f.write(f"エラー: {len(errors)}\n")
        f.write(f"警告: {len(warnings)}\n\n")
        
        if errors:
            f.write("エラー詳細:\n")
            for error in errors:
                f.write(f"- {error.FormatProblem()}\n")
            f.write("\n")
        
        if warnings:
            f.write("警告詳細:\n")
            for warning in warnings:
                f.write(f"- {warning.FormatProblem()}\n")
    
    print("詳細レポートを validation_summary.txt に保存しました")
    
    return len(errors) == 0

if __name__ == "__main__":
    success = validate_gtfs()
    sys.exit(0 if success else 1)
