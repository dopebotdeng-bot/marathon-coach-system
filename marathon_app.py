#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - Web UI (升級版)
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ========================
# 頁面設定
# ========================
st.set_page_config(
    page_title="🏃 馬拉松教練系統",
    page_icon="🏃",
    layout="wide"
)

# ========================
# 跑步地點與對應訓練
# ========================
LOCATIONS = {
    "公路/街道": {
        "icon": "🛣️",
        "特點": "最接近比賽情境，練習穩定性",
        "建議輪胎": "公路跑鞋 / all-road",
        "訓練類型": ["長距離", "節奏跑", " LSD"],
        "難度": "中等"
    },
    "跑步機": {
        "icon": "🏃",
        "特點": "可控制環境，穩定配速",
        "建議輪胎": "緩震為主",
        "訓練類型": ["輕鬆跑", "間歇", "暖身"],
        "難度": "簡單"
    },
    "操場 PU 跑道": {
        "icon": "🔴",
        "特點": "軟硬度適中，緩衝好",
        "建議輪胎": "跑道專用鞋",
        "訓練類型": ["間歇跑", "衝刺", "練習"],
        "難度": "簡單"
    },
    "田徑場草地": {
        "icon": "🌱",
        "特點": "軟草地，衝擊小",
        "建議輪胎": "輕量訓練鞋",
        "訓練類型": ["恢復跑", "法萊克"],
        "難度": "簡單"
    },
    "公園綠地": {
        "icon": "🌳",
        "特點": "變化地形，訓練平衡",
        "建議輪胎": "trail 越野鞋",
        "訓練類型": ["輕鬆跑", "漸速跑"],
        "難度": "中等"
    },
    "河堤步道": {
        "icon": "🌊",
        "特點": "風景好，路面平穩",
        "建議輪胎": "公路跑鞋",
        "訓練類型": ["長距離", "Tempo"],
        "難度": "中等"
    },
    "山坡地/丘陵": {
        "icon": "⛰️",
        "特點": "坡度訓練，增強爬坡能力",
        "建議輪胎": "競速越野鞋",
        "訓練類型": ["坡度跑", "階梯訓練"],
        "難度": "困難"
    },
    "登山步道": {
        "icon": "🥾",
        "特點": "自然地形，綜合訓練",
        "建議輪胎": "越野登山鞋",
        "訓練類型": ["越野跑", "技術訓練"],
        "難度": "困難"
    },
    "田徑場紅土": {
        "icon": "🍂",
        "特點": "軟紅土，保護關節",
        "建議輪胎": "練習鞋",
        "訓練類型": ["長距離", "輕鬆跑"],
        "難度": "簡單"
    },
    "海灘/沙灘": {
        "icon": "🏖️",
        "特點": "軟沙，加強腳踝",
        "建議輪胎": "沙灘專用鞋",
        "訓練類型": ["沖刺", "阻力訓練"],
        "難度": "困難"
    }
}

# ========================
# 鞋款資料庫（50+）
# ========================
SHOES_DB = {
    # 日常訓練鞋 (入門/休閒)
    "入門/休閒": [
        "Nike Air Zoom Pegasus 41", "ASICS Gel-Cumulus 26", "Hoka Clifton 10",
        "Brooks Ghost 16", "New Balance 1080 v14", "Saucony Ride 17",
        "adidas Ultraboost 23", "Puma Forever Run", "ASICS Dynafit"
    ],
    # 輕鬆跑鞋
    "輕鬆跑": [
        "Nike Air Zoom Pegasus 41 Turbo", "Hoka Clifton 9", "ASICS Gel-Nimbus 26",
        "Brooks Glycerin 21", "Nike React Miler 4", "adidas Solarthun",
        "Hoka Arahi 7", "New Balance 880v14", "Saucony Endorphin Shift 4"
    ],
    # 節奏跑 / Tempo
    "節奏跑": [
        "Nike Air Zoom Streak 10", "adidas Boston 13", "Saucony Endorphin Speed 4",
        "New Balance FuelCell Rebel v4", "Puma Deviate Nitro 3", "Hoka Mach 5",
        "Nike Vaporfly 3 (Tempo用)", "ASICS MetaSpeed", "Saucony Fastwitch"
    ],
    # 間歇跑 /Interval
    "間歇跑": [
        "Nike ZoomX Vaporfly 3", "Nike ZoomX Streakfly", "adidas Takumi Sen 10",
        "New Balance FuelCell Dragonfly", "Puma Fast-Trac", "Hoka Rocket X3",
        "Saucony Endorphin Pro 4", "Nike Streak 9", "adidas Adizero AV2"
    ],
    # 長距離 / Long Run
    "長距離": [
        "Hoka Bondi 8", "Nike React Infinity Run 3", "ASICS Gel-Nimbus 26",
        "Brooks Glycerin Max", "adidas Ultraboost Light", "Hoka Clifton Edge",
        "Puma Magnify Nitro 2", "New Balance 1070v14", "Saucony Triumph 22"
    ],
    # 越野 Trail
    "越野/登山": [
        "Hoka Speedgoat 6", "ASICS FujiTrabuco 14", "Brooks Caldera 7",
        "New Balance Fresh Foam X More", "Nike Pegasus Trail 5", "Salomon Speedcross",
        "adidas Terrex", "Hoka Challenger", "Saucony Endorphin Trail"
    ],
    # 跑道專用
    "跑道/田徑": [
        "Nike Streak 9", "Nike Streak LC", "Adidas Takumi San", 
        "New Balance FuelCell Supercomp", "Miz波鞋", "Puma evoSpeed",
        "Saucony type A9", "Brooks pureGrit", "ASICS Tarther"
    ],
    # 恢復跑
    "恢復跑": [
        "Hoka Ora Recovery", "ASICS Gel-Kayano 31", "Brooks Adrenaline",
        "Nike Invincible Run 3", "Hoka Clifton L", "Saucony Cohesion",
        "New Balance 990v6", "Puma Tazon", "ASICS Load"
    ],
    # 比賽用鞋
    "比賽/競速": [
        "Nike Vaporfly 3 /4%", "Nike Alphafly 3", "adidas Adizero Pro 4",
        "adidas Takumi Sen 10", "Hoka Rocket X3", "Saucony Endorphin Pro 4",
        "New Balance FuelCell Supercomp", "Puma Nitro", "Miz波王",
        "NB 160X", "Brooks Hyperion Max", "Saucony Endorphin Elite"
    ],
    # 冬季/雨天
    "冬季/雨天": [
        "Nike Pegasus Shield", "ASICS GT-2000", "Brooks Beargato",
        "adidas Terrex Free Hiker", "Hoka Taranga", "Waterproof鞋款"
    ]
}

# ========================
# 訓練課表資料
# ========================
TRAINING_PHASES = {
    "基礎期 (4週)": {
        "focus": "有氧基礎 + 姿勢調整",
        "weekly_km": "30-40km",
        "intensity": "低",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00/km"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00/km"},
            {"day": "週四", "type": "rest", "title": "休息 / 核心訓練"},
            {"day": "週五", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00/km"},
            {"day": "週六", "type": "long", "title": "長距離 10-12km", "pace": "6:30-7:00/km"},
            {"day": "週日", "type": "easy", "title": "恢復跑 4-5km", "pace": "7:00/km"}
        ]
    },
    "建設期 (8週)": {
        "focus": "里程提升 + 間歇訓練",
        "weekly_km": "45-65km",
        "intensity": "中等",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "interval", "title": "間歇 6x800m", "pace": "4:30-5:00/km"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 8-10km", "pace": "6:00-6:30/km"},
            {"day": "週四", "type": "tempo", "title": "節奏跑 10-12km", "pace": "5:45-6:00/km"},
            {"day": "週五", "type": "rest", "title": "休息 / 核心訓練"},
            {"day": "週六", "type": "long", "title": "長距離 18-25km", "pace": "6:00-6:30/km"},
            {"day": "週日", "type": "easy", "title": "恢復跑 6-8km", "pace": "6:30-7:00/km"}
        ]
    },
    "巔峰期 (8週)": {
        "focus": "強度訓練 + 馬拉松配速",
        "weekly_km": "60-85km",
        "intensity": "高",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "interval", "title": "間歇 8x1000m", "pace": "4:20-4:40/km"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 10-12km", "pace": "5:45-6:15/km"},
            {"day": "週四", "type": "tempo", "title": "節奏跑 12-18km", "pace": "5:30-5:45/km"},
            {"day": "週五", "type": "rest", "title": "休息 / 核心訓練"},
            {"day": "週六", "type": "long", "title": "長距離 22-32km", "pace": "5:45-6:15/km"},
            {"day": "週日", "type": "easy", "title": "恢復跑 8-10km", "pace": "6:30-7:00/km"}
        ]
    },
    "減量期 (4週)": {
        "focus": "恢復 + 巔峰狀態",
        "weekly_km": "35-50km",
        "intensity": "低-中",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "interval", "title": "短間歇 4x400m", "pace": "4:00/km"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 6-8km", "pace": "6:00-6:30/km"},
            {"day": "週四", "type": "tempo", "title": "短節奏 8-10km", "pace": "5:30/km"},
            {"day": "週五", "type": "rest", "title": "休息"},
            {"day": "週六", "type": "race", "title": "比賽日！", "pace": "目標配速"},
            {"day": "週日", "type": "easy", "title": "恢復跑 5km", "pace": "7:00/km"}
        ]
    }
}

def parse_time(t):
    """解析時間格式"""
    try:
        parts = t.split(":")
        return int(parts[0]) * 60 + int(parts[1])
    except:
        return 0

# ========================
# 主程式
# ========================
def main():
    st.title("🏃 馬拉松教練系統")
    st.markdown("### 建立你的專屬訓練計畫！")
    st.markdown("---")
    
    # 側邊欄 - 資料輸入
    with st.sidebar:
        st.header("👤 運動員資料")
        name = st.text_input("名字", "Kevin")
        
        st.markdown("### 📊 目前成績")
        col1, col2 = st.columns(2)
        with col1:
            current_half = st.text_input("半馬", "1:56")
        with col2:
            target_half = st.text_input("目標半馬", "1:50")
        
        col3, col4 = st.columns(2)
        with col3:
            current_marathon = st.text_input("全馬", "4:28")
        with col4:
            target_marathon = st.text_input("目標全馬", "4:00")
        
        race_date = st.date_input("目標比賽日期", value=datetime(2026, 12, 19))
        
        # 跑步地點偏好
        st.markdown("### 🏃 跑步地點偏好")
        location_options = list(LOCATIONS.keys())
        selected_locations = st.multiselect("選擇你常跑步的地點", location_options, default=["公路/街道", "跑步機"])
        
        # 鞋款偏好輸入
        st.markdown("### 👟 鞋款偏好")
        shoe_type = st.selectbox("選擇訓練類型", list(SHOES_DB.keys()))
        custom_shoes = st.text_input("或輸入你自己的鞋款（用逗號分開）", "")
        
        st.markdown("---")
        st.markdown("**💡 按 Generate 產生課表！**")
        
        generate_btn = st.button("🏃 Generate Training Plan", type="primary")
    
    # 主內容區 - 跑步地點分析
    st.subheader("🏃 跑步��點分析")
    
    if selected_locations:
        col1, col2, col3 = st.columns(3)
        
        # 顯示每個地點的特點
        for idx, loc in enumerate(selected_locations):
            data = LOCATIONS[loc]
            with [col1, col2, col3][idx % 3]:
                with st.expander(f"{data['icon']} {loc}", expanded=True):
                    st.markdown(f"**特點**: {data['特點']}")
                    st.markdown(f"**建議輪胎**: {data['建議輪胎']}")
                    st.markdown(f"**難度**: {data['難度']}")
                    st.markdown(f"**訓練類型**: {', '.join(data['訓練類型'])}")
    else:
        st.info("請在側邊欄選擇你常跑步的地點")
    
    st.markdown("---")
    
    # 顯示鞋款選項
    st.subheader(f"👟 {shoe_type} 鞋款建議")
    
    # 合併選項
    all_shoes = SHOES_DB[shoe_type]
    if custom_shoes:
        custom_list = [s.strip() for s in custom_shoes.split(",")]
        all_shoes = custom_list + all_shoes
    
    shoes_df = pd.DataFrame(all_shoes[:50], columns=["鞋款"])
    st.dataframe(shoes_df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    # 訓練生成區
    st.header("🗓️ 訓練課表")
    
    if generate_btn:
        # 解析時間
        current_half_sec = parse_time(current_half)
        target_half_sec = parse_time(target_half)
        current_marathon_sec = parse_time(current_marathon)
        target_marathon_sec = parse_time(target_marathon)
        
        days_to_race = (race_date - datetime.now().date()).days
        
        # 顯示分析結果
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("半馬差距", f"-{(current_half_sec - target_half_sec)//60}分鐘", f"目標: {target_half}")
        with col2:
            st.metric("全馬差距", f"-{(current_marathon_sec - target_marathon_sec)//60}分鐘", f"目標: {target_marathon}")
        with col3:
            st.metric("備戰天數", f"{days_to_race}天", "加油！")
        
        st.markdown("---")
        
        # 選擇訓練階段
        phase = st.selectbox("選擇訓練階段", list(TRAINING_PHASES.keys()), index=1)
        
        # 顯示課表
        phase_data = TRAINING_PHASES[phase]
        
        st.markdown(f"**📌 訓練重點**: {phase_data['focus']}")
        st.markdown(f"**🏃 週跑量**: {phase_data['weekly_km']}")
        st.markdown(f"**⚡ 強度**: {phase_data['intensity']}")
        
        st.markdown("### 📅 本週訓練")
        
        schedule_df = pd.DataFrame(phase_data['schedule'])
        
        # 顯示訓練
        for idx, row in schedule_df.iterrows():
            col_a, col_b = st.columns([3, 2])
            with col_a:
                emoji = {"rest": "😴", "easy": "🚶", "interval": "⚡", "tempo": "🏃", "long": "🏔️", "race": "🏆"}
                st.markdown(f"**{emoji.get(row['type'], '🏃')} {row['day']}**: {row['title']}")
            with col_b:
                st.markdown(f"配速: {row['pace']}")
            
            # 根據選擇的地點推薦鞋款
            if selected_locations and row['type'] != 'rest':
                for loc in selected_locations[:1]:
                    suggested = LOCATIONS[loc]['建議輪胎']
                    st.caption(f"👟 {loc}: {suggested}")

    st.markdown("---")
    st.caption("🏃 馬拉松教練系統 | Build with Streamlit")

if __name__ == "__main__":
    main()