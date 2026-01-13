"""
ESG Insights Generator
Generates actionable sustainability insights based on transaction patterns.
"""

from typing import List, Dict, Any
from collections import defaultdict


def generate_insights(transactions: List[Dict[str, Any]], green_score: int) -> Dict[str, Any]:
    """
    Generate ESG insights and recommendations based on spending patterns.
    
    Returns:
        Dictionary containing insights, recommendations, and highlights
    """
    if not transactions:
        return {
            "summary": "No transaction data available for analysis.",
            "highlights": [],
            "recommendations": [],
            "esg_insights": {}
        }
    
    # Analyze patterns
    category_analysis = analyze_categories(transactions)
    impact_analysis = analyze_impacts(transactions)
    
    # Generate insights
    highlights = generate_highlights(transactions, impact_analysis)
    recommendations = generate_recommendations(category_analysis, impact_analysis, green_score)
    esg_insights = generate_esg_specific_insights(transactions)
    
    # Create summary
    summary = create_summary(green_score, impact_analysis)
    
    return {
        "summary": summary,
        "highlights": highlights,
        "recommendations": recommendations,
        "esg_insights": esg_insights,
        "patterns": {
            "by_category": category_analysis,
            "impact_distribution": impact_analysis
        }
    }


def analyze_categories(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze spending by category."""
    categories = defaultdict(lambda: {"count": 0, "total_amount": 0, "avg_impact": 0, "impacts": []})
    
    for txn in transactions:
        cat = txn.get("category", "Other")
        categories[cat]["count"] += 1
        categories[cat]["total_amount"] += txn.get("amount", 0)
        categories[cat]["impacts"].append(txn.get("eco_impact", 0))
    
    # Calculate averages
    for cat, data in categories.items():
        if data["impacts"]:
            data["avg_impact"] = round(sum(data["impacts"]) / len(data["impacts"]), 2)
        del data["impacts"]  # Remove raw data
    
    return dict(categories)


def analyze_impacts(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Analyze impact distribution."""
    positive = []
    negative = []
    neutral = []
    
    for txn in transactions:
        impact = txn.get("eco_impact", 0)
        if impact > 0:
            positive.append(txn)
        elif impact < 0:
            negative.append(txn)
        else:
            neutral.append(txn)
    
    return {
        "positive_count": len(positive),
        "negative_count": len(negative),
        "neutral_count": len(neutral),
        "best_transaction": max(transactions, key=lambda x: x.get("eco_impact", 0)) if transactions else None,
        "worst_transaction": min(transactions, key=lambda x: x.get("eco_impact", 0)) if transactions else None,
        "total_positive_impact": sum(t.get("eco_impact", 0) for t in positive),
        "total_negative_impact": sum(t.get("eco_impact", 0) for t in negative)
    }


def generate_highlights(transactions: List[Dict[str, Any]], impact_analysis: Dict) -> List[Dict[str, str]]:
    """Generate achievement highlights."""
    highlights = []
    
    # Best transaction highlight
    if impact_analysis.get("best_transaction"):
        best = impact_analysis["best_transaction"]
        highlights.append({
            "type": "positive",
            "icon": "🌟",
            "title": "Top Sustainable Choice",
            "description": f"{best['description']} - Excellent eco-friendly decision!",
            "impact": f"+{best.get('eco_impact', 0)}"
        })
    
    # Count sustainable actions
    positive_count = impact_analysis.get("positive_count", 0)
    if positive_count >= 5:
        highlights.append({
            "type": "achievement",
            "icon": "🏆",
            "title": "Sustainability Champion",
            "description": f"You made {positive_count} eco-friendly transactions!",
            "impact": None
        })
    
    # Check for specific achievements
    for txn in transactions:
        desc = txn.get("description", "").lower()
        if "donation" in desc or "charity" in desc:
            highlights.append({
                "type": "social",
                "icon": "💚",
                "title": "Green Contributor",
                "description": "Your donations support environmental causes!",
                "impact": None
            })
            break
    
    return highlights[:5]  # Limit to 5 highlights


def generate_recommendations(category_analysis: Dict, impact_analysis: Dict, green_score: int) -> List[Dict[str, str]]:
    """Generate actionable recommendations."""
    recommendations = []
    
    # Score-based recommendations
    if green_score < 50:
        recommendations.append({
            "priority": "high",
            "icon": "🚨",
            "title": "Boost Your GreenScore",
            "action": "Replace high-emission activities with sustainable alternatives",
            "potential_impact": "+15 to +25 points"
        })
    
    # Category-specific recommendations
    transport = category_analysis.get("Transport", {})
    if transport.get("avg_impact", 0) < 0:
        recommendations.append({
            "priority": "medium",
            "icon": "🚇",
            "title": "Switch to Green Transport",
            "action": "Consider public transit, cycling, or electric vehicles for daily commute",
            "potential_impact": "+10 to +20 points"
        })
    
    # Negative impact reduction
    if impact_analysis.get("negative_count", 0) > 3:
        worst = impact_analysis.get("worst_transaction", {})
        recommendations.append({
            "priority": "high",
            "icon": "📉",
            "title": "Reduce Negative Impacts",
            "action": f"Review spending like '{worst.get('description', 'high-impact purchases')}'",
            "potential_impact": "+5 to +15 points"
        })
    
    # Positive reinforcement
    if impact_analysis.get("positive_count", 0) > 0:
        recommendations.append({
            "priority": "low",
            "icon": "✨",
            "title": "Keep Up the Good Work",
            "action": "Continue your sustainable choices in transport and shopping",
            "potential_impact": "Maintain your score"
        })
    
    # General tips
    recommendations.append({
        "priority": "medium",
        "icon": "🛒",
        "title": "Shop Sustainably",
        "action": "Choose second-hand, local, and eco-certified products",
        "potential_impact": "+5 to +10 points"
    })
    
    return recommendations[:4]  # Limit to 4 recommendations


def generate_esg_specific_insights(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Generate insights specific to E, S, G components."""
    
    # Environmental insights
    env_transactions = [t for t in transactions if t.get("category") in ["Transport", "Utilities", "Food", "Shopping"]]
    env_positive = sum(1 for t in env_transactions if t.get("eco_impact", 0) > 0)
    
    # Social insights
    social_transactions = [t for t in transactions if t.get("category") in ["Donations", "Entertainment"]]
    has_donations = any("donation" in t.get("description", "").lower() for t in transactions)
    
    # Governance insights
    digital_payments = sum(1 for t in transactions if "upi" in t.get("description", "").lower() or "digital" in t.get("description", "").lower())
    
    return {
        "environmental": {
            "score_contribution": "primary",
            "status": "strong" if env_positive > len(env_transactions) * 0.5 else "needs_improvement",
            "insight": f"{env_positive} of {len(env_transactions)} transactions are eco-friendly"
        },
        "social": {
            "score_contribution": "moderate",
            "status": "engaged" if has_donations else "opportunity",
            "insight": "Consider supporting environmental causes through donations" if not has_donations else "Great social contribution through charitable giving!"
        },
        "governance": {
            "score_contribution": "supporting",
            "status": "good" if digital_payments > 0 else "standard",
            "insight": f"{digital_payments} digital/transparent payment(s) detected" if digital_payments > 0 else "Digital payments enhance transparency"
        }
    }


def create_summary(green_score: int, impact_analysis: Dict) -> str:
    """Create a summary statement."""
    positive = impact_analysis.get("positive_count", 0)
    negative = impact_analysis.get("negative_count", 0)
    
    if green_score >= 75:
        return f"🌿 Excellent sustainability profile! You made {positive} eco-friendly choices this period."
    elif green_score >= 50:
        return f"📊 Good progress with {positive} sustainable transactions. Reducing {negative} high-impact activities could boost your score."
    else:
        return f"🔄 Room for improvement. Focus on shifting from {negative} high-impact activities to greener alternatives."
