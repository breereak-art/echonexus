# EchoWorld Nexus - Complete Technical Documentation

**AI Financial Guardian for Global Mobility**  
*Hackathon Demo - December 2025*

---

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture](#2-architecture)
3. [Core Modules](#3-core-modules)
4. [Data Sources](#4-data-sources)
5. [API Integrations](#5-api-integrations)
6. [User Interface](#6-user-interface)
7. [Function Reference](#7-function-reference)
8. [Configuration](#8-configuration)
9. [Deployment](#9-deployment)

---

## 1. Overview

### 1.1 Purpose
EchoWorld Nexus is an AI-powered financial planning tool that helps users simulate and optimize their finances for international relocation. It provides:

- **VTC Simulation**: Visa Transaction Controls simulation using Visa API sandbox
- **Monte Carlo Analysis**: Alternative financial path optimization
- **Audio Guidance**: Text-to-speech financial coaching from a "Financial Guardian"
- **NFT Passport**: Blockchain-based verification of financial readiness on Polygon
- **DAO Governance**: Decentralized community planning for mobility groups
- **Collaborative Budgeting**: Multi-user shared financial planning

### 1.2 Key Features

| Feature | Description | Module |
|---------|-------------|--------|
| Cost of Living Data | 12 countries, 25+ cities with cross-verified data | `data_module.py` |
| VTC Simulation | Transaction approval/decline simulation | `vtc_engine.py` |
| VTC API Integration | Visa sandbox API integration | `vtc_api.py` |
| Monte Carlo Engine | Financial path optimization | `monte_carlo_engine.py` |
| RAG Data Retrieval | LangChain-powered retrieval | `rag_module.py` |
| AI Guidance | OpenAI-powered personalized advice | `ai_guidance.py` |
| Text-to-Speech | gTTS audio generation | `tts_module.py` |
| Voice Input | Whisper transcription | `voice_input.py` |
| NFT Minting | Polygon Amoy testnet NFTs | `nft_module.py` |
| PDF Export | ReportLab roadmap generation | `pdf_export.py` |
| Collaborative Planning | Multi-user budgeting | `collaborative.py` |
| DAO Governance | Decentralized community voting | `dao_governance.py` |
| 3D Visualization | Three.js interactive charts | `visualization_3d.py` |

### 1.3 Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Python 3.11
- **AI/ML**: OpenAI GPT-5, Whisper, LangChain, FAISS
- **Blockchain**: Web3.py, Polygon Amoy Testnet
- **Audio**: gTTS (Google Text-to-Speech)
- **PDF**: ReportLab
- **Data Visualization**: Plotly, Three.js

---

## 2. Architecture

### 2.1 System Architecture

```
                    +------------------+
                    |   Streamlit UI   |
                    |    (app.py)      |
                    +--------+---------+
                             |
         +-------------------+-------------------+
         |                   |                   |
+--------v-------+  +--------v-------+  +--------v-------+
|  Data Layer    |  | Simulation     |  | AI/Voice       |
|  data_module   |  | Engine         |  | Layer          |
|  rag_module    |  | vtc_engine     |  | ai_guidance    |
|                |  | monte_carlo    |  | tts_module     |
|                |  | vtc_api        |  | voice_input    |
+----------------+  +----------------+  +----------------+
         |                   |                   |
+--------v-------+  +--------v-------+  +--------v-------+
| External APIs  |  | Blockchain     |  | Export         |
| World Bank     |  | nft_module     |  | pdf_export     |
| Numbeo         |  | dao_governance |  | collaborative  |
| Visa Sandbox   |  | Polygon RPC    |  |                |
+----------------+  +----------------+  +----------------+
```

### 2.2 File Structure

```
echoworld-nexus/
├── app.py                 # Main Streamlit application (1470 lines)
├── data_module.py         # Cost of living data & utilities (29KB)
├── vtc_engine.py          # VTC simulation engine (205 lines)
├── vtc_api.py             # Visa API sandbox client (294 lines)
├── monte_carlo_engine.py  # Monte Carlo simulation (245 lines)
├── rag_module.py          # RAG retrieval system (399 lines)
├── ai_guidance.py         # AI guidance generation (242 lines)
├── tts_module.py          # Text-to-speech (131 lines)
├── voice_input.py         # Voice input handling (377 lines)
├── nft_module.py          # NFT minting (228 lines)
├── pdf_export.py          # PDF generation (212 lines)
├── collaborative.py       # Multi-user budgeting (435 lines)
├── dao_governance.py      # DAO governance (475 lines)
├── visualization_3d.py    # Three.js visualizations (511 lines)
├── .streamlit/
│   └── config.toml        # Streamlit configuration
└── pyproject.toml         # Python dependencies
```

---

## 3. Core Modules

### 3.1 Data Module (`data_module.py`)

The foundation of all financial calculations.

#### 3.1.1 Cost of Living Data Structure

```python
COST_OF_LIVING_DATA = {
    "Germany": {
        "Berlin": {
            "rent_1br_city": 1200,        # EUR/month
            "rent_1br_outside": 850,      # EUR/month
            "groceries_monthly": 350,     # EUR/month
            "utilities_monthly": 250,     # EUR/month
            "transport_monthly": 86,      # EUR/month
            "internet_monthly": 35,       # EUR/month
            "meal_cheap": 12,             # EUR
            "meal_mid": 45,               # EUR for 2 people
            "coffee": 3.50,               # EUR
            "currency": "EUR",
            "ppp_index": 0.85,            # Purchasing Power Parity
            "visa_fund_proof": 11208,     # Blocked account requirement
            "min_salary_tech": 3500,      # EUR/month
            "avg_salary_tech": 5500,      # EUR/month
        },
        # ... more cities
    },
    # 12 countries total
}
```

#### 3.1.2 Countries Covered

| Country | Cities | Currency | Visa Fund Proof |
|---------|--------|----------|-----------------|
| Germany | Berlin, Munich, Frankfurt | EUR | €11,208 |
| Japan | Tokyo, Osaka | JPY | ¥2,000,000 |
| United States | New York, San Francisco, Austin | USD | $15,000 |
| United Kingdom | London, Manchester | GBP | £12,500 |
| Canada | Toronto, Vancouver | CAD | C$13,000 |
| Australia | Sydney, Melbourne | AUD | A$24,500 |
| Netherlands | Amsterdam, Rotterdam | EUR | €12,000 |
| Singapore | Singapore | SGD | S$30,000 |
| France | Paris, Lyon | EUR | €7,380 |
| Spain | Barcelona, Madrid | EUR | €6,500 |
| UAE | Dubai, Abu Dhabi | AED | AED 20,000 |
| Portugal | Lisbon, Porto | EUR | €9,120 |

#### 3.1.3 World Bank Data Structure

```python
WORLD_BANK_DATA = {
    "Germany": {
        "gdp_per_capita": 51203,       # USD
        "inflation_rate": 6.9,         # %
        "unemployment_rate": 3.0,      # %
        "currency_code": "EUR",
        "exchange_to_usd": 1.08,
        "country_code": "DEU",
        "region": "Europe & Central Asia",
        "income_level": "High income"
    },
    # ... 12 countries
}
```

#### 3.1.4 Key Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `get_countries()` | None | `List[str]` | List of all country names |
| `get_cities(country)` | `country: str` | `List[str]` | Cities in country |
| `get_cost_of_living(country, city)` | `country: str, city: str` | `Dict` | Full cost data for city |
| `get_world_bank_data(country)` | `country: str` | `Dict` | Economic indicators |
| `get_visa_requirements(country)` | `country: str` | `Dict` | Visa details |
| `convert_to_eur(amount, currency)` | `amount: float, currency: str` | `float` | Currency conversion |
| `calculate_confidence_score(col_data, wb_data)` | Two dicts | `float` | Data confidence (0-1) |
| `compare_countries_cost(countries)` | `List[str]` | `List[Dict]` | Multi-country comparison |

#### 3.1.5 VTC Rules Configuration

```python
VTC_RULES = {
    "standard": {
        "daily_limit": 2500,
        "max_single_transaction": 1000,
        "max_international": 500,
        "max_atm_withdrawal": 300,
        "allow_atm": True,
        "block_high_risk_merchants": True,
        "description": "Balanced controls for everyday spending"
    },
    "conservative": {
        "daily_limit": 1500,
        "max_single_transaction": 500,
        "max_international": 300,
        "max_atm_withdrawal": 200,
        "allow_atm": True,
        "block_high_risk_merchants": True,
        "description": "Strict controls for maximum savings"
    },
    "flexible": {
        "daily_limit": 5000,
        "max_single_transaction": 2000,
        "max_international": 1000,
        "max_atm_withdrawal": 500,
        "allow_atm": True,
        "block_high_risk_merchants": False,
        "description": "Relaxed controls for established budgets"
    }
}
```

#### 3.1.6 Transaction Categories

```python
TRANSACTION_CATEGORIES = {
    "housing": {"risk_level": "low", "icon": "🏠"},
    "groceries": {"risk_level": "low", "icon": "🛒"},
    "transport": {"risk_level": "low", "icon": "🚌"},
    "utilities": {"risk_level": "low", "icon": "💡"},
    "dining": {"risk_level": "medium", "icon": "🍽️"},
    "shopping": {"risk_level": "medium", "icon": "🛍️"},
    "entertainment": {"risk_level": "medium", "icon": "🎬"},
    "travel": {"risk_level": "high", "icon": "✈️"},
    "atm": {"risk_level": "medium", "icon": "🏧"},
    "subscription": {"risk_level": "low", "icon": "📱"},
}
```

---

### 3.2 VTC Engine (`vtc_engine.py`)

Simulates Visa Transaction Controls for spending management.

#### 3.2.1 Core Functions

**`simulate_vtc(transactions, rules_profile, daily_spent)`**

Processes a list of transactions against VTC rules.

```python
# Input
transactions = [
    {"desc": "Rent Payment", "amount": 1200, "category": "housing", "location": "international"},
    {"desc": "Grocery Store", "amount": 85, "category": "groceries", "location": "international"},
]

# Output per transaction
{
    "tx": "Rent Payment",
    "amount": 1200,
    "category": "housing",
    "location": "international",
    "status": "Declined",  # "Approved", "Declined", or "Flagged"
    "reason": "Exceeds single transaction limit (€1000)",
    "vtc_action": "VTC blocked this large purchase—consider splitting or pre-approving",
    "savings_impact": 1200,
    "icon": "🏠",
    "risk_level": "low",
    "running_daily_total": 0
}
```

**`calculate_vtc_summary(sim_feed)`**

Aggregates simulation results.

```python
# Returns
{
    "total_transactions": 10,
    "approved_count": 7,
    "declined_count": 2,
    "flagged_count": 1,
    "approval_rate": 70.0,
    "total_approved": 2500.0,
    "total_declined": 1500.0,
    "potential_savings": 1500.0,
    "category_breakdown": {
        "housing": {"approved": 0, "declined": 1200, "total": 1200},
        "groceries": {"approved": 350, "declined": 0, "total": 350},
        # ...
    }
}
```

**`get_vtc_recommendations(sim_feed, rules_profile)`**

Generates optimization suggestions.

```python
# Returns list of strings
[
    "Consider splitting large purchases (over €1000) into smaller transactions",
    "Set up travel notifications with your bank before moving abroad",
    "VTC saved you €1500 from potential overspending—use this for visa fund proof"
]
```

**`generate_vtc_guardian_message(sim_feed, country, rules_profile)`**

Creates narrated guidance text for TTS.

---

### 3.3 VTC API (`vtc_api.py`)

Visa Transaction Controls Sandbox API integration.

#### 3.3.1 VTCSandboxClient Class

```python
class VTCSandboxClient:
    def __init__(self, force_simulation: bool = False):
        # Uses VISA_VTC_SANDBOX_KEY and VISA_VTC_SANDBOX_SECRET env vars
        
    def create_control_profile(self, rules: Dict, profile_name: str) -> Dict
    def authorize_transaction(self, amount, category, location, merchant_name, rules) -> Dict
    def get_analytics(self) -> Dict
    def get_transaction_history(self) -> List[Dict]
    def reset_session(self)
```

#### 3.3.2 API Response Format

```python
# Transaction authorization response
{
    "success": True,
    "transaction_id": "tx_1702901234567",
    "authorization_code": "a1b2c3d4",  # None if declined
    "status": "approved",  # or "declined"
    "decline_reason": None,  # or reason string
    "risk_score": 0.2,
    "response_code": "00",  # "00" = approved, "05" = declined
    "real_time_decision": True,
    "sandbox_mode": True
}
```

#### 3.3.3 Connection Status

```python
get_vtc_api_status()
# Returns
{
    "sandbox_mode": True,
    "api_available": True,
    "session_active": True,
    "real_api_configured": False,
    "last_error": None,
    "message": "Simulation Mode - Add VISA_VTC_SANDBOX_KEY..."
}
```

---

### 3.4 Monte Carlo Engine (`monte_carlo_engine.py`)

Financial path optimization through Monte Carlo simulation.

#### 3.4.1 Core Function

**`run_monte_carlo(base_salary, base_expenses, variables, num_sims, months, seed)`**

```python
# Default variables
variables = {
    "upskill_boost": [0, 0.15, 0.25],      # Salary increase options
    "expense_reduction": [0, 0.1, 0.2],     # Expense cut options
    "side_income": [0, 200, 500]            # Additional income
}

# Returns
{
    "top_paths": [
        {
            "path_name": "Career Accelerator Path",
            "path_description": "+25% salary through upskilling",
            "salary": 6875.0,
            "expenses": 1350.0,
            "monthly_savings": 5525.0,
            "total_savings_12m": 66300.0,
            "approval_prob": 0.92,
            "visa_fund_met": True,
            "stability_score": 85.0,
            "upskill_boost": 0.25,
            "expense_cut": 0.1,
            "side_income": 0
        },
        # 2 more paths
    ],
    "all_outcomes": [...],  # All 100 simulations
    "statistics": {
        "avg_salary": 5500.0,
        "max_salary": 7375.0,
        "min_salary": 5000.0,
        "avg_savings": 48000.0,
        "max_savings": 66300.0,
        "min_savings": 36000.0,
        "avg_approval_prob": 0.78,
        "max_approval_prob": 0.92,
        "visa_fund_success_rate": 85.0,
        "total_simulations": 100
    },
    "base_scenario": {
        "salary": 5000,
        "expenses": 3500,
        "monthly_savings": 1500,
        "approval_prob": 0.65
    }
}
```

#### 3.4.2 Path Naming Logic

| Condition | Path Name |
|-----------|-----------|
| upskill_boost >= 0.2 | Career Accelerator Path |
| expense_cut >= 0.15 | Frugal Pioneer Path |
| side_income >= 400 | Hustle Builder Path |
| upskill + expense_cut > 0 | Balanced Growth Path |
| Default | Steady Progress Path |

#### 3.4.3 Helper Functions

| Function | Description |
|----------|-------------|
| `calculate_approval_probability(salary, expenses, savings)` | 0.1-0.98 probability score |
| `calculate_stability_score(salary, expenses, monthly_savings)` | 0-100 stability metric |
| `compare_paths(paths)` | Natural language comparison |

---

### 3.5 RAG Module (`rag_module.py`)

Retrieval-Augmented Generation for grounded data retrieval.

#### 3.5.1 RAGRetriever Class

```python
class RAGRetriever:
    def __init__(self):
        # Initializes with FAISS vector store if OpenAI API available
        # Falls back to keyword search otherwise
        
    def query(self, query: str, country: str, city: str, k: int) -> Dict
    def get_context_for_guidance(self, country: str, city: str, topics: List[str]) -> str
    def get_status(self) -> Dict
```

#### 3.5.2 Document Types

1. **World Bank Documents**: Country-level economic data
2. **Cost of Living Documents**: City-specific expenses
3. **Visa Requirements Documents**: Immigration information

#### 3.5.3 Query Response

```python
{
    "success": True,
    "results": [
        {
            "content": "City: Berlin, Germany\nCurrency: EUR\n...",
            "metadata": {"type": "cost_of_living", "country": "Germany", "city": "Berlin"},
            "source": "Numbeo + World Bank Cross-Verified"
        }
    ],
    "confidence": 0.92,
    "mode": "rag",  # or "fallback_keyword"
    "query": "cost of living in Berlin",
    "num_results": 3
}
```

---

### 3.6 AI Guidance (`ai_guidance.py`)

OpenAI-powered personalized financial guidance.

#### 3.6.1 Main Function

**`generate_guardian_guidance(country, city, vtc_summary, monte_carlo_results, user_salary, user_savings, use_ai)`**

- Uses GPT-5 when `OPENAI_API_KEY` is available
- Falls back to template-based guidance otherwise

#### 3.6.2 Template Guidance Structure

```
Hello, this is your Financial Guardian calling from {city}, {country}.
I've been analyzing your financial simulation, and I'm here to share insights.

Based on your expected salary of €X/month and savings of €Y:
- Your VTC approval rate is X%
- [Blocked transaction info if applicable]

I recommend the "{path_name}" approach with {success_prob}% success probability.
[Encouragement based on success level]

Remember, this is a simulated planning tool to help you prepare.
```

---

### 3.7 TTS Module (`tts_module.py`)

Google Text-to-Speech for audio guidance.

#### 3.7.1 Functions

| Function | Parameters | Returns | Description |
|----------|------------|---------|-------------|
| `generate_audio_guidance(text, language, include_watermark)` | `str, str, bool` | `bytes` | MP3 audio bytes |
| `generate_audio_file(text, output_path, language, include_watermark)` | `str, str, str, bool` | `bool` | Save to file |
| `generate_intro_audio(country, city)` | `str, str` | `bytes` | Greeting audio |
| `generate_summary_audio(approval_rate, savings, best_path, success_prob)` | `float, float, str, float` | `bytes` | Quick summary |
| `estimate_audio_duration(text)` | `str` | `float` | Seconds estimate |

#### 3.7.2 Watermark

All audio includes ethical watermark:
> "Note: This is a simulated financial planning tool."

---

### 3.8 Voice Input (`voice_input.py`)

Speech recognition and conversational interface.

#### 3.8.1 VoiceConversationManager Class

```python
class VoiceConversationManager:
    def process_voice_input(self, audio_bytes: bytes) -> Dict
    def process_text_input(self, text: str) -> Dict
    def set_context(self, country: str, city: str)
    def get_history(self) -> List[Dict]
    def clear_history()
```

#### 3.8.2 Intent Detection

| Intent | Keywords |
|--------|----------|
| `cost_inquiry` | cost, expensive, cheap, afford, price, rent |
| `visa_inquiry` | visa, permit, requirement, document |
| `salary_inquiry` | salary, income, earn, pay, wage |
| `comparison` | compare, vs, versus, difference, better |
| `budget_planning` | budget, save, saving, plan, simulate |
| `vtc_inquiry` | vtc, transaction, control, spending |

#### 3.8.3 Response Format

```python
{
    "success": True,
    "user_text": "What's the rent in Berlin?",
    "parsed_intent": {
        "intent": "cost_inquiry",
        "entities": {"country": "Germany"},
        "confidence": 0.85
    },
    "response": "Berlin is quite affordable for a major European capital...",
    "context": {"country": "Germany", "city": "Berlin"}
}
```

---

### 3.9 NFT Module (`nft_module.py`)

Polygon blockchain integration for Mobility Passport NFTs.

#### 3.9.1 Configuration

```python
POLYGON_AMOY_RPC = "https://rpc-amoy.polygon.technology"
POLYGON_AMOY_CHAIN_ID = 80002
```

#### 3.9.2 NFT Metadata Structure

```python
{
    "name": "EchoWorld Mobility Passport - Germany",
    "description": "This NFT certifies the holder's simulated financial readiness...",
    "image": "ipfs://placeholder_mobility_passport_image",
    "external_url": "https://echoworld-nexus.replit.app",
    "attributes": [
        {"trait_type": "Destination Country", "value": "Germany"},
        {"trait_type": "Destination City", "value": "Berlin"},
        {"trait_type": "Success Probability", "value": "85%"},
        {"trait_type": "Readiness Tier", "value": "Gold"},
        {"trait_type": "VTC Optimized", "value": "Yes"},
        {"trait_type": "Approval Rate", "value": "92%"},
        {"trait_type": "Projected Annual Savings", "value": "€18,000"},
        {"trait_type": "Recommended Path", "value": "Career Accelerator Path"},
        {"display_type": "date", "trait_type": "Simulation Date", "value": 1702901234}
    ],
    "properties": {
        "tier": "Gold",
        "tier_description": "Exceptional financial readiness",
        "simulation_version": "1.0.0",
        "disclaimer": "This NFT represents simulated financial planning data..."
    }
}
```

#### 3.9.3 Tier System

| Success Probability | Tier | Description |
|---------------------|------|-------------|
| >= 85% | Gold | Exceptional financial readiness |
| >= 70% | Silver | Strong financial foundation |
| >= 50% | Bronze | Developing financial readiness |
| < 50% | Starter | Beginning your journey |

#### 3.9.4 Functions

| Function | Description |
|----------|-------------|
| `create_mobility_passport_metadata(...)` | Generate NFT metadata |
| `prepare_mint_transaction(wallet_address, metadata)` | Prepare blockchain tx |
| `get_nft_preview_card(metadata)` | UI preview data |
| `generate_shareable_link(metadata)` | Mock sharing link |
| `check_web3_availability()` | Check Polygon connection |

---

### 3.10 PDF Export (`pdf_export.py`)

ReportLab-powered PDF generation.

#### 3.10.1 PDF Contents

1. **Header**: EchoWorld Nexus branding
2. **Executive Summary Table**:
   - Expected Salary
   - Current Savings
   - VTC Approval Rate
   - Success Probability
   - Recommended Path
3. **VTC Simulation Results**: Category breakdown table
4. **Alternative Financial Paths**: Top 3 paths with details
5. **Key Recommendations**: Numbered list
6. **Disclaimer**: Legal notice

#### 3.10.2 Functions

```python
generate_financial_roadmap_pdf(
    country, city, user_salary, user_savings,
    vtc_summary, monte_carlo_results, sim_feed, recommendations
) -> bytes  # PDF bytes

get_pdf_filename(country, city) -> str
# Returns: "EchoWorld_Roadmap_Berlin_Germany_20251218.pdf"
```

---

### 3.11 Collaborative Module (`collaborative.py`)

Multi-user budgeting for groups.

#### 3.11.1 Data Classes

```python
@dataclass
class BudgetMember:
    member_id: str
    name: str
    role: str  # "owner" or "contributor"
    income: float
    currency: str = "EUR"
    contribution_percent: float = 50.0

@dataclass
class SharedExpense:
    expense_id: str
    category: str
    description: str
    amount: float
    currency: str
    split_type: str  # "equal", "income_based", "custom"
    member_shares: Dict[str, float]

@dataclass
class CollaborativeBudget:
    budget_id: str
    name: str
    destination_country: str
    destination_city: str
    target_move_date: str
    members: List[BudgetMember]
    shared_expenses: List[SharedExpense]
    savings_goal: float
    current_savings: float
```

#### 3.11.2 Manager Functions

| Function | Description |
|----------|-------------|
| `create_budget(name, creator_name, country, city, date, income, goal)` | New budget |
| `add_member(budget_id, name, income, role)` | Add participant |
| `remove_member(budget_id, member_id)` | Remove participant |
| `add_shared_expense(budget_id, category, desc, amount, currency, split_type)` | Add expense |
| `get_member_summary(budget_id, member_id)` | Individual breakdown |
| `get_budget_overview(budget_id)` | Full budget stats |
| `generate_invite_code(budget_id)` | Shareable code |
| `join_with_invite(invite_code, name, income)` | Join via code |

---

### 3.12 DAO Governance (`dao_governance.py`)

Decentralized community governance.

#### 3.12.1 Data Classes

```python
@dataclass
class GovernanceProposal:
    proposal_id: str
    title: str
    description: str
    proposal_type: str
    creator_address: str
    created_at: str
    voting_ends: str
    votes_for: int = 0
    votes_against: int = 0
    votes_abstain: int = 0
    status: str = "active"  # "active", "passed", "rejected"

@dataclass
class DAOMember:
    address: str
    passport_nfts: List[str]
    voting_power: int = 0
    proposals_created: int = 0
    votes_cast: int = 0
    reputation_score: float = 0.0

@dataclass
class MobilityCommunity:
    community_id: str
    name: str
    destination_country: str
    destination_city: str
    treasury_address: str
    members: List[DAOMember]
    proposals: List[GovernanceProposal]
    treasury_balance: float = 0.0
    governance_token: str = "ECHO"
```

#### 3.12.2 Proposal Types

| Type | Description |
|------|-------------|
| `treasury_allocation` | Spend community treasury funds |
| `community_guidelines` | Change rules and guidelines |
| `partnership` | Service provider partnerships |
| `member_spotlight` | Member recognition/rewards |
| `resource_sharing` | Shared housing tips, job leads |
| `governance_change` | Voting rules changes |

#### 3.12.3 Voting Power

| NFT Tier | Voting Power |
|----------|--------------|
| Gold | 100 |
| Silver | 50 |
| Bronze | 25 |
| Default | 10 |

---

### 3.13 3D Visualization (`visualization_3d.py`)

Three.js interactive visualizations.

#### 3.13.1 Visualization Types

1. **Globe Visualization**: World map with country markers
2. **3D Bar Chart**: Cost comparison across countries
3. **Savings Path Visualization**: Monte Carlo paths in 3D
4. **Financial Dashboard**: Combined interactive view

#### 3.13.2 Configuration Objects

```python
# Globe config
{
    "type": "globe",
    "markers": [...],
    "rotation_speed": 0.001,
    "camera_distance": 300
}

# Bar chart config
{
    "type": "bar_chart_3d",
    "bars": [...],
    "animation": {"enabled": True, "duration": 1000},
    "interaction": {"hover_enabled": True, "tooltip_enabled": True}
}
```

---

## 4. Data Sources

### 4.1 Primary Sources

| Source | Data Type | Update Frequency |
|--------|-----------|------------------|
| Numbeo | Cost of living | Cross-verified Dec 2024 |
| World Bank Open Data | Economic indicators | Latest available |
| Official Immigration | Visa requirements | Current regulations |

### 4.2 Confidence Scoring

The system calculates a confidence score (0-1) based on:
- Data recency
- Cross-verification status
- Source reliability
- Coverage completeness

---

## 5. API Integrations

### 5.1 Required API Keys

| Service | Environment Variable | Required | Purpose |
|---------|---------------------|----------|---------|
| OpenAI | `OPENAI_API_KEY` | No* | AI guidance, RAG embeddings |
| Visa Sandbox | `VISA_VTC_SANDBOX_KEY` | No* | Live VTC API |
| Visa Sandbox | `VISA_VTC_SANDBOX_SECRET` | No* | Live VTC API |

*All features have fallback modes without API keys

### 5.2 Fallback Behavior

| Feature | With API Key | Without API Key |
|---------|--------------|-----------------|
| AI Guidance | GPT-5 personalized | Template-based |
| RAG Retrieval | FAISS vector search | Keyword matching |
| Voice Transcription | Whisper API | Text input only |
| VTC API | Live sandbox | Local simulation |
| Audio Generation | gTTS (always free) | gTTS (always free) |

---

## 6. User Interface

### 6.1 Main App Structure (`app.py`)

#### 6.1.1 Sidebar

- Demo Mode toggle
- Country/City selection
- Financial inputs (salary, savings)
- VTC Profile selection
- Transaction upload
- Ethics information

#### 6.1.2 Hero Dashboard

Four key metrics cards:
1. Data Confidence (%)
2. Proof of Funds status
3. Monthly Salary (with PPP toggle)
4. VTC Profile

#### 6.1.3 Main Tabs

**Tab 1: Simulate & Optimize**
- Run Financial Simulation button
- VTC Results display
- Monte Carlo scatter plot
- Alternative paths cards
- Transaction feed

**Tab 2: Voice & Guidance**
- Chat Assistant (text-based)
- Audio Guidance generation
- Audio player

**Tab 3: Export & Advanced**
- PDF Export
- NFT Passport minting
- Collaborative Budgeting
- DAO Governance

### 6.2 Session State Variables

```python
st.session_state.simulation_run = False
st.session_state.sim_results = None
st.session_state.audio_generated = False
st.session_state.collab_budget = None
st.session_state.dao_community = None
st.session_state.conversation_history = []
st.session_state.demo_mode = False
st.session_state.ppp_view = False
```

---

## 7. Function Reference

### 7.1 app.py Main Functions

| Function | Line | Description |
|----------|------|-------------|
| `main()` | 441 | Main app entry point |
| `display_hero_dashboard()` | 572 | Hero metrics section |
| `display_pof_verification()` | 649 | Proof of funds check |
| `display_ethics_sidebar()` | 703 | Ethics information |
| `display_simulation_tab()` | 715 | Main simulation tab |
| `display_guidance_tab()` | 768 | Voice/audio tab |
| `display_advanced_tab()` | 785 | Export/NFT/DAO tab |
| `display_voice_assistant_section()` | 823 | Chat interface |
| `display_collaborative_section()` | 894 | Multi-user budget |
| `display_dao_section()` | 930 | DAO features |
| `run_simulation()` | 970 | Execute full simulation |
| `display_results()` | 1034 | Show simulation results |
| `display_audio_guidance()` | 1197 | Audio generation |
| `display_nft_section()` | 1259 | NFT minting |
| `display_export_section()` | 1350 | PDF export |

---

## 8. Configuration

### 8.1 Streamlit Config (`.streamlit/config.toml`)

```toml
[server]
headless = true
address = "0.0.0.0"
port = 5000

[browser]
gatherUsageStats = false
```

### 8.2 Dependencies (`pyproject.toml`)

```
streamlit
anthropic
faiss-cpu
gtts
langchain
langchain-community
langchain-openai
numpy
openai
pandas
plotly
reportlab
requests
web3
```

---

## 9. Deployment

### 9.1 Running Locally

```bash
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

### 9.2 Replit Deployment

- **Target**: Autoscale
- **Port**: 5000
- **Command**: `streamlit run app.py --server.port 5000`

### 9.3 Environment Variables

Set in Replit Secrets or environment:
- `OPENAI_API_KEY` (optional)
- `VISA_VTC_SANDBOX_KEY` (optional)
- `VISA_VTC_SANDBOX_SECRET` (optional)

---

## Appendix A: Sample Transactions

```python
SAMPLE_TRANSACTIONS = [
    {"desc": "Rent Payment", "amount": 1200, "category": "housing", "location": "international"},
    {"desc": "Grocery Store", "amount": 85, "category": "groceries", "location": "international"},
    {"desc": "Metro Pass", "amount": 86, "category": "transport", "location": "international"},
    {"desc": "Internet Bill", "amount": 35, "category": "utilities", "location": "international"},
    {"desc": "Dining Out", "amount": 45, "category": "dining", "location": "international"},
    {"desc": "Shopping Mall", "amount": 150, "category": "shopping", "location": "international"},
    {"desc": "ATM Withdrawal", "amount": 200, "category": "atm", "location": "international"},
    {"desc": "Utility Bill", "amount": 250, "category": "utilities", "location": "international"},
    {"desc": "Streaming Service", "amount": 15, "category": "subscription", "location": "domestic"},
    {"desc": "Flight Booking", "amount": 450, "category": "travel", "location": "international"},
]
```

---

## Appendix B: Currency Exchange Rates

```python
CURRENCY_EXCHANGE_RATES = {
    "EUR": 1.08,
    "USD": 1.0,
    "GBP": 1.27,
    "JPY": 0.0067,
    "CAD": 0.74,
    "AUD": 0.66,
    "SGD": 0.74,
    "AED": 0.27,
}
```

---

## Appendix C: Ethical Guidelines

The application follows these ethical principles:

1. **Transparency**: All AI-generated content is watermarked
2. **Privacy**: No personal data is stored
3. **Disclaimer**: Clear indication this is a simulation tool
4. **Accuracy**: Cross-verified data sources with confidence scores
5. **Accessibility**: Fallback modes for all features

---

*Documentation generated for EchoWorld Nexus v1.0.0 - December 2025*
