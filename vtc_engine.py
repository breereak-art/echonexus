"""
VTC (Visa Transaction Controls) Simulation Engine
Simulates transaction approvals and declines based on Visa control rules
"""

from typing import List, Dict, Any
from data_module import TRANSACTION_CATEGORIES, get_vtc_rules


def simulate_vtc(
    transactions: List[Dict[str, Any]], 
    rules_profile: str = "standard",
    daily_spent: float = 0
) -> List[Dict[str, Any]]:
    """
    Simulate VTC transaction processing
    
    Args:
        transactions: List of transactions with desc, amount, category, location
        rules_profile: VTC profile (standard, conservative, flexible)
        daily_spent: Amount already spent today
        
    Returns:
        List of processed transactions with status and reason
    """
    rules = get_vtc_rules(rules_profile)
    sim_feed = []
    running_daily_total = daily_spent
    
    for tx in transactions:
        amount = tx.get("amount", 0)
        location = tx.get("location", "domestic")
        category = tx.get("category", "shopping")
        desc = tx.get("desc", "Unknown Transaction")
        
        status = "Approved"
        reason = "Transaction approved"
        vtc_action = None
        savings_impact = 0
        
        cat_info = TRANSACTION_CATEGORIES.get(category, {"risk_level": "medium", "icon": "💳"})
        
        if location == "international" and amount > rules["max_international"]:
            status = "Declined"
            reason = f"Exceeds international limit (€{rules['max_international']})"
            vtc_action = "VTC blocked this international transaction to protect your budget"
            savings_impact = amount
            
        elif amount > rules["max_single_transaction"]:
            status = "Declined"
            reason = f"Exceeds single transaction limit (€{rules['max_single_transaction']})"
            vtc_action = "VTC blocked this large purchase—consider splitting or pre-approving"
            savings_impact = amount
            
        elif running_daily_total + amount > rules["daily_limit"]:
            status = "Declined"
            reason = f"Would exceed daily limit (€{rules['daily_limit']})"
            vtc_action = "Daily spending limit reached—transaction blocked for budget safety"
            savings_impact = amount
            
        elif category == "atm":
            if not rules["allow_atm"]:
                status = "Declined"
                reason = "ATM withdrawals blocked by VTC settings"
                vtc_action = "ATM access disabled in your VTC profile"
                savings_impact = amount
            elif amount > rules["max_atm_withdrawal"]:
                status = "Declined"
                reason = f"Exceeds ATM withdrawal limit (€{rules['max_atm_withdrawal']})"
                vtc_action = "ATM withdrawal limit exceeded"
                savings_impact = amount
                
        elif cat_info["risk_level"] == "high" and rules["block_high_risk_merchants"]:
            if amount > rules["max_international"] * 0.8:
                status = "Flagged"
                reason = "High-value transaction in high-risk category"
                vtc_action = "Transaction flagged for review—consider using a different payment method"
        
        if status == "Approved":
            running_daily_total += amount
        
        sim_feed.append({
            "tx": desc,
            "amount": amount,
            "category": category,
            "location": location,
            "status": status,
            "reason": reason,
            "vtc_action": vtc_action,
            "savings_impact": savings_impact,
            "icon": cat_info["icon"],
            "risk_level": cat_info["risk_level"],
            "running_daily_total": running_daily_total if status == "Approved" else running_daily_total
        })
    
    return sim_feed


def calculate_vtc_summary(sim_feed: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate summary statistics from VTC simulation"""
    
    total_transactions = len(sim_feed)
    approved = sum(1 for tx in sim_feed if tx["status"] == "Approved")
    declined = sum(1 for tx in sim_feed if tx["status"] == "Declined")
    flagged = sum(1 for tx in sim_feed if tx["status"] == "Flagged")
    
    total_approved_amount = sum(tx["amount"] for tx in sim_feed if tx["status"] == "Approved")
    total_declined_amount = sum(tx["amount"] for tx in sim_feed if tx["status"] == "Declined")
    total_savings = sum(tx["savings_impact"] for tx in sim_feed)
    
    approval_rate = (approved / total_transactions * 100) if total_transactions > 0 else 0
    
    category_breakdown = {}
    for tx in sim_feed:
        cat = tx["category"]
        if cat not in category_breakdown:
            category_breakdown[cat] = {"approved": 0, "declined": 0, "total": 0}
        category_breakdown[cat]["total"] += tx["amount"]
        if tx["status"] == "Approved":
            category_breakdown[cat]["approved"] += tx["amount"]
        else:
            category_breakdown[cat]["declined"] += tx["amount"]
    
    return {
        "total_transactions": total_transactions,
        "approved_count": approved,
        "declined_count": declined,
        "flagged_count": flagged,
        "approval_rate": approval_rate,
        "total_approved": total_approved_amount,
        "total_declined": total_declined_amount,
        "potential_savings": total_savings,
        "category_breakdown": category_breakdown
    }


def get_vtc_recommendations(sim_feed: List[Dict[str, Any]], rules_profile: str) -> List[str]:
    """Generate VTC optimization recommendations"""
    
    recommendations = []
    rules = get_vtc_rules(rules_profile)
    
    declined_high_value = [tx for tx in sim_feed if tx["status"] == "Declined" and tx["amount"] > 500]
    if declined_high_value:
        recommendations.append(
            f"Consider splitting large purchases (over €{rules['max_single_transaction']}) into smaller transactions"
        )
    
    international_declines = [tx for tx in sim_feed if tx["status"] == "Declined" and tx["location"] == "international"]
    if len(international_declines) > 2:
        recommendations.append(
            "Set up travel notifications with your bank before moving abroad to increase international limits"
        )
    
    total_declined = sum(tx["amount"] for tx in sim_feed if tx["status"] == "Declined")
    if total_declined > 1000:
        recommendations.append(
            f"VTC saved you €{total_declined:.0f} from potential overspending—use this for visa fund proof"
        )
    
    if rules_profile == "conservative":
        recommendations.append(
            "Your conservative VTC profile is ideal for the first 3 months abroad—consider upgrading later"
        )
    elif rules_profile == "flexible":
        recommendations.append(
            "Flexible VTC profile detected—ensure you have emergency savings before high spending"
        )
    
    if not recommendations:
        recommendations.append(
            "Your spending pattern is well-optimized for your VTC profile—keep it up!"
        )
    
    return recommendations


def generate_vtc_guardian_message(sim_feed: List[Dict[str, Any]], country: str, rules_profile: str) -> str:
    """Generate the Financial Guardian's VTC-focused message"""
    
    summary = calculate_vtc_summary(sim_feed)
    recommendations = get_vtc_recommendations(sim_feed, rules_profile)
    
    message = f"Hello, this is your Financial Guardian calling from {country}. "
    message += "I've analyzed your simulated transactions using Visa Transaction Controls. "
    
    if summary["declined_count"] > 0:
        message += f"I blocked {summary['declined_count']} transactions totaling €{summary['total_declined']:.0f}. "
        message += "This wasn't to restrict you, but to protect your relocation budget. "
        
        if summary["potential_savings"] > 500:
            message += f"By setting these controls, you could save €{summary['potential_savings']:.0f} for your visa fund proof. "
    else:
        message += "All your planned transactions would be approved with current VTC settings. "
    
    message += f"Your approval rate is {summary['approval_rate']:.0f}%. "
    
    if recommendations:
        message += f"My top recommendation: {recommendations[0]} "
    
    message += "Remember, this is a simulated planning tool to help you prepare financially. "
    message += "Set up real Visa controls before your move for seamless international spending."
    
    return message
