#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - Web UI
每個人都可以上來填寫數據、生成專屬課表！
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json

# ========================
# 頁面設定
# ========================
st.set_page_config(
    page_title="🏃 馬拉松教練系統",
    page_icon="🏃",
    layout="wide"
)

# ========================
# 訓練階段範本
# ========================
WEEKLY_TEMPLATES = {
    "基礎期 (4週)": {
        "name": "基礎期",
        "focus": "有氧基礎",
        "weekly_km": "30-40km",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00/km", "shoes": "日常訓練鞋"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00/km", "shoes": "日常訓練鞋"},
            {"day": "週四", "type": "rest", "title": "休息或核心訓練"},
            {"day": "週五", "type": "easy", "title": "輕鬆跑 5-6km", "pace": "6:30-7:00/km", "shoes": "日常訓練鞋"},
            {"day": "週六", "type": "long", "title": "長距離 10-12km", "pace": "6:30-7:00/km", "shoes": "長距離鞋"},
            {"day": "週日", "type": "easy", "title": "恢復跑 4-5km", "pace": "7:00/km", "shoes": "日常訓練鞋"}
        ]
    },
    "建設期 (8週)": {
        "name": "建設期",
        "focus": "里程提升 + 間歇訓練",
        "weekly_km": "40-60km",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "interval", "title": "間歇訓練 6x800m", "pace": "4:30-5:00/km", "shoes": "間歇跑鞋"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 8-10km", "pace": "6:00-6:30/km", "shoes": "日常訓練鞋"},
            {"day": "週四", "type": "tempo", "title": "節奏跑 10-12km", "pace": "5:45-6:00/km", "shoes": "節奏跑鞋"},
            {"day": "週五", "type": "rest", "title": "休息或核心訓練"},
            {"day": "週六", "type": "long", "title": "長距離 15-20km", "pace": "6:00-6:30/km", "shoes": "長距離鞋"},
            {"day": "週日", "type": "easy", "title": "恢復跑 6-8km", "pace": "6:30-7:00/km", "shoes": "日常訓練鞋"}
        ]
    },
    "巔峰期 (8週)": {
        "name": "巔峰期",
        "focus": "強度訓練 + 耐力",
        "weekly_km": "55-80km",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "interval", "title": "間歇訓練 8x1000m", "pace": "4:20-4:40/km", "shoes": "間歇跑鞋"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 10-12km", "pace": "5:45-6:15/km", "shoes": "日常訓練鞋"},
            {"day": "週四", "type": "tempo", "title": "節奏跑 12-15km", "pace": "5:30-5:45/km", "shoes": "節奏跑鞋"},
            {"day": "週五", "type": "rest", "title": "休息或核心訓練"},
            {"day": "週六", "type": "long", "title": "長距離 20-28km", "pace": "5:45-6:15/km", "shoes": "長距離鞋"},
            {"day": "週日", "type": "easy", "title": "恢復跑 8-10km", "pace": "6:30-7:00/km", "shoes": "日常訓練鞋"}
        ]
    },
    "減量期 (4週)": {
        "name": "減量期",
        "focus": "恢復 + 衝刺",
        "weekly_km": "35-50km",
        "schedule": [
            {"day": "週一", "type": "rest", "title": "休息"},
            {"day": "週二", "type": "interval", "title": "短間歇 4x400m", "pace": "4:00/km", "shoes": "間歇跑鞋"},
            {"day": "週三", "type": "easy", "title": "輕鬆跑 6-8km", "pace": "6:00-6:30/km", "shoes": "日常訓練鞋"},
            {"day": "週四", "type": "tempo", "title": "短節奏 8-10km", "pace": "5:30/km", "shoes": "節奏跑鞋"},
            {"day": "週五", "type": "rest", "title": "休息"},
            {"day": "週六", "type": "long", "title": "長距離 15-20km", "pace": "5:45-6:00/km", "shoes": "長距離鞋"},
            {"day": "週日", "type": "easy", "title": "恢復跑 5km", "pace": "7:00/km", "shoes": "日常訓練鞋"}
        ]
    }
}

# ========================
# 鞋款資料庫
# ========================
SHOES_DB = {
    "日常訓練鞋": ["Nike Air Zoom Pegasus 41", "ASICS Gel-Cumulus 26", "Hoka Clifton 9", "Brooks Ghost 16"],
    "節奏跑鞋": ["Nike Air Zoom Streak 9", "adidas Boston 13", "Saucony Endorphin Speed", "New Balance 880v14"],
    "間歇跑鞋": ["Nike ZoomX Vaporfly 3", "adidas Takumi Sen 9", "New Balance FuelCell Rebel", "Puma Deviate Nitro"],
    "長距離鞋": ["Hoka Bondi 8", "Nike React Infinity Run 3", "ASICS Gel-Nimbus 26", "Brooks Glycerin 21"],
    "比賽用鞋": ["Nike Vaporfly 3", "adidas Adizero Pro 3", "Hoka Rocket X2", "Saucony Endorphin Pro"]
}

# ========================
# 主程式
# ========================
def main():
    # 標題
    st.title("🏃 馬拉松教練系統")
    st.markdown("### 輸入你的數據，生成專屬訓練計畫！")
    st.markdown("---")
    
    # 側邊欄 - 輸入資料
    with st.sidebar:
        st.header("👤 運動員資料")
        
        name = st.text_input("姓名", "Kevin")
        
        col1, col2 = st.columns(2)
        with col1:
            current_half = st.text_input("目前半馬", "1:56")
        with col2:
            target_half = st.text_input("目標半馬", "1:50")
        
        col3, col4 = st.columns(2)
        with col3:
            current_marathon = st.text_input("目前全馬", "4:28")
        with col4:
            target_marathon = st.text_input("目標全馬", "4:00")
        
        race_date = st.date_input("目標比賽日期", value=datetime(2026, 12, 19))
        
        st.markdown("---")
        st.header("👟 鞋款偏好")
        budget = st.select_slider("預算", options=["經濟實惠", "中等", "專業"])
        terrain = st.multiselect("常跑步的地點", ["公路", "操場", "地形", "跑步機"])
    
    # 主內容
    # 計算差距
    st.subheader("📊 能力分析")
    
    # 解析時間
    def parse_time(t):
        try:
            parts = t.split(":")
            return int(parts[0]) * 60 + int(parts[1])
        except:
            return 0
    
    current_half_sec = parse_time(current_half)
    target_half_sec = parse_time(target_half)
    current_marathon_sec = parse_time(current_marathon)
    target_marathon_sec = parse_time(target_marathon)
    
    # 顯示差距
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("半馬差距", f"-{current_half_sec - target_half_sec}分鐘", f"目標: {target_half}")
    with col2:
        st.metric("全馬差距", f"-{current_marathon_sec - target_marathon_sec}分鐘", f"目標: {target_marathon}")
    with col3:
        days_to_race = (race_date - datetime.now().date()).days
        st.metric("備戰天數", f"{days_to_race}天", "加油！")
    
    st.markdown("---")
    
    # 訓練階段選擇
    st.subheader("🗓️ 選擇訓練階段")
    
    phase_options = list(WEEKLY_TEMPLATES.keys())
    selected_phase = st.selectbox("選擇你要的訓練週期", phase_options)
    
    # 顯示該階段課表
    phase_data = WEEKLY_TEMPLATES[selected_phase]
    
    st.markdown(f"**📌 訓練重點**: {phase_data['focus']}")
    st.markdown(f"**🏃 週跑量**: {phase_data['weekly_km']}")
    
    # 顯示每週訓練
    st.subheader(f"📅 {selected_phase} 課表")
    
    schedule_df = pd.DataFrame(phase_data['schedule'])
    
    # 格式化顯示
    for idx, row in schedule_df.iterrows():
        with st.expander(f"{row['day']} - {row['title']}", expanded=True):
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown(f"**🏃 訓練**: {row['title']}")
                st.markdown(f"**⏱️ 配速**: {row['pace']}")
            with col_b:
                st.markdown(f"**👟 建議鞋款**: {row['shoes']}")
                # 顯示鞋款建議
                shoe_options = SHOES_DB.get(row['shoes'], [])
                st.markdown(f"💡 推荐: {', '.join(shoe_options[:2])}")
    
    st.markdown("---")
    
    # 鞋款總覽
    st.subheader("👟 鞋款資料庫")
    
    shoe_tab1, shoe_tab2, shoe_tab3, shoe_tab4, shoe_tab5 = st.tabs(["日常訓練", "節奏跑", "間歇跑", "長距離", "比賽用"])
    
    with shoe_tab1:
        st.dataframe(pd.DataFrame(SHOES_DB["日常訓練鞋"], columns=["鞋款"]), hide_index=True)
    with shoe_tab2:
        st.dataframe(pd.DataFrame(SHOES_DB["節奏跑鞋"], columns=["鞋款"]), hide_index=True)
    with shoe_tab3:
        st.dataframe(pd.DataFrame(SHOES_DB["間歇跑鞋"], columns=["鞋款"]), hide_index=True)
    with shoe_tab4:
        st.dataframe(pd.DataFrame(SHOES_DB["長距離鞋"], columns=["鞋款"]), hide_index=True)
    with shoe_tab5:
        st.dataframe(pd.DataFrame(SHOES_DB["比賽用鞋"], columns=["鞋款"]), hide_index=True)
    
    # Footer
    st.markdown("---")
    st.caption("🏃 馬拉松教練系統 | 2026")

if __name__ == "__main__":
    main()