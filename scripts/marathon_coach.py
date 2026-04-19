#!/usr/bin/env python3
"""
馬拉松教練系統 - 課表生成器
目標：全馬 4:00 / 半馬 1:50
"""

from datetime import datetime, timedelta
import json

# ========================
# 運動員資料
# ========================
ATHLETE = {
    "name": "Kevin Deng",
    "current_marathon": "4:28:00",  # 4小時28分
    "current_half": "1:56:00",       # 1小時56分
    "target_marathon": "4:00:00",    # 目標 4小時
    "target_half": "1:50:00",        # 目標 1小時50分
    "race_date": "2026-12-19",       # 奈良馬拉松
    "days_to_race": 244
}

# ========================
# 訓練課表範本 (每週)
# ========================
WEEKLY_TEMPLATES = {
    "base": {
        "name": "基礎期",
        "focus": "有氧基礎",
        "weekly_km": 35,
        "schedule": [
            {"day": 1, "type": "rest", "title": "休息"},
            {"day": 2, "type": "easy", "title": "輕鬆跑 6km", "pace": "6:30-7:00"},
            {"day": 3, "type": "tempo", "title": "節奏跑 8km", "pace": "6:00-6:30"},
            {"day": 4, "type": "easy", "title": "輕鬆跑 5km", "pace": "6:30-7:00"},
            {"day": 5, "type": "rest", "title": "休息或核心"},
            {"day": 6, "type": "long", "title": "長距離 15km", "pace": "6:30-7:00"},
            {"day": 7, "type": "easy", "title": "恢復跑 6km", "pace": "7:00"}
        ]
    },
    "build": {
        "name": "建設期",
        "focus": "里程 + 間歇",
        "weekly_km": 55,
        "schedule": [
            {"day": 1, "type": "rest", "title": "休息"},
            {"day": 2, "type": "interval", "title": "間歇 6x800m", "pace": "4:30-5:00"},
            {"day": 3, "type": "easy", "title": "輕鬆跑 10km", "pace": "6:00-6:30"},
            {"day": 4, "type": "tempo", "title": "門診日 12km", "pace": "5:45-6:00"},
            {"day": 5, "type": "rest", "title": "休息或核心"},
            {"day": 6, "type": "long", "title": "長距離 22km", "pace": "6:00-6:30"},
            {"day": 7, "type": "easy", "title": "恢復跑 8km", "pace": "6:30-7:00"}
        ]
    },
    "peak": {
        "name": "巔峰期",
        "focus": "強度 + 耐力",
        "weekly_km": 70,
        "schedule": [
            {"day": 1, "type": "rest", "title": "休息"},
            {"day": 2, "type": "interval", "title": "間歇 8x1000m", "pace": "4:20-4:40"},
            {"day": 3, "type": "easy", "title": "輕鬆跑 12km", "pace": "5:45-6:15"},
            {"day": 4, "type": "tempo", "title": "節奏跑 15km", "pace": "5:30-5:45"},
            {"day": 5, "type": "rest", "title": "休息或核心"},
            {"day": 6, "type": "long", "title": "長距離 28km", "pace": "5:45-6:15"},
            {"day": 7, "type": "easy", "title": "恢復跑 10km", "pace": "6:30-7:00"}
        ]
    },
    "taper": {
        "name": "減量期",
        "focus": "恢復 + 衝刺",
        "weekly_km": 45,
        "schedule": [
            {"day": 1, "type": "rest", "title": "休息"},
            {"day": 2, "type": "interval", "title": "短間歇 4x400m", "pace": "4:00"},
            {"day": 3, "type": "easy", "title": "輕鬆跑 8km", "pace": "6:00-6:30"},
            {"day": 4, "type": "tempo", "title": "短節奏 10km", "pace": "5:30"},
            {"day": 5, "type": "rest", "title": "休息"},
            {"day": 6, "type": "race", "title": "比賽日！", "subtitle": "奈良馬拉松"},
            {"day": 7, "type": "easy", "title": "恢復跑 5km", "pace": "7:00"}
        ]
    }
}

# ========================
# 鞋款建議
# ========================
SHOE_RECOMMENDATIONS = {
    "easy": {"name": "日常訓練", "shoes": ["Nike Air Zoom Pegasus 41", "ASICS Gel-Cumulus 26", "Hoka Clifton 9"]},
    "tempo": {"name": "節奏跑", "shoes": ["Nike Air Zoom Streak 9", "adidas Boston 13", "Saucony Endorphin Speed"]},
    "interval": {"name": "間歇跑", "shoes": ["Nike ZoomX Vaporfly 3", "adidas Takumi Sen 9", "New Balance FuelCell Rebel"]},
    "long": {"name": "長距離", "shoes": ["Hoka Bondi 8", "Nike React Infinity", "ASICS Gel-Nimbus 26"]},
    "race": {"name": "比賽用", "shoes": ["Nike Vaporfly 3", "adidas Adizero Pro 3", "Hoka Rocket X2"]}
}

def generate_training_plan():
    """生成完整訓練計畫"""
    weeks = ATHLETE["days_to_race"] // 7
    plan = []
    
    # 分配訓練階段
    phases = [
        ("base", 4),      # 基礎期 4週
        ("build", 8),     # 建設期 8週  
        ("peak", 8),     # 巔峰期 8週
        ("taper", 4),    # 減量期 4週
    ]
    
    week_num = 1
    for phase, weeks_count in phases:
        for w in range(weeks_count):
            phase_data = WEEKLY_TEMPLATES[phase]
            week_plan = {
                "week": week_num,
                "phase": phase_data["name"],
                "focus": phase_data["focus"],
                "weekly_km": phase_data["weekly_km"],
                "days": phase_data["schedule"]
            }
            plan.append(week_plan)
            week_num += 1
    
    return plan

def get_shoe_for_training(training_type):
    """取得訓練適用的鞋款"""
    return SHOE_RECOMMENDATIONS.get(training_type, {})

# ========================
# 主程式
# ========================
def main():
    print("="*60)
    print("🏃 馬拉松教練系統 - Kevin Deng 專用")
    print("="*60)
    print(f"\n📅 目標比賽: {ATHLETE['race_date']} 奈良馬拉松")
    print(f"⏰ 備戰天數: {ATHLETE['days_to_race']} 天")
    print(f"\n📊 目標:")
    print(f"   全馬: {ATHLETE['current_marathon']} → {ATHLETE['target_marathon']}")
    print(f"   半馬: {ATHLETE['current_half']} → {ATHLETE['target_half']}")
    
    # 生成課表
    plan = generate_training_plan()
    
    print(f"\n🗓️ 訓練計畫 ({len(plan)} 週)")
    print("-"*60)
    
    for week in plan[:8]:  # 顯示前8週
        print(f"第{week['week']:2d}週 | {week['phase']:8s} | 里程: {week['weekly_km']:2d}km | {week['focus']}")
    
    print("-"*60)
    print(f"... 共 {len(plan)} 週訓練計畫")
    
    # 顯示鞋款建議
    print(f"\n👟 鞋款建議:")
    for type_, shoes in SHOE_RECOMMENDATIONS.items():
        print(f"   {type_:10s}: {shoes['name']}")
    
    print("\n" + "="*60)
    print("✅ 教練系統就緒！")
    print("="*60)

if __name__ == "__main__":
    main()