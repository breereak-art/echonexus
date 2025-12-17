"""
Data module for EchoWorld Nexus
Contains cost of living data, VTC rules, and World Bank indicators for Germany and Japan
"""

COST_OF_LIVING_DATA = {
    "Germany": {
        "Berlin": {
            "rent_1br_city": 1200,
            "rent_1br_outside": 850,
            "groceries_monthly": 350,
            "utilities_monthly": 250,
            "transport_monthly": 86,
            "internet_monthly": 35,
            "meal_cheap": 12,
            "meal_mid": 45,
            "coffee": 3.50,
            "currency": "EUR",
            "ppp_index": 0.85,
            "visa_fund_proof": 11208,
            "min_salary_tech": 3500,
            "avg_salary_tech": 5500,
        },
        "Munich": {
            "rent_1br_city": 1600,
            "rent_1br_outside": 1100,
            "groceries_monthly": 380,
            "utilities_monthly": 280,
            "transport_monthly": 95,
            "internet_monthly": 38,
            "meal_cheap": 14,
            "meal_mid": 55,
            "coffee": 4.00,
            "currency": "EUR",
            "ppp_index": 0.82,
            "visa_fund_proof": 11208,
            "min_salary_tech": 4000,
            "avg_salary_tech": 6500,
        }
    },
    "Japan": {
        "Tokyo": {
            "rent_1br_city": 180000,
            "rent_1br_outside": 95000,
            "groceries_monthly": 45000,
            "utilities_monthly": 15000,
            "transport_monthly": 12000,
            "internet_monthly": 5000,
            "meal_cheap": 800,
            "meal_mid": 2500,
            "coffee": 450,
            "currency": "JPY",
            "ppp_index": 0.72,
            "visa_fund_proof": 2000000,
            "min_salary_tech": 350000,
            "avg_salary_tech": 550000,
        },
        "Osaka": {
            "rent_1br_city": 120000,
            "rent_1br_outside": 70000,
            "groceries_monthly": 40000,
            "utilities_monthly": 13000,
            "transport_monthly": 10000,
            "internet_monthly": 4500,
            "meal_cheap": 700,
            "meal_mid": 2000,
            "coffee": 400,
            "currency": "JPY",
            "ppp_index": 0.75,
            "visa_fund_proof": 2000000,
            "min_salary_tech": 320000,
            "avg_salary_tech": 480000,
        }
    }
}

WORLD_BANK_DATA = {
    "Germany": {
        "gdp_per_capita": 51203,
        "inflation_rate": 6.9,
        "unemployment_rate": 3.0,
        "currency_code": "EUR",
        "exchange_to_usd": 1.08,
        "country_code": "DEU",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    },
    "Japan": {
        "gdp_per_capita": 33815,
        "inflation_rate": 3.3,
        "unemployment_rate": 2.6,
        "currency_code": "JPY",
        "exchange_to_usd": 0.0067,
        "country_code": "JPN",
        "region": "East Asia & Pacific",
        "income_level": "High income"
    }
}

VTC_RULES = {
    "standard": {
        "max_international": 500,
        "max_single_transaction": 1000,
        "daily_limit": 2500,
        "block_high_risk_merchants": True,
        "allow_atm": True,
        "max_atm_withdrawal": 500,
        "description": "Standard spending controls for everyday transactions"
    },
    "conservative": {
        "max_international": 200,
        "max_single_transaction": 500,
        "daily_limit": 1000,
        "block_high_risk_merchants": True,
        "allow_atm": True,
        "max_atm_withdrawal": 200,
        "description": "Strict controls for budget-conscious travelers"
    },
    "flexible": {
        "max_international": 2000,
        "max_single_transaction": 3000,
        "daily_limit": 5000,
        "block_high_risk_merchants": False,
        "allow_atm": True,
        "max_atm_withdrawal": 1000,
        "description": "Relaxed controls for established expats"
    }
}

TRANSACTION_CATEGORIES = {
    "rent": {"risk_level": "low", "icon": "🏠", "category": "Housing"},
    "groceries": {"risk_level": "low", "icon": "🛒", "category": "Food"},
    "utilities": {"risk_level": "low", "icon": "💡", "category": "Bills"},
    "transport": {"risk_level": "low", "icon": "🚌", "category": "Transport"},
    "dining": {"risk_level": "medium", "icon": "🍽️", "category": "Food"},
    "entertainment": {"risk_level": "medium", "icon": "🎬", "category": "Leisure"},
    "shopping": {"risk_level": "medium", "icon": "🛍️", "category": "Shopping"},
    "electronics": {"risk_level": "high", "icon": "💻", "category": "Shopping"},
    "travel": {"risk_level": "high", "icon": "✈️", "category": "Travel"},
    "atm": {"risk_level": "low", "icon": "🏧", "category": "Cash"},
    "healthcare": {"risk_level": "low", "icon": "🏥", "category": "Health"},
    "education": {"risk_level": "low", "icon": "📚", "category": "Education"},
}

SAMPLE_TRANSACTIONS = [
    {"desc": "Monthly Rent", "amount": 1200, "category": "rent", "location": "international"},
    {"desc": "Grocery Store", "amount": 85, "category": "groceries", "location": "international"},
    {"desc": "Metro Pass", "amount": 86, "category": "transport", "location": "international"},
    {"desc": "Restaurant Dinner", "amount": 65, "category": "dining", "location": "international"},
    {"desc": "Laptop Purchase", "amount": 1200, "category": "electronics", "location": "international"},
    {"desc": "Utility Bills", "amount": 180, "category": "utilities", "location": "international"},
    {"desc": "ATM Withdrawal", "amount": 200, "category": "atm", "location": "international"},
    {"desc": "Online Course", "amount": 150, "category": "education", "location": "domestic"},
    {"desc": "Health Insurance", "amount": 250, "category": "healthcare", "location": "international"},
    {"desc": "Weekend Trip", "amount": 450, "category": "travel", "location": "international"},
]


def get_cost_of_living(country: str, city: str = None) -> dict:
    """Get cost of living data for a country/city"""
    if country not in COST_OF_LIVING_DATA:
        return None
    
    country_data = COST_OF_LIVING_DATA[country]
    if city and city in country_data:
        return country_data[city]
    
    first_city = list(country_data.keys())[0]
    return country_data[first_city]


def get_cities(country: str) -> list:
    """Get list of cities for a country"""
    if country not in COST_OF_LIVING_DATA:
        return []
    return list(COST_OF_LIVING_DATA[country].keys())


def get_world_bank_data(country: str) -> dict:
    """Get World Bank indicators for a country"""
    return WORLD_BANK_DATA.get(country, None)


def get_vtc_rules(profile: str = "standard") -> dict:
    """Get VTC rules for a profile"""
    return VTC_RULES.get(profile, VTC_RULES["standard"])


def calculate_confidence_score(col_data: dict, wb_data: dict) -> float:
    """Calculate data confidence score based on cross-verification"""
    if not col_data or not wb_data:
        return 0.7
    
    base_confidence = 0.85
    
    if col_data.get("currency") == wb_data.get("currency_code"):
        base_confidence += 0.05
    
    if wb_data.get("income_level") == "High income":
        base_confidence += 0.05
    
    return min(0.98, base_confidence)


def get_monthly_expenses(country: str, city: str = None) -> dict:
    """Calculate typical monthly expenses"""
    col_data = get_cost_of_living(country, city)
    if not col_data:
        return None
    
    currency = col_data["currency"]
    
    expenses = {
        "rent": col_data["rent_1br_city"],
        "groceries": col_data["groceries_monthly"],
        "utilities": col_data["utilities_monthly"],
        "transport": col_data["transport_monthly"],
        "internet": col_data["internet_monthly"],
        "dining_out": col_data["meal_mid"] * 8,
        "misc": col_data["groceries_monthly"] * 0.3,
    }
    
    total = sum(expenses.values())
    expenses["total"] = total
    expenses["currency"] = currency
    
    return expenses
