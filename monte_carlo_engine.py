"""
Monte Carlo Alternative Paths Engine
Simulates financial outcomes with different variables
"""

import numpy as np
from typing import Dict, List, Any


def run_monte_carlo(
    base_salary: float = 2000,
    base_expenses: float = 1500,
    variables: Dict[str, List[float]] = None,
    num_sims: int = 100,
    months: int = 12
) -> Dict[str, Any]:
    """
    Run Monte Carlo simulation for financial outcomes
    
    Args:
        base_salary: Starting monthly salary
        base_expenses: Starting monthly expenses
        variables: Dict of variable names to possible values/boosts
        num_sims: Number of simulations to run
        months: Number of months to simulate
        
    Returns:
        Dict with top paths, statistics, and recommendations
    """
    
    if variables is None:
        variables = {
            "upskill_boost": [0, 0.15, 0.25],
            "expense_reduction": [0, 0.1, 0.2],
            "side_income": [0, 200, 500]
        }
    
    outcomes = []
    
    for sim in range(num_sims):
        upskill = np.random.choice(variables.get("upskill_boost", [0, 0.2]))
        expense_cut = np.random.choice(variables.get("expense_reduction", [0, 0.1]))
        side_income = np.random.choice(variables.get("side_income", [0, 200]))
        
        effective_salary = base_salary * (1 + upskill) + side_income
        effective_expenses = base_expenses * (1 - expense_cut)
        
        monthly_savings = effective_salary - effective_expenses
        total_savings = monthly_savings * months
        
        approval_prob = calculate_approval_probability(
            effective_salary, 
            effective_expenses, 
            total_savings
        )
        
        visa_fund_met = total_savings >= 11208
        
        stability_score = calculate_stability_score(
            effective_salary, 
            effective_expenses, 
            monthly_savings
        )
        
        outcomes.append({
            "salary": effective_salary,
            "expenses": effective_expenses,
            "monthly_savings": monthly_savings,
            "total_savings_12m": total_savings,
            "approval_prob": approval_prob,
            "visa_fund_met": visa_fund_met,
            "stability_score": stability_score,
            "upskill_applied": upskill > 0,
            "upskill_boost": upskill,
            "expense_cut": expense_cut,
            "side_income": side_income
        })
    
    sorted_outcomes = sorted(outcomes, key=lambda x: x["approval_prob"], reverse=True)
    
    top_paths = get_distinct_top_paths(sorted_outcomes, n=3)
    
    stats = calculate_simulation_stats(outcomes)
    
    return {
        "top_paths": top_paths,
        "all_outcomes": outcomes,
        "statistics": stats,
        "base_scenario": {
            "salary": base_salary,
            "expenses": base_expenses,
            "monthly_savings": base_salary - base_expenses,
            "approval_prob": calculate_approval_probability(
                base_salary, base_expenses, (base_salary - base_expenses) * months
            )
        }
    }


def calculate_approval_probability(salary: float, expenses: float, savings: float) -> float:
    """Calculate probability of financial success/approval"""
    
    ratio = salary / expenses if expenses > 0 else 2
    
    base_prob = min(0.5 + (ratio - 1) * 0.25, 0.75)
    
    if savings >= 15000:
        base_prob += 0.15
    elif savings >= 11208:
        base_prob += 0.10
    elif savings >= 5000:
        base_prob += 0.05
    
    if ratio >= 1.5:
        base_prob += 0.05
    
    return min(0.98, max(0.1, base_prob))


def calculate_stability_score(salary: float, expenses: float, monthly_savings: float) -> float:
    """Calculate financial stability score (0-100)"""
    
    score = 50
    
    ratio = salary / expenses if expenses > 0 else 2
    score += min(20, (ratio - 1) * 20)
    
    savings_rate = monthly_savings / salary if salary > 0 else 0
    score += min(20, savings_rate * 100)
    
    if monthly_savings >= 500:
        score += 10
    
    return min(100, max(0, score))


def get_distinct_top_paths(outcomes: List[Dict], n: int = 3) -> List[Dict]:
    """Get top N distinct paths (avoid near-duplicates)"""
    
    distinct_paths = []
    
    for outcome in outcomes:
        is_distinct = True
        for existing in distinct_paths:
            salary_diff = abs(outcome["salary"] - existing["salary"])
            if salary_diff < 200:
                is_distinct = False
                break
        
        if is_distinct:
            path = outcome.copy()
            path["path_name"] = generate_path_name(outcome)
            path["path_description"] = generate_path_description(outcome)
            distinct_paths.append(path)
            
            if len(distinct_paths) >= n:
                break
    
    return distinct_paths


def generate_path_name(outcome: Dict) -> str:
    """Generate a descriptive name for a path"""
    
    if outcome["upskill_boost"] >= 0.2:
        return "Career Accelerator Path"
    elif outcome["expense_cut"] >= 0.15:
        return "Frugal Pioneer Path"
    elif outcome["side_income"] >= 400:
        return "Hustle Builder Path"
    elif outcome["upskill_boost"] > 0 and outcome["expense_cut"] > 0:
        return "Balanced Growth Path"
    else:
        return "Steady Progress Path"


def generate_path_description(outcome: Dict) -> str:
    """Generate a description for a path"""
    
    parts = []
    
    if outcome["upskill_boost"] >= 0.15:
        parts.append(f"+{outcome['upskill_boost']*100:.0f}% salary through upskilling")
    
    if outcome["expense_cut"] >= 0.1:
        parts.append(f"{outcome['expense_cut']*100:.0f}% expense reduction")
    
    if outcome["side_income"] > 0:
        parts.append(f"€{outcome['side_income']:.0f} side income")
    
    if not parts:
        parts.append("Current trajectory maintained")
    
    return " + ".join(parts)


def calculate_simulation_stats(outcomes: List[Dict]) -> Dict[str, Any]:
    """Calculate aggregate statistics from all simulations"""
    
    salaries = [o["salary"] for o in outcomes]
    savings = [o["total_savings_12m"] for o in outcomes]
    probs = [o["approval_prob"] for o in outcomes]
    
    visa_met_count = sum(1 for o in outcomes if o["visa_fund_met"])
    
    return {
        "avg_salary": np.mean(salaries),
        "max_salary": np.max(salaries),
        "min_salary": np.min(salaries),
        "avg_savings": np.mean(savings),
        "max_savings": np.max(savings),
        "min_savings": np.min(savings),
        "avg_approval_prob": np.mean(probs),
        "max_approval_prob": np.max(probs),
        "visa_fund_success_rate": (visa_met_count / len(outcomes)) * 100,
        "total_simulations": len(outcomes)
    }


def compare_paths(paths: List[Dict]) -> str:
    """Generate comparison text between paths"""
    
    if len(paths) < 2:
        return "Single path analyzed."
    
    best = paths[0]
    comparison = f"The {best['path_name']} offers the highest success probability at {best['approval_prob']*100:.0f}%. "
    
    if len(paths) >= 2:
        second = paths[1]
        diff = (best["approval_prob"] - second["approval_prob"]) * 100
        savings_diff = best["total_savings_12m"] - second["total_savings_12m"]
        
        comparison += f"Compared to {second['path_name']}, it provides {diff:.0f}% better approval odds "
        comparison += f"and €{abs(savings_diff):.0f} {'more' if savings_diff > 0 else 'less'} in annual savings."
    
    return comparison
