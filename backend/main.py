"""
GreenScore API - FastAPI Backend
Sustainability Credit Scoring Platform

Endpoints:
- GET /score - Get current GreenScore
- GET /transactions - Get all transactions
- GET /insights - Get ESG insights
- GET /incentives - Get eligible incentives
- POST /classify - Classify a transaction
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from mock_data import get_all_transactions, get_transaction_by_id, get_transactions_by_category
from scoring import calculate_green_score, calculate_esg_breakdown
from classifier import classify_transaction, batch_classify
from insights import generate_insights
from incentives import get_eligible_incentives, get_incentive_comparison

# Initialize FastAPI app
app = FastAPI(
    title="GreenScore API",
    description="Sustainability Credit Scoring Platform - ESG-driven financial analysis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for demo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class TransactionInput(BaseModel):
    description: str
    amount: Optional[float] = None


class ClassificationResponse(BaseModel):
    category: str
    eco_impact: int
    reasoning: str
    confidence: float


# ==================== API Endpoints ====================

@app.get("/")
async def root():
    """API health check and info."""
    return {
        "name": "GreenScore API",
        "version": "1.0.0",
        "status": "running",
        "description": "Sustainability Credit Scoring Platform",
        "endpoints": {
            "score": "/score",
            "transactions": "/transactions",
            "insights": "/insights",
            "incentives": "/incentives",
            "classify": "/classify",
            "docs": "/docs"
        }
    }


@app.get("/score")
async def get_score():
    """
    Get the current GreenScore based on all transactions.
    
    Returns:
        - score: 0-100 GreenScore
        - status: low/medium/high
        - breakdown: Score breakdown by category
        - esg: E, S, G component scores
    """
    transactions = get_all_transactions()
    score_result = calculate_green_score(transactions)
    esg_breakdown = calculate_esg_breakdown(transactions)
    
    return {
        "score": score_result["score"],
        "status": score_result["status"],
        "explanation": score_result["explanation"],
        "breakdown": score_result["breakdown"],
        "esg": esg_breakdown,
        "total_transactions": score_result["total_transactions"],
        "net_impact": score_result["net_impact"]
    }


@app.get("/transactions")
async def get_transactions(category: Optional[str] = None):
    """
    Get all transactions or filter by category.
    
    Query Parameters:
        - category: Filter by category (Transport, Food, Shopping, etc.)
    
    Returns:
        List of transactions with eco impact data
    """
    if category:
        transactions = get_transactions_by_category(category)
    else:
        transactions = get_all_transactions()
    
    return {
        "count": len(transactions),
        "transactions": transactions
    }


@app.get("/transactions/{txn_id}")
async def get_transaction(txn_id: str):
    """Get a specific transaction by ID."""
    transaction = get_transaction_by_id(txn_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@app.get("/insights")
async def get_insights():
    """
    Get ESG insights and recommendations.
    
    Returns:
        - summary: Overall sustainability summary
        - highlights: Achievement highlights
        - recommendations: Actionable recommendations
        - esg_insights: E, S, G specific insights
    """
    transactions = get_all_transactions()
    score_result = calculate_green_score(transactions)
    insights = generate_insights(transactions, score_result["score"])
    
    return insights


@app.get("/incentives")
async def get_incentives():
    """
    Get eligible FinTech incentives based on GreenScore.
    
    Returns:
        - current_tier: User's current tier
        - incentives: List of eligible incentives
        - next_tier: Info about reaching the next tier
    """
    transactions = get_all_transactions()
    score_result = calculate_green_score(transactions)
    incentives = get_eligible_incentives(score_result["score"])
    
    return {
        "green_score": score_result["score"],
        **incentives
    }


@app.get("/incentives/comparison")
async def get_incentives_comparison():
    """Get comparison of all tier benefits."""
    return {
        "tiers": get_incentive_comparison()
    }


@app.post("/classify")
async def classify(transaction: TransactionInput):
    """
    Classify a transaction for sustainability impact.
    
    Request Body:
        - description: Transaction description
        - amount: Transaction amount (optional)
    
    Returns:
        - category: Transaction category
        - eco_impact: -5 to +5 impact score
        - reasoning: Explanation of classification
    """
    result = classify_transaction(
        transaction.description,
        transaction.amount
    )
    return result


@app.get("/esg-breakdown")
async def get_esg_breakdown():
    """
    Get detailed ESG (Environmental, Social, Governance) breakdown.
    
    Returns separate scores for each ESG component.
    """
    transactions = get_all_transactions()
    esg = calculate_esg_breakdown(transactions)
    score_result = calculate_green_score(transactions)
    
    return {
        "overall_score": score_result["score"],
        "esg_scores": esg,
        "explanation": {
            "environmental": "Based on transport, utilities, food, and shopping choices",
            "social": "Based on donations and community engagement",
            "governance": "Based on digital payments and transparency"
        }
    }


@app.get("/categories")
async def get_categories():
    """Get all available transaction categories with stats."""
    transactions = get_all_transactions()
    categories = {}
    
    for txn in transactions:
        cat = txn.get("category", "Other")
        if cat not in categories:
            categories[cat] = {"count": 0, "total_amount": 0, "avg_impact": 0, "impacts": []}
        categories[cat]["count"] += 1
        categories[cat]["total_amount"] += txn.get("amount", 0)
        categories[cat]["impacts"].append(txn.get("eco_impact", 0))
    
    # Calculate averages
    for cat in categories:
        impacts = categories[cat]["impacts"]
        categories[cat]["avg_impact"] = round(sum(impacts) / len(impacts), 2) if impacts else 0
        del categories[cat]["impacts"]
    
    return categories


# ==================== Run Server ====================

if __name__ == "__main__":
    print("🌿 Starting GreenScore API Server...")
    print("📖 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
