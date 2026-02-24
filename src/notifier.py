import os
import requests
import logging

# 設定 Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_summary(summaries):
    """
    發送 Telegram 訊息
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        logger.error("未設定 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID，無法發送通知。")
        return False

    # 組裝訊息
    if not summaries:
        final_message = "🤖 <b>每日 AI 趨勢報告</b>\n\n今日無符合條件的新熱門專案。"
    else:
        message_lines = ["🚀 <b>每日 AI 趨勢報告</b> 🚀", ""]
        for item in summaries:
            name = item.get("name", "Unknown Repo")
            url = item.get("url", "#")
            summary = item.get("summary", "無摘要")
            line = f"🔹 <a href='{url}'>{name}</a> - {summary}"
            message_lines.append(line)
            message_lines.append("")
        message_lines.append(f"<i>Generating: {len(summaries)} items</i>")
        final_message = "\n".join(message_lines)
    
    final_message = "\n".join(message_lines)
    
    # 限制字數 (Telegram 上限 4096)
    if len(final_message) > 4000:
        final_message = final_message[:4000] + "... (truncated)"
    
    # 發送 API
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": final_message,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        
        if response.status_code != 200:
            logger.error(f"Telegram API 回傳錯誤: {response.status_code} - {response.text}")
            return False
            
        if response.json().get("ok"):
            logger.info("Telegram 訊息發送成功！")
            return True
        else:
            logger.error(f"Telegram API 回傳 ok=False: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Telegram 發送失敗 (網路錯誤): {e}")
        return False
