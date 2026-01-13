"""
FinTech Incentives Simulation Module
Maps GreenScore to simulated financial benefits.
No real financial transactions occur - prototype only.
"""

from typing import Dict, Any, List


# Incentive tiers based on GreenScore ranges
INCENTIVE_TIERS = {
    "platinum": {
        "min_score": 85,
        "max_score": 100,
        "tier_name": "Platinum Green",
        "tier_color": "#00D4AA",
        "badge": "🌟"
    },
    "gold": {
        "min_score": 70,
        "max_score": 84,
        "tier_name": "Gold Green",
        "tier_color": "#FFD700",
        "badge": "🥇"
    },
    "silver": {
        "min_score": 50,
        "max_score": 69,
        "tier_name": "Silver Green",
        "tier_color": "#C0C0C0",
        "badge": "🥈"
    },
    "bronze": {
        "min_score": 30,
        "max_score": 49,
        "tier_name": "Bronze Green",
        "tier_color": "#CD7F32",
        "badge": "🥉"
    },
    "starter": {
        "min_score": 0,
        "max_score": 29,
        "tier_name": "Green Starter",
        "tier_color": "#808080",
        "badge": "🌱"
    }
}

# Available incentives
INCENTIVES = {
    "cashback": {
        "id": "cashback",
        "name": "Green Cashback",
        "description": "Cashback on eco-friendly purchases",
        "icon": "💰",
        "tiers": {
            "platinum": {"rate": "5%", "max_monthly": "₹2,500"},
            "gold": {"rate": "3%", "max_monthly": "₹1,500"},
            "silver": {"rate": "1.5%", "max_monthly": "₹750"},
            "bronze": {"rate": "0.5%", "max_monthly": "₹250"},
            "starter": {"rate": "0%", "max_monthly": "₹0"}
        }
    },
    "green_loan": {
        "id": "green_loan",
        "name": "Green Loan Benefits",
        "description": "Reduced interest rates on eco-friendly purchases",
        "icon": "🏦",
        "tiers": {
            "platinum": {"rate_reduction": "2.0%", "eligible": True},
            "gold": {"rate_reduction": "1.5%", "eligible": True},
            "silver": {"rate_reduction": "0.75%", "eligible": True},
            "bronze": {"rate_reduction": "0.25%", "eligible": True},
            "starter": {"rate_reduction": "0%", "eligible": False}
        }
    },
    "rewards": {
        "id": "rewards",
        "name": "Green Reward Points",
        "description": "Bonus reward points on sustainable transactions",
        "icon": "🎁",
        "tiers": {
            "platinum": {"multiplier": "3x", "bonus_points": 500},
            "gold": {"multiplier": "2x", "bonus_points": 300},
            "silver": {"multiplier": "1.5x", "bonus_points": 150},
            "bronze": {"multiplier": "1x", "bonus_points": 50},
            "starter": {"multiplier": "1x", "bonus_points": 0}
        }
    },
    "insurance": {
        "id": "insurance",
        "name": "Green Insurance Discount",
        "description": "Premium discounts on vehicle and health insurance",
        "icon": "🛡️",
        "tiers": {
            "platinum": {"discount": "15%", "eligible": True},
            "gold": {"discount": "10%", "eligible": True},
            "silver": {"discount": "5%", "eligible": True},
            "bronze": {"discount": "2%", "eligible": True},
            "starter": {"discount": "0%", "eligible": False}
        }
    },
    "credit_limit": {
        "id": "credit_limit",
        "name": "Enhanced Credit Limit",
        "description": "Higher credit limits for sustainable spenders",
        "icon": "💳",
        "tiers": {
            "platinum": {"boost": "+25%", "eligible": True},
            "gold": {"boost": "+15%", "eligible": True},
            "silver": {"boost": "+5%", "eligible": True},
            "bronze": {"boost": "0%", "eligible": False},
            "starter": {"boost": "0%", "eligible": False}
        }
    }
}


def get_user_tier(green_score: int) -> Dict[str, Any]:
    """Determine user's incentive tier based on GreenScore."""
    for tier_id, tier_data in INCENTIVE_TIERS.items():
        if tier_data["min_score"] <= green_score <= tier_data["max_score"]:
            return {
                "tier_id": tier_id,
                **tier_data
            }
    return {"tier_id": "starter", **INCENTIVE_TIERS["starter"]}


def get_eligible_incentives(green_score: int) -> Dict[str, Any]:
    """
    Get all eligible incentives for a given GreenScore.
    
    Returns detailed incentive information including:
    - Current tier
    - All available incentives with eligibility
    - Next tier information
    """
    current_tier = get_user_tier(green_score)
    tier_id = current_tier["tier_id"]
    
    # Get incentive details for current tier
    eligible_incentives = []
    for incentive_id, incentive_data in INCENTIVES.items():
        tier_benefits = incentive_data["tiers"].get(tier_id, {})
        is_eligible = tier_benefits.get("eligible", True) if "eligible" in tier_benefits else True
        
        # Check if benefit is meaningful (not 0%)
        benefit_value = tier_benefits.get("rate") or tier_benefits.get("rate_reduction") or tier_benefits.get("discount") or tier_benefits.get("boost")
        if benefit_value == "0%" or benefit_value == "0":
            is_eligible = False
        
        eligible_incentives.append({
            "id": incentive_id,
            "name": incentive_data["name"],
            "description": incentive_data["description"],
            "icon": incentive_data["icon"],
            "eligible": is_eligible,
            "benefits": tier_benefits
        })
    
    # Calculate next tier info
    next_tier_info = get_next_tier_info(green_score, tier_id)
    
    # Calculate total estimated monthly value
    estimated_value = calculate_estimated_value(tier_id)
    
    return {
        "current_tier": current_tier,
        "incentives": eligible_incentives,
        "next_tier": next_tier_info,
        "estimated_monthly_value": estimated_value,
        "disclaimer": "These are simulated incentives for demonstration purposes. No real financial benefits are provided."
    }


def get_next_tier_info(green_score: int, current_tier_id: str) -> Dict[str, Any]:
    """Get information about the next tier and how to reach it."""
    tier_order = ["starter", "bronze", "silver", "gold", "platinum"]
    
    try:
        current_index = tier_order.index(current_tier_id)
        if current_index >= len(tier_order) - 1:
            return {
                "exists": False,
                "message": "You're at the highest tier! 🎉"
            }
        
        next_tier_id = tier_order[current_index + 1]
        next_tier = INCENTIVE_TIERS[next_tier_id]
        points_needed = next_tier["min_score"] - green_score
        
        return {
            "exists": True,
            "tier_id": next_tier_id,
            "tier_name": next_tier["tier_name"],
            "points_needed": points_needed,
            "min_score_required": next_tier["min_score"],
            "message": f"Earn {points_needed} more points to unlock {next_tier['tier_name']}!"
        }
    except (ValueError, IndexError):
        return {"exists": False, "message": "Unable to calculate next tier"}


def calculate_estimated_value(tier_id: str) -> str:
    """Calculate estimated monthly value of incentives."""
    values = {
        "platinum": "₹3,000 - ₹5,000",
        "gold": "₹1,500 - ₹3,000",
        "silver": "₹500 - ₹1,500",
        "bronze": "₹100 - ₹500",
        "starter": "₹0"
    }
    return values.get(tier_id, "₹0")


def get_incentive_comparison() -> List[Dict[str, Any]]:
    """Get a comparison table of all tiers and incentives."""
    comparison = []
    
    for tier_id, tier_data in INCENTIVE_TIERS.items():
        tier_incentives = {}
        for incentive_id, incentive_data in INCENTIVES.items():
            tier_incentives[incentive_id] = incentive_data["tiers"].get(tier_id, {})
        
        comparison.append({
            "tier_id": tier_id,
            "tier_name": tier_data["tier_name"],
            "score_range": f"{tier_data['min_score']} - {tier_data['max_score']}",
            "badge": tier_data["badge"],
            "incentives": tier_incentives
        })
    
    return comparison
