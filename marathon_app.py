#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - Web UI (完整版)
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# ========================
# 頁面設定
# ========================
st.set_page_config(page_title="🏃 馬拉松教練", page_icon="🏃", layout="wide")

# ========================
# 跑步地點
# ========================
LOCATIONS = {
    "公路/街道": {"icon": "🛣️", "特點": "最接近比賽情境", "建議": "公路跑鞋", "難度": "中等"},
    "跑步機": {"icon": "🏃", "特點": "可控制環境", "建議": "緩震跑鞋", "難度": "簡單"},
    "操場 PU 跑道": {"icon": "🔴", "特點": "軟硬度適中", "建議": "跑道專用", "難度": "簡單"},
    "公園綠地": {"icon": "🌳", "特點": "變化地形", "建議": "輕量訓練鞋", "難度": "中等"},
    "河堤步道": {"icon": "🌊", "特點": "風景好路面平", "建議": "公路跑鞋", "難度": "中等"},
    "山坡丘陵": {"icon": "⛰️", "特點": "坡度訓練", "建議": "越野跑鞋", "難度": "難"},
    "登山步道": {"icon": "🥾", "特點": "自然地形", "建議": "登山鞋", "難度": "難"},
    "田徑場紅土": {"icon": "🍂", "特點": "軟紅土", "建議": "練習鞋", "難度": "簡單"},
}

# ========================
# 鞋款資料庫（50+）
# ========================
SHOES = {
    "入門/休閒": ["Nike Pegasus 41", "ASICS Gel-Cumulus 26", "Hoka Clifton 10", "Brooks Ghost 16", "NB 1080 v14"],
    "輕鬆跑": ["Nike Pegasus 41 Turbo", "Hoka Clifton 9", "ASICS Gel-Nimbus 26", "Brooks Glycerin 21", "Nike React Miler 4"],
    "節奏跑": ["Nike Air Zoom Streak 10", "adidas Boston 13", "Saucony Endorphin Speed 4", "New Balance FuelCell Rebel v4", "Puma Deviate Nitro 3"],
    "間歇跑": ["Nike ZoomX Vaporfly 3", "Nike ZoomX Streakfly", "adidas Takumi Sen 10", "NB FuelCell Dragonfly", "Hoka Rocket X3"],
    "長距離": ["Hoka Bondi 8", "Nike React Infinity Run 3", "ASICS Gel-Nimbus 26", "Brooks Glycerin Max", "adidas Ultraboost Light"],
    "越野": ["Hoka Speedgoat 6", "ASICS FujiTrabuco 14", "Brooks Caldera 7", "Nike Pegasus Trail 5", "Salomon Speedcross"],
    "跑道": ["Nike Streak 9", "Nike Streak LC", "adidas Takumi San", "NB FuelCell Supercomp", "Miz波鞋"],
    "恢復跑": ["Hoka Ora Recovery", "ASICS Gel-Kayano 31", "Brooks Adrenaline", "Nike Invincible Run 3", "Saucony Cohesion"],
    "比賽": ["Nike Vaporfly 4%", "Nike Alphafly 3", "adidas Adizero Pro 4", "Hoka Rocket X3", "Saucony Endorphin Pro 4", "NB 160X"],
    "冬季/雨天": ["Nike Pegasus Shield", "ASICS GT-2000", "Brooks Beargato", "adidas Terrex"]
}

# ========================
# 課表資料
# ========================
TRAINING_PHASES = {
    "基礎期 (4週)": {"focus": "有氧基礎", "km": "30-40", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "pace": "-"},
        {"day": "週二", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00"},
        {"day": "週四", "type": "rest", "title": "休息/核心", "pace": "-"},
        {"day": "週五", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00"},
        {"day": "週六", "type": "long", "title": "長距離 10-12km", "pace": "6:30-7:00"},
        {"day": "週日", "type": "easy", "title": "恢復跑 4-5km", "pace": "7:00"}
    ]},
    "建設期 (8週)": {"focus": "里程+間歇", "km": "45-65", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "pace": "-"},
        {"day": "週二", "type": "interval", "title": "間歇 6x800m", "pace": "4:30-5:00"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 8-10km", "pace": "6:00-6:30"},
        {"day": "週四", "type": "tempo", "title": "節奏跑 10-12km", "pace": "5:45-6:00"},
        {"day": "週五", "type": "rest", "title": "休息/核心", "pace": "-"},
        {"day": "週六", "type": "long", "title": "長距離 18-25km", "pace": "6:00-6:30"},
        {"day": "週日", "type": "easy", "title": "恢復跑 6-8km", "pace": "6:30-7:00"}
    ]},
    "巔峰期 (8週)": {"focus": "強度", "km": "60-85", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "pace": "-"},
        {"day": "週二", "type": "interval", "title": "間歇 8x1000m", "pace": "4:20-4:40"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 10-12km", "pace": "5:45-6:15"},
        {"day": "週四", "type": "tempo", "title": "節奏跑 12-18km", "pace": "5:30-5:45"},
        {"day": "週五", "type": "rest", "title": "休息/核心", "pace": "-"},
        {"day": "週六", "type": "long", "title": "長距離 22-32km", "pace": "5:45-6:15"},
        {"day": "週日", "type": "easy", "title": "恢復跑 8-10km", "pace": "6:30-7:00"}
    ]},
    "減量期 (4週)": {"focus": "恢復", "km": "35-50", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "pace": "-"},
        {"day": "週二", "type": "interval", "title": "短間歇 4x400m", "pace": "4:00"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 6-8km", "pace": "6:00-6:30"},
        {"day": "週四", "type": "tempo", "title": "短節奏 8-10km", "pace": "5:30"},
        {"day": "週五", "type": "rest", "title": "休息", "pace": "-"},
        {"day": "週六", "type": "race", "title": "比賽日！", "pace": "目標配速"},
        {"day": "週日", "type": "easy", "title": "恢復跑 5km", "pace": "7:00"}
    ]}
}

# ========================
# 主程式
# ========================
def main():
    st.title("🏃 馬拉松教練系統")
    st.markdown("### 建立你的專屬訓練計畫！")
    st.markdown("---")
    
    with st.sidebar:
        st.header("👤 運動員資料")
        name = st.text_input("名字", "Kevin")
        
        st.markdown("### 📊 目前的馬")
        c1, c2 = st.columns(2)
        with c1:
            ch = st.text_input("半馬", "1:56")
        with c2:
            th = st.text_input("目標半馬", "1:50")
        c3, c4 = st.columns(2)
        with c3:
            cm = st.text_input("全馬", "4:28")
        with c4:
            tm = st.text_input("目標全馬", "4:00")
        
        rd = st.date_input("目標比賽", value=datetime(2026,12,19))
        
        # === 重點：現有鞋款 ===
        st.markdown("---")
        st.header("👟 你的現有鞋款")
        st.markdown("**輸入你擁有的跑鞋**（用逗號分開）")
        my_shoes = st.text_area("例如: Nike Pegasus 41, Hoka Clifton 9", 
                              placeholder="Nike Pegasus 41, Hoka Clifton 9, ASICS Gel-Nimbus")
        
        # 解析現有鞋款
        existing_shoes = [s.strip() for s in my_shoes.split(",") if s.strip()]
        
        # 跑步地點
        st.markdown("---")
        st.header("🏃 跑步地點")
        locs = st.multiselect("選擇你常跑步的地點", list(LOCATIONS.keys()), 
                              default=["公路/街道"])
        
    # 顯示分析
    st.subheader("📊 能力分析")
    
    def parse_time(t):
        try:
            p = t.split(":")
            return int(p[0])*60 + int(p[1])
        except:
            return 0
    
    cs, ts = parse_time(ch), parse_time(th)
    cm2, tm2 = parse_time(cm), parse_time(tm)
    days = (rd - datetime.now().date()).days
    
    c1, c2, c3 = st.columns(3)
    c1.metric("半馬差距", f"-{cs-ts}分", f"目標: {th}")
    c2.metric("全馬差距", f"-{cm2-tm2}分", f"目標: {tm}")
    c3.metric("備戰天", f"{days}天", "加油!")
    
    st.markdown("---")
    
    # === 顯示鞋款建議 ===
    st.header("👟 鞋款與地點建議")
    
    if existing_shoes:
        st.success(f"✅ 你現有 {len(existing_shoes)} 雙鞋: {', '.join(existing_shoes)}")
    else:
        st.info("請在側邊欄輸入你現有的鞋款，我會推薦最適合的！")
    
    # 根據訓練顯示建議
    st.markdown("#### 🔍 根據你的地點推薦")
    for loc in locs:
        data = LOCATIONS[loc]
        st.markdown(f"**{data['icon']} {loc}**: {data['特點']} → 建議: {data['建議']}")
    
    st.markdown("---")
    
    # === 訓練課表 ===
    st.header("🗓️ 訓練課表")
    phase = st.selectbox("選擇訓練週期", list(TRAINING_PHASES.keys()), index=1)
    pdata = TRAINING_PHASES[phase]
    
    st.markdown(f"**目標**: {pdata['focus']} | **週跑量**: {pdata['km']}km")
    
    # 顯示每天訓練
    for row in pdata["schedule"]:
        emoji = {"rest": "😴", "easy": "🚶", "interval": "⚡", "tempo": "🏃", "long": "🏔️", "race": "🏆"}
        
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown(f"**{emoji[row['type']]} {row['day']}**: {row['title']} ({row['pace']})")
        with col_b:
            # 根據訓練類型顯示鞋款建議
            if row['type'] != 'rest':
                shoe_map = {
                    "easy": "輕鬆跑/恢��跑",
                    "interval": "間歇跑/比賽",
                    "tempo": "節奏跑",
                    "long": "長距離",
                    "race": "比賽"
                }
                recommend_cat = shoe_map.get(row['type'], "輕鬆跑")
                # 找相關鞋款
                rec_shoes = SHOES.get(recommend_cat, [])[:2]
                if existing_shoes:
                    st.caption(f"👟 推薦: {', '.join(rec_shoes[:2])} (你有: {existing_shoes[0] if existing_shoes else '?'})")
                else:
                    st.caption(f"👟 推薦: {', '.join(rec_shoes[:2])}")

    st.markdown("---")
    st.caption("🏃 馬拉松教練系統 | 訓練後記得更新 Strava！")

if __name__ == "__main__":
    main()