# main.py - AI Trend Watcher
# 每日追蹤 AI 熱門專案並發送摘要
# 規格請參考 README.md

import schedule
import time
import os
import logging
import traceback
from dotenv import load_dotenv
from src.github_client import search_trending_repos
from src.ai_summarizer import summarize_repos
from src.notifier import send_telegram_summary

# 載入環境變數 (支援 .env 檔案)
load_dotenv()

# 設定 Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def send_alert(error_msg):
    """
    發送緊急錯誤通知給管理員
    """
    try:
        import requests
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if bot_token and chat_id:
            text = f"🚨 *AI Trend Watcher 系統警報* 🚨\n\n程式發生嚴重錯誤，請檢查：\n`{error_msg}`"
            requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
            )
    except Exception:
        logging.error("無法發送錯誤通知 (可能網路或 Token 有問題)")

def daily_job():
    """每日執行的核心任務"""
    logging.info("開始執行每日 AI 趨勢掃描...")
    
    try:
        # 1. 搜尋熱門 GitHub 專案
        trending_repos = search_trending_repos(limit=10)
        
        if not trending_repos:
            logging.info("今日無特別熱門專案符合條件。")
            return

        # 2. AI 生成摘要
        summaries = summarize_repos(trending_repos)
        
        # 3. 發送 Telegram 通知
        success = send_telegram_summary(summaries)
        
        if success:
            logging.info("每日 AI 趨勢報告發送成功！")
        else:
            logging.error("每日 AI 趨勢報告發送失敗。")
            send_alert("每日報告發送失敗，請檢查 Log。")
            
    except Exception as e:
        error_msg = f"每日任務執行發生錯誤: {str(e)}\n{traceback.format_exc()}"
        logging.error(error_msg)
        send_alert(error_msg)

def send_startup_message():
    """
    發送啟動宣告，確認連線正常
    """
    try:
        import requests
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")
        
        logging.info(f"正在嘗試發送啟動訊息... Chat ID: {chat_id}")
        
        if bot_token and chat_id:
            text = "🤖 *AI Trend Watcher 服務已啟動*\n\n正在連線並準備執行首播測試..."
            response = requests.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"},
                timeout=10
            )
            response.raise_for_status()
            logging.info("啟動訊息發送成功。")
        else:
            logging.warning(f"缺少環境變數: TELEGRAM_BOT_TOKEN={bool(bot_token)}, TELEGRAM_CHAT_ID={bool(chat_id)}")
    except Exception as e:
        logging.error(f"無法發送啟動通知: {e}")

def main():
    """主程式入口"""
    try:
        # 讀取排程時間 (預設 21:00 UTC)
        schedule_time = os.getenv("SCHEDULE_TIME", "21:00")
        
        logging.info("程式啟動中...")
        send_startup_message()
        
        # 啟動時先跑一次測試 (確認功能正常)
        logging.info("執行啟動測試：嘗試抓取一次 AI 專案...")
        daily_job()
        
        # 設定排程
        schedule.every().day.at(schedule_time).do(daily_job)
        
        logging.info(f"AI Trend Watcher 已啟動，設定每日於 {schedule_time} (UTC) 執行任務。")
        
        # 啟動排程迴圈
        while True:
            schedule.run_pending()
            time.sleep(60)
            
    except Exception as e:
        error_msg = f"主程式崩潰 (Main Loop Crash): {str(e)}\n{traceback.format_exc()}"
        logging.critical(error_msg)
        send_alert(error_msg)
        raise e

if __name__ == "__main__":
    main()
