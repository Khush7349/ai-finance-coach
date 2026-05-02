# 💰 AI Finance Coach

An AI-powered personal finance assistant that analyzes your transactions, detects anomalies, and provides intelligent financial insights using RAG (Retrieval-Augmented Generation) and LLMs.

---

## 🚀 Features

- 📊 Transaction Analysis & Visualization  
- 🧠 AI-Generated Financial Insights  
- 🚨 Anomaly Detection (spending spikes, unusual patterns)  
- 🤖 Chat with Your Financial Data (RAG-based)  
- 🎯 Goal Planning with Smart Recommendations  
- ⚡ FastAPI Backend + Streamlit Dashboard  

---

## 🏗️ Tech Stack

- **Backend:** FastAPI  
- **Frontend:** Streamlit  
- **AI/ML:** Sentence Transformers, FAISS, LLM (Ollama)  
- **Data:** Pandas  
- **API Communication:** Requests  

---

## 📁 Project Structure
```

backend/
│
├── main.py
├── config.py
├── llm.py
│
├── routes/
│ ├── transactions.py
│ ├── chat.py
│ ├── insights.py
│ └── goals.py
│
├── services/
│ ├── loader.py
│ ├── categorizer.py
│ ├── anomaly.py
│ ├── rag.py
│ ├── insights.py
│ └── goals.py
│
└── data/
└── sample.csv

frontend/
└── app.py
```

---

## ⚙️ Setup Instructions

### 1. Clone the repository


- git clone https://github.com/your-username/ai-finance-coach.git

- cd ai-finance-coach


---

### 2. Create virtual environment


- python -m venv venv
- source venv/bin/activate # macOS/Linux
- venv\Scripts\activate # Windows


---

### 3. Install dependencies


pip install -r requirements.txt


---

### 4. Start backend


uvicorn backend.main:app --reload


---

### 5. Start frontend


streamlit run frontend/app.py


---

## 🔗 API Endpoints

| Endpoint | Description |
|--------|------------|
| `/api/v1/transactions` | Get transactions |
| `/api/v1/insights` | Generate insights |
| `/api/v1/chat` | Ask finance questions |
| `/api/v1/goals` | Generate savings plan |

---

## 🧠 How It Works

1. **Data Loading** → Transaction CSV is processed  
2. **RAG System** → Embeddings + FAISS for retrieval  
3. **LLM Layer** → Generates insights & answers  
4. **Anomaly Detection** → Detects unusual spending  
5. **Frontend Dashboard** → Visualizes everything  


---

## ⭐ Contribute

Feel free to fork, improve, and submit pull requests!

---

## 👤 Author

**Khushi Sharma**

---
