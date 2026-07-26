import os
import re
import subprocess
from pathlib import Path

print("=" * 50)
print("Chrome バージョン確認ツール")
print("=" * 50)
print()

def get_chrome_version():
    """Windows レジストリから Chrome バージョンを取得"""
    try:
        result = subprocess.run(
            ['reg', 'query', r'HKEY_CURRENT_USER\Software\Google\Chrome\Binaries', '/v', 'pv'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            match = re.search(r'(\d+\.\d+\.\d+\.\d+)', result.stdout)
            if match:
                return match.group(1)
    except:
        pass

    return None

version = get_chrome_version()

if version:
    print(f"✓ Chrome バージョン: {version}")
    print()
    major_version = version.split('.')[0]
    print(f"ダウンロード手順:")
    print(f"1. 以下のURLにアクセス:")
    print(f"   https://googlechromelabs.github.io/chrome-for-testing/")
    print()
    print(f"2. バージョン {version} (major {major_version}) の chromedriver をダウンロード")
    print()
    print(f"3. chromedriver.exe をこのフォルダに配置")
    print()
    print(f"4. setup.bat を実行してセットアップ完了")
else:
    print("⚠ Chrome が見つかりません")
    print("以下の方法で確認してください:")
    print("1. Chrome を起動")
    print("2. 右上のメニュー > Google Chromeについて")
    print("3. バージョン番号をメモ")
    print()
    print("例: 126.0.6478.123")

print()
input("Enter キーを押して終了...")
