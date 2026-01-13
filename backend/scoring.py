"""
GreenScore Sustainability Scoring Engine
Transparent, rule-based scoring logic for ESG compliance.
"""

from typing import List, Dict, Any

# Score thresholds for status classification
SCORE_THRESHOLDS = {
    "low": (0, 40),
    "medium": (41, 70),
    "high": (71, 100)
}

# Category weights for ESG components
ESG_WEIGHTS = {
    "environmental": {
        "Transport": 1.5,
        "Utilities": 1.3,
        "Food": 1.0,
        "Shopping": 0.8
    },
    "social": {
        "Donations": 1.5,
        "Entertainment": 0.5
    },
    "governance": {
        "all": 1.0  # Digital payments, transparency
    }
}


def calculate_green_score(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate GreenScore from transaction eco impacts.
    
    Scoring Logic (Transparent):
    - Base score: 50 (neutral starting point)
    - Each transaction's eco_impact (-5 to +5) is weighted by category
    - Final score normalized to 0-100 range
    
    Returns detailed breakdown for explainability (Governance requirement).
    """
    if not transactions:
        return {
            "score": 50,
            "status": "medium",
            "breakdown": {},
            "explanation": "No transactions to analyze"
        }
    
    # Calculate weighted impacts by category
    category_impacts = {}
    total_weighted_impact = 0
    
    for txn in transactions:
        category = txn.get("category", "Other")
        eco_impact = txn.get("eco_impact", 0)
        
        # Apply category weight
        weight = ESG_WEIGHTS["environmental"].get(
            category, 
            ESG_WEIGHTS["social"].get(category, 1.0)
        )
        weighted_impact = eco_impact * weight
        
        # Accumulate by category
        if category not in category_impacts:
            category_impacts[category] = {
                "count": 0,
                "total_impact": 0,
                "weighted_impact": 0
            }
        
        category_impacts[category]["count"] += 1
        category_impacts[category]["total_impact"] += eco_impact
        category_impacts[category]["weighted_impact"] += weighted_impact
        total_weighted_impact += weighted_impact
    
    # Calculate final score
    # Scale factor: normalize based on transaction count
    scale_factor = min(len(transactions), 20) / 20  # Cap at 20 transactions
    score_adjustment = total_weighted_impact * 2.5 * scale_factor
    
    raw_score = 50 + score_adjustment
    final_score = max(0, min(100, round(raw_score)))
    
    # Determine status
    status = get_score_status(final_score)
    
    # Generate explanation
    explanation = generate_score_explanation(final_score, category_impacts)
    
    return {
        "score": final_score,
        "status": status,
        "breakdown": category_impacts,
        "total_transactions": len(transactions),
        "net_impact": round(total_weighted_impact, 2),
        "explanation": explanation
    }


def get_score_status(score: int) -> str:
    """Determine score status category."""
    for status, (low, high) in SCORE_THRESHOLDS.items():
        if low <= score <= high:
            return status
    return "medium"


def generate_score_explanation(score: int, breakdown: Dict) -> str:
    """Generate human-readable explanation of the score."""
    if score >= 80:
        return "Excellent! Your spending habits strongly support sustainability. Keep up the great work!"
    elif score >= 60:
        return "Good progress! You're making sustainable choices. A few improvements could boost your score further."
    elif score >= 40:
        return "Room for improvement. Consider shifting towards more eco-friendly alternatives."
    else:
        return "Your spending patterns have significant environmental impact. Small changes can make a big difference!"


def calculate_esg_breakdown(transactions: List[Dict[str, Any]]) -> Dict[str, float]:
    """
    Calculate separate E, S, G scores for detailed insights.
    """
    e_score = 0  # Environmental
    s_score = 0  # Social
    g_score = 0  # Governance
    
    e_count = 0
    s_count = 0
    
    for txn in transactions:
        category = txn.get("category", "Other")
        eco_impact = txn.get("eco_impact", 0)
        
        # Environmental categories
        if category in ["Transport", "Utilities", "Food", "Shopping"]:
            e_score += eco_impact
            e_count += 1
        
        # Social categories
        if category in ["Donations", "Entertainment"]:
            s_score += eco_impact
            s_count += 1
        
        # Governance: based on digital payment adoption (all UPI/digital = positive)
        if "UPI" in txn.get("description", "") or "Digital" in txn.get("description", ""):
            g_score += 2
    
    # Normalize to 0-100
    e_normalized = max(0, min(100, 50 + (e_score / max(e_count, 1)) * 10)) if e_count > 0 else 50
    s_normalized = max(0, min(100, 50 + (s_score / max(s_count, 1)) * 10)) if s_count > 0 else 50
    g_normalized = max(0, min(100, 50 + g_score * 5))
    
    return {
        "environmental": round(e_normalized),
        "social": round(s_normalized),
        "governance": round(g_normalized)
    }
