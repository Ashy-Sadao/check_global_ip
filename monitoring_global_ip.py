import requests
import os

# --- 設定ここから ---
WEBHOOK_URL = os.environ.get('WEBHOOK_URL')  # 自分のWebhook URLをここに
LAST_IP_FILE = os.environ.get('LAST_IP_FILE')  # IP保存用ファイルのパス
# --- 設定ここまで ---

def get_global_ip():
    try:
        return requests.get("https://api.ipify.org/").text
    except Exception as e:
        print("IP取得エラー:", e)
        return None

def send_to_discord(ip):
    payload = {
        "username": "さだロイド",
        "content": f"🔔 **グローバルIPが変更されました！**\n```{ip}```"
    }
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print("Discord通知エラー:", e)

def read_last_ip():
    if os.path.exists(LAST_IP_FILE):
        with open(LAST_IP_FILE, "r") as f:
            return f.read()
    return None

def save_current_ip(ip):
    os.makedirs(os.path.dirname(LAST_IP_FILE), exist_ok=True)
    with open(LAST_IP_FILE, "w") as f:
        f.write(ip)

def main():
    current_ip = get_global_ip()
    if not current_ip:
        return

    last_ip = read_last_ip()

    if current_ip != last_ip:
        send_to_discord(current_ip)
        save_current_ip(current_ip)
        print(f"IPが変化しました: {current_ip}")
    else:
        print("IPに変化はありません。")

if __name__ == "__main__":
    main()
