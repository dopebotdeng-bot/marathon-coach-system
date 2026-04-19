#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - Web UI (下拉選單版)
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
# 鞋款資料庫（50+）- 全部展開
# ========================
SHOES = {
    "入門/休閒": [
        "Nike Air Zoom Pegasus 41", "ASICS Gel-Cumulus 26", "Hoka Clifton 10",
        "Brooks Ghost 16", "New Balance 1080 v14", "Saucony Ride 17",
        "adidas Ultraboost 23", "Puma Forever Run", "ASICS Dynafit",
        "Brooks Ghost Max", "Nike React Miler 3"
    ],
    "輕鬆跑": [
        "Nike Air Zoom Pegasus 41 Turbo", "Hoka Clifton 9", "ASICS Gel-Nimbus 26",
        "Brooks Glycerin 21", "Nike React Miler 4", "adidas Solarthun",
        "Hoka Arahi 7", "New Balance 880v14", "Saucony Endorphin Shift 4",
        "ASICS Gel-Kayano 31", "Brooks Adrenaline GTS"
    ],
    "節奏跑/ Tempo": [
        "Nike Air Zoom Streak 10", "adidas Boston 13", "Saucony Endorphin Speed 4",
        "New Balance FuelCell Rebel v4", "Puma Deviate Nitro 3", "Hoka Mach 5",
        "Nike Vaporfly 3 (Tempo用)", "ASICS MetaSpeed Edge", "Saucony Fastwitch",
        "adidas ADIZERO SL", "New Balance 880 v13"
    ],
    "間歇跑": [
        "Nike ZoomX Vaporfly 3", "Nike ZoomX Streakfly", "adidas Takumi Sen 10",
        "New Balance FuelCell Dragonfly", "Puma Fast-Trac", "Hoka Rocket X3",
        "Saucony Endorphin Pro 4", "Nike Streak 9", "adidas Adizero AV2",
        "Puma Nitro", "NB 160X v3"
    ],
    "長距離": [
        "Hoka Bondi 8", "Nike React Infinity Run 3", "ASICS Gel-Nimbus 26",
        "Brooks Glycerin Max", "adidas Ultraboost Light", "Hoka Clifton Edge",
        "Puma Magnify Nitro 2", "New Balance 1070v14", "Saucony Triumph 22",
        "Brooks Glycerin 20", "Nike Air Zoom Vomero"
    ],
    "越野 Trail": [
        "Hoka Speedgoat 6", "ASICS FujiTrabuco 14", "Brooks Caldera 7",
        "Nike Pegasus Trail 5", "Salomon Speedcross", "adidas Terrex",
        "Hoka Challenger", "Saucony Endorphin Trail", "New Balance Fresh Foam More",
        "Brooks Catamount", "ASICS Fujiy"
    ],
    "跑道專用": [
        "Nike Streak 9", "Nike Streak LC", "adidas Takumi San", 
        "New Balance FuelCell Supercomp", "Miz波鞋", "Puma evoSpeed",
        "Saucony type A9", "Brooks pureGrit", "ASICS Tarther",
        "Nike Streak LT", "adidas Takumi Sen 8"
    ],
    "恢復跑": [
        "Hoka Ora Recovery", "ASICS Gel-Kayano 31", "Brooks Adrenaline",
        "Nike Invincible Run 3", "Hoka Clifton L", "Saucony Cohesion",
        "New Balance 990v6", "Puma Tazon", "ASICS Load",
        "Brooks Dyad"
    ],
    "比賽/競速": [
        "Nike Vaporfly 4/3%", "Nike Alphafly 3", "adidas Adizero Pro 4",
        "adidas Takumi Sen 10", "Hoka Rocket X3", "Saucony Endorphin Pro 4",
        "New Balance 160X", "Brooks Hyperion Max", "Saucony Endorphin Elite",
        "Puma Nitro Elite", "NB 1000", "Hoka Dragonfly"
    ],
    "冬季/雨天": [
        "Nike Pegasus Shield", "ASICS GT-2000", "Brooks Beargato",
        "adidas Terrex Free Hiker", "Hoka Taranga", "Waterproof款",
        "ASICS-DS Trainer", "Broogs防潑"
    ]
}

# ========================
# 訓練課表
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
    "巔峰期 (8週)": {"focus": "強���", "km": "60-85", "schedule": [
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

def parse_time(t):
    try:
        p = t.split(":")
        return int(p[0])*60 + int(p[1])
    except:
        return 0

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
        with c1: ch = st.text_input("半馬", "1:56")
        with c2: th = st.text_input("目標半馬", "1:50")
        c3, c4 = st.columns(2)
        with c3: cm = st.text_input("全馬", "4:28")
        with c4: tm = st.text_input("目標全馬", "4:00")
        rd = st.date_input("目標比賽", value=datetime(2026,12,19))
        
        # === 我現有的鞋款 ===
        st.markdown("---")
        st.header("👟 選擇你現有的鞋款")
        st.markdown("最多選 3 雙")
        
        # 收集所有鞋款選項 + 自訂
        all_shoe_options = []
        for cat, shoes in SHOES.items():
            for s in shoes:
                all_shoe_options.append(f"[{cat}] {s}")
        
        my_shoes = st.multiselect(
            "從清單選擇或輸入新鞋款",
            options=all_shoe_options,
            default=[],
            format_func=lambda x: x if x else "選擇鞋款..."
        )
        
        # 自訂輸入
        custom_shoe = st.text_input("或輸入新款（不在清單中）", "")
        if custom_shoe:
            my_shoes.append(f"[自訂] {custom_shoe}")
        
        st.markdown("---")
        
        # 跑步��點
        st.header("🏃 跑步地點")
        locs = st.multiselect("選擇", list(LOCATIONS.keys()), default=["公路/街道"])
    
    # 顯示分析
    st.subheader("📊 能力分析")
    cs, ts = parse_time(ch), parse_time(th)
    cm2, tm2 = parse_time(cm), parse_time(tm)
    days = (rd - datetime.now().date()).days
    
    c1, c2, c3 = st.columns(3)
    c1.metric("半馬差距", f"-{cs-ts}分", f"目標: {th}")
    c2.metric("全馬差距", f"-{cm2-tm2}分", f"目標: {tm}")
    c3.metric("備戰天", f"{days}天", "加油!")
    
    st.markdown("---")
    
    # 顯示鞋款與地點
    st.header("👟 你現有的鞋款分析")
    if my_shoes:
        for shoe in my_shoes:
            st.success(f"✅ {shoe}")
    else:
        st.info("請在上方選擇你現有的鞋款")
    
    # 地點建議
    st.subheader("🏃 跑步地點資訊")
    for loc in locs:
        data = LOCATIONS[loc]
        st.markdown(f"**{data['icon']} {loc}**: {data['特點']} → 建議: {data['建議']}")
    
    st.markdown("---")
    
    # 訓練課表
    st.header("🗓️ 訓練課表")
    phase = st.selectbox("選擇訓練週期", list(TRAINING_PHASES.keys()), index=1)
    pdata = TRAINING_PHASES[phase]
    
    st.markdown(f"**目標**: {pdata['focus']} | **週跑量**: {pdata['km']}km")
    
    # 顯示每天
    for row in pdata["schedule"]:
        emoji = {"rest": "😴", "easy": "🚶", "interval": "⚡", "tempo": "🏃", "long": "🏔️", "race": "🏆"}
        
        col_a, col_b = st.columns([3, 2])
        with col_a:
            st.markdown(f"**{emoji[row['type']]} {row['day']}**: {row['title']} ({row['pace']})")
        with col_b:
            if row['type'] != 'rest':
                # 根據訓練類型推薦鞋款
                cat_map = {
                    "easy": "輕鬆跑",
                    "interval": "間歇跑", 
                    "tempo": "節奏跑/ Tempo",
                    "long": "長距離",
                    "race": "比賽/競速"
                }
                cat = cat_map.get(row['type'], "輕鬆跑")
                rec_shoes = SHOES.get(cat, [])[:3]
                owned = []
                for s in my_shoes:
                    for rs in rec_shoes:
                        if rs in s: owned.append(rs)
                
                if owned:
                    st.caption(f"👟 你有: {', '.join(owned)}")
                else:
                    st.caption(f"👟 推薦: {', '.join(rec_shoes[:2])}")

    st.markdown("---")
    st.caption("🏃 馬拉松教練系統 | 訓練愉快！")

if __name__ == "__main__":
    main()