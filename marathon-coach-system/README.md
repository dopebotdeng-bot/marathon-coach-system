# Marathon Coach System 🏃

🏃 馬拉松教練系統 - 網頁版

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)

## 📱 功能

- 輸入個人跑步數據
- 自動計算能力差距（全馬/半馬）
- 生成專屬訓練課表（24週）
- 鞋款推薦（根據訓練類型）
- 備戰天數倒數

## 🚀 部署到 Streamlit Cloud

### 快速部署

1. 前往 https://share.streamlit.io
2. 用 GitHub 登入
3. 選擇這個 Repo: `dopebotdeng-bot/marathon-coach-system`
4. Main file: `marathon_app.py`
5. 點擊 Deploy！

### 本地運行

```bash
# 安裝依賴
pip install -r requirements.txt

# 啟動
streamlit run marathon_app.py
```

## 📁 檔案説明

| 檔案 | 説明 |
|------|------|
| `marathon_app.py` | Web 主程式 |
| `marathon_coach.md` | 教練手冊 |
| `scripts/marathon_coach.py` | 課表生成器 |
| `requirements.txt` | Python 依賴 |

## 👤 作者

- Kevin Deng (用戶)
- System: OpenClaw AI

## 📝 License

MIT