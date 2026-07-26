#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
パチンコ情報スクレイピング - シンプルセットアップ（venv不要版）
"""
import sys
import subprocess

def main():
    print("=" * 60)
    print("セットアップ: ライブラリインストール")
    print("=" * 60)

    print(f"\n[確認] Python バージョン: {sys.version}\n")

    # インストール対象
    packages = [
        "selenium",
        "requests",
        "beautifulsoup4",
    ]

    print("[1/2] 依存ライブラリをインストール中...\n")

    # pip install 実行
    cmd = [sys.executable, "-m", "pip", "install", "-q"] + packages
    print(f"実行: pip install {' '.join(packages)}\n")

    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("\n❌ インストール中にエラーが発生しました")
        return False

    # インストール確認
    print("\n[2/2] インストール確認中...\n")

    try:
        import selenium
        import requests
        import bs4

        print("✓ selenium")
        print("✓ requests")
        print("✓ beautifulsoup4")

    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        return False

    print("\n" + "=" * 60)
    print("✓ セットアップ完了！")
    print("=" * 60)

    print("\n次のステップ:")
    print("\n1️⃣  Chrome バージョン確認")
    print("   python check_chrome_version.py")

    print("\n2️⃣  ChromeDriver をダウンロード")
    print("   → https://googlechromelabs.github.io/chrome-for-testing/")
    print("   → chromedriver.exe をこのフォルダに配置")

    print("\n3️⃣  初回ログイン（対象サイトの認証）")
    print("   python scraping/first_login.py")

    print("\n4️⃣  GitHub Pages セットアップ（GITHUB_SETUP.md 参照）")

    print("\n5️⃣  セットアップ確認")
    print("   python test_setup.py")

    print("\n" + "=" * 60)
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)
    finally:
        input("\nEnter キーを押して終了...")
