# main.py - AI Trend Watcher
# 每日追蹤 AI 熱門專案並發送摘要
# 規格請參考 README.md

import schedule
import time
import os
import logging
from src.github_client import search_trending_repos
from src.ai_summarizer import summarize_repos
from src.notifier import send_telegram_summary

# 設定 Log
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
            
    except Exception as e:
        logging.error(f"每日任務執行發生錯誤: {e}")

def main():
    """主程式入口"""
    # 讀取排程時間 (預設 05:00)
    schedule_time = os.getenv("SCHEDULE_TIME", "05:00")
    
    # 啟動時先跑一次測試 (確認功能正常)
    # Zeabur 每次部署都會觸發一次通知！
    logging.info("執行啟動測試：嘗試抓取一次 AI 專案...")
    daily_job()
    
    # 設定排程
    schedule.every().day.at(schedule_time).do(daily_job)
    
    logging.info(f"AI Trend Watcher 已啟動，設定每日於 {schedule_time} 執行任務。")
    
    # 啟動排程迴圈
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
