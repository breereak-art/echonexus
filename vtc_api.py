"""
Visa VTC Sandbox API Integration Module
Simulates integration with Visa Transaction Controls API for real-time testing
"""

import os
import json
import hashlib
import time
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import requests


VTC_SANDBOX_BASE_URL = "https://sandbox.api.visa.com/vtc/v1"
VTC_SANDBOX_ENABLED = (
    os.environ.get("VISA_VTC_SANDBOX_KEY") is not None and 
    os.environ.get("VISA_VTC_SANDBOX_SECRET") is not None
)


class VTCSandboxClient:
    """Client for Visa VTC Sandbox API"""
    
    def __init__(self, force_simulation: bool = False):
        self.api_key = os.environ.get("VISA_VTC_SANDBOX_KEY", "")
        self.api_secret = os.environ.get("VISA_VTC_SANDBOX_SECRET", "")
        self.sandbox_mode = force_simulation or not (self.api_key and self.api_secret)
        self.session_id = self._generate_session_id()
        self.transaction_log = []
        self.last_api_error = None
        
    def _generate_session_id(self) -> str:
        """Generate unique session ID for sandbox testing"""
        return hashlib.sha256(f"{time.time()}".encode()).hexdigest()[:16]
    
    def _make_request(self, endpoint: str, method: str = "POST", data: Dict = None) -> Dict:
        """Make request to VTC sandbox API - uses real API when credentials available"""
        
        if not self.sandbox_mode:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "X-VTC-Session": self.session_id
            }
            
            try:
                if method == "POST":
                    response = requests.post(
                        f"{VTC_SANDBOX_BASE_URL}/{endpoint}",
                        headers=headers,
                        json=data,
                        timeout=10
                    )
                else:
                    response = requests.get(
                        f"{VTC_SANDBOX_BASE_URL}/{endpoint}",
                        headers=headers,
                        timeout=10
                    )
                
                self.last_api_error = None
                
                if response.status_code >= 400:
                    error_msg = f"API Error {response.status_code}: {response.text[:200]}"
                    self.last_api_error = error_msg
                    return {
                        "success": False,
                        "error": error_msg,
                        "status_code": response.status_code,
                        "live_api": True
                    }
                
                result = response.json()
                result["live_api"] = True
                return result
                
            except requests.exceptions.Timeout:
                self.last_api_error = "Request timeout - Visa API did not respond"
                return {"error": self.last_api_error, "live_api": True, "fallback_to_simulation": True}
            except requests.exceptions.ConnectionError as e:
                self.last_api_error = f"Connection error: {str(e)}"
                return {"error": self.last_api_error, "live_api": True, "fallback_to_simulation": True}
            except Exception as e:
                self.last_api_error = f"Unexpected error: {str(e)}"
                return {"error": self.last_api_error, "live_api": True, "fallback_to_simulation": True}
        
        result = self._simulate_response(endpoint, data)
        result["simulated"] = True
        return result
    
    def _simulate_response(self, endpoint: str, data: Dict = None) -> Dict:
        """Simulate VTC API response for sandbox testing"""
        
        if endpoint == "controls/create":
            return {
                "success": True,
                "control_id": f"ctrl_{self.session_id[:8]}",
                "status": "active",
                "created_at": datetime.now().isoformat(),
                "rules": data.get("rules", {}),
                "message": "VTC control profile created successfully (Sandbox)"
            }
        
        elif endpoint == "transaction/authorize":
            amount = data.get("amount", 0)
            category = data.get("category", "other")
            location = data.get("location", "domestic")
            rules = data.get("rules", {})
            
            result = self._evaluate_transaction(amount, category, location, rules)
            return result
        
        elif endpoint == "controls/list":
            return {
                "success": True,
                "controls": [
                    {
                        "control_id": f"ctrl_{self.session_id[:8]}",
                        "type": "spending_limit",
                        "status": "active"
                    }
                ]
            }
        
        elif endpoint == "analytics/summary":
            return {
                "success": True,
                "summary": {
                    "total_transactions": len(self.transaction_log),
                    "approved": sum(1 for t in self.transaction_log if t.get("status") == "approved"),
                    "declined": sum(1 for t in self.transaction_log if t.get("status") == "declined"),
                    "total_approved_amount": sum(t.get("amount", 0) for t in self.transaction_log if t.get("status") == "approved"),
                    "total_blocked_amount": sum(t.get("amount", 0) for t in self.transaction_log if t.get("status") == "declined")
                }
            }
        
        return {"success": False, "error": "Unknown endpoint"}
    
    def _evaluate_transaction(self, amount: float, category: str, location: str, rules: Dict) -> Dict:
        """Evaluate transaction against VTC rules"""
        
        max_single = rules.get("max_single_transaction", 1000)
        max_international = rules.get("max_international", 500)
        daily_limit = rules.get("daily_limit", 2500)
        block_high_risk = rules.get("block_high_risk_merchants", True)
        
        high_risk_categories = ["gambling", "crypto", "adult"]
        
        status = "approved"
        decline_reason = None
        risk_score = 0.2
        
        if amount > max_single:
            status = "declined"
            decline_reason = f"Exceeds single transaction limit ({max_single})"
            risk_score = 0.8
        
        elif location == "international" and amount > max_international:
            status = "declined"
            decline_reason = f"Exceeds international transaction limit ({max_international})"
            risk_score = 0.7
        
        elif category.lower() in high_risk_categories and block_high_risk:
            status = "declined"
            decline_reason = "High-risk merchant category blocked"
            risk_score = 0.9
        
        transaction_record = {
            "id": f"tx_{int(time.time() * 1000)}",
            "amount": amount,
            "category": category,
            "location": location,
            "status": status,
            "decline_reason": decline_reason,
            "risk_score": risk_score,
            "timestamp": datetime.now().isoformat()
        }
        
        self.transaction_log.append(transaction_record)
        
        return {
            "success": True,
            "transaction_id": transaction_record["id"],
            "authorization_code": hashlib.md5(str(time.time()).encode()).hexdigest()[:8] if status == "approved" else None,
            "status": status,
            "decline_reason": decline_reason,
            "risk_score": risk_score,
            "response_code": "00" if status == "approved" else "05",
            "real_time_decision": True,
            "sandbox_mode": self.sandbox_mode
        }
    
    def create_control_profile(self, rules: Dict, profile_name: str = "default") -> Dict:
        """Create a VTC control profile"""
        return self._make_request("controls/create", data={
            "profile_name": profile_name,
            "rules": rules
        })
    
    def authorize_transaction(
        self, 
        amount: float, 
        category: str,
        location: str = "domestic",
        merchant_name: str = "",
        rules: Dict = None
    ) -> Dict:
        """Authorize a transaction through VTC"""
        
        if rules is None:
            rules = {
                "max_single_transaction": 1000,
                "max_international": 500,
                "daily_limit": 2500,
                "block_high_risk_merchants": True
            }
        
        return self._make_request("transaction/authorize", data={
            "amount": amount,
            "category": category,
            "location": location,
            "merchant_name": merchant_name,
            "rules": rules
        })
    
    def get_analytics(self) -> Dict:
        """Get analytics summary from sandbox"""
        return self._make_request("analytics/summary", method="GET")
    
    def get_transaction_history(self) -> List[Dict]:
        """Get transaction history from current session"""
        return self.transaction_log
    
    def reset_session(self):
        """Reset sandbox session"""
        self.session_id = self._generate_session_id()
        self.transaction_log = []


_vtc_client = None

def get_vtc_client() -> VTCSandboxClient:
    """Get or create singleton VTC client"""
    global _vtc_client
    if _vtc_client is None:
        _vtc_client = VTCSandboxClient()
    return _vtc_client


def simulate_vtc_api_batch(transactions: List[Dict], rules: Dict) -> List[Dict]:
    """Simulate batch VTC authorization for multiple transactions"""
    
    client = get_vtc_client()
    results = []
    
    for tx in transactions:
        result = client.authorize_transaction(
            amount=tx.get("amount", 0),
            category=tx.get("category", "other"),
            location=tx.get("location", "domestic"),
            merchant_name=tx.get("desc", ""),
            rules=rules
        )
        
        results.append({
            "transaction": tx,
            "vtc_response": result,
            "status": "Approved" if result.get("status") == "approved" else "Declined",
            "auth_code": result.get("authorization_code"),
            "risk_score": result.get("risk_score", 0)
        })
    
    return results


def get_vtc_api_status() -> Dict:
    """Check VTC API connection status"""
    client = get_vtc_client()
    
    if client.sandbox_mode:
        mode_message = "Simulation Mode - Add VISA_VTC_SANDBOX_KEY and VISA_VTC_SANDBOX_SECRET for live API"
    else:
        mode_message = "Live API Mode - Connected to Visa VTC Sandbox"
    
    return {
        "sandbox_mode": client.sandbox_mode,
        "api_available": True,
        "session_active": client.session_id is not None,
        "real_api_configured": VTC_SANDBOX_ENABLED,
        "last_error": client.last_api_error,
        "message": mode_message
    }
