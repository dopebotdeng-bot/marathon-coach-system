#!/usr/bin/env python3
"""
🏃 馬拉松教練系統 - 完整版
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
# 鞋款資料庫（完整的）
# ========================
SHOES = {
    "輕鬆跑/Easy Run": [
        # On Cloud
        "On CloudMonster 2", "On Cloud", "On Cloud nova",
        # Hoka
        "Hoka Clifton 10", "Hoka Clifton 9", "Hoka Arahi 7", "Hoka Clifton Edge",
        # ASICS
        "ASICS Gel-Nimbus 26", "ASICS Gel-Cumulus 26", "ASICS Gel-Kayano 31", 
        "ASICS Dynafit", "ASICS Gel-Quantum",
        # Nike
        "Nike Air Zoom Pegasus 41", "Nike Air Zoom Pegasus 41 Turbo", "Nike React Miler 4",
        # adidas
        "adidas Ultraboost 23", "adidas Solarthun", "adidas Ultraboost Light",
        # Brooks
        "Brooks Ghost 16", "Brooks Glycerin 21", "Brooks Glycerin Max", "Brooks Ghost Max",
        # New Balance
        "New Balance 1080 v14", "New Balance 880v14", "New Balance 990v6",
        # Saucony
        "Saucony Ride 17", "Saucony Triumph 22", "Saucony Endorphin Shift 4",
        # Puma
        "Puma Forever Run", "Puma Magnify Nitro 2",
        # 其他
        "特步兩千公里3代", "Bmai 驚嘆3.0"
    ],
    "節奏跑/Tempo": [
        "On CloudBoom", "On Cloud surf",
        "Hoka Mach 5", "Hoka Mach 4",
        "adidas Boston 13", "adidas Takumi Sen 10", "adidas evo sl",
        "ASICS MetaSpeed Edge", "ASICS GlideMax",
        "Nike Air Zoom Streak 10", "Nike Streak 9",
        "Saucony Endorphin Speed 4", "Saucony Fastwitch",
        "New Balance FuelCell Rebel v4", "New Balance 880 v13",
        "Puma Deviate Nitro 3", "Puma Fast-Trac",
        "Superblast4", "Novablast4"
    ],
    "間歇跑/Interval": [
        "On CloudBoom", "On Cloud X",
        "Nike ZoomX Vaporfly 3", "Nike ZoomX Streakfly", "Nike Alphafly 3",
        "adidas Takumi Sen 10", "adidas Adizero Pro 4", "adidas ADIZERO SL",
        "ASICS MetaSpeed", "ASICS GlideMax",
        "Saucony Endorphin Pro 4", "Saucony Endorphin Elite",
        "New Balance FuelCell Dragonfly", "New Balance 160X v3", "NB 160X",
        "Puma Nitro", "Puma Nitro Elite",
        "Hoka Rocket X3", "Brooks Hyperion Max",
        "Superblast4", "Novablast4"
    ],
    "長距離/Long Run": [
        "Hoka Bondi 8", "Hoka Bondi 7", "Hoka Clifton Edge",
        "Nike React Infinity Run 3", "Nike Vaporfly 3", "Nike Air Zoom Vomero",
        "adidas Ultraboost Light", "adidas Adizero Pro 4",
        "ASICS Gel-Nimbus 26", "ASICS Gel-Kayano 31", "ASICS Gel-Quantum",
        "Brooks Glycerin Max", "Brooks Glycerin 21",
        "New Balance 1070v14", "New Balance 1080 v14",
        "Saucony Triumph 22", "Saucony Endorphin Shift 4",
        "Puma Magnify Nitro 2"
    ],
    "恢復跑/Recovery": [
        "Hoka Ora Recovery", "Hoka Clifton L", "Hoka Arahi 7",
        "ASICS Gel-Kayano 31", "ASICS Load", "ASICS Dyad",
        "Brooks Adrenaline GTS", "Brooks Ghost 16",
        "Nike Invincible Run 3", "Nike React Miler 4",
        "Saucony Cohesion", "Saucony Ride 17",
        "New Balance 990v6", "New Balance 880v14",
        "特步兩千公里3代", "Puma Tazon"
    ],
    "跑道/田徑": [
        "Nike Streak 9", "Nike Streak LC", "Nike Streak LT",
        "adidas Takumi San", "adidas Takumi Sen 10", "adidas ADIZERO SL",
        "New Balance FuelCell Supercomp", "NB 1000",
        "Miz波鞋", "Puma evoSpeed", "Puma Fast-Trac",
        "Saucony type A9", "Brooks pureGrit",
        "ASICS Tarther", "ASICS DS Trainer"
    ],
    "比賽/競速": [
        "Nike Vaporfly 4/3%", "Nike Alphafly 3", "Nike Alphafly 2",
        "adidas Adizero Pro 4", "adidas Takumi Sen 10", "adidas Takumi Sen 8",
        "Hoka Rocket X3", "Hoka Dragonfly", "Hoka Cielo X",
        "Saucony Endorphin Pro 4", "Saucony Endorphin Elite", "Saucony Fastwitch",
        "New Balance 160X v3", "NB 160X", "NB FuelCell Supercomp",
        "Puma Nitro Elite", "Puma Deviate Nitro 3",
        "Brooks Hyperion Max", "Brooks Hyperion Tempo",
        "Superblast4", "Novablast4", "On CloudBoom"
    ]
}

# ========================
# 練習地點
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
# 練習課表
# ========================
TRAINING_PHASES = {
    "基礎期 (4週)": {"focus": "有氧基礎", "km": "30-40", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息 - 讓身體恢復", "note": "🛏️ 充分休息，補足睡眠", "pace": "-"},
        {"day": "週二", "type": "easy", "title": "輕鬆跑 5-6km @ 6:30-7:00/km", "note": "🚶 輕鬆跑，維持心跳<140", "pace": "6:30-7:00"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 5-6km @ 6:30-7:00/km", "note": "🚶 同上，保持微笑跑", "pace": "6:30-7:00"},
        {"day": "週四", "type": "rest", "title": "休息或核心訓練", "note": "🧘 核心/伸展/按摩滾筒", "pace": "-"},
        {"day": "週五", "type": "easy", "title": "輕鬆跑 5-6km @ 6:30-7:00/km", "note": "🚶 輕鬆跑，不要衝", "pace": "6:30-7:00"},
        {"day": "週六", "type": "long", "title": "長距離 10-12km @ 6:30-7:00/km", "note": "🏔️ 享受長跑，補水!", "pace": "6:30-7:00"},
        {"day": "週日", "type": "easy", "title": "恢復跑 4-5km @ 7:00/km", "note": "🚶 慢慢跑，恢復為主", "pace": "7:00"}
    ]},
    "建設期 (8週)": {"focus": "里程+間歇", "km": "45-65", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "note": "🛏️ 充分休息", "pace": "-"},
        {"day": "週二", "type": "interval", "title": "間歇 6x800m @ 4:30-5:00/km", "note": "⚡ 全力衝刺，恢復慢跑", "pace": "4:30-5:00"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 8-10km @ 6:00-6:30/km", "note": "🚶 恢復跑，補充水分", "pace": "6:00-6:30"},
        {"day": "週四", "type": "tempo", "title": "節奏跑 10-12km @ 5:45-6:00/km", "note": "🏃 配速跑，找到節奏", "pace": "5:45-6:00"},
        {"day": "週五", "type": "rest", "title": "休息或核心", "note": "🧘 按摩、伸展、营养", "pace": "-"},
        {"day": "週六", "type": "long", "title": "長距離 18-25km @ 6:00-6:30/km", "note": "🏔️  LSD，補充足量", "pace": "6:00-6:30"},
        {"day": "週日", "type": "easy", "title": "恢復跑 6-8km @ 6:30-7:00/km", "note": "🚶 慢慢跑，伸展", "pace": "6:30-7:00"}
    ]},
    "巔峰期 (8週)": {"focus": "強度", "km": "60-85", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "note": "🛏️ 完全休息", "pace": "-"},
        {"day": "週二", "type": "interval", "title": "間歇 8x1000m @ 4:20-4:40/km", "note": "⚡ 強度課表，全力!", "pace": "4:20-4:40"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 10-12km @ 5:45-6:15/km", "note": "🚶 恢復為主", "pace": "5:45-6:15"},
        {"day": "週四", "type": "tempo", "title": "節奏跑 12-18km @ 5:30-5:45/km", "note": "🏃 配速跑，維持節奏", "pace": "5:30-5:45"},
        {"day": "週五", "type": "rest", "title": "休息", "note": "🧘 休息+營養", "pace": "-"},
        {"day": "週六", "type": "long", "title": "長距離 22-32km @ 5:45-6:15/km", "note": "🏔️  LSD，碳水補充", "pace": "5:45-6:15"},
        {"day": "週日", "type": "easy", "title": "恢復跑 8-10km @ 6:30-7:00/km", "note": "🚶 放鬆跑", "pace": "6:30-7:00"}
    ]},
    "減量期 (4週)": {"focus": "恢復", "km": "35-50", "schedule": [
        {"day": "週一", "type": "rest", "title": "休息", "note": "🛏️ 完全休息", "pace": "-"},
        {"day": "週二", "type": "interval", "title": "短間歇 4x400m @ 4:00/km", "note": "⚡ 短衝刺，保持強度", "pace": "4:00"},
        {"day": "週三", "type": "easy", "title": "輕鬆跑 6-8km @ 6:00-6:30/km", "note": "🚶 輕鬆跑", "pace": "6:00-6:30"},
        {"day": "週四", "type": "tempo", "title": "短節奏 8-10km @ 5:30/km", "note": "🏃 確認狀態", "pace": "5:30"},
        {"day": "週五", "type": "rest", "title": "休息", "note": "🧘 休息、減法", "pace": "-"},
        {"day": "週六", "type": "race", "title": "🏆 比賽日！", "note": "🎉 全力出擊!", "pace": "目標配速"},
        {"day": "週日", "type": "easy", "title": "恢復跑 5km @ 7:00/km", "note": "🚶 慢慢跑，慶功", "pace": "7:00"}
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
        
        st.markdown("### 📊 目前的成績")
        c1, c2 = st.columns(2)
        with c1: ch = st.text_input("半馬", "1:56")
        with c2: th = st.text_input("目標半馬", "1:50")
        c3, c4 = st.columns(2)
        with c3: cm = st.text_input("全馬", "4:28")
        with c4: tm = st.text_input("目標全馬", "4:00")
        rd = st.date_input("目標比賽", value=datetime(2026,12,19))
        
        # 選擇鞋款
        st.markdown("---")
        st.header("👟 選擇你現有的鞋款")
        
        my_shoes = []
        for cat, shoes in SHOES.items():
            selected = st.multiselect(
                f"🏃 {cat}", 
                options=shoes,
                default=[],
                key=f"cat_{cat}"
            )
            my_shoes.extend(selected)
        
        custom = st.text_input("➕ 其他鞋款（用逗號分開）", "")
        if custom:
            my_shoes.extend([s.strip() for s in custom.split(",") if s.strip()])
        
        st.markdown("---")
        st.header("🏃 跑步地點")
        locs = st.multiselect("選��", list(LOCATIONS.keys()), default=["公路/街道"])
    
    # 顯示分析
    st.subheader("📊 能力分析")
    cs, ts = parse_time(ch), parse_time(th)
    cm2, tm2 = parse_time(cm), parse_time(tm)
    days = (rd - datetime.now().date()).days
    
    c1, c2, c3 = st.columns(3)
    c1.metric("半馬差距", f"-{cs-ts}分", f"目標: {th}")
    c2.metric("全馬差距", f"-{cm2-tm2}分", f"目標: {tm}")
    c3.metric("備戰天", f"{days}天", "加油!")
    
    # === 顯示表格課表 ===
    st.markdown("---")
    st.header("🗓️ 本週訓練課表")
    
    phase = st.selectbox("選擇訓練週期", list(TRAINING_PHASES.keys()), index=1)
    pdata = TRAINING_PHASES[phase]
    
    st.markdown(f"**目標**: {pdata['focus']} | **週跑量**: {pdata['km']}km")
    
    # 轉成 DataFrame 顯示表格
    df = pd.DataFrame(pdata["schedule"])
    
    # 新增鞋款欄位
    shoe_recs = []
    for row in pdata["schedule"]:
        if row['type'] == 'rest':
            shoe_recs.append("-")
        else:
            # 根據訓練類型推薦鞋款
            type_map = {
                "easy": "輕鬆跑/Easy Run",
                "interval": "間歇跑/Interval", 
                "tempo": "節奏跑/Tempo",
                "long": "長距離/Long Run",
                "race": "比賽/競速"
            }
            cat = type_map.get(row['type'], "輕鬆跑/Easy Run")
            rec = SHOES.get(cat, [])[:2]
            
            # 檢查用戶是否有
            owned = []
            for s in my_shoes:
                for r in rec:
                    if r in s or s in r:
                        owned.append(r)
            
            if owned:
                shoe_recs.append(f"✅ {', '.join(owned)}")
            else:
                shoe_recs.append(f"➕ {', '.join(rec[:2])}")
    
    df["建議鞋款"] = shoe_recs
    
    # 顯示表格
    st.dataframe(
        df[["day", "title", "pace", "note", "建議鞋款"]],
        use_container_width=True,
        hide_index=True
    )
    
    # 桌布下載
    st.markdown("---")
    st.header("📱 手機桌布下載")
    
    # 生成文字內容
    race_date_str = rd.strftime("%Y-%m-%d")
        wall_text = f"""🏃 Kevin的馬拉松訓練
📅 目標: {race_date_str}
🎯 目標: 全馬 {tm} / 半馬 {th}
📆 訓練期: {phase}

═══════════════════════
📅  本週訓練課表
═══════════════════════
"""
    for row in pdata["schedule"]:
        wall_text += f"""
{row['day']} {row['title']}
⏱️ 配速: {row['pace']}
📝 {row['note']}
"""
    
    wall_text += f"""
═══════════════════════
🏃 加油！訓練愉快！
═══════════════════════
"""
    
    # 直接顯示下載按鈕
    st.download_button(
        label="📥 下載課表到電腦/手機",
        data=wall_text,
        file_name=f"marathon_schedule_{rd}.txt",
        mime_type="text/plain"
    )
    
    st.info("💡 下載後可存到手機備忘錄，设為手機桌布！")

    st.markdown("---")
    st.caption("🏃 馬拉松教訓系統 | 訓練愉快！")

if __name__ == "__main__":
    main()