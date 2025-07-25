
import requests
import os
from datetime import datetime, timedelta
import pytz
import pandas as pd

# Carrega as variáveis diretamente do ambiente (usadas como GitHub Secrets)
APP_KEY = os.getenv("RUNRUN_APP_KEY")
USER_TOKEN = os.getenv("RUNRUN_USER_TOKEN")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

HEADERS = {
    "App-Key": APP_KEY,
    "User-Token": USER_TOKEN,
    "Content-Type": "application/json"
}

def fetch_comments_paginated():
    page = 1
    per_page = 100
    all_comments = []
    while True:
        url = f"https://runrun.it/api/v1.0/comments?page={page}&per_page={per_page}"
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            print(f"Erro na página {page}: {response.text}")
            break
        data = response.json()
        comments = data.get("data", []) if isinstance(data, dict) else data
        if not comments:
            break
        all_comments.extend(comments)
        print(f"Página {page} coletada com {len(comments)} comentários.")
        page += 1
    return all_comments

def filter_yesterday_comments(comments):
    brt = pytz.timezone("America/Sao_Paulo")
    today = datetime.now(brt).date()
    yesterday = today - timedelta(days=1)
    filtered = []
    for c in comments:
        created_at = c.get("created_at")
        try:
            dt = datetime.fromisoformat(created_at.replace("Z", "+00:00")).astimezone(brt)
            if dt.date() == yesterday:
                filtered.append({
                    "DATA": dt.strftime("%d/%m/%Y %H:%M:%S"),
                    "COMMENTER_NAME": c.get("commenter_name", ""),
                    "TASK": c.get("task", {}).get("title", ""),
                    "PROJECT": c.get("task", {}).get("project_name", ""),
                    "SYSTEM_MSG": str(c.get("system_msg", False)).lower(),
                    "TEXT": c.get("text", "").strip()
                })
        except Exception as e:
            print(f"Erro ao processar comentário: {e}")
            continue
    return filtered

def export_to_excel(data, file_path="comentarios_diarios.xlsx"):
    df = pd.DataFrame(data)
    df.to_excel(file_path, index=False)
    return file_path

def send_file_to_telegram(file_path):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendDocument"
    with open(file_path, "rb") as f:
        response = requests.post(url, data={"chat_id": CHAT_ID}, files={"document": f})
    if response.status_code != 200:
        print("Erro ao enviar arquivo para o Telegram:", response.text)

def main():
    comments = fetch_comments_paginated()
    filtered = filter_yesterday_comments(comments)
    print(f"Total de comentários do dia anterior: {len(filtered)}")
    if filtered:
        excel_path = export_to_excel(filtered)
        send_file_to_telegram(excel_path)
    else:
        print("Nenhum comentário para o dia anterior.")

if __name__ == "__main__":
    if not all([APP_KEY, USER_TOKEN, BOT_TOKEN, CHAT_ID]):
        raise Exception("⚠️ Variável de ambiente faltando.")
    main()
