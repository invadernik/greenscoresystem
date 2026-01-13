"""
Mock Users Database for GreenScore Platform
Contains 100 unique users with individual credentials and transaction data.
"""

import random
import hashlib
from datetime import datetime, timedelta

# First names pool
FIRST_NAMES = [
    "Aarav", "Vivaan", "Aditya", "Vihaan", "Arjun", "Sai", "Reyansh", "Ayaan", "Krishna", "Ishaan",
    "Ananya", "Diya", "Saanvi", "Aanya", "Aadhya", "Isha", "Navya", "Aisha", "Pari", "Myra",
    "Rahul", "Amit", "Priya", "Neha", "Ravi", "Sunita", "Vikram", "Pooja", "Deepak", "Anjali",
    "Rohit", "Sanjay", "Sneha", "Kavita", "Manish", "Meera", "Rajesh", "Rekha", "Suresh", "Geeta",
    "Karan", "Nisha", "Arun", "Divya", "Varun", "Shruti", "Nikhil", "Ritika", "Siddharth", "Tanvi",
    "Akash", "Pallavi", "Gaurav", "Swati", "Harsh", "Komal", "Dev", "Ritu", "Jay", "Simran",
    "Aryan", "Kritika", "Yash", "Megha", "Kunal", "Preeti", "Sahil", "Aditi", "Mohit", "Shweta",
    "Rohan", "Kirti", "Vishal", "Sapna", "Abhishek", "Vrinda", "Tushar", "Rashi", "Pranav", "Nikita",
    "Dhruv", "Bhavna", "Kartik", "Shalini", "Ankit", "Tanya", "Mayank", "Rupal", "Shubham", "Vandana",
    "Aakash", "Hema", "Vivek", "Malika", "Raghav", "Jyoti", "Nakul", "Sonali", "Parth", "Kriti"
]

LAST_NAMES = [
    "Sharma", "Verma", "Gupta", "Singh", "Kumar", "Patel", "Shah", "Joshi", "Mehta", "Chopra",
    "Reddy", "Nair", "Iyer", "Menon", "Pillai", "Rao", "Naidu", "Choudhury", "Das", "Bose",
    "Banerjee", "Mukherjee", "Chatterjee", "Sen", "Roy", "Dutta", "Ghosh", "Sinha", "Mishra", "Pandey",
    "Tiwari", "Dubey", "Saxena", "Agarwal", "Jain", "Goyal", "Mittal", "Kapoor", "Khanna", "Malhotra",
    "Arora", "Bhatia", "Sethi", "Kohli", "Dhawan", "Bajaj", "Ahuja", "Oberoi", "Mehra", "Tandon"
]

# Transaction templates for generating user-specific data
TRANSACTION_TEMPLATES = [
    # Positive impact transactions
    {"desc": "Metro Rail Pass - {month}", "category": "Transport", "amount_range": (800, 2000), "impact": 5},
    {"desc": "Electric Scooter Charging", "category": "Transport", "amount_range": (100, 500), "impact": 4},
    {"desc": "Organic Store Purchase", "category": "Food", "amount_range": (500, 3000), "impact": 3},
    {"desc": "Solar Panel EMI", "category": "Utilities", "amount_range": (5000, 12000), "impact": 5},
    {"desc": "Plant-Based Restaurant", "category": "Food", "amount_range": (300, 1200), "impact": 4},
    {"desc": "Carpool Ride", "category": "Transport", "amount_range": (100, 400), "impact": 3},
    {"desc": "Thrift Store Shopping", "category": "Shopping", "amount_range": (500, 2000), "impact": 4},
    {"desc": "Bicycle Accessories", "category": "Transport", "amount_range": (200, 1500), "impact": 4},
    {"desc": "Tree Plantation Donation", "category": "Donations", "amount_range": (500, 5000), "impact": 5},
    {"desc": "Eco-Friendly Products", "category": "Shopping", "amount_range": (300, 1500), "impact": 3},
    {"desc": "Local Farmers Market", "category": "Food", "amount_range": (200, 800), "impact": 3},
    {"desc": "Digital Magazine Subscription", "category": "Entertainment", "amount_range": (100, 500), "impact": 2},
    {"desc": "Reusable Products Store", "category": "Shopping", "amount_range": (400, 1200), "impact": 3},
    {"desc": "Public Bus Pass", "category": "Transport", "amount_range": (500, 1500), "impact": 4},
    {"desc": "NGO Contribution", "category": "Donations", "amount_range": (1000, 10000), "impact": 5},
    
    # Neutral transactions
    {"desc": "Electricity Bill", "category": "Utilities", "amount_range": (1500, 5000), "impact": 0},
    {"desc": "Mobile Recharge", "category": "Utilities", "amount_range": (200, 1000), "impact": 0},
    {"desc": "Internet Bill", "category": "Utilities", "amount_range": (500, 2000), "impact": 0},
    {"desc": "Water Bill", "category": "Utilities", "amount_range": (200, 800), "impact": 0},
    {"desc": "Streaming Subscription", "category": "Entertainment", "amount_range": (150, 800), "impact": 1},
    
    # Negative impact transactions
    {"desc": "Petrol Fill-up", "category": "Transport", "amount_range": (2000, 6000), "impact": -4},
    {"desc": "Flight Booking - {dest}", "category": "Transport", "amount_range": (4000, 15000), "impact": -5},
    {"desc": "Fast Fashion Shopping", "category": "Shopping", "amount_range": (1500, 8000), "impact": -4},
    {"desc": "Plastic Bottled Water Case", "category": "Food", "amount_range": (300, 1000), "impact": -3},
    {"desc": "Single-Use Disposables", "category": "Shopping", "amount_range": (200, 800), "impact": -3},
    {"desc": "Diesel Auto Fare", "category": "Transport", "amount_range": (100, 500), "impact": -2},
    {"desc": "Imported Products", "category": "Shopping", "amount_range": (1000, 5000), "impact": -2},
    {"desc": "Meat Restaurant", "category": "Food", "amount_range": (500, 2000), "impact": -2},
    {"desc": "Private Cab Ride", "category": "Transport", "amount_range": (200, 1500), "impact": -2},
    {"desc": "AC Usage Bill (High)", "category": "Utilities", "amount_range": (3000, 8000), "impact": -2},
]

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
DESTINATIONS = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune", "Goa", "Jaipur", "Kochi"]


def generate_user_id(index: int) -> str:
    """Generate unique user ID."""
    return f"USR{str(index + 1).zfill(4)}"


def generate_email(first_name: str, last_name: str, index: int) -> str:
    """Generate unique email."""
    domains = ["gmail.com", "outlook.com", "yahoo.com", "example.com"]
    return f"{first_name.lower()}.{last_name.lower()}{index % 100}@{random.choice(domains)}"


def generate_phone() -> str:
    """Generate Indian phone number."""
    return f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"


def generate_transactions_for_user(user_id: str, user_seed: int) -> list:
    """Generate 10-20 transactions for a user with consistent randomness."""
    random.seed(user_seed)
    num_transactions = random.randint(10, 20)
    transactions = []
    
    base_date = datetime(2026, 1, 13)
    
    for i in range(num_transactions):
        template = random.choice(TRANSACTION_TEMPLATES)
        
        # Generate description with placeholders filled
        desc = template["desc"]
        if "{month}" in desc:
            desc = desc.replace("{month}", random.choice(MONTHS))
        if "{dest}" in desc:
            desc = desc.replace("{dest}", random.choice(DESTINATIONS))
        
        # Generate transaction date going backwards
        txn_date = base_date - timedelta(days=i * random.randint(1, 3))
        
        transactions.append({
            "id": f"{user_id}-TXN{str(i + 1).zfill(3)}",
            "user_id": user_id,
            "description": desc,
            "amount": round(random.uniform(*template["amount_range"]), 2),
            "category": template["category"],
            "date": txn_date.strftime("%Y-%m-%d"),
            "eco_impact": template["impact"],
            "reasoning": get_reasoning(template["impact"], template["category"])
        })
    
    random.seed()  # Reset random seed
    return transactions


def get_reasoning(impact: int, category: str) -> str:
    """Get reasoning text based on impact."""
    if impact >= 4:
        return f"Excellent sustainability choice in {category}! This significantly reduces your carbon footprint."
    elif impact >= 2:
        return f"Good eco-friendly decision. {category} choices like this help the environment."
    elif impact >= 0:
        return f"Neutral environmental impact. Standard {category} transaction."
    elif impact >= -2:
        return f"Moderate environmental concern. Consider greener {category} alternatives."
    else:
        return f"High environmental impact. Reducing such {category} activities can improve your score."


def calculate_user_score(transactions: list) -> dict:
    """Calculate GreenScore for a user based on their transactions."""
    if not transactions:
        return {"score": 50, "status": "medium"}
    
    total_impact = sum(t["eco_impact"] for t in transactions)
    score = max(0, min(100, 50 + total_impact * 2))
    
    if score >= 71:
        status = "high"
    elif score >= 41:
        status = "medium"
    else:
        status = "low"
    
    return {
        "score": round(score),
        "status": status,
        "total_impact": total_impact,
        "transaction_count": len(transactions)
    }


def generate_all_users() -> list:
    """Generate 100 unique users."""
    users = []
    used_names = set()
    
    for i in range(100):
        # Ensure unique name combination
        while True:
            first_name = FIRST_NAMES[i % len(FIRST_NAMES)]
            last_name = LAST_NAMES[(i + random.randint(0, 49)) % len(LAST_NAMES)]
            full_name = f"{first_name} {last_name}"
            if full_name not in used_names:
                used_names.add(full_name)
                break
        
        user_id = generate_user_id(i)
        user_seed = hash(user_id) % 1000000  # Consistent seed for this user
        
        # Generate transactions for this user
        transactions = generate_transactions_for_user(user_id, user_seed)
        score_data = calculate_user_score(transactions)
        
        users.append({
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name,
            "full_name": full_name,
            "email": generate_email(first_name, last_name, i),
            "phone": generate_phone(),
            "avatar_color": f"hsl({(i * 37) % 360}, 70%, 50%)",  # Unique color for each user
            "green_score": score_data["score"],
            "score_status": score_data["status"],
            "total_transactions": score_data["transaction_count"],
            "net_impact": score_data["total_impact"],
            "joined_date": (datetime(2025, 1, 1) + timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
        })
    
    return users


# Pre-generate all users on module load
MOCK_USERS = generate_all_users()

# Cache for user transactions
USER_TRANSACTIONS_CACHE = {}


def get_all_users() -> list:
    """Return all users."""
    return MOCK_USERS


def get_user_by_id(user_id: str) -> dict:
    """Get a specific user by ID."""
    for user in MOCK_USERS:
        if user["id"] == user_id:
            return user
    return None


def search_users(query: str) -> list:
    """Search users by name, email, or ID."""
    query_lower = query.lower()
    results = []
    for user in MOCK_USERS:
        if (query_lower in user["full_name"].lower() or 
            query_lower in user["email"].lower() or
            query_lower in user["id"].lower()):
            results.append(user)
    return results


def get_user_transactions(user_id: str) -> list:
    """Get transactions for a specific user."""
    if user_id in USER_TRANSACTIONS_CACHE:
        return USER_TRANSACTIONS_CACHE[user_id]
    
    # Find user and regenerate their transactions
    user = get_user_by_id(user_id)
    if not user:
        return []
    
    user_index = int(user_id.replace("USR", "")) - 1
    user_seed = hash(user_id) % 1000000
    transactions = generate_transactions_for_user(user_id, user_seed)
    
    USER_TRANSACTIONS_CACHE[user_id] = transactions
    return transactions


def get_users_by_score_range(min_score: int, max_score: int) -> list:
    """Filter users by score range."""
    return [u for u in MOCK_USERS if min_score <= u["green_score"] <= max_score]


def get_user_improvement_areas(user_id: str) -> list:
    """Get improvement suggestions for negative impact transactions."""
    transactions = get_user_transactions(user_id)
    improvements = []
    
    # Group negative transactions by category
    negative_by_category = {}
    for txn in transactions:
        if txn["eco_impact"] < 0:
            cat = txn["category"]
            if cat not in negative_by_category:
                negative_by_category[cat] = {"count": 0, "total_impact": 0, "examples": []}
            negative_by_category[cat]["count"] += 1
            negative_by_category[cat]["total_impact"] += txn["eco_impact"]
            if len(negative_by_category[cat]["examples"]) < 2:
                negative_by_category[cat]["examples"].append(txn["description"])
    
    # Generate improvement suggestions
    improvement_tips = {
        "Transport": {
            "icon": "🚇",
            "action": "Switch to public transport, carpooling, or cycling",
            "potential": "+15 to +25 points"
        },
        "Shopping": {
            "icon": "🛍️", 
            "action": "Choose thrift stores, local brands, and sustainable products",
            "potential": "+10 to +15 points"
        },
        "Food": {
            "icon": "🥗",
            "action": "Reduce single-use plastics, choose local and plant-based options",
            "potential": "+8 to +12 points"
        },
        "Utilities": {
            "icon": "⚡",
            "action": "Reduce AC usage, switch to energy-efficient appliances",
            "potential": "+5 to +10 points"
        }
    }
    
    for cat, data in sorted(negative_by_category.items(), key=lambda x: x[1]["total_impact"]):
        tip = improvement_tips.get(cat, {"icon": "📍", "action": f"Reduce high-impact {cat} activities", "potential": "+5 points"})
        improvements.append({
            "category": cat,
            "icon": tip["icon"],
            "issue": f"{data['count']} high-impact transaction(s) in {cat}",
            "examples": data["examples"],
            "impact": data["total_impact"],
            "suggestion": tip["action"],
            "potential_improvement": tip["potential"],
            "priority": "high" if data["total_impact"] <= -5 else "medium"
        })
    
    return improvements
