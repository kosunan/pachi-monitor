#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
パチンコ情報スクレイピング - セットアップスクリプト
"""
import sys
import subprocess
import os
from pathlib import Path

def run_command(cmd, description):
    """コマンド実行"""
    print(f"\n[{description}]")
    print(f"実行: {' '.join(cmd)}\n")

    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"\n❌ エラー: {description} に失敗しました")
        return False
    return True

def main():
    print("=" * 60)
    print("パチンコ情報スクレイピング - 環境セットアップ")
    print("=" * 60)

    # Python バージョン確認
    print(f"\n[確認] Python バージョン: {sys.version}")

    # カレントディレクトリ
    current_dir = Path(__file__).parent
    os.chdir(current_dir)

    # 1. 仮想環境の存在確認・作成
    venv_dir = current_dir / "venv"

    if venv_dir.exists():
        print(f"✓ 仮想環境が既に存在します: {venv_dir}")
    else:
        print("\n[1/3] 仮想環境を作成中...")
        if not run_command([sys.executable, "-m", "venv", "venv"], "仮想環境作成"):
            return False

    # 仮想環境の Python パス
    if sys.platform == "win32":
        venv_python = venv_dir / "Scripts" / "python.exe"
        venv_pip = venv_dir / "Scripts" / "pip.exe"
    else:
        venv_python = venv_dir / "bin" / "python"
        venv_pip = venv_dir / "bin" / "pip"

    if not venv_python.exists():
        print(f"❌ 仮想環境の Python が見つかりません: {venv_python}")
        return False

    # 2. pip をアップグレード
    print("\n[2/3] pip をアップグレード中...")
    if not run_command([str(venv_pip), "install", "--upgrade", "pip"], "pip アップグレード"):
        return False

    # 3. 依存ライブラリをインストール
    print("\n[3/3] 依存ライブラリをインストール中...")

    packages = [
        "selenium",
        "requests",
        "beautifulsoup4",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client",
    ]

    if not run_command([str(venv_pip), "install"] + packages, "ライブラリインストール"):
        return False

    # 4. インストール確認
    print("\n[確認] ライブラリのインストール確認...")
    try:
        result = subprocess.run(
            [str(venv_python), "-c", "import selenium, requests, bs4, google.auth; print('✓ 全ライブラリ正常')"],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"⚠ 警告: {result.stderr}")
    except Exception as e:
        print(f"⚠ 確認エラー: {e}")

    # 5. フォルダ構成確認
    print("\n" + "=" * 60)
    print("✓ セットアップ完了！")
    print("=" * 60)

    print("\n次のステップ:")
    print("\n1️⃣  Chrome バージョン確認")
    print("   python check_chrome_version.py")

    print("\n2️⃣  ChromeDriver をダウンロード")
    print("   → https://googlechromelabs.github.io/chrome-for-testing/")
    print("   → chromedriver.exe をこのフォルダに配置")

    print("\n3️⃣  セットアップ確認")
    print("   python test_setup.py")

    print("\n仮想環境の有効化:")
    if sys.platform == "win32":
        print("   venv\\Scripts\\activate.bat")
    else:
        print("   source venv/bin/activate")

    print("\n" + "=" * 60)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        sys.exit(1)

    input("\nEnter キーを押して終了...")
