"""
GreenScore API - FastAPI Backend
Sustainability Credit Scoring Platform

Endpoints:
- GET /score - Get current GreenScore
- GET /transactions - Get all transactions
- GET /insights - Get ESG insights
- GET /incentives - Get eligible incentives
- POST /classify - Classify a transaction
- GET /users - Get all users
- GET /users/{user_id} - Get specific user
- GET /users/{user_id}/score - Get user's score
- GET /users/{user_id}/transactions - Get user's transactions
- GET /users/{user_id}/improvements - Get improvement suggestions
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import uvicorn

from mock_data import get_all_transactions, get_transaction_by_id, get_transactions_by_category
from scoring import calculate_green_score, calculate_esg_breakdown
from classifier import classify_transaction, batch_classify
from insights import generate_insights
from incentives import get_eligible_incentives, get_incentive_comparison
from users import (
    get_all_users, get_user_by_id, search_users, 
    get_user_transactions, get_user_improvement_areas
)

# Initialize FastAPI app
app = FastAPI(
    title="GreenScore API",
    description="Sustainability Credit Scoring Platform - ESG-driven financial analysis",
    version="2.0.0",
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
        "version": "2.0.0",
        "status": "running",
        "description": "Sustainability Credit Scoring Platform - Multi-User Edition",
        "endpoints": {
            "users": "/users",
            "user_detail": "/users/{user_id}",
            "user_score": "/users/{user_id}/score",
            "user_transactions": "/users/{user_id}/transactions",
            "user_improvements": "/users/{user_id}/improvements",
            "score": "/score",
            "transactions": "/transactions",
            "insights": "/insights",
            "incentives": "/incentives",
            "classify": "/classify",
            "docs": "/docs"
        },
        "total_users": 100
    }


# ==================== User Endpoints ====================

@app.get("/users")
async def list_users(
    search: Optional[str] = Query(None, description="Search by name, email, or ID"),
    limit: Optional[int] = Query(100, description="Maximum number of users to return"),
    offset: Optional[int] = Query(0, description="Offset for pagination")
):
    """
    Get all users or search for specific users.
    """
    if search:
        users = search_users(search)
    else:
        users = get_all_users()
    
    # Apply pagination
    paginated = users[offset:offset + limit]
    
    return {
        "total": len(users),
        "count": len(paginated),
        "offset": offset,
        "users": paginated
    }


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get a specific user by ID."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/{user_id}/score")
async def get_user_score(user_id: str):
    """Get detailed score breakdown for a specific user."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = get_user_transactions(user_id)
    score_result = calculate_green_score(transactions)
    esg_breakdown = calculate_esg_breakdown(transactions)
    
    return {
        "user_id": user_id,
        "user_name": user["full_name"],
        "score": score_result["score"],
        "status": score_result["status"],
        "explanation": score_result["explanation"],
        "breakdown": score_result["breakdown"],
        "esg": esg_breakdown,
        "total_transactions": score_result["total_transactions"],
        "net_impact": score_result["net_impact"]
    }


@app.get("/users/{user_id}/transactions")
async def get_user_txns(
    user_id: str,
    category: Optional[str] = Query(None, description="Filter by category")
):
    """Get all transactions for a specific user."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = get_user_transactions(user_id)
    
    if category:
        transactions = [t for t in transactions if t["category"].lower() == category.lower()]
    
    return {
        "user_id": user_id,
        "count": len(transactions),
        "transactions": transactions
    }


@app.get("/users/{user_id}/insights")
async def get_user_insights(user_id: str):
    """Get ESG insights for a specific user."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    transactions = get_user_transactions(user_id)
    score_result = calculate_green_score(transactions)
    insights = generate_insights(transactions, score_result["score"])
    
    return {
        "user_id": user_id,
        "user_name": user["full_name"],
        **insights
    }


@app.get("/users/{user_id}/incentives")
async def get_user_incentives(user_id: str):
    """Get eligible incentives for a specific user."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    incentives = get_eligible_incentives(user["green_score"])
    
    return {
        "user_id": user_id,
        "user_name": user["full_name"],
        "green_score": user["green_score"],
        **incentives
    }


@app.get("/users/{user_id}/improvements")
async def get_user_improvements(user_id: str):
    """Get improvement suggestions for negative impact areas."""
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    improvements = get_user_improvement_areas(user_id)
    
    return {
        "user_id": user_id,
        "user_name": user["full_name"],
        "current_score": user["green_score"],
        "improvement_areas": improvements,
        "total_potential": sum(len(i.get("potential_improvement", "").split()) for i in improvements),
        "message": "Focus on these areas to boost your GreenScore!" if improvements else "Great job! No major improvement areas identified."
    }


# ==================== Legacy Endpoints (for backward compatibility) ====================

@app.get("/score")
async def get_score():
    """Get the current GreenScore based on all transactions."""
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
    """Get all transactions or filter by category."""
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
    """Get ESG insights and recommendations."""
    transactions = get_all_transactions()
    score_result = calculate_green_score(transactions)
    insights = generate_insights(transactions, score_result["score"])
    return insights


@app.get("/incentives")
async def get_incentives():
    """Get eligible FinTech incentives based on GreenScore."""
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
    return {"tiers": get_incentive_comparison()}


@app.post("/classify")
async def classify(transaction: TransactionInput):
    """Classify a transaction for sustainability impact."""
    result = classify_transaction(transaction.description, transaction.amount)
    return result


@app.get("/esg-breakdown")
async def get_esg_breakdown():
    """Get detailed ESG breakdown."""
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
    
    for cat in categories:
        impacts = categories[cat]["impacts"]
        categories[cat]["avg_impact"] = round(sum(impacts) / len(impacts), 2) if impacts else 0
        del categories[cat]["impacts"]
    
    return categories


# ==================== Run Server ====================

if __name__ == "__main__":
    print("🌿 Starting GreenScore API Server v2.0...")
    print("👥 Loaded 100 users with individual tracking")
    print("📖 API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

