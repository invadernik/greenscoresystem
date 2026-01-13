"""
AI-Based Transaction Classification Module
Simulates AI classification for demo purposes.
Ready for LLM API integration (GPT, Gemini, etc.)
"""

from typing import Dict, Any, Optional
import re

# Classification rules (simulating AI behavior)
CLASSIFICATION_RULES = {
    # Transport - Sustainable
    "metro": {"category": "Transport", "eco_impact": 5, "keywords": ["metro", "subway", "tube"]},
    "electric": {"category": "Transport", "eco_impact": 4, "keywords": ["electric", "ev ", "tesla"]},
    "bicycle": {"category": "Transport", "eco_impact": 5, "keywords": ["bicycle", "bike", "cycling"]},
    "carpool": {"category": "Transport", "eco_impact": 3, "keywords": ["carpool", "rideshare", "shared ride"]},
    
    # Transport - Harmful
    "flight": {"category": "Transport", "eco_impact": -5, "keywords": ["flight", "airline", "aviation"]},
    "petrol": {"category": "Transport", "eco_impact": -4, "keywords": ["petrol", "diesel", "fuel", "gas station"]},
    
    # Food - Sustainable
    "organic": {"category": "Food", "eco_impact": 3, "keywords": ["organic", "natural", "farm fresh"]},
    "plant_based": {"category": "Food", "eco_impact": 4, "keywords": ["vegan", "plant-based", "vegetarian"]},
    "local": {"category": "Food", "eco_impact": 2, "keywords": ["local vendor", "farmer", "market"]},
    
    # Food - Harmful
    "plastic": {"category": "Food", "eco_impact": -3, "keywords": ["plastic bottle", "disposable", "single-use"]},
    
    # Shopping - Sustainable
    "thrift": {"category": "Shopping", "eco_impact": 4, "keywords": ["thrift", "second-hand", "vintage", "pre-owned"]},
    "sustainable_brand": {"category": "Shopping", "eco_impact": 3, "keywords": ["sustainable", "eco-friendly", "green"]},
    
    # Shopping - Harmful
    "fast_fashion": {"category": "Shopping", "eco_impact": -4, "keywords": ["fast fashion", "quicktrends", "cheap clothing"]},
    
    # Utilities
    "solar": {"category": "Utilities", "eco_impact": 5, "keywords": ["solar", "renewable", "wind energy"]},
    "electricity": {"category": "Utilities", "eco_impact": 0, "keywords": ["electricity", "power bill"]},
    
    # Entertainment
    "digital": {"category": "Entertainment", "eco_impact": 1, "keywords": ["streaming", "netflix", "spotify", "digital"]},
    
    # Donations
    "charity": {"category": "Donations", "eco_impact": 5, "keywords": ["donation", "charity", "foundation", "ngo"]},
}

# Reasoning templates
REASONING_TEMPLATES = {
    5: "Excellent sustainability choice! {detail}",
    4: "Great eco-friendly decision. {detail}",
    3: "Good sustainable practice. {detail}",
    2: "Moderately positive environmental impact. {detail}",
    1: "Slightly positive environmental impact. {detail}",
    0: "Neutral environmental impact. {detail}",
    -1: "Slightly negative environmental impact. {detail}",
    -2: "Moderate environmental concern. {detail}",
    -3: "Notable negative environmental impact. {detail}",
    -4: "Significant environmental concern. {detail}",
    -5: "High environmental impact. {detail}",
}


def classify_transaction(description: str, amount: Optional[float] = None) -> Dict[str, Any]:
    """
    Classify a transaction based on its description.
    
    This function simulates AI classification behavior.
    In production, this would call an LLM API (GPT, Gemini, etc.)
    
    Args:
        description: Transaction description text
        amount: Transaction amount (optional, for context)
    
    Returns:
        Dictionary with category, eco_impact, and reasoning
    """
    description_lower = description.lower()
    
    # Try to match against classification rules
    for rule_name, rule_data in CLASSIFICATION_RULES.items():
        for keyword in rule_data["keywords"]:
            if keyword in description_lower:
                eco_impact = rule_data["eco_impact"]
                detail = get_impact_detail(rule_name, eco_impact)
                
                return {
                    "category": rule_data["category"],
                    "eco_impact": eco_impact,
                    "reasoning": REASONING_TEMPLATES[eco_impact].format(detail=detail),
                    "confidence": 0.85,
                    "classification_method": "rule_based"
                }
    
    # Default classification for unmatched transactions
    return {
        "category": "Other",
        "eco_impact": 0,
        "reasoning": "Unable to determine specific environmental impact. Classified as neutral.",
        "confidence": 0.5,
        "classification_method": "default"
    }


def get_impact_detail(rule_name: str, eco_impact: int) -> str:
    """Generate specific detail for the reasoning."""
    details = {
        "metro": "Public transport reduces carbon emissions by up to 45% compared to private vehicles.",
        "electric": "Electric vehicles produce zero direct emissions and reduce air pollution.",
        "bicycle": "Zero-emission transport with added health benefits.",
        "carpool": "Sharing rides reduces per-person carbon footprint and road congestion.",
        "flight": "Aviation accounts for ~2.5% of global CO2 emissions. Consider alternatives when possible.",
        "petrol": "Fossil fuel consumption contributes directly to carbon emissions.",
        "organic": "Organic farming avoids synthetic pesticides and supports soil health.",
        "plant_based": "Plant-based diets have 50% lower carbon footprint than meat-based diets.",
        "local": "Local sourcing reduces transportation emissions and supports community.",
        "plastic": "Plastic pollution affects oceans and wildlife. Consider reusable alternatives.",
        "thrift": "Second-hand shopping extends product lifecycle and reduces manufacturing demand.",
        "sustainable_brand": "Supporting sustainable brands encourages eco-friendly business practices.",
        "fast_fashion": "Fast fashion contributes to textile waste and excessive water usage.",
        "solar": "Solar energy investment reduces reliance on fossil fuels.",
        "electricity": "Impact depends on the energy source mix of your provider.",
        "digital": "Digital entertainment has lower footprint than physical alternatives.",
        "charity": "Direct contribution to environmental protection and sustainability initiatives.",
    }
    return details.get(rule_name, "Environmental impact assessed based on transaction type.")


async def classify_with_llm(description: str, api_key: Optional[str] = None) -> Dict[str, Any]:
    """
    Placeholder for LLM-based classification.
    
    In production, this would call an LLM API like:
    - OpenAI GPT-4
    - Google Gemini
    - Anthropic Claude
    
    For the prototype, we fall back to rule-based classification.
    """
    # TODO: Implement actual LLM API call
    # Example prompt structure:
    # "Classify this financial transaction for sustainability impact:
    #  Transaction: {description}
    #  Return: category, eco_impact (-5 to +5), reasoning"
    
    # For now, use rule-based classification
    return classify_transaction(description)


def batch_classify(transactions: list) -> list:
    """Classify multiple transactions at once."""
    results = []
    for txn in transactions:
        description = txn.get("description", "")
        amount = txn.get("amount")
        classification = classify_transaction(description, amount)
        results.append({
            **txn,
            **classification
        })
    return results
