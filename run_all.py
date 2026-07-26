#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
一括実行スクリプト: スクレイピング → データ編集(サイト生成) → GitHub 反映

タスクスケジューラーからはこのファイルを実行するだけでOK:
  python run_all.py
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'scraping'))

from scraper import main as scrape_main
from site_generator import generate_site
from git_publish import publish


def main():
    print("#" * 60)
    print("# パチスロ情報 自動更新パイプライン")
    print("#" * 60)

    print("\n--- [1/3] スクレイピング ---")
    if not scrape_main():
        print("❌ スクレイピング失敗のため中断します")
        return False

    print("\n--- [2/3] サイト生成 ---")
    if not generate_site():
        print("❌ サイト生成失敗のため中断します")
        return False

    print("\n--- [3/3] GitHub へ反映 ---")
    if not publish():
        print("⚠ GitHub への反映に失敗しました（データ自体は保存済みです）")
        return False

    print("\n" + "#" * 60)
    print("# ✓ 全工程完了")
    print("#" * 60)
    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)
