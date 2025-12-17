"""
Multi-User Collaborative Budgeting Module for EchoWorld Nexus
Enables shared mobility planning for families, partners, and groups
"""

import json
import hashlib
import time
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass, field, asdict


@dataclass
class BudgetMember:
    """Represents a member in a collaborative budget"""
    member_id: str
    name: str
    role: str
    income: float
    currency: str = "EUR"
    contribution_percent: float = 50.0
    joined_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class SharedExpense:
    """Represents a shared expense in collaborative planning"""
    expense_id: str
    category: str
    description: str
    amount: float
    currency: str
    split_type: str
    member_shares: Dict[str, float]
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict:
        return asdict(self)


@dataclass
class CollaborativeBudget:
    """Represents a collaborative mobility budget"""
    budget_id: str
    name: str
    destination_country: str
    destination_city: str
    target_move_date: str
    members: List[BudgetMember] = field(default_factory=list)
    shared_expenses: List[SharedExpense] = field(default_factory=list)
    savings_goal: float = 0.0
    current_savings: float = 0.0
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = "active"
    
    def to_dict(self) -> Dict:
        return {
            "budget_id": self.budget_id,
            "name": self.name,
            "destination_country": self.destination_country,
            "destination_city": self.destination_city,
            "target_move_date": self.target_move_date,
            "members": [m.to_dict() for m in self.members],
            "shared_expenses": [e.to_dict() for e in self.shared_expenses],
            "savings_goal": self.savings_goal,
            "current_savings": self.current_savings,
            "created_at": self.created_at,
            "status": self.status
        }


class CollaborativeBudgetManager:
    """Manages collaborative budgets for multi-user planning"""
    
    def __init__(self):
        self.budgets: Dict[str, CollaborativeBudget] = {}
        self.invites: Dict[str, Dict] = {}
    
    def create_budget(
        self,
        name: str,
        creator_name: str,
        destination_country: str,
        destination_city: str,
        target_move_date: str,
        creator_income: float,
        savings_goal: float = 0.0
    ) -> CollaborativeBudget:
        """Create a new collaborative budget"""
        
        budget_id = self._generate_id("budget")
        member_id = self._generate_id("member")
        
        creator = BudgetMember(
            member_id=member_id,
            name=creator_name,
            role="owner",
            income=creator_income,
            contribution_percent=100.0
        )
        
        budget = CollaborativeBudget(
            budget_id=budget_id,
            name=name,
            destination_country=destination_country,
            destination_city=destination_city,
            target_move_date=target_move_date,
            members=[creator],
            savings_goal=savings_goal
        )
        
        self.budgets[budget_id] = budget
        return budget
    
    def add_member(
        self,
        budget_id: str,
        name: str,
        income: float,
        role: str = "contributor"
    ) -> Optional[BudgetMember]:
        """Add a member to a collaborative budget"""
        
        if budget_id not in self.budgets:
            return None
        
        budget = self.budgets[budget_id]
        member_id = self._generate_id("member")
        
        new_member = BudgetMember(
            member_id=member_id,
            name=name,
            role=role,
            income=income,
            contribution_percent=0.0
        )
        
        budget.members.append(new_member)
        self._rebalance_contributions(budget_id)
        
        return new_member
    
    def remove_member(self, budget_id: str, member_id: str) -> bool:
        """Remove a member from collaborative budget"""
        
        if budget_id not in self.budgets:
            return False
        
        budget = self.budgets[budget_id]
        budget.members = [m for m in budget.members if m.member_id != member_id]
        self._rebalance_contributions(budget_id)
        
        return True
    
    def add_shared_expense(
        self,
        budget_id: str,
        category: str,
        description: str,
        amount: float,
        currency: str,
        split_type: str = "equal",
        custom_shares: Dict[str, float] = None,
        created_by: str = ""
    ) -> Optional[SharedExpense]:
        """Add a shared expense to the budget"""
        
        if budget_id not in self.budgets:
            return None
        
        budget = self.budgets[budget_id]
        expense_id = self._generate_id("expense")
        
        if split_type == "equal":
            num_members = len(budget.members)
            share_amount = amount / num_members if num_members > 0 else amount
            member_shares = {m.member_id: share_amount for m in budget.members}
        elif split_type == "income_based":
            total_income = sum(m.income for m in budget.members)
            if total_income > 0:
                member_shares = {
                    m.member_id: amount * (m.income / total_income) 
                    for m in budget.members
                }
            else:
                member_shares = {m.member_id: amount / len(budget.members) for m in budget.members}
        elif split_type == "custom" and custom_shares:
            member_shares = custom_shares
        else:
            member_shares = {}
        
        expense = SharedExpense(
            expense_id=expense_id,
            category=category,
            description=description,
            amount=amount,
            currency=currency,
            split_type=split_type,
            member_shares=member_shares,
            created_by=created_by
        )
        
        budget.shared_expenses.append(expense)
        return expense
    
    def get_member_summary(self, budget_id: str, member_id: str) -> Dict:
        """Get financial summary for a specific member"""
        
        if budget_id not in self.budgets:
            return {}
        
        budget = self.budgets[budget_id]
        member = next((m for m in budget.members if m.member_id == member_id), None)
        
        if not member:
            return {}
        
        total_responsibility = sum(
            e.member_shares.get(member_id, 0) 
            for e in budget.shared_expenses
        )
        
        monthly_savings = member.income - total_responsibility
        savings_rate = (monthly_savings / member.income * 100) if member.income > 0 else 0
        
        return {
            "member_name": member.name,
            "role": member.role,
            "monthly_income": member.income,
            "contribution_percent": member.contribution_percent,
            "total_expense_responsibility": total_responsibility,
            "monthly_savings": monthly_savings,
            "savings_rate": savings_rate,
            "expense_breakdown": {
                e.category: e.member_shares.get(member_id, 0)
                for e in budget.shared_expenses
            }
        }
    
    def get_budget_overview(self, budget_id: str) -> Dict:
        """Get overview of entire collaborative budget"""
        
        if budget_id not in self.budgets:
            return {}
        
        budget = self.budgets[budget_id]
        
        total_income = sum(m.income for m in budget.members)
        total_expenses = sum(e.amount for e in budget.shared_expenses)
        total_savings_potential = total_income - total_expenses
        
        progress_to_goal = (budget.current_savings / budget.savings_goal * 100) if budget.savings_goal > 0 else 0
        
        months_to_goal = 0
        if total_savings_potential > 0 and budget.savings_goal > budget.current_savings:
            remaining = budget.savings_goal - budget.current_savings
            months_to_goal = remaining / total_savings_potential
        
        return {
            "budget_name": budget.name,
            "destination": f"{budget.destination_city}, {budget.destination_country}",
            "target_move_date": budget.target_move_date,
            "num_members": len(budget.members),
            "total_combined_income": total_income,
            "total_shared_expenses": total_expenses,
            "combined_savings_potential": total_savings_potential,
            "savings_goal": budget.savings_goal,
            "current_savings": budget.current_savings,
            "progress_percent": progress_to_goal,
            "estimated_months_to_goal": months_to_goal,
            "members": [
                {"name": m.name, "role": m.role, "contribution": m.contribution_percent}
                for m in budget.members
            ],
            "expense_categories": self._get_expense_by_category(budget)
        }
    
    def update_contribution(self, budget_id: str, member_id: str, new_percent: float) -> bool:
        """Update a member's contribution percentage"""
        
        if budget_id not in self.budgets:
            return False
        
        budget = self.budgets[budget_id]
        member = next((m for m in budget.members if m.member_id == member_id), None)
        
        if not member:
            return False
        
        member.contribution_percent = new_percent
        return True
    
    def update_savings(self, budget_id: str, amount: float) -> bool:
        """Update current savings amount"""
        
        if budget_id not in self.budgets:
            return False
        
        self.budgets[budget_id].current_savings = amount
        return True
    
    def generate_invite_code(self, budget_id: str) -> str:
        """Generate invite code for sharing budget"""
        
        invite_code = self._generate_id("invite")[:8].upper()
        self.invites[invite_code] = {
            "budget_id": budget_id,
            "created_at": datetime.now().isoformat(),
            "used": False
        }
        return invite_code
    
    def join_with_invite(
        self, 
        invite_code: str, 
        name: str, 
        income: float
    ) -> Optional[Dict]:
        """Join a budget using invite code"""
        
        if invite_code not in self.invites:
            return None
        
        invite = self.invites[invite_code]
        if invite["used"]:
            return None
        
        budget_id = invite["budget_id"]
        member = self.add_member(budget_id, name, income)
        
        if member:
            invite["used"] = True
            return {
                "success": True,
                "budget_id": budget_id,
                "member": member.to_dict()
            }
        
        return None
    
    def _rebalance_contributions(self, budget_id: str):
        """Rebalance contribution percentages among members"""
        
        if budget_id not in self.budgets:
            return
        
        budget = self.budgets[budget_id]
        num_members = len(budget.members)
        
        if num_members > 0:
            equal_share = 100.0 / num_members
            for member in budget.members:
                member.contribution_percent = equal_share
    
    def _get_expense_by_category(self, budget: CollaborativeBudget) -> Dict:
        """Group expenses by category"""
        
        categories = {}
        for expense in budget.shared_expenses:
            if expense.category not in categories:
                categories[expense.category] = 0
            categories[expense.category] += expense.amount
        
        return categories
    
    def _generate_id(self, prefix: str) -> str:
        """Generate unique ID"""
        return f"{prefix}_{hashlib.sha256(str(time.time()).encode()).hexdigest()[:12]}"


_collab_manager = None

def get_collab_manager() -> CollaborativeBudgetManager:
    """Get or create singleton collaborative budget manager"""
    global _collab_manager
    if _collab_manager is None:
        _collab_manager = CollaborativeBudgetManager()
    return _collab_manager


def create_demo_collaborative_budget(country: str, city: str) -> CollaborativeBudget:
    """Create a demo collaborative budget for testing"""
    
    manager = get_collab_manager()
    
    budget = manager.create_budget(
        name=f"Move to {city} Together",
        creator_name="Partner A",
        destination_country=country,
        destination_city=city,
        target_move_date="2025-06-01",
        creator_income=4000,
        savings_goal=20000
    )
    
    manager.add_member(budget.budget_id, "Partner B", 3500)
    
    from data_module import get_cost_of_living
    col_data = get_cost_of_living(country, city)
    
    if col_data:
        manager.add_shared_expense(
            budget.budget_id,
            "Housing",
            "Shared Apartment Rent",
            col_data.get("rent_1br_city", 1200),
            col_data.get("currency", "EUR"),
            split_type="equal"
        )
        
        manager.add_shared_expense(
            budget.budget_id,
            "Utilities",
            "Shared Utilities",
            col_data.get("utilities_monthly", 200),
            col_data.get("currency", "EUR"),
            split_type="equal"
        )
        
        manager.add_shared_expense(
            budget.budget_id,
            "Groceries",
            "Shared Groceries",
            col_data.get("groceries_monthly", 350),
            col_data.get("currency", "EUR"),
            split_type="income_based"
        )
    
    return budget
