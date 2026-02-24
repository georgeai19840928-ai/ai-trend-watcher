import os
import requests
import logging

# 設定 Log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_telegram_summary(github_summaries, clawhub_summaries):
    """
    發送 Telegram 訊息，區分 GitHub 與 ClawHub 區塊
    """
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    
    if not bot_token or not chat_id:
        logger.error("未設定 TELEGRAM_BOT_TOKEN 或 TELEGRAM_CHAT_ID，無法發送通知。")
        return False

    if not github_summaries and not clawhub_summaries:
        final_message = "🤖 <b>每日 AI 趨勢報告</b>\n\n今日無符合條件的新熱門專案。"
    else:
        message_lines = ["🚀 <b>每日 AI 趨勢報告</b> 🚀", ""]
        
        # GitHub Section
        if github_summaries:
            message_lines.append("📂 <b>GitHub 熱門專案</b>")
            for item in github_summaries:
                name = item.get("name", "Unknown Repo")
                url = item.get("url", "#")
                summary = item.get("summary", "無摘要")
                message_lines.append(f"🔹 <a href='{url}'>{name}</a> - {summary}")
            message_lines.append("")

        # ClawHub Section
        if clawhub_summaries:
            message_lines.append("🦐 <b>ClawHub 技能熱門</b>")
            for item in clawhub_summaries:
                name = item.get("name", "Unknown Skill")
                url = item.get("url", "#")
                summary = item.get("summary", "無摘要")
                message_lines.append(f"🔹 <a href='{url}'>{name}</a> - {summary}")
            message_lines.append("")

        message_lines.append(f"<i>Total: {len(github_summaries) + len(clawhub_summaries)} items</i>")
        final_message = "\n".join(message_lines)
    
    # 限制字數 (Telegram 上限 4096)
    if len(final_message) > 4000:
        final_message = final_message[:4000] + "... (truncated)"
    
    # 發送 API
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": final_message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code != 200:
            logger.error(f"Telegram API 回傳錯誤: {response.status_code} - {response.text}")
            return False
        return True
    except Exception as e:
        logger.error(f"Telegram 發送失敗: {e}")
        return False
