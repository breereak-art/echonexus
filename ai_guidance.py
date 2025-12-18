"""
AI Guidance Module for EchoWorld Nexus
Generates personalized financial guidance using OpenAI with RAG-grounded data
"""

import os
import json
from typing import Dict, Any, List

from rag_module import get_rag_context_for_guidance, get_rag_retriever


def get_openai_client():
    """Get OpenAI client if API key is available"""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return None
    
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception:
        return None


def generate_guardian_guidance(
    country: str,
    city: str,
    vtc_summary: Dict[str, Any],
    monte_carlo_results: Dict[str, Any],
    user_salary: float,
    user_savings: float,
    use_ai: bool = True
) -> str:
    """
    Generate comprehensive financial guidance
    
    Args:
        country: Destination country
        city: Destination city
        vtc_summary: VTC simulation summary
        monte_carlo_results: Monte Carlo analysis results
        user_salary: User's current/expected salary
        user_savings: User's current savings
        use_ai: Whether to use OpenAI for enhanced guidance
        
    Returns:
        Guidance text for TTS
    """
    
    client = get_openai_client() if use_ai else None
    
    if client:
        return generate_ai_guidance(
            client, country, city, vtc_summary, 
            monte_carlo_results, user_salary, user_savings
        )
    else:
        return generate_template_guidance(
            country, city, vtc_summary, 
            monte_carlo_results, user_salary, user_savings
        )


def generate_ai_guidance(
    client,
    country: str,
    city: str,
    vtc_summary: Dict[str, Any],
    monte_carlo_results: Dict[str, Any],
    user_salary: float,
    user_savings: float
) -> str:
    """Generate guidance using OpenAI with RAG-grounded context"""
    
    top_path = monte_carlo_results["top_paths"][0] if monte_carlo_results.get("top_paths") else None
    
    rag_context = get_rag_context_for_guidance(country, city)
    
    # the newest OpenAI model is "gpt-5" which was released August 7, 2025.
    # do not change this unless explicitly requested by the user
    context = f"""
    You are a Financial Guardian - a friendly, supportive AI advisor helping someone plan their move to {city}, {country}.
    
    IMPORTANT: Use the following RAG-retrieved, cross-verified data to ground your advice:
    
    {rag_context}
    
    User Financial Profile:
    - Expected Salary: €{user_salary:,.0f}/month
    - Current Savings: €{user_savings:,.0f}
    
    VTC Simulation Results:
    - Approval Rate: {vtc_summary.get('approval_rate', 0):.0f}%
    - Transactions Blocked: {vtc_summary.get('declined_count', 0)}
    - Potential Savings from VTC: €{vtc_summary.get('potential_savings', 0):,.0f}
    
    Best Financial Path Found:
    - Path Name: {top_path.get('path_name', 'Unknown') if top_path is not None else 'N/A'}
    - Success Probability: {(top_path.get('approval_prob', 0)*100) if top_path is not None else 0:.0f}%
    - Projected 12-month Savings: €{(top_path.get('total_savings_12m', 0) if top_path is not None else 0):,.0f}
    
    Generate a warm, encouraging 60-second audio guidance script (about 150 words) that:
    1. Greets them as their "Financial Guardian from {country}"
    2. Summarizes their financial readiness using SPECIFIC numbers from the RAG data
    3. Explains how VTC can protect their budget
    4. Recommends their best path forward with data-backed reasoning
    5. Ends with an encouraging message
    
    Keep it conversational and supportive. Reference specific costs from the data (like rent, visa requirements).
    This is for text-to-speech, so write naturally.
    End with: "Remember, this is a simulated planning tool to help you prepare."
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-5",
            messages=[
                {"role": "system", "content": "You are a warm, supportive financial advisor helping people plan international moves. Always ground your advice in the specific data provided."},
                {"role": "user", "content": context}
            ],
            max_completion_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return generate_template_guidance(
            country, city, vtc_summary, 
            monte_carlo_results, user_salary, user_savings
        )


def generate_template_guidance(
    country: str,
    city: str,
    vtc_summary: Dict[str, Any],
    monte_carlo_results: Dict[str, Any],
    user_salary: float,
    user_savings: float
) -> str:
    """Generate guidance using templates when AI is unavailable"""
    
    approval_rate = vtc_summary.get("approval_rate", 75)
    declined = vtc_summary.get("declined_count", 0)
    savings = vtc_summary.get("potential_savings", 0)
    
    top_path = monte_carlo_results.get("top_paths", [{}])[0] if monte_carlo_results else {}
    path_name = top_path.get("path_name", "Balanced Growth Path")
    success_prob = top_path.get("approval_prob", 0.75) * 100
    projected_savings = top_path.get("total_savings_12m", user_salary * 3)
    
    guidance = f"""
Hello, this is your Financial Guardian calling from {city}, {country}. 
I've been analyzing your financial simulation, and I'm here to share some insights about your upcoming move.

Based on your expected salary of {user_salary:,.0f} euros per month and current savings of {user_savings:,.0f} euros, 
here's what I found:

Your Visa Transaction Controls simulation shows a {approval_rate:.0f} percent approval rate. 
"""

    if declined > 0:
        guidance += f"""
I identified {declined} transactions that would be blocked by VTC settings, 
potentially saving you {savings:,.0f} euros that can go toward your visa fund proof.
"""
    else:
        guidance += """
All your planned transactions align well with the VTC settings - you're spending wisely!
"""

    guidance += f"""
Looking at your alternative paths, I recommend the "{path_name}" approach. 
This gives you a {success_prob:.0f} percent probability of financial success, 
with projected 12-month savings of {projected_savings:,.0f} euros.
"""

    if success_prob >= 80:
        guidance += """
You're in excellent shape for this move! Keep following this path and you'll thrive abroad.
"""
    elif success_prob >= 60:
        guidance += """
You're on a solid foundation. Consider the upskilling boost to increase your success rate even further.
"""
    else:
        guidance += """
I'd suggest building up a bit more savings or considering expense reductions before the move.
"""

    guidance += """
Remember, this is a simulated planning tool to help you prepare financially. 
Set up real Visa controls and consult with financial advisors before your move.
I believe in your journey. Good luck with your global mobility adventure!
"""
    
    return guidance.strip()


def generate_quick_insight(
    metric_name: str,
    metric_value: float,
    context: str = "general"
) -> str:
    """Generate a quick one-liner insight for a metric"""
    
    insights = {
        "approval_rate": {
            "high": f"Excellent! {metric_value:.0f}% approval rate means your spending is well-controlled.",
            "medium": f"Good progress - {metric_value:.0f}% approval rate. Minor adjustments can boost this.",
            "low": f"Heads up - {metric_value:.0f}% approval rate suggests tighter VTC settings might help."
        },
        "savings_rate": {
            "high": f"Impressive {metric_value:.0f}% savings rate! You're building a strong safety net.",
            "medium": f"Solid {metric_value:.0f}% savings rate. Room to grow with small lifestyle tweaks.",
            "low": f"At {metric_value:.0f}% savings, consider reducing non-essential expenses."
        },
        "success_prob": {
            "high": f"{metric_value:.0f}% success probability - you're set for a smooth transition!",
            "medium": f"{metric_value:.0f}% success rate is promising. Small optimizations can help.",
            "low": f"At {metric_value:.0f}% probability, consider delaying or adjusting your plan."
        }
    }
    
    if metric_value >= 80:
        level = "high"
    elif metric_value >= 50:
        level = "medium"
    else:
        level = "low"
    
    return insights.get(metric_name, {}).get(level, f"{metric_name}: {metric_value:.0f}%")


def get_ethical_disclaimer() -> str:
    """Return the ethical disclaimer for audio watermarking"""
    return (
        "This is a simulated financial planning tool. "
        "All projections are estimates based on provided data. "
        "Consult qualified financial advisors for actual decisions. "
        "No personal data is stored."
    )
