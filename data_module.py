"""
Data module for EchoWorld Nexus
Contains cost of living data, VTC rules, and World Bank indicators for 12 countries
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
        },
        "Frankfurt": {
            "rent_1br_city": 1400,
            "rent_1br_outside": 950,
            "groceries_monthly": 360,
            "utilities_monthly": 260,
            "transport_monthly": 90,
            "internet_monthly": 36,
            "meal_cheap": 13,
            "meal_mid": 50,
            "coffee": 3.80,
            "currency": "EUR",
            "ppp_index": 0.83,
            "visa_fund_proof": 11208,
            "min_salary_tech": 4200,
            "avg_salary_tech": 6800,
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
    },
    "United States": {
        "New York": {
            "rent_1br_city": 3500,
            "rent_1br_outside": 2200,
            "groceries_monthly": 600,
            "utilities_monthly": 180,
            "transport_monthly": 130,
            "internet_monthly": 65,
            "meal_cheap": 18,
            "meal_mid": 80,
            "coffee": 5.50,
            "currency": "USD",
            "ppp_index": 1.0,
            "visa_fund_proof": 15000,
            "min_salary_tech": 6000,
            "avg_salary_tech": 12000,
        },
        "San Francisco": {
            "rent_1br_city": 3200,
            "rent_1br_outside": 2400,
            "groceries_monthly": 550,
            "utilities_monthly": 150,
            "transport_monthly": 100,
            "internet_monthly": 60,
            "meal_cheap": 20,
            "meal_mid": 90,
            "coffee": 6.00,
            "currency": "USD",
            "ppp_index": 1.0,
            "visa_fund_proof": 15000,
            "min_salary_tech": 8000,
            "avg_salary_tech": 15000,
        },
        "Austin": {
            "rent_1br_city": 1800,
            "rent_1br_outside": 1400,
            "groceries_monthly": 400,
            "utilities_monthly": 140,
            "transport_monthly": 45,
            "internet_monthly": 55,
            "meal_cheap": 15,
            "meal_mid": 60,
            "coffee": 5.00,
            "currency": "USD",
            "ppp_index": 1.0,
            "visa_fund_proof": 15000,
            "min_salary_tech": 5500,
            "avg_salary_tech": 10000,
        }
    },
    "United Kingdom": {
        "London": {
            "rent_1br_city": 2200,
            "rent_1br_outside": 1500,
            "groceries_monthly": 350,
            "utilities_monthly": 200,
            "transport_monthly": 180,
            "internet_monthly": 35,
            "meal_cheap": 15,
            "meal_mid": 65,
            "coffee": 4.00,
            "currency": "GBP",
            "ppp_index": 0.70,
            "visa_fund_proof": 12500,
            "min_salary_tech": 3500,
            "avg_salary_tech": 6000,
        },
        "Manchester": {
            "rent_1br_city": 1100,
            "rent_1br_outside": 800,
            "groceries_monthly": 280,
            "utilities_monthly": 170,
            "transport_monthly": 85,
            "internet_monthly": 32,
            "meal_cheap": 12,
            "meal_mid": 50,
            "coffee": 3.50,
            "currency": "GBP",
            "ppp_index": 0.72,
            "visa_fund_proof": 12500,
            "min_salary_tech": 3000,
            "avg_salary_tech": 4800,
        }
    },
    "Canada": {
        "Toronto": {
            "rent_1br_city": 2400,
            "rent_1br_outside": 1800,
            "groceries_monthly": 450,
            "utilities_monthly": 160,
            "transport_monthly": 150,
            "internet_monthly": 70,
            "meal_cheap": 18,
            "meal_mid": 70,
            "coffee": 5.00,
            "currency": "CAD",
            "ppp_index": 0.79,
            "visa_fund_proof": 13000,
            "min_salary_tech": 5000,
            "avg_salary_tech": 8500,
        },
        "Vancouver": {
            "rent_1br_city": 2600,
            "rent_1br_outside": 1900,
            "groceries_monthly": 420,
            "utilities_monthly": 140,
            "transport_monthly": 120,
            "internet_monthly": 65,
            "meal_cheap": 17,
            "meal_mid": 75,
            "coffee": 5.50,
            "currency": "CAD",
            "ppp_index": 0.78,
            "visa_fund_proof": 13000,
            "min_salary_tech": 5500,
            "avg_salary_tech": 9000,
        }
    },
    "Australia": {
        "Sydney": {
            "rent_1br_city": 2800,
            "rent_1br_outside": 2000,
            "groceries_monthly": 500,
            "utilities_monthly": 180,
            "transport_monthly": 180,
            "internet_monthly": 70,
            "meal_cheap": 22,
            "meal_mid": 90,
            "coffee": 5.00,
            "currency": "AUD",
            "ppp_index": 0.71,
            "visa_fund_proof": 24500,
            "min_salary_tech": 6000,
            "avg_salary_tech": 10000,
        },
        "Melbourne": {
            "rent_1br_city": 2200,
            "rent_1br_outside": 1600,
            "groceries_monthly": 450,
            "utilities_monthly": 170,
            "transport_monthly": 160,
            "internet_monthly": 65,
            "meal_cheap": 20,
            "meal_mid": 80,
            "coffee": 4.50,
            "currency": "AUD",
            "ppp_index": 0.73,
            "visa_fund_proof": 24500,
            "min_salary_tech": 5500,
            "avg_salary_tech": 9000,
        }
    },
    "Netherlands": {
        "Amsterdam": {
            "rent_1br_city": 1900,
            "rent_1br_outside": 1400,
            "groceries_monthly": 350,
            "utilities_monthly": 200,
            "transport_monthly": 100,
            "internet_monthly": 45,
            "meal_cheap": 15,
            "meal_mid": 55,
            "coffee": 3.80,
            "currency": "EUR",
            "ppp_index": 0.87,
            "visa_fund_proof": 12000,
            "min_salary_tech": 3800,
            "avg_salary_tech": 6000,
        },
        "Rotterdam": {
            "rent_1br_city": 1400,
            "rent_1br_outside": 1000,
            "groceries_monthly": 320,
            "utilities_monthly": 180,
            "transport_monthly": 90,
            "internet_monthly": 42,
            "meal_cheap": 14,
            "meal_mid": 50,
            "coffee": 3.50,
            "currency": "EUR",
            "ppp_index": 0.88,
            "visa_fund_proof": 12000,
            "min_salary_tech": 3500,
            "avg_salary_tech": 5500,
        }
    },
    "Singapore": {
        "Singapore": {
            "rent_1br_city": 2800,
            "rent_1br_outside": 2000,
            "groceries_monthly": 400,
            "utilities_monthly": 120,
            "transport_monthly": 130,
            "internet_monthly": 35,
            "meal_cheap": 6,
            "meal_mid": 50,
            "coffee": 5.50,
            "currency": "SGD",
            "ppp_index": 0.85,
            "visa_fund_proof": 30000,
            "min_salary_tech": 5000,
            "avg_salary_tech": 8500,
        }
    },
    "France": {
        "Paris": {
            "rent_1br_city": 1500,
            "rent_1br_outside": 1000,
            "groceries_monthly": 380,
            "utilities_monthly": 180,
            "transport_monthly": 84,
            "internet_monthly": 30,
            "meal_cheap": 15,
            "meal_mid": 60,
            "coffee": 3.50,
            "currency": "EUR",
            "ppp_index": 0.82,
            "visa_fund_proof": 7380,
            "min_salary_tech": 3200,
            "avg_salary_tech": 5000,
        },
        "Lyon": {
            "rent_1br_city": 900,
            "rent_1br_outside": 650,
            "groceries_monthly": 320,
            "utilities_monthly": 150,
            "transport_monthly": 67,
            "internet_monthly": 28,
            "meal_cheap": 13,
            "meal_mid": 45,
            "coffee": 3.00,
            "currency": "EUR",
            "ppp_index": 0.85,
            "visa_fund_proof": 7380,
            "min_salary_tech": 2800,
            "avg_salary_tech": 4200,
        }
    },
    "Spain": {
        "Barcelona": {
            "rent_1br_city": 1200,
            "rent_1br_outside": 800,
            "groceries_monthly": 300,
            "utilities_monthly": 130,
            "transport_monthly": 55,
            "internet_monthly": 35,
            "meal_cheap": 12,
            "meal_mid": 45,
            "coffee": 2.00,
            "currency": "EUR",
            "ppp_index": 0.68,
            "visa_fund_proof": 6500,
            "min_salary_tech": 2500,
            "avg_salary_tech": 4000,
        },
        "Madrid": {
            "rent_1br_city": 1100,
            "rent_1br_outside": 750,
            "groceries_monthly": 280,
            "utilities_monthly": 120,
            "transport_monthly": 55,
            "internet_monthly": 32,
            "meal_cheap": 12,
            "meal_mid": 40,
            "coffee": 1.80,
            "currency": "EUR",
            "ppp_index": 0.70,
            "visa_fund_proof": 6500,
            "min_salary_tech": 2400,
            "avg_salary_tech": 3800,
        }
    },
    "UAE": {
        "Dubai": {
            "rent_1br_city": 6000,
            "rent_1br_outside": 4000,
            "groceries_monthly": 450,
            "utilities_monthly": 150,
            "transport_monthly": 100,
            "internet_monthly": 95,
            "meal_cheap": 10,
            "meal_mid": 80,
            "coffee": 5.50,
            "currency": "AED",
            "ppp_index": 0.55,
            "visa_fund_proof": 20000,
            "min_salary_tech": 12000,
            "avg_salary_tech": 25000,
        },
        "Abu Dhabi": {
            "rent_1br_city": 5000,
            "rent_1br_outside": 3500,
            "groceries_monthly": 400,
            "utilities_monthly": 140,
            "transport_monthly": 80,
            "internet_monthly": 90,
            "meal_cheap": 10,
            "meal_mid": 70,
            "coffee": 5.00,
            "currency": "AED",
            "ppp_index": 0.57,
            "visa_fund_proof": 20000,
            "min_salary_tech": 11000,
            "avg_salary_tech": 22000,
        }
    },
    "Portugal": {
        "Lisbon": {
            "rent_1br_city": 1100,
            "rent_1br_outside": 750,
            "groceries_monthly": 250,
            "utilities_monthly": 120,
            "transport_monthly": 40,
            "internet_monthly": 35,
            "meal_cheap": 10,
            "meal_mid": 35,
            "coffee": 1.20,
            "currency": "EUR",
            "ppp_index": 0.58,
            "visa_fund_proof": 9120,
            "min_salary_tech": 1800,
            "avg_salary_tech": 3000,
        },
        "Porto": {
            "rent_1br_city": 850,
            "rent_1br_outside": 600,
            "groceries_monthly": 220,
            "utilities_monthly": 110,
            "transport_monthly": 38,
            "internet_monthly": 32,
            "meal_cheap": 9,
            "meal_mid": 30,
            "coffee": 1.00,
            "currency": "EUR",
            "ppp_index": 0.60,
            "visa_fund_proof": 9120,
            "min_salary_tech": 1600,
            "avg_salary_tech": 2600,
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
    },
    "United States": {
        "gdp_per_capita": 76329,
        "inflation_rate": 4.1,
        "unemployment_rate": 3.7,
        "currency_code": "USD",
        "exchange_to_usd": 1.0,
        "country_code": "USA",
        "region": "North America",
        "income_level": "High income"
    },
    "United Kingdom": {
        "gdp_per_capita": 45850,
        "inflation_rate": 7.9,
        "unemployment_rate": 4.2,
        "currency_code": "GBP",
        "exchange_to_usd": 1.27,
        "country_code": "GBR",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    },
    "Canada": {
        "gdp_per_capita": 52051,
        "inflation_rate": 3.9,
        "unemployment_rate": 5.4,
        "currency_code": "CAD",
        "exchange_to_usd": 0.74,
        "country_code": "CAN",
        "region": "North America",
        "income_level": "High income"
    },
    "Australia": {
        "gdp_per_capita": 64674,
        "inflation_rate": 5.6,
        "unemployment_rate": 3.5,
        "currency_code": "AUD",
        "exchange_to_usd": 0.66,
        "country_code": "AUS",
        "region": "East Asia & Pacific",
        "income_level": "High income"
    },
    "Netherlands": {
        "gdp_per_capita": 57025,
        "inflation_rate": 4.1,
        "unemployment_rate": 3.6,
        "currency_code": "EUR",
        "exchange_to_usd": 1.08,
        "country_code": "NLD",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    },
    "Singapore": {
        "gdp_per_capita": 65233,
        "inflation_rate": 4.8,
        "unemployment_rate": 2.0,
        "currency_code": "SGD",
        "exchange_to_usd": 0.74,
        "country_code": "SGP",
        "region": "East Asia & Pacific",
        "income_level": "High income"
    },
    "France": {
        "gdp_per_capita": 44408,
        "inflation_rate": 5.7,
        "unemployment_rate": 7.1,
        "currency_code": "EUR",
        "exchange_to_usd": 1.08,
        "country_code": "FRA",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    },
    "Spain": {
        "gdp_per_capita": 32027,
        "inflation_rate": 3.5,
        "unemployment_rate": 12.1,
        "currency_code": "EUR",
        "exchange_to_usd": 1.08,
        "country_code": "ESP",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    },
    "UAE": {
        "gdp_per_capita": 47790,
        "inflation_rate": 3.1,
        "unemployment_rate": 2.9,
        "currency_code": "AED",
        "exchange_to_usd": 0.27,
        "country_code": "ARE",
        "region": "Middle East & North Africa",
        "income_level": "High income"
    },
    "Portugal": {
        "gdp_per_capita": 25307,
        "inflation_rate": 4.3,
        "unemployment_rate": 6.5,
        "currency_code": "EUR",
        "exchange_to_usd": 1.08,
        "country_code": "PRT",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    }
}

VISA_REQUIREMENTS = {
    "Germany": {
        "visa_types": ["Job Seeker", "EU Blue Card", "Skilled Worker"],
        "blocked_account": 11208,
        "monthly_withdrawal": 934,
        "processing_time_weeks": 8,
        "health_insurance_required": True,
        "language_requirement": "A1-B1 German recommended",
        "work_permit_included": True,
        "validity_months": 18,
        "renewal_possible": True
    },
    "Japan": {
        "visa_types": ["Highly Skilled Professional", "Engineer", "Intra-company Transferee"],
        "blocked_account": 2000000,
        "monthly_withdrawal": None,
        "processing_time_weeks": 4,
        "health_insurance_required": True,
        "language_requirement": "JLPT N2 preferred",
        "work_permit_included": True,
        "validity_months": 36,
        "renewal_possible": True
    },
    "United States": {
        "visa_types": ["H-1B", "L-1", "O-1", "E-2"],
        "blocked_account": 15000,
        "monthly_withdrawal": None,
        "processing_time_weeks": 12,
        "health_insurance_required": False,
        "language_requirement": "English proficiency",
        "work_permit_included": True,
        "validity_months": 36,
        "renewal_possible": True
    },
    "United Kingdom": {
        "visa_types": ["Skilled Worker", "Global Talent", "Innovator"],
        "blocked_account": 12500,
        "monthly_withdrawal": None,
        "processing_time_weeks": 3,
        "health_insurance_required": True,
        "language_requirement": "B1 English IELTS",
        "work_permit_included": True,
        "validity_months": 60,
        "renewal_possible": True
    },
    "Canada": {
        "visa_types": ["Express Entry", "Provincial Nominee", "LMIA Work Permit"],
        "blocked_account": 13000,
        "monthly_withdrawal": None,
        "processing_time_weeks": 6,
        "health_insurance_required": False,
        "language_requirement": "CLB 7 English/French",
        "work_permit_included": True,
        "validity_months": 36,
        "renewal_possible": True
    },
    "Australia": {
        "visa_types": ["Skilled Independent 189", "Skilled Nominated 190", "TSS 482"],
        "blocked_account": 24500,
        "monthly_withdrawal": None,
        "processing_time_weeks": 8,
        "health_insurance_required": True,
        "language_requirement": "IELTS 6.0+",
        "work_permit_included": True,
        "validity_months": 48,
        "renewal_possible": True
    },
    "Netherlands": {
        "visa_types": ["Highly Skilled Migrant", "Startup Visa", "Orientation Year"],
        "blocked_account": 12000,
        "monthly_withdrawal": None,
        "processing_time_weeks": 2,
        "health_insurance_required": True,
        "language_requirement": "Dutch recommended but not required",
        "work_permit_included": True,
        "validity_months": 60,
        "renewal_possible": True
    },
    "Singapore": {
        "visa_types": ["Employment Pass", "S Pass", "Tech.Pass"],
        "blocked_account": 30000,
        "monthly_withdrawal": None,
        "processing_time_weeks": 3,
        "health_insurance_required": False,
        "language_requirement": "English",
        "work_permit_included": True,
        "validity_months": 24,
        "renewal_possible": True
    },
    "France": {
        "visa_types": ["Talent Passport", "Salaried Employee", "Startup Founder"],
        "blocked_account": 7380,
        "monthly_withdrawal": 615,
        "processing_time_weeks": 4,
        "health_insurance_required": True,
        "language_requirement": "A1 French recommended",
        "work_permit_included": True,
        "validity_months": 48,
        "renewal_possible": True
    },
    "Spain": {
        "visa_types": ["Highly Qualified Professional", "Entrepreneur", "Digital Nomad"],
        "blocked_account": 6500,
        "monthly_withdrawal": None,
        "processing_time_weeks": 4,
        "health_insurance_required": True,
        "language_requirement": "Spanish helpful",
        "work_permit_included": True,
        "validity_months": 24,
        "renewal_possible": True
    },
    "UAE": {
        "visa_types": ["Employment Visa", "Golden Visa", "Freelancer Visa"],
        "blocked_account": 20000,
        "monthly_withdrawal": None,
        "processing_time_weeks": 2,
        "health_insurance_required": True,
        "language_requirement": "English",
        "work_permit_included": True,
        "validity_months": 24,
        "renewal_possible": True
    },
    "Portugal": {
        "visa_types": ["Tech Visa", "D7 Passive Income", "Startup Visa"],
        "blocked_account": 9120,
        "monthly_withdrawal": 760,
        "processing_time_weeks": 4,
        "health_insurance_required": True,
        "language_requirement": "Portuguese recommended",
        "work_permit_included": True,
        "validity_months": 24,
        "renewal_possible": True
    }
}

CURRENCY_EXCHANGE_RATES = {
    "EUR": 1.08,
    "USD": 1.0,
    "GBP": 1.27,
    "JPY": 0.0067,
    "CAD": 0.74,
    "AUD": 0.66,
    "SGD": 0.74,
    "AED": 0.27
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


from typing import Optional, Dict, Any, List

def get_cost_of_living(country: str, city: Optional[str] = None) -> Optional[Dict[str, Any]]:
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


def get_countries() -> list:
    """Get list of all supported countries"""
    return list(COST_OF_LIVING_DATA.keys())


def get_world_bank_data(country: str) -> Optional[Dict[str, Any]]:
    """Get World Bank indicators for a country"""
    return WORLD_BANK_DATA.get(country)


def get_visa_requirements(country: str) -> Optional[Dict[str, Any]]:
    """Get visa requirements for a country"""
    return VISA_REQUIREMENTS.get(country)


def get_vtc_rules(profile: str = "standard") -> dict:
    """Get VTC rules for a profile"""
    return VTC_RULES.get(profile, VTC_RULES["standard"])


def convert_to_usd(amount: float, currency: str) -> float:
    """Convert amount to USD"""
    rate = CURRENCY_EXCHANGE_RATES.get(currency, 1.0)
    return amount * rate


def convert_to_eur(amount: float, currency: str) -> float:
    """Convert amount to EUR"""
    usd_amount = convert_to_usd(amount, currency)
    return usd_amount / CURRENCY_EXCHANGE_RATES.get("EUR", 1.08)


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


def get_monthly_expenses(country: str, city: Optional[str] = None) -> Optional[Dict[str, Any]]:
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


def get_ppp_adjusted_salary(salary_eur: float, target_country: str) -> float:
    """Get PPP-adjusted salary for target country"""
    col_data = get_cost_of_living(target_country)
    if not col_data:
        return salary_eur
    
    ppp_index = col_data.get("ppp_index", 1.0)
    return salary_eur * (1 / ppp_index)


def compare_countries_cost(countries: list) -> list:
    """Compare cost of living across countries"""
    comparisons = []
    
    for country in countries:
        col_data = get_cost_of_living(country)
        if col_data:
            monthly_cost = sum([
                col_data.get("rent_1br_city", 0),
                col_data.get("groceries_monthly", 0),
                col_data.get("utilities_monthly", 0),
                col_data.get("transport_monthly", 0),
                col_data.get("internet_monthly", 0)
            ])
            
            monthly_cost_eur = convert_to_eur(monthly_cost, col_data.get("currency", "EUR"))
            
            comparisons.append({
                "country": country,
                "monthly_cost_local": monthly_cost,
                "currency": col_data.get("currency", "EUR"),
                "monthly_cost_eur": monthly_cost_eur,
                "ppp_index": col_data.get("ppp_index", 1.0),
                "avg_tech_salary": col_data.get("avg_salary_tech", 0)
            })
    
    return sorted(comparisons, key=lambda x: x["monthly_cost_eur"])
