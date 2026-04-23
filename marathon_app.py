#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - 完整版 (VDOT 科學訓練 + Garmin/Strava 同步)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

st.set_page_config(page_title="🏃 馬拉松教練", page_icon="🏃", layout="wide")

# ========================
# 設定檔案
# ========================
CONFIG_FILE = "data/garmin_config.json"

# ========================
# VDOT 配速表
# ========================
VDOT_PACE = {
    30: {"E": "7:12-8:02", "M": "6:23", "T": "5:56", "I": "5:29", "R": "4:51"},
    31: {"E": "7:02-7:50", "M": "6:13", "T": "5:47", "I": "5:21", "R": "4:44"},
    32: {"E": "6:53-7:39", "M": "6:04", "T": "5:38", "I": "5:13", "R": "4:37"},
    33: {"E": "6:44-7:29", "M": "5:55", "T": "5:30", "I": "5:06", "R": "4:31"},
    34: {"E": "6:35-7:19", "M": "5:47", "T": "5:22", "I": "4:59", "R": "4:25"},
    35: {"E": "6:27-7:10", "M": "5:39", "T": "5:14", "I": "4:52", "R": "4:19"},
    36: {"E": "6:20-7:01", "M": "5:31", "T": "5:07", "I": "4:46", "R": "4:14"},
    37: {"E": "6:12-6:53", "M": "5:24", "T": "5:00", "I": "4:40", "R": "4:08"},
    38: {"E": "6:05-6:45", "M": "5:16", "T": "4:53", "I": "4:34", "R": "4:03"},
    39: {"E": "5:58-6:38", "M": "5:09", "T": "4:46", "I": "4:29", "R": "3:58"},
    40: {"E": "5:51-6:30", "M": "5:02", "T": "4:40", "I": "4:24", "R": "3:53"},
}

# ========================
# 鞋款資料庫
# ========================
SHOES = {
    "輕鬆跑/Easy Run": ["On CloudMonster 2", "On Cloud", "Hoka Clifton 10", "ASICS Gel-Nimbus 26",
        "Nike Air Zoom Pegasus 41", "adidas Ultraboost 23", "Brooks Ghost 16", "New Balance 1080 v14",
        "Saucony Ride 17", "特步兩千公里3代", "Bmai 驚嘆3.0"],
    "節奏跑/Tempo": ["On CloudBoom", "Hoka Mach 5", "adidas Boston 13", "adidas Takumi Sen 10",
        "ASICS MetaSpeed Edge", "Nike Air Zoom Streak 10", "Saucony Endorphin Speed 4",
        "New Balance FuelCell Rebel v4", "Superblast4", "Novablast4"],
    "間歇跑/Interval": ["On CloudBoom", "Nike ZoomX Vaporfly 3", "Nike ZoomX Streakfly",
        "adidas Takumi Sen 10", "adidas Adizero Pro 4", "ASICS MetaSpeed",
        "Saucony Endorphin Pro 4", "New Balance 160X v3", "Puma Nitro", "Hoka Rocket X3"],
    "長距離/Long Run": ["Hoka Bondi 8", "Hoka Clifton Edge", "Nike React Infinity Run 3",
        "Nike Vaporfly 3", "adidas Ultraboost Light", "ASICS Gel-Nimbus 26",
        "Brooks Glycerin Max", "New Balance 1070v14", "Saucony Triumph 22"],
    "恢復跑/Recovery": ["Hoka Ora Recovery", "Hoka Arahi 7", "ASICS Gel-Kayano 31",
        "Brooks Ghost 16", "Nike Invincible Run 3", "Saucony Cohesion"],
    "比賽/競速": ["Nike Vaporfly 4/3%", "Nike Alphafly 3", "adidas Adizero Pro 4",
        "Hoka Rocket X3", "Saucony Endorphin Pro 4", "New Balance 160X", "Superblast4"]
}

# ========================
# Garmin/Strava API 類別
# ========================
class GarminAPI:
    """Garmin Connect API"""
    
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = None
        self.token = None
    
    def login(self):
        """登入 Garmin Connect"""
        try:
            import requests
            
            # Garmin Connect 登入
            url = "https://connect.garmin.com/signin"
            s = requests.Session()
            
            # 獲取 CSRF token
            resp = s.get(url)
            csrf = resp.cookies.get("CSRF")
            
            # 登入
            data = {
                "username": self.email,
                "password": self.password,
                "csrid": "斧", 
                "remme": "on"
            }
            headers = {"X-CSRF": csrf}
            
            resp = s.post(url, data=data, headers=headers)
            
            if resp.ok:
                self.session = s
                self.token = csrf
                return True
        except Exception as e:
            print(f"登入錯誤: {e}")
        return False
    
    def get_activities(self, start=0, limit=10):
        """取得活動列表"""
        if not self.session:
            return []
        
        try:
            url = f"https://connect.garmin.com/activitylist-service/users/activities"
            params = {"start": start, "limit": limit}
            resp = self.session.get(url, params=params)
            
            if resp.ok:
                return resp.json()
        except:
            pass
        return []
    
    def get_daily_summary(self, date=None):
        """取得每日摘要"""
        if not self.session:
            return {}
        
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            url = f"https://connect.garmin.com/wellness-api/dailies"
            params = {"date": date}
            resp = self.session.get(url, params=params)
            
            if resp.ok:
                return resp.json()
        except:
            pass
        return {}

class StravaAPI:
    """Strava API"""
    
    def __init__(self, access_token):
        self.access_token = access_token
    
    def get_activities(self, limit=10):
        """取得活動列表"""
        try:
            import requests
            url = "https://www.strava.com/api/v3/activities"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            params = {"per_page": limit}
            
            resp = requests.get(url, headers=headers, params=params)
            
            if resp.ok:
                return resp.json()
        except:
            pass
        return []
    
    def get_athlete(self):
        """取得運動員資料"""
        try:
            import requests
            url = "https://www.strava.com/api/v3/athlete"
            headers = {"Authorization": f"Bearer {self.access_token}"}
            
            resp = requests.get(url, headers=headers)
            
            if resp.ok:
                return resp.json()
        except:
            pass
        return {}

# ========================
# 生成訓練計劃
# ========================
def generate_training_plan(vdot, weeks=24):
    """根據 VDOT 生成訓練課表"""
    
    if vdot >= 40:
        marathon_time = "3:30-3:45"
    elif vdot >= 36:
        marathon_time = "3:45-4:00"
    elif vdot >= 33:
        marathon_time = "4:00-4:15"
    elif vdot >= 30:
        marathon_time = "4:15-4:30"
    else:
        marathon_time = "4:30-5:00"
    
    pace = VDOT_PACE.get(vdot, VDOT_PACE[33])
    
    plan = []
    
    # 基礎期 (1-4週)
    for week in range(1, 5):
        plan.append({
            "週": f"W{week}", "階段": "🏗️ 基礎期", "主題": "有氧基礎",
            "里程": f"{30 + week*2}km", "重點": "E配速",
            "課表": [
                {"day": "週二", "type": "E", "title": f"Easy {5+week}km", "pace": pace["E"]},
                {"day": "週四", "type": "E", "title": f"Easy {5+week}km", "pace": pace["E"]},
                {"day": "週六", "type": "E", "title": f"長距離 {8+week*2}km", "pace": pace["E"]},
                {"day": "週日", "type": "R", "title": f"恢復跑 {3+week}km", "pace": "輕鬆"},
            ]
        })
    
    # 建設期 (5-12週)
    for week in range(5, 13):
        w = week - 4
        plan.append({
            "週": f"W{week}", "階段": "🔨 建設期", "主題": "里程+間歇",
            "里程": f"{40 + w*3}km", "重點": "T跑和間歇",
            "課表": [
                {"day": "週二", "type": "I", "title": f"間歇 {6+w}x800m", "pace": pace["I"]},
                {"day": "週三", "type": "E", "title": f"Easy {8+w}km", "pace": pace["E"]},
                {"day": "週四", "type": "T", "title": f"節奏跑 {8+w}km", "pace": pace["T"]},
                {"day": "週六", "type": "E", "title": f"長距離 {15+w*2}km", "pace": pace["E"]},
                {"day": "週日", "type": "R", "title": f"恢復跑 {5+w}km", "pace": "輕鬆"},
            ]
        })
    
    # 巔峰期 (13-20週)
    for week in range(13, 21):
        w = week - 12
        plan.append({
            "週": f"W{week}", "階段": "⚡ 巔峰期", "主題": "強度訓練",
            "里程": f"{55 + w*4}km", "重點": "MP長跑",
            "課表": [
                {"day": "週二", "type": "I", "title": f"間歇 {8+w}x1000m", "pace": pace["I"]},
                {"day": "週三", "type": "E", "title": f"Easy {10+w}km", "pace": pace["E"]},
                {"day": "週四", "type": "T", "title": f"節奏跑 {12+w}km", "pace": pace["T"]},
                {"day": "週六", "type": "M", "title": f"MP長跑 {18+w*2}km", "pace": pace["M"]},
                {"day": "週日", "type": "R", "title": f"恢復跑 {6+w}km", "pace": "輕鬆"},
            ]
        })
    
    # 減量期 (21-24週)
    for week in range(21, 25):
        w = week - 20
        plan.append({
            "週": f"W{week}", "階段": "📉 減量期", "主題": "恢復",
            "里程": f"{45 - w*5}km", "重點": "減少里程",
            "課表": [
                {"day": "週二", "type": "I", "title": f"短間歇 {4}x400m", "pace": pace["R"]},
                {"day": "週三", "type": "E", "title": f"Easy {6-w}km", "pace": pace["E"]},
                {"day": "週四", "type": "T", "title": f"確認配速 {8-w}km", "pace": pace["T"]},
                {"day": "週六", "type": "RACE", "title": "🏆 比賽日！", "pace": "目標配速"},
                {"day": "週日", "type": "R", "title": "恢復跑 5km", "pace": "輕鬆"},
            ]
        })
    
    return plan, marathon_time, pace

# ========================
# 主程式
# ========================
def main():
    st.title("🏃 馬拉松教練系統")
    st.markdown("### VDOT 科學訓練 + Garmin/Strava 同步")
    st.markdown("---")
    
    # 側邊欄
    with st.sidebar:
        st.header("🔗 API 設定")
        
        api_provider = st.radio("選擇平台", ["Garmin", "Strava", "手動輸入"])
        
        if api_provider == "Garmin":
            st.markdown("### Garmin 登入")
            garmin_email = st.text_input("Email", "0603.kevin63@gmail.com")
            garmin_password = st.text_input("密碼", type="password")
            
            if st.button("🔗 連接 Garmin"):
                with st.spinner("連接中..."):
                    garmin = GarminAPI(garmin_email, garmin_password)
                    if garmin.login():
                        st.success("✅ Garmin 連接成功!")
                        
                        # 取得數據
                        daily = garmin.get_daily_summary()
                        activities = garmin.get_activities()
                        
                        st.session_state['garmin'] = garmin
                        st.session_state['garmin_daily'] = daily
                        st.session_state['garmin_activities'] = activities
                    else:
                        st.error("❌ 登入失敗")
        
        elif api_provider == "Strava":
            st.markdown("### Strava API")
            strava_token = st.text_input("Access Token", type="password")
            
            if st.button("🔗 連接 Strava"):
                with st.spinner("連接中..."):
                    strava = StravaAPI(strava_token)
                    athlete = strava.get_athlete()
                    activities = strava.get_activities()
                    
                    if athlete:
                        st.success(f"✅ Strava 連接成功! {athlete.get('firstname', '')}")
                        st.session_state['strava'] = strava
                        st.session_state['strava_activities'] = activities
                    else:
                        st.error("❌ 連接失敗")
        
        else:
            st.info("💡 在下方手動輸入數據")
        
        st.markdown("---")
        st.header("👤 運動員資料")
        
        name = st.text_input("名字", "Kevin")
        
        st.markdown("### 📊 體能數據")
        
        col1, col2 = st.columns(2)
        with col1:
            vdot = st.number_input("VDOT", min_value=20, max_value=70, value=33)
        with col2:
            vo2max = st.number_input("VO2max", min_value=20, max_value=80, value=45)
        
        rhr = st.number_input("RHR (bpm)", value=52)
        hrv = st.number_input("HRV (ms)", value=45)
        
        st.markdown("### 😴 恢復狀態")
        
        col1, col2 = st.columns(2)
        with col1:
            body_battery = st.slider("Body Battery", 0, 100, 70)
        with col2:
            sleep_score = st.slider("睡眠分數", 0, 100, 75)
        
        # 恢復燈號
        if body_battery >= 80 and sleep_score >= 75 and hrv >= 40:
            recovery_status = "🟢 恢復良好"
        elif body_battery >= 60 or sleep_score >= 65:
            recovery_status = "🟡 適中"
        else:
            recovery_status = "🔴 恢復不足"
        
        st.info(recovery_status)
        
        st.markdown("### 🎯 目標")
        
        col1, col2 = st.columns(2)
        with col1:
            target_marathon = st.text_input("目標全馬", "4:00")
        with col2:
            target_half = st.text_input("目標半馬", "1:50")
        
        race_date = st.date_input("比賽日期", value=datetime(2026, 12, 19))
        
        st.markdown("---")
        st.header("👟 鞋款")
        my_shoes = []
        for cat, shoes in SHOES.items():
            selected = st.multiselect(f"🏃 {cat}", shoes, default=[], key=f"cat_{cat}")
            my_shoes.extend(selected)
    
    # ========================
    # 主內容
    # ========================
    
    # 檢查 API 連接
    if 'garmin_activities' in st.session_state and st.session_state['garmin_activities']:
        st.header("📊 Garmin 訓練數據")
        
        activities = st.session_state['garmin_activities']
        
        # 轉換為表格
        activity_data = []
        for a in activities[:10]:
            activity_data.append({
                "日期": a.get("startTimeLocal", "")[:10] if a.get("startTimeLocal") else "-",
                "運動": a.get("activityType", {}).get("typeKey", "unknown"),
                "距離": f"{a.get('distance', 0)/1000:.2f} km" if a.get('distance') else "-",
                "時間": a.get("duration", "-"),
                "Training Load": a.get("trainingLoad", "-"),
            })
        
        if activity_data:
            st.dataframe(pd.DataFrame(activity_data), use_container_width=True)
    
    elif 'strava_activities' in st.session_state and st.session_state['strava_activities']:
        st.header("📊 Strava 訓練數據")
        
        activities = st.session_state['strava_activities']
        
        activity_data = []
        for a in activities:
            activity_data.append({
                "日期": a.get("start_date_local", "")[:10] if a.get("start_date_local") else "-",
                "運動": a.get("type", "unknown"),
                "距離": f"{a.get('distance', 0)/1000:.2f} km" if a.get('distance') else "-",
                "時間": f"{a.get('moving_time', 0)//60} 分" if a.get('moving_time') else "-",
                "配速": a.get("average_speed", "-"),
            })
        
        if activity_data:
            st.dataframe(pd.DataFrame(activity_data), use_container_width=True)
    
    else:
        st.info("💡 請在左側連接 Garmin 或 Strava API")
    
    st.markdown("---")
    
    # 體能分析
    st.header("📊 體能分析")
    
    days_to_race = (race_date - datetime.now().date()).days
    weeks_to_race = days_to_race // 7
    plan, marathon_time, pace = generate_training_plan(vdot, weeks_to_race)
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("VDOT", vdot, f"馬拉松: {marathon_time}")
    col2.metric("VO2max", vo2max)
    col3.metric("RHR", f"{rhr} bpm")
    col4.metric("備戰", f"{days_to_race}天")
    
    # 配速區間
    st.header("⏱️ VDOT 配速區間")
    
    pace_df = pd.DataFrame(VDOT_PACE.get(vdot, VDOT_PACE[33]).items(), 
                          columns=["區間", "配速"])
    st.dataframe(pace_df, hide_index=True, use_container_width=True)
    
    # 恢復狀態
    st.header("😴 恢復狀態")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Body Battery", body_battery)
    col2.metric("睡眠", sleep_score)
    col3.metric("HRV", f"{hrv} ms")
    col4.metric("RHR", f"{rhr} bpm")
    
    # 恢復建議
    if body_battery < 50 or hrv < 30 or sleep_score < 60:
        st.warning("⚠️ 恢復不足，今天建議休息或輕鬆訓練")
    else:
        st.success("✅ 恢復狀態良好，可以訓練!")
    
    st.markdown("---")
    
    # 訓練課表
    st.header("🗓️ 訓練課表")
    
    week_options = [p["週"] for p in plan]
    selected_week = st.selectbox("選擇週數", week_options, 
                              index=min(weeks_to_race-1, len(week_options)-1) if weeks_to_race > 0 else 0)
    
    for p in plan:
        if p["週"] == selected_week:
            st.markdown(f"**{p['階段']}** | {p['主題']} | {p['里程']}")
            
            schedule_data = []
            for row in p["課表"]:
                type_map = {"E": "輕鬆跑", "M": "長距離", "T": "節奏跑", 
                           "I": "間歇跑", "R": "恢復跑", "RACE": "比賽"}
                cat = row["type"]
                schedule_data.append({
                    "day": row["day"],
                    "type": row["type"],
                    "title": row["title"],
                    "pace": row["pace"]
                })
            
            st.dataframe(pd.DataFrame(schedule_data), use_container_width=True, hide_index=True)
    
    # 下載
    st.header("📥 下載")
    
    race_date_str = race_date.strftime("%Y-%m-%d")
    
    download_text = f"""🏃 Kevin馬拉松訓練
目標: {target_marathon} / {target_half}
VDOT: {vdot} | VO2max: {vo2max}
比賽: {race_date_str}
備戰: {days_to_race}天

📊 體能
VDOT: {vdot}
VO2max: {vo2max}
RHR: {rhr} | HRV: {hrv}
Body Battery: {body_battery}
睡眠: {sleep_score}

⏱️ 配速區間
E: {pace['E']}
M: {pace['M']}
T: {pace['T']}
I: {pace['I']}
R: {pace['R']}

📅 課表
"""
    for p in plan:
        download_text += f"\n{p['週']} - {p['階段']}\n"
        for row in p["課表"]:
            download_text += f"  {row['day']}: {row['title']} @ {row['pace']}\n"
    
    st.download_button("📥 下載訓練計畫", download_text, f"marathon_{race_date_str}.txt")
    
    st.markdown("---")
    st.caption("🏃 馬拉松教練系統")

if __name__ == "__main__":
    main()