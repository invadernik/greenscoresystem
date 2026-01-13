"""
Mock Transaction Dataset for GreenScore Platform
Contains demo financial transactions with sustainability impact data.
"""

MOCK_TRANSACTIONS = [
    {
        "id": "TXN001",
        "description": "Metro Rail Monthly Pass",
        "amount": 1500.00,
        "category": "Transport",
        "merchant": "Delhi Metro",
        "date": "2026-01-10",
        "eco_impact": 5,
        "reasoning": "Public transport significantly reduces carbon emissions compared to private vehicles"
    },
    {
        "id": "TXN002",
        "description": "Electric Vehicle Charging",
        "amount": 450.00,
        "category": "Transport",
        "merchant": "Tata Power EV",
        "date": "2026-01-09",
        "eco_impact": 4,
        "reasoning": "Electric vehicles produce zero direct emissions and support clean energy transition"
    },
    {
        "id": "TXN003",
        "description": "Organic Grocery Shopping",
        "amount": 2300.00,
        "category": "Food",
        "merchant": "Nature's Basket",
        "date": "2026-01-08",
        "eco_impact": 3,
        "reasoning": "Organic products avoid harmful pesticides and support sustainable farming"
    },
    {
        "id": "TXN004",
        "description": "Fast Fashion Purchase",
        "amount": 4500.00,
        "category": "Shopping",
        "merchant": "QuickTrends",
        "date": "2026-01-07",
        "eco_impact": -4,
        "reasoning": "Fast fashion contributes to textile waste and high water consumption"
    },
    {
        "id": "TXN005",
        "description": "Solar Panel Installation EMI",
        "amount": 8500.00,
        "category": "Utilities",
        "merchant": "SunPower India",
        "date": "2026-01-06",
        "eco_impact": 5,
        "reasoning": "Solar energy investment reduces dependency on fossil fuels"
    },
    {
        "id": "TXN006",
        "description": "Flight Ticket - Domestic",
        "amount": 7500.00,
        "category": "Transport",
        "merchant": "AirIndia",
        "date": "2026-01-05",
        "eco_impact": -5,
        "reasoning": "Air travel has high carbon emissions per passenger kilometer"
    },
    {
        "id": "TXN007",
        "description": "Plant-Based Restaurant",
        "amount": 850.00,
        "category": "Food",
        "merchant": "Green Leaf Cafe",
        "date": "2026-01-04",
        "eco_impact": 4,
        "reasoning": "Plant-based meals have significantly lower environmental footprint"
    },
    {
        "id": "TXN008",
        "description": "Ride Share - Carpool",
        "amount": 250.00,
        "category": "Transport",
        "merchant": "QuickRide",
        "date": "2026-01-03",
        "eco_impact": 3,
        "reasoning": "Carpooling reduces per-person emissions and road congestion"
    },
    {
        "id": "TXN009",
        "description": "Electricity Bill Payment",
        "amount": 3200.00,
        "category": "Utilities",
        "merchant": "BSES Rajdhani",
        "date": "2026-01-02",
        "eco_impact": 0,
        "reasoning": "Standard utility - impact depends on energy source mix"
    },
    {
        "id": "TXN010",
        "description": "Petrol Fuel Purchase",
        "amount": 5000.00,
        "category": "Transport",
        "merchant": "Indian Oil",
        "date": "2026-01-01",
        "eco_impact": -4,
        "reasoning": "Fossil fuel consumption contributes to carbon emissions"
    },
    {
        "id": "TXN011",
        "description": "Thrift Store Shopping",
        "amount": 1200.00,
        "category": "Shopping",
        "merchant": "SecondChance Store",
        "date": "2025-12-30",
        "eco_impact": 4,
        "reasoning": "Second-hand shopping reduces textile waste and manufacturing demand"
    },
    {
        "id": "TXN012",
        "description": "Digital Subscription - Netflix",
        "amount": 649.00,
        "category": "Entertainment",
        "merchant": "Netflix",
        "date": "2025-12-29",
        "eco_impact": 1,
        "reasoning": "Digital entertainment has lower footprint than physical media"
    },
    {
        "id": "TXN013",
        "description": "Charity Donation - Tree Plantation",
        "amount": 2000.00,
        "category": "Donations",
        "merchant": "GreenEarth Foundation",
        "date": "2025-12-28",
        "eco_impact": 5,
        "reasoning": "Direct contribution to carbon sequestration and biodiversity"
    },
    {
        "id": "TXN014",
        "description": "Plastic Bottled Water - Bulk",
        "amount": 800.00,
        "category": "Food",
        "merchant": "MegaMart",
        "date": "2025-12-27",
        "eco_impact": -3,
        "reasoning": "Single-use plastic contributes to pollution and waste"
    },
    {
        "id": "TXN015",
        "description": "Bicycle Purchase",
        "amount": 12000.00,
        "category": "Transport",
        "merchant": "Hero Cycles",
        "date": "2025-12-26",
        "eco_impact": 5,
        "reasoning": "Zero-emission transportation with health benefits"
    },
    {
        "id": "TXN016",
        "description": "UPI Payment - Local Vendor",
        "amount": 150.00,
        "category": "Food",
        "merchant": "Street Food Vendor",
        "date": "2025-12-25",
        "eco_impact": 2,
        "reasoning": "Digital payments and local sourcing reduce environmental impact"
    }
]

def get_all_transactions():
    """Return all mock transactions."""
    return MOCK_TRANSACTIONS

def get_transaction_by_id(txn_id: str):
    """Get a specific transaction by ID."""
    for txn in MOCK_TRANSACTIONS:
        if txn["id"] == txn_id:
            return txn
    return None

def get_transactions_by_category(category: str):
    """Get transactions filtered by category."""
    return [txn for txn in MOCK_TRANSACTIONS if txn["category"].lower() == category.lower()]
