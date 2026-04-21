#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - 完整版 (VDOT 科學訓練)
參考: garmin-ai-coach + Coach H
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="🏃 馬拉松教練", page_icon="🏃", layout="wide")

# ========================
# VDOT 配速表 (Daniels' Running Formula)
# ========================
VDOT_PACE = {
    # VDOT 30-35 (全馬 4:00-4:30)
    30: {"E": "7:12-8:02", "M": "6:23", "T": "5:56", "I": "5:29", "R": "4:51"},
    31: {"E": "7:02-7:50", "M": "6:13", "T": "5:47", "I": "5:21", "R": "4:44"},
    32: {"E": "6:53-7:39", "M": "6:04", "T": "5:38", "I": "5:13", "R": "4:37"},
    33: {"E": "6:44-7:29", "M": "5:55", "T": "5:30", "I": "5:06", "R": "4:31"},
    34: {"E": "6:35-7:19", "M": "5:47", "T": "5:22", "I": "4:59", "R": "4:25"},
    35: {"E": "6:27-7:10", "M": "5:39", "T": "5:14", "I": "4:52", "R": "4:19"},
    # VDOT 36-40 (全馬 3:30-4:00)
    36: {"E": "6:20-7:01", "M": "5:31", "T": "5:07", "I": "4:46", "R": "4:14"},
    37: {"E": "6:12-6:53", "M": "5:24", "T": "5:00", "I": "4:40", "R": "4:08"},
    38: {"E": "6:05-6:45", "M": "5:16", "T": "4:53", "I": "4:34", "R": "4:03"},
    39: {"E": "5:58-6:38", "M": "5:09", "T": "4:46", "I": "4:29", "R": "3:58"},
    40: {"E": "5:51-6:30", "M": "5:02", "T": "4:40", "I": "4:24", "R": "3:53"},
}

# 配速區間說明
PACE_ZONES = {
    "E": {"name": "Easy / Marathon (輕鬆/馬拉松配速)", "心率": "60-70%"},
    "M": {"name": "Marathon (馬拉松配速)", "心率": "70-80%"},
    "T": {"name": "Threshold (門檻配速)", "心率": "80-88%"},
    "I": {"name": "Interval (間歇)", "心率": "88-92%"},
    "R": {"name": "Repetition (重複跑)", "心率": "92-100%"},
}

# ========================
# 鞋款資料庫
# ========================
SHOES = {
    "輕鬆跑/Easy Run": [
        "On CloudMonster 2", "On Cloud", "Hoka Clifton 10", "Hoka Clifton 9",
        "ASICS Gel-Nimbus 26", "ASICS Gel-Cumulus 26", "ASICS Gel-Kayano 31",
        "Nike Air Zoom Pegasus 41", "Nike React Miler 4",
        "adidas Ultraboost 23", "adidas Ultraboost Light",
        "Brooks Ghost 16", "Brooks Glycerin 21",
        "New Balance 1080 v14", "New Balance 880v14",
        "Saucony Ride 17", "Saucony Triumph 22",
        "特步兩千公里3代", "Bmai 驚嘆3.0"
    ],
    "節奏跑/Tempo": [
        "On CloudBoom", "Hoka Mach 5", "adidas Boston 13",
        "adidas Takumi Sen 10", "adidas evo sl",
        "ASICS MetaSpeed Edge", "Nike Air Zoom Streak 10",
        "Saucony Endorphin Speed 4", "Saucony Fastwitch",
        "New Balance FuelCell Rebel v4", "Puma Deviate Nitro 3",
        "Superblast4", "Novablast4"
    ],
    "間歇跑/Interval": [
        "On CloudBoom", "Nike ZoomX Vaporfly 3", "Nike ZoomX Streakfly",
        "adidas Takumi Sen 10", "adidas Adizero Pro 4",
        "ASICS MetaSpeed", "Saucony Endorphin Pro 4",
        "New Balance 160X v3", "Puma Nitro",
        "Hoka Rocket X3", "Brooks Hyperion Max",
        "Superblast4", "Novablast4"
    ],
    "長距離/Long Run": [
        "Hoka Bondi 8", "Hoka Clifton Edge", "Nike React Infinity Run 3",
        "Nike Vaporfly 3", "adidas Ultraboost Light",
        "ASICS Gel-Nimbus 26", "Brooks Glycerin Max",
        "New Balance 1070v14", "Saucony Triumph 22"
    ],
    "恢復跑/Recovery": [
        "Hoka Ora Recovery", "Hoka Arahi 7", "ASICS Gel-Kayano 31",
        "Brooks Ghost 16", "Nike Invincible Run 3",
        "Saucony Cohesion", "New Balance 990v6"
    ],
    "比賽/競速": [
        "Nike Vaporfly 4/3%", "Nike Alphafly 3",
        "adidas Adizero Pro 4", "Hoka Rocket X3",
        "Saucony Endorphin Pro 4", "New Balance 160X",
        "Puma Nitro Elite", "Superblast4"
    ]
}

# ========================
# 跑步地點
# ========================
LOCATIONS = {
    "公路/街道": {"icon": "🛣️", "特點": "最接近比賽情境", "建議": "公路跑鞋", "難度": "中等"},
    "跑步機": {"icon": "🏃", "特點": "可控制環境", "建議": "緩震跑鞋", "難度": "簡單"},
    "操場 PU 跑道": {"icon": "🔴", "特點": "軟硬度適中", "建議": "跑道專用", "難度": "簡單"},
    "河堤步道": {"icon": "🌊", "特點": "風景好路面平", "建議": "公路跑鞋", "難度": "中等"},
    "山坡丘陵": {"icon": "⛰️", "特點": "坡度訓練", "建議": "越野跑鞋", "難度": "難"},
}

# ========================
# 科學化訓練課表 (24週)
# ========================
def generate_training_plan(vdot, weeks=24):
    """根據 VDOT 生成訓練課表"""
    
    # 根據 VDOT 估算目標馬拉松時間
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
    
    # 24週訓練計劃
    plan = []
    
    # 基礎期 (1-4週)
    for week in range(1, 5):
        plan.append({
            "週": f"W{week}",
            "階段": "🏗️ 基礎期",
            "主題": "有氧基礎 + 姿勢",
            "里程": f"{30 + week*2}km",
            "重點": "E配速為主，建立習慣",
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
            "週": f"W{week}",
            "階段": "🔨 建設期",
            "主題": "里程 + 間歇 + 節奏",
            "里程": f"{40 + w*3}km",
            "重點": "加入T跑和間歇",
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
            "週": f"W{week}",
            "階段": "⚡ 巔峰期",
            "主題": "強度訓練 + 長跑",
            "里程": f"{55 + w*4}km",
            "重點": "馬拉松配速長跑",
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
            "週": f"W{week}",
            "階段": "📉 減量期",
            "主題": "恢復 + 衝刺",
            "里程": f"{45 - w*5}km",
            "重點": "減少里程，保持強度",
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
    st.markdown("### 基於 VDOT 科學化訓練 | 參考 Daniels' Running Formula")
    st.markdown("---")
    
    with st.sidebar:
        st.header("👤 運動員資料")
        
        name = st.text_input("名字", "Kevin")
        
        # 體能數據
        st.markdown("### 📊 體能數據 (Garmin)")
        
        col1, col2 = st.columns(2)
        with col1:
            vdot = st.number_input("VDOT", min_value=20, max_value=70, value=33)
        with col2:
            vo2max = st.number_input("VO2max", min_value=20, max_value=80, value=45)
        
        rhr = st.number_input("靜止心率 RHR (bpm)", value=52)
        hrv = st.number_input("HRV (ms)", value=45)
        
        # 恢復狀態
        st.markdown("### 😴 今日恢復狀態")
        
        col1, col2 = st.columns(2)
        with col1:
            body_battery = st.slider("Body Battery", 0, 100, 70)
        with col2:
            sleep_score = st.slider("睡眠分數", 0, 100, 75)
        
        # 恢復燈號
        if body_battery >= 80 and sleep_score >= 75 and hrv >= 40:
            recovery_status = "🟢 恢復良好，可以訓練"
        elif body_battery >= 60 or sleep_score >= 65:
            recovery_status = "🟡 適中，適量訓練"
        else:
            recovery_status = "🔴 恢復不足，建議休息"
        
        st.info(recovery_status)
        
        # 目標
        st.markdown("### 🎯 比賽目標")
        col1, col2 = st.columns(2)
        with col1:
            target_marathon = st.text_input("目標全馬", "4:00")
        with col2:
            target_half = st.text_input("目標半馬", "1:50")
        
        race_date = st.date_input("目標比賽", value=datetime(2026, 12, 19))
        
        # 鞋款
        st.markdown("---")
        st.header("👟 你的鞋款")
        my_shoes = []
        for cat, shoes in SHOES.items():
            selected = st.multiselect(f"🏃 {cat}", shoes, default=[], key=f"cat_{cat}")
            my_shoes.extend(selected)
        
        # 地點
        st.markdown("---")
        st.header("🏃 跑步地點")
        locs = st.multiselect("選擇", list(LOCATIONS.keys()), default=["公路/街道"])
    
    # ========================
    # 主內容
    # ========================
    
    # 計算
    days_to_race = (race_date - datetime.now().date()).days
    weeks_to_race = days_to_race // 7
    
    # 產生訓練計劃
    plan, marathon_time, pace = generate_training_plan(vdot, weeks_to_race)
    
    # 顯示分析
    st.header("📊 體能分析")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("VDOT", vdot, f"馬拉松預估: {marathon_time}")
    col2.metric("VO2max", vo2max)
    col3.metric("RHR", f"{rhr} bpm")
    col4.metric("備戰", f"{days_to_race}天 / {weeks_to_race}週")
    
    # 配速區間
    st.header("⏱️ 你的 VDOT 配速區間")
    
    pace_df = pd.DataFrame(VDOT_PACE.get(vdot, VDOT_PACE[33]).items(), 
                          columns=["區間", "配速"])
    st.dataframe(pace_df, hide_index=True, use_container_width=True)
    
    with st.expander("📖 配速區間說明"):
        for zone, info in PACE_ZONES.items():
            st.markdown(f"**{zone}**: {info['name']} (心率 {info['心率']})")
    
    # 恢復狀態
    st.header("😴 今日恢復狀態")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Body Battery", body_battery, "能量狀態")
    col2.metric("睡眠分數", sleep_score)
    col3.metric("HRV", f"{hrv} ms")
    col4.metric("RHR", f"{rhr} bpm")
    
    # 恢復建議
    st.markdown("#### 💡 恢復建議")
    
    if body_battery < 50:
        st.warning("⚠️ Body Battery 過低，今天建議休息或只做輕鬆恢復跑")
    elif hrv < 30:
        st.warning("⚠️ HRV 偏低，神經系統疲勞，建議減少強度")
    elif sleep_score < 60:
        st.info("💤 睡眠不足，今天訓練強度降低")
    else:
        st.success("✅ 恢復狀態良好，可以執行計畫訓練！")
    
    # 訓練課表
    st.header("🗓️ 訓練課表 (24週)")
    
    # 選擇週數
    week_options = [p["週"] for p in plan]
    selected_week = st.selectbox("選擇週數", week_options, index=min(weeks_to_race-1, len(week_options)-1) if weeks_to_race > 0 else 0)
    
    # 找到選擇的週
    selected_plan = None
    for p in plan:
        if p["週"] == selected_week:
            selected_plan = p
            break
    
    if selected_plan:
        st.markdown(f"""
        **{selected_plan['階段']}** | {selected_plan['主題']}  
        **本週里程**: {selected_plan['里程']} | **重點**: {selected_plan['重點']}
        """)
        
        # 課表表格
        schedule_data = []
        for row in selected_plan["課表"]:
            # 找鞋款建議
            type_map = {"E": "輕鬆跑/Easy Run", "M": "長距離/Long Run", 
                       "T": "節奏跑/Tempo", "I": "間歇跑/Interval", 
                       "R": "恢復跑/Recovery", "RACE": "比賽/競速"}
            cat = type_map.get(row["type"], "輕鬆跑/Easy Run")
            rec_shoes = SHOES.get(cat, [])[:2]
            
            # 檢查用戶是否有
            owned = [s for s in my_shoes if any(r in s for r in rec_shoes)]
            
            schedule_data.append({
                "day": row["day"],
                "type": row["type"],
                "title": row["title"],
                "pace": row["pace"],
                "shoes": ", ".join(owned) if owned else f"➕ {rec_shoes[0]}" if rec_shoes else "-"
            })
        
        schedule_df = pd.DataFrame(schedule_data)
        st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        
        # 配速說明
        with st.expander("📖 本週訓練配速說明"):
            for row in selected_plan["課表"]:
                if row["type"] != "RACE":
                    st.markdown(f"**{row['day']} {row['title']}**: {row['pace']}")
    
    # 鞋款建議
    st.header("👟 鞋款建議")
    
    if my_shoes:
        st.success(f"✅ 你已有 {len(my_shoes)} 雙鞋: {', '.join(my_shoes[:5])}")
    else:
        st.info("請在側邊欄選擇你現有的鞋款")
    
    tab1, tab2, tab3 = st.tabs(["輕鬆跑", "間歇/節奏", "長距離/比賽"])
    
    with tab1:
        st.dataframe(pd.DataFrame(SHOES["輕鬆跑/Easy Run"][:10], columns=["鞋款"]), hide_index=True)
    with tab2:
        st.dataframe(pd.DataFrame(SHOES["間歇跑/Interval"][:10], columns=["鞋款"]), hide_index=True)
    with tab3:
        st.dataframe(pd.DataFrame(SHOES["長距離/Long Run"][:10], columns=["鞋款"]), hide_index=True)
    
    # 下載功能
    st.header("📱 下載課表")
    
    if st.button("📥 生成下載"):
        race_date_str = race_date.strftime("%Y-%m-%d")
        
        download_text = f"""🏃 Kevin的馬拉松訓練
目標: {target_marathon} (全馬) / {target_half} (半馬)
VDOT: {vdot} | VO2max: {vo2max}
比賽日期: {race_date_str}
備戰: {days_to_race}天

═══════════════════════
📊 體能數據
═══════════════════════
VDOT: {vdot}
VO2max: {vo2max}
RHR: {rhr} bpm
HRV: {hrv} ms
Body Battery: {body_battery}
睡眠分數: {sleep_score}

═══════════════════════
⏱️ 配速區間 (VDOT {vdot})
═══════════════════════
E區間: {pace['E']}
M區間: {pace['M']}
T區間: {pace['T']}
I區間: {pace['I']}
R區間: {pace['R']}

═══════════════════════
📅 訓練課表
═══════════════════════
"""
        
        for p in plan:
            download_text += f"\n{p['週']} - {p['階段']}\n"
            download_text += f"里程: {p['里程']} | 重點: {p['重點']}\n"
            for row in p["課表"]:
                download_text += f"  {row['day']}: {row['title']} @ {row['pace']}\n"
        
        st.download_button(
            label="📥 下載完整訓練計畫",
            data=download_text,
            file_name=f"marathon_plan_{race_date_str}.txt",
            mime_type="text/plain"
        )
    
    st.markdown("---")
    st.caption("🏃 馬拉松教練系統 | 科學化訓練，快樂跑步！")

if __name__ == "__main__":
    main()