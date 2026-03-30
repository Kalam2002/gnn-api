# 🚀 GNN-Based Intrusion Detection System (IDS) API

A **Graph Neural Network (GNN)-powered Intrusion Detection System API** built using **FastAPI**, capable of detecting multiple cyber attacks such as **DDoS, XSS, Password attacks, and more** from network flow data.

---

## 🧠 Project Overview

This project implements an advanced **Graph-based Machine Learning model** to analyze network traffic and classify it into different attack categories.

Instead of traditional ML approaches, this system:

* Models network flows as a **graph structure**
* Uses **GraphSAGE (GNN)** for feature learning
* Performs **multi-class attack classification**
* Provides predictions via a **REST API**

---

## ⚙️ Tech Stack

* **Backend:** FastAPI
* **Model:** Graph Neural Network (DGL + PyTorch)
* **Libraries:**

  * PyTorch
  * DGL (Deep Graph Library)
  * Pandas, NumPy
  * Scikit-learn
  * Category Encoders
* **Deployment:** Render (Docker)

---

## 📁 Project Structure

```
gnn-api/
│
├── app/
│   ├── main.py
│   ├── inference.py
│   ├── preprocess.py
│   ├── graph_builder.py
│   ├── model_loader.py
│   ├── model_architecture.py
│   └── schemas.py
│
├── artifacts/
│   ├── model.pt
│   ├── encoder.pkl
│   ├── scaler.pkl
│   ├── label_encoder.pkl
│   └── feature_cols.pkl
│
├── requirements.txt
├── Dockerfile
└── README.md
```

---

## 🌐 Live API

🔗 **Base URL:**

```
https://gnn-api-t7k7.onrender.com/
```

---

## 🧪 API Usage

### 🔹 Endpoint: `/predict`

**Method:** POST
**Content-Type:** application/json

---

### 📥 Sample Request

```json

curl -X 'POST' \
  'https://gnn-api-t7k7.onrender.com/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "flows": [
    {
      "src_ip": "192.168.1.193",
      "src_port": 49180,
      "dst_ip": "192.168.1.37",
      "dst_port": 8080,
      "proto": "tcp",
      "service": "-",
      "duration": 0.00013,
      "src_bytes": 0,
      "dst_bytes": 0,
      "conn_state": "REJ",
      "src_pkts": 1,
      "dst_pkts": 1
    }
  ]
}'

```

---

### 📤 Sample Response

```json
{
  "num_flows": 1,
  "predictions": [
    "ddos"
  ]
}
```

---

## 🔥 Features

* ✅ Graph-based intrusion detection
* ✅ Multi-class attack classification
* ✅ Real-time prediction API
* ✅ Supports multiple flows
* ✅ Cloud deployed & publicly accessible
* ✅ Scalable and modular architecture

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/gnn-api.git
cd gnn-api
```

---

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the API

```bash
uvicorn app.main:app --reload
```

---

### 4️⃣ Open Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing with CURL

```bash
curl -X POST "https://gnn-api-t7k7.onrender.com/predict" \
-H "Content-Type: application/json" \
-d '{ "flows": [ ... ] }'
```

---

## 📡 System Architecture

```
Honeypot (Traffic Capture)
        ↓
   GNN API (This Project)
        ↓
Dashboard (Visualization)
```

---

## 👨‍💻 Contributors

* Abdul Kalam – GNN Model & API
* Anusha – Honeypot & Blockchain
* Anupama – Dashboard

---

## 📌 Future Enhancements

* 🔥 Real-time packet capture integration
* 📊 Live dashboard visualization
* ⚡ Streaming (Kafka/Redis)
* ☁️ Scalable cloud deployment

---

## 🏆 Highlights

* Graph-based ML for cybersecurity
* Real-time intrusion detection
* Distributed system architecture
* Production-ready API deployment

---

## 📄 License

This project is for educational and research purposes.

---

⭐ Star this repo if you like it!
