# 🌿 GreenScore

### Sustainability Credit Scoring Platform

> *"Operationalizing ESG principles at the individual level using AI-driven transaction analysis and sustainability-based scoring."*

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [ESG Framework](#-esg-framework)
- [Scoring Logic](#-scoring-logic)
- [Incentive Tiers](#-incentive-tiers)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**GreenScore** is a prototype FinTech + Sustainability platform that demonstrates how financial transaction data can be analyzed using AI-based classification to generate a **Sustainability Credit Score (0–100)**, aligned with **ESG (Environmental, Social, Governance)** principles.

### Key Objectives

- 🌱 **Demonstrate feasibility** of ESG-driven credit scoring
- 📊 **Visualize sustainability impact** of financial decisions
- 💡 **Encourage sustainable behavior** through actionable insights
- 🏆 **Simulate FinTech incentives** tied to sustainability performance

> ⚠️ **Note:** This is a prototype using mock data. No real banking integrations or financial transactions occur.

---

## ✨ Features

### Core Functionality

| Feature | Description |
|---------|-------------|
| **GreenScore Dashboard** | Real-time sustainability score (0-100) with visual indicators |
| **Transaction Analysis** | Categorized spending with eco-impact scores (-5 to +5) |
| **AI Classification** | Intelligent transaction categorization with reasoning |
| **ESG Breakdown** | Separate Environmental, Social, and Governance scores |
| **Smart Insights** | Personalized recommendations to improve sustainability |
| **Incentive Simulation** | Tier-based rewards (cashback, loans, discounts) |

### UI/UX Highlights

- 🌙 **Dark Mode** with glassmorphism design
- 📱 **Responsive** layout for all devices
- ⚡ **Animated** score displays and transitions
- 📈 **Interactive Charts** with Chart.js

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend                              │
│              (HTML5 + CSS3 + JavaScript)                    │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │  Dashboard  │ │   Charts    │ │ Transactions│           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
┌────────────────────────▼────────────────────────────────────┐
│                     Backend (FastAPI)                        │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ Scoring  │ │Classifier│ │ Insights │ │Incentives│       │
│  │  Engine  │ │   (AI)   │ │Generator │ │Simulator │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│                    Mock Data Layer                           │
│              (Simulated Transactions)                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🚀 Installation

### Prerequisites

- **Python 3.8+** ([Download](https://www.python.org/downloads/))
- **Modern Web Browser** (Chrome, Firefox, Edge, Safari)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/greenscore.git
cd greenscore
```

### Step 2: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Start the Backend Server

```bash
python main.py
```

The API will be available at: **http://localhost:8000**

### Step 4: Open the Frontend

Open `frontend/index.html` in your browser, or use a local server:

```bash
# Using Python's built-in server
cd frontend
python -m http.server 3000
```

Then visit: **http://localhost:3000**

---

## 💻 Usage

### Dashboard Overview

1. **GreenScore Ring** - Your overall sustainability score (0-100)
2. **ESG Breakdown** - Radar chart showing Environmental, Social, and Governance scores
3. **Tier Status** - Current incentive tier with progress to next level
4. **Transaction List** - All transactions with eco-impact indicators
5. **Insights Panel** - Personalized recommendations
6. **Incentives Grid** - Available benefits based on your tier

### Filtering Transactions

Use the filter tabs to view transactions by category:
- **All** - All transactions
- **Transport** - Travel and commute
- **Food** - Dining and groceries
- **Shopping** - Retail purchases

---

## 📡 API Reference

### Base URL
```
http://localhost:8000
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check and API info |
| `GET` | `/score` | Get GreenScore with ESG breakdown |
| `GET` | `/transactions` | List all transactions |
| `GET` | `/transactions/{id}` | Get single transaction |
| `GET` | `/insights` | Get sustainability insights |
| `GET` | `/incentives` | Get eligible incentives |
| `POST` | `/classify` | Classify a new transaction |
| `GET` | `/esg-breakdown` | Detailed ESG analysis |
| `GET` | `/categories` | Category statistics |

### Example: Get Score

```bash
curl http://localhost:8000/score
```

**Response:**
```json
{
  "score": 67,
  "status": "medium",
  "explanation": "Good progress! You're making sustainable choices...",
  "esg": {
    "environmental": 72,
    "social": 55,
    "governance": 60
  }
}
```

### Example: Classify Transaction

```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"description": "Metro Rail Pass", "amount": 1500}'
```

**Response:**
```json
{
  "category": "Transport",
  "eco_impact": 5,
  "reasoning": "Excellent sustainability choice! Public transport reduces carbon emissions...",
  "confidence": 0.85
}
```

### Interactive Docs

Visit **http://localhost:8000/docs** for Swagger UI documentation.

---

## 🌍 ESG Framework

### Environmental (E)
Evaluates carbon footprint and environmental impact:

| Category | Positive Impact | Negative Impact |
|----------|-----------------|-----------------|
| Transport | Public transit, EV, cycling | Flights, petrol |
| Food | Organic, plant-based, local | Plastic packaging |
| Shopping | Thrift, sustainable brands | Fast fashion |
| Utilities | Solar, renewable energy | High consumption |

### Social (S)
Measures community and social responsibility:
- Charitable donations
- Shared mobility usage
- Digital financial inclusion

### Governance (G)
Assesses transparency and ethical practices:
- Digital/transparent payments
- Consent-based data handling
- Explainable scoring logic

---

## 📊 Scoring Logic

### Formula

```python
# Base Score
base_score = 50  # Neutral starting point

# Eco Impact per Transaction
eco_impact = -5 to +5  # Based on sustainability

# Category Weights
weights = {
    "Transport": 1.5,
    "Utilities": 1.3,
    "Food": 1.0,
    "Shopping": 0.8
}

# Final Calculation
weighted_impact = sum(eco_impact * weight for each transaction)
green_score = clamp(0, 100, base_score + weighted_impact * scale_factor)
```

### Score Status

| Range | Status | Meaning |
|-------|--------|---------|
| 0-40 | 🔴 Low | Significant room for improvement |
| 41-70 | 🟡 Medium | Good progress, can do better |
| 71-100 | 🟢 High | Excellent sustainability profile |

---

## 🏆 Incentive Tiers

| Tier | Score | Cashback | Loan Discount | Rewards |
|------|-------|----------|---------------|---------|
| 🌟 **Platinum** | 85-100 | 5% | -2.0% APR | 3x points |
| 🥇 **Gold** | 70-84 | 3% | -1.5% APR | 2x points |
| 🥈 **Silver** | 50-69 | 1.5% | -0.75% APR | 1.5x points |
| 🥉 **Bronze** | 30-49 | 0.5% | -0.25% APR | 1x points |
| 🌱 **Starter** | 0-29 | - | - | Entry level |

> 💡 **These are simulated incentives for demonstration purposes only.**

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

### Frontend
- **HTML5** - Semantic structure
- **CSS3** - Modern styling with CSS variables
- **JavaScript** - Vanilla JS for interactivity
- **Chart.js** - Data visualization

### Design
- **Glassmorphism** - Frosted glass effects
- **Dark Theme** - Easy on the eyes
- **Inter Font** - Clean typography

---

## 📁 Project Structure

```
GREEN/
├── backend/
│   ├── main.py           # FastAPI application & routes
│   ├── mock_data.py      # Demo transaction dataset
│   ├── scoring.py        # GreenScore calculation engine
│   ├── classifier.py     # AI transaction classification
│   ├── insights.py       # ESG insights generator
│   ├── incentives.py     # FinTech incentives logic
│   ├── test_api.py       # API test suite
│   └── requirements.txt  # Python dependencies
│
├── frontend/
│   ├── index.html        # Dashboard UI
│   ├── styles.css        # Styling & animations
│   └── app.js            # API integration & charts
│
└── README.md             # This file
```

---

## 🧪 Testing

### Run API Tests

```bash
cd backend
pip install pytest
pytest test_api.py -v
```

### Test Coverage

- ✅ Health check endpoint
- ✅ Score calculation
- ✅ Transaction CRUD
- ✅ Insights generation
- ✅ Incentives logic
- ✅ Classification accuracy

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- ESG frameworks and sustainability guidelines
- FastAPI and Python community
- Chart.js for beautiful visualizations

---

<div align="center">

**Built with 💚 for a sustainable future**

[Report Bug](https://github.com/yourusername/greenscore/issues) · [Request Feature](https://github.com/yourusername/greenscore/issues)

</div>
