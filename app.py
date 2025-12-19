"""
EchoWorld Nexus - AI Financial Guardian for Global Mobility
Main Streamlit Application with Advanced Features
Optimized for Hackathon Demo - Dec 2025
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import json
import numpy as np
import streamlit.components.v1 as components

from data_module import (
    get_cost_of_living, get_cities, get_countries, get_world_bank_data,
    calculate_confidence_score, get_monthly_expenses, SAMPLE_TRANSACTIONS,
    TRANSACTION_CATEGORIES, VTC_RULES, get_visa_requirements, compare_countries_cost
)
from vtc_engine import (
    simulate_vtc, calculate_vtc_summary, get_vtc_recommendations,
    generate_vtc_guardian_message
)
from vtc_api import (
    get_vtc_client, simulate_vtc_api_batch, get_vtc_api_status
)
from monte_carlo_engine import run_monte_carlo, compare_paths
from ai_guidance import generate_guardian_guidance, get_ethical_disclaimer
from tts_module import generate_audio_guidance, estimate_audio_duration
from nft_module import (
    create_mobility_passport_metadata, prepare_mint_transaction,
    get_nft_preview_card, check_web3_availability
)
from pdf_export import generate_financial_roadmap_pdf, get_pdf_filename
from rag_module import get_rag_retriever, query_cost_of_living
from collaborative import (
    get_collab_manager, create_demo_collaborative_budget
)
from voice_input import (
    get_conversation_manager, parse_financial_query,
    generate_conversational_response, check_voice_input_available
)
from visualization_3d import (
    get_visualization_for_streamlit, generate_threejs_dashboard_html
)
from dao_governance import (
    get_dao_manager, create_demo_community, prepare_mainnet_nft_mint,
    get_dao_proposal_types
)

st.set_page_config(
    page_title="EchoWorld Nexus",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0ea5e9 0%, #6366f1 50%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        padding: 0.5rem 0;
        margin-bottom: 0;
        letter-spacing: -0.02em;
    }
    
    .tagline {
        text-align: center;
        color: #cbd5e1;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 400;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }
    
    .hero-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
        border: 1px solid rgba(99, 102, 241, 0.3);
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.12), 0 0 0 1px rgba(99, 102, 241, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .hero-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #0ea5e9, #6366f1, #8b5cf6);
    }
    
    .hero-metric {
        font-size: 2.25rem;
        font-weight: 700;
        margin: 0.5rem 0;
        background: linear-gradient(135deg, #fff 0%, #e2e8f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero-label {
        font-size: 0.8rem;
        color: #94a3b8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.25rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
        margin-bottom: 0.75rem;
    }
    
    .alert-card {
        padding: 1rem 1.25rem;
        border-radius: 12px;
        margin: 0.75rem 0;
        display: flex;
        align-items: flex-start;
        gap: 0.75rem;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%);
        border: 1px solid #f87171;
        color: #fecaca;
    }
    
    .alert-danger strong {
        color: #fca5a5;
    }
    
    .alert-warning {
        background: linear-gradient(135deg, #78350f 0%, #92400e 100%);
        border: 1px solid #fbbf24;
        color: #fcd34d;
    }
    
    .alert-warning strong {
        color: #fde68a;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #064e3b 0%, #065f46 100%);
        border: 1px solid #6ee7b7;
        color: #a7f3d0;
    }
    
    .alert-success strong {
        color: #d1fae5;
    }
    
    .status-approved { color: #059669; font-weight: 600; }
    .status-declined { color: #dc2626; font-weight: 600; }
    .status-flagged { color: #d97706; font-weight: 600; }
    
    .nft-card {
        background: linear-gradient(145deg, #0f172a 0%, #1e1b4b 50%, #1e293b 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        border: 1px solid rgba(139, 92, 246, 0.4);
        box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15), 0 0 60px rgba(139, 92, 246, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .nft-card::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 100%;
        height: 100%;
        background: radial-gradient(circle, rgba(139, 92, 246, 0.1) 0%, transparent 70%);
    }
    
    .pof-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 1.5rem;
        border-radius: 16px;
        color: white;
        border: 1px solid rgba(59, 130, 246, 0.3);
    }
    
    .pof-status-ok { color: #10b981; }
    .pof-status-risk { color: #ef4444; }
    
    .ethics-badge {
        background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
        padding: 0.5rem 1rem;
        border-radius: 100px;
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        margin: 0.25rem;
        font-size: 0.8rem;
        font-weight: 500;
        color: #475569;
        border: 1px solid #e2e8f0;
    }
    
    .demo-banner {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
        padding: 0.75rem 1.25rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 600;
        box-shadow: 0 2px 8px rgba(16, 185, 129, 0.3);
    }
    
    .disclaimer {
        background: rgba(30, 41, 59, 0.5);
        padding: 1.25rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        font-size: 0.875rem;
        color: #cbd5e1;
        line-height: 1.6;
    }
    
    .chat-message {
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin: 0.75rem 0;
        line-height: 1.6;
    }
    
    .user-message {
        background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
        border: 1px solid #a5b4fc;
        text-align: right;
        margin-left: 20%;
    }
    
    .guardian-message {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-left: 4px solid #10b981;
        margin-right: 20%;
    }
    
    .step-indicator {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin-bottom: 2rem;
        padding: 1.5rem;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        border: 1px solid rgba(226, 232, 240, 0.1);
    }
    
    .step {
        text-align: center;
        opacity: 0.4;
        transition: all 0.3s ease;
        padding: 0.5rem 1.5rem;
    }
    
    .step.active {
        opacity: 1;
    }
    
    .step-number {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background: #cbd5e1;
        color: #64748b;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 1rem;
        margin-bottom: 0.5rem;
        transition: all 0.3s ease;
    }
    
    .step.active .step-number {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
    }
    
    .step p {
        margin: 0;
        font-size: 0.85rem;
        font-weight: 500;
        color: #94a3b8;
    }
    
    .step.active p {
        color: #cbd5e1;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .card-container {
        background: rgba(30, 41, 59, 0.5);
        border-radius: 16px;
        padding: 1.5rem;
        border: 1px solid rgba(226, 232, 240, 0.2);
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        margin-bottom: 1rem;
        color: #e2e8f0;
    }
    
    .gradient-text {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    .stat-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: 1rem;
    }
    
    .stat-item {
        text-align: center;
        padding: 1rem;
        background: rgba(30, 41, 59, 0.5);
        border-radius: 12px;
        border: 1px solid rgba(226, 232, 240, 0.1);
    }
    
    .stat-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: #cbd5e1;
    }
    
    .stat-label {
        font-size: 0.75rem;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.25rem;
    }
    
    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.5) 0%, rgba(30, 41, 59, 0.3) 100%);
    }
    
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button[kind="primary"]:hover {
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
        transform: translateY(-1px);
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: rgba(30, 41, 59, 0.5);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-weight: 500;
        color: #94a3b8;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(30, 41, 59, 0.8) !important;
        color: #e2e8f0 !important;
        box-shadow: 0 1px 3px rgba(99, 102, 241, 0.3);
    }
    
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #6366f1, #8b5cf6);
    }
    
    .stMetric {
        background: rgba(30, 41, 59, 0.5);
        padding: 1rem;
        border-radius: 12px;
        border: 1px solid rgba(226, 232, 240, 0.1);
        color: #e2e8f0;
    }
    
    .stExpander {
        border: 1px solid rgba(226, 232, 240, 0.2);
        border-radius: 12px;
        background: rgba(30, 41, 59, 0.5);
        color: #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

if "simulation_run" not in st.session_state:
    st.session_state.simulation_run = False
if "sim_results" not in st.session_state:
    st.session_state.sim_results = None
if "audio_generated" not in st.session_state:
    st.session_state.audio_generated = False
if "collab_budget" not in st.session_state:
    st.session_state.collab_budget = None
if "dao_community" not in st.session_state:
    st.session_state.dao_community = None
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "demo_mode" not in st.session_state:
    st.session_state.demo_mode = False
if "ppp_view" not in st.session_state:
    st.session_state.ppp_view = False


def main():
    st.markdown('<h1 class="main-header">EchoWorld Nexus</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Simulate your abroad finances securely—get audio guidance from your future self, '
        'powered by Visa controls and DeFi insights.</p>',
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        if st.button("🎯 Judge Demo Mode", type="primary", use_container_width=True):
            st.session_state.demo_mode = True
            st.session_state.simulation_run = False
            st.rerun()
        
        if st.session_state.demo_mode:
            st.markdown('<div class="demo-banner">Demo Mode Active</div>', unsafe_allow_html=True)
            if st.button("Exit Demo Mode", use_container_width=True):
                st.session_state.demo_mode = False
                st.session_state.simulation_run = False
                st.rerun()
        
        st.divider()
        st.header("Your Profile")
        
        countries = get_countries()
        default_country = "Germany"
        default_idx = countries.index(default_country) if default_country in countries else 0
        
        country = st.selectbox(
            "Destination Country",
            countries,
            index=default_idx,
            help="Select your target destination country"
        )
        
        if country:
            cities = get_cities(country)
            city = st.selectbox("Destination City", cities)
        else:
            city = None
        
        st.divider()
        
        st.subheader("Financial Information")
        
        col_data = get_cost_of_living(country, city) if country and city else None
        default_salary = col_data.get("avg_salary_tech", 4000) if col_data else 4000
        currency = col_data.get("currency", "EUR") if col_data else "EUR"
        
        if currency == "EUR":
            salary_eur = st.number_input(
                "Expected Monthly Salary (EUR)",
                min_value=1000,
                max_value=50000,
                value=int(default_salary),
                step=100,
                help="Your expected monthly salary in EUR"
            )
        else:
            local_salary = st.number_input(
                f"Expected Monthly Salary ({currency})",
                min_value=1000,
                max_value=1000000,
                value=int(default_salary),
                step=1000,
                help=f"Your expected monthly salary in {currency}"
            )
            from data_module import convert_to_eur
            salary_eur = convert_to_eur(local_salary, currency)
            st.caption(f"≈ EUR {salary_eur:,.0f}")
        
        current_savings = st.number_input(
            "Current Savings (EUR)",
            min_value=0,
            max_value=500000,
            value=5000 if not st.session_state.demo_mode else 8000,
            step=500,
            help="Your current available savings"
        )
        
        st.divider()
        
        st.subheader("VTC Profile")
        vtc_profile = st.selectbox(
            "Visa Transaction Controls",
            list(VTC_RULES.keys()),
            format_func=lambda x: f"{x.capitalize()} - {VTC_RULES[x]['description'][:30]}..."
        )
        
        st.divider()
        
        st.subheader("Upload Transactions")
        uploaded_file = st.file_uploader(
            "Upload CSV (optional)",
            type=["csv"],
            help="Upload your transaction history CSV"
        )
        
        use_sample = st.checkbox("Use sample transactions", value=True)
        
        st.divider()
        display_ethics_sidebar()
    
    if not country or not city:
        st.warning("Please select a destination country and city to begin.")
        return
    
    display_hero_dashboard(country, city, salary_eur, current_savings, vtc_profile)
    
    main_tabs = st.tabs([
        "📊 Simulate & Optimize",
        "🎙️ Voice & Guidance", 
        "🚀 Export & Advanced"
    ])
    
    with main_tabs[0]:
        display_simulation_tab(country, city, salary_eur, current_savings, vtc_profile, uploaded_file, use_sample)
    
    with main_tabs[1]:
        display_guidance_tab(country, city, salary_eur, current_savings, vtc_profile)
    
    with main_tabs[2]:
        display_advanced_tab(country, city, salary_eur, current_savings, vtc_profile)
    
    st.divider()
    st.markdown(
        '<div class="disclaimer">' + get_ethical_disclaimer() + '</div>',
        unsafe_allow_html=True
    )


def display_hero_dashboard(country, city, salary, savings, vtc_profile):
    """Display hero metrics dashboard at the top"""
    
    col_data = get_cost_of_living(country, city) if country and city else None
    wb_data = get_world_bank_data(country) if country else None
    
    if col_data and wb_data:
        confidence = calculate_confidence_score(col_data, wb_data)
        visa_fund_required = col_data.get("visa_fund_proof", 11208)
        currency = col_data.get("currency", "EUR")
        ppp_index = col_data.get("ppp_index", 1.0)
        
        if currency != "EUR":
            from data_module import convert_to_eur
            visa_fund_eur = convert_to_eur(visa_fund_required, currency)
        else:
            visa_fund_eur = visa_fund_required
        
        pof_status = savings >= visa_fund_eur
        pof_percent = min(100, (savings / visa_fund_eur) * 100) if visa_fund_eur > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="hero-card">
                <p class="hero-label">Data Confidence</p>
                <p class="hero-metric">{confidence*100:.0f}%</p>
                <p class="hero-label">Cross-Verified Sources</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            pof_icon = "✓" if pof_status else "!"
            pof_bg = "linear-gradient(135deg, #064e3b 0%, #059669 100%)" if pof_status else "linear-gradient(135deg, #7f1d1d 0%, #dc2626 100%)"
            pof_border = "rgba(16, 185, 129, 0.4)" if pof_status else "rgba(239, 68, 68, 0.4)"
            st.markdown(f"""
            <div class="hero-card" style="background: {pof_bg}; border-color: {pof_border};">
                <p class="hero-label">Proof of Funds</p>
                <p class="hero-metric">{pof_icon} {pof_percent:.0f}%</p>
                <p class="hero-label">€{savings:,.0f} / €{visa_fund_eur:,.0f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            ppp_display = salary * ppp_index if st.session_state.ppp_view else salary
            ppp_label = "PPP Adjusted" if st.session_state.ppp_view else "Nominal"
            st.markdown(f"""
            <div class="hero-card">
                <p class="hero-label">Monthly Salary ({ppp_label})</p>
                <p class="hero-metric">€{ppp_display:,.0f}</p>
                <p class="hero-label">PPP Index: {ppp_index:.2f}</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="hero-card">
                <p class="hero-label">VTC Profile</p>
                <p class="hero-metric" style="font-size: 1.75rem;">{vtc_profile.capitalize()}</p>
                <p class="hero-label">Transaction Controls</p>
            </div>
            """, unsafe_allow_html=True)
        
        col_toggle1, col_toggle2 = st.columns([1, 3])
        with col_toggle1:
            if st.button("🔄 Toggle PPP View", use_container_width=True):
                st.session_state.ppp_view = not st.session_state.ppp_view
                st.rerun()
        
        with col_toggle2:
            if st.session_state.ppp_view:
                st.info(f"💡 Purchasing Power Parity: Your €{salary:,.0f} has the buying power of €{salary * ppp_index:,.0f} in {city}")
    else:
        st.info("Select a destination to see key metrics")


def display_pof_verification(country, city, savings):
    """Display Proof of Funds verification section"""
    
    col_data = get_cost_of_living(country, city) if country and city else None
    
    if not col_data:
        return
    
    visa_fund = col_data.get("visa_fund_proof", 11208)
    currency = col_data.get("currency", "EUR")
    
    if currency != "EUR":
        from data_module import convert_to_eur
        visa_fund_eur = convert_to_eur(visa_fund, currency)
    else:
        visa_fund_eur = visa_fund
    
    pof_met = savings >= visa_fund_eur
    pof_percent = min(100, (savings / visa_fund_eur) * 100) if visa_fund_eur > 0 else 0
    shortfall = max(0, visa_fund_eur - savings)
    
    st.subheader("Proof of Funds Verification")
    
    if pof_met:
        st.markdown(f"""
        <div class="alert-card alert-success">
            <strong>✓ Proof of Funds Met!</strong><br>
            Your savings of EUR {savings:,.0f} exceed the required EUR {visa_fund_eur:,.0f} for {country} visa requirements.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="alert-card alert-danger">
            <strong>⚠ Visa Risk: Proof of Funds Not Met</strong><br>
            You need EUR {visa_fund_eur:,.0f} but have EUR {savings:,.0f}. 
            <strong>Shortfall: EUR {shortfall:,.0f}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    st.progress(pof_percent / 100)
    st.caption(f"{pof_percent:.0f}% of required proof of funds")
    
    visa_info = get_visa_requirements(country)
    if visa_info:
        with st.expander("Visa Fund Details"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Blocked Account Requirement:** EUR {visa_fund_eur:,.0f}")
                st.markdown(f"**Monthly Allowance:** EUR {visa_fund_eur/12:,.0f}")
            with col2:
                st.markdown(f"**Processing Time:** {visa_info.get('processing_time_weeks', 'N/A')} weeks")
                st.markdown(f"**Validity:** {visa_info.get('validity_months', 'N/A')} months")


def display_ethics_sidebar():
    """Display ethics badges in sidebar"""
    
    st.subheader("Ethics & Privacy")
    
    badges = [
        ("🔒", "No Data Stored"),
        ("🎭", "Audio Watermarked"),
        ("📊", "RAG Confidence Shown"),
        ("💭", "Symbolic Guidance Only")
    ]
    
    for icon, text in badges:
        st.markdown(f'<span class="ethics-badge">{icon} {text}</span>', unsafe_allow_html=True)


def display_simulation_tab(country, city, salary, savings, vtc_profile, uploaded_file, use_sample):
    """Display main simulation tab with improved flow"""
    
    step = 1 if not st.session_state.simulation_run else 2
    
    st.markdown(f"""
    <div class="step-indicator">
        <div class="step {'active' if step >= 1 else ''}">
            <span class="step-number">1</span>
            <p>Configure</p>
        </div>
        <div class="step {'active' if step >= 2 else ''}">
            <span class="step-number">2</span>
            <p>Simulate</p>
        </div>
        <div class="step {'active' if step >= 3 else ''}">
            <span class="step-number">3</span>
            <p>Optimize</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    display_pof_verification(country, city, savings)
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        button_text = "🚀 Run Financial Simulation" if not st.session_state.demo_mode else "🎯 Run Demo Simulation"
        if st.button(button_text, type="primary", use_container_width=True):
            run_simulation(
                country, city, salary, savings, 
                vtc_profile, uploaded_file, use_sample
            )
    
    with col2:
        col_data = get_cost_of_living(country, city) if country and city else None
        wb_data = get_world_bank_data(country) if country else None
        if col_data and wb_data:
            confidence = calculate_confidence_score(col_data, wb_data)
            st.metric("Data Confidence", f"{confidence*100:.0f}%", help="Cross-verified accuracy")
    
    if st.session_state.simulation_run and st.session_state.sim_results:
        display_results(country, city, salary, savings, vtc_profile)
    else:
        display_data_preview(country, city)


def display_guidance_tab(country, city, salary, savings, vtc_profile):
    """Display voice assistant and audio guidance tab"""
    
    tab1, tab2 = st.tabs(["💬 Chat Assistant", "🎙️ Audio Guidance"])
    
    with tab1:
        display_voice_assistant_section(country, city)
    
    with tab2:
        if st.session_state.simulation_run and st.session_state.sim_results:
            vtc_summary = st.session_state.sim_results.get("vtc_summary", {})
            mc_results = st.session_state.sim_results.get("mc_results", {})
            display_audio_guidance(country, city, vtc_summary, mc_results, salary, savings)
        else:
            st.info("Run a simulation first to generate personalized audio guidance")


def display_advanced_tab(country, city, salary, savings, vtc_profile):
    """Display advanced features tab"""
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 PDF Export", 
        "🎨 NFT Passport",
        "👥 Collaborative",
        "🏛️ DAO & More"
    ])
    
    with tab1:
        if st.session_state.simulation_run and st.session_state.sim_results:
            results = st.session_state.sim_results
            display_export_section(
                country, city, salary, savings,
                results["vtc_summary"], results["mc_results"],
                results["sim_feed"], results["vtc_recommendations"]
            )
        else:
            st.info("Run a simulation first to generate PDF export")
    
    with tab2:
        if st.session_state.simulation_run and st.session_state.sim_results:
            display_nft_section(
                country, city,
                st.session_state.sim_results["vtc_summary"],
                st.session_state.sim_results["mc_results"]
            )
        else:
            st.info("Run a simulation first to mint your Mobility Passport NFT")
    
    with tab3:
        display_collaborative_section(country, city)
    
    with tab4:
        display_dao_section(country, city)


def display_voice_assistant_section(country, city):
    """Display voice input and conversational assistant"""
    
    st.subheader("Chat with Your Financial Guardian")
    
    voice_status = check_voice_input_available()
    
    if voice_status.get("whisper_available"):
        st.success("Voice transcription available")
    else:
        st.caption("Text chat mode active")
    
    conversation_manager = get_conversation_manager()
    conversation_manager.set_context(country=country, city=city)
    
    for msg in st.session_state.conversation_history[-6:]:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{msg["text"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message guardian-message">{msg["text"]}</div>', unsafe_allow_html=True)
    
    st.divider()
    
    user_input = st.text_input(
        "Ask your Financial Guardian:",
        placeholder=f"e.g., What's the cost of living in {city}?",
        key="voice_text_input"
    )
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if st.button("Send Message", type="primary", use_container_width=True):
            if user_input:
                result = conversation_manager.process_text_input(user_input)
                
                st.session_state.conversation_history.append({
                    "role": "user",
                    "text": user_input
                })
                st.session_state.conversation_history.append({
                    "role": "guardian",
                    "text": result.get("response", "I couldn't process that. Please try again.")
                })
                st.rerun()
    
    with col2:
        if st.button("Clear Chat"):
            st.session_state.conversation_history = []
            conversation_manager.clear_history()
            st.rerun()
    
    st.divider()
    
    st.caption("Quick Questions:")
    quick_questions = [
        f"What's the rent in {city}?",
        f"Visa requirements for {country}?",
        "How can VTC help me?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(quick_questions):
        with cols[i]:
            if st.button(question, key=f"quick_{i}", use_container_width=True):
                result = conversation_manager.process_text_input(question)
                st.session_state.conversation_history.append({"role": "user", "text": question})
                st.session_state.conversation_history.append({"role": "guardian", "text": result.get("response", "")})
                st.rerun()


def display_collaborative_section(country, city):
    """Display collaborative budgeting (simplified)"""
    
    st.subheader("Collaborative Mobility Planning")
    st.markdown("Plan your move together with partners, family, or friends")
    
    if st.session_state.collab_budget is None:
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Load Demo Collaborative Budget", type="primary", use_container_width=True):
                budget = create_demo_collaborative_budget(country, city)
                st.session_state.collab_budget = budget
                st.success("Demo budget loaded!")
                st.rerun()
        
        with col2:
            st.info("Create shared budgets with partners moving together")
    else:
        budget = st.session_state.collab_budget
        manager = get_collab_manager()
        overview = manager.get_budget_overview(budget.budget_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Members", overview.get("num_members", 0))
        with col2:
            st.metric("Combined Income", f"EUR {overview.get('total_combined_income', 0):,.0f}")
        with col3:
            st.metric("Goal Progress", f"{overview.get('progress_percent', 0):.0f}%")
        
        if st.button("Clear Budget"):
            st.session_state.collab_budget = None
            st.rerun()


def display_dao_section(country, city):
    """Display DAO features (simplified)"""
    
    st.subheader("Decentralized Mobility Community")
    st.caption("Join or create a DAO for collective mobility planning")
    
    if st.session_state.dao_community is None:
        if st.button("Load Demo Community", type="primary"):
            community = create_demo_community(country, city)
            st.session_state.dao_community = community
            st.rerun()
    else:
        community = st.session_state.dao_community
        manager = get_dao_manager()
        stats = manager.get_community_stats(community.community_id)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Members", stats.get("total_members", 0))
        with col2:
            st.metric("Proposals", stats.get("total_proposals", 0))
        with col3:
            st.metric("Active Votes", stats.get("active_proposals", 0))
        
        if st.button("Leave Community"):
            st.session_state.dao_community = None
            st.rerun()


def get_country_iso(country_name):
    """Get ISO country code"""
    iso_map = {
        "Germany": "DEU", "Japan": "JPN", "United States": "USA",
        "United Kingdom": "GBR", "Canada": "CAN", "Australia": "AUS",
        "Netherlands": "NLD", "Singapore": "SGP", "France": "FRA",
        "Spain": "ESP", "UAE": "ARE", "Portugal": "PRT"
    }
    return iso_map.get(country_name, "")


def run_simulation(country, city, salary, savings, vtc_profile, uploaded_file, use_sample):
    """Run the full financial simulation with deterministic seed for demo"""
    
    if st.session_state.demo_mode:
        np.random.seed(42)
    
    with st.spinner("Running financial simulation..."):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            transactions = df.to_dict('records')
        elif use_sample:
            transactions = SAMPLE_TRANSACTIONS.copy()
            col_data = get_cost_of_living(country, city) if country and city else None
            if col_data:
                transactions[0]["amount"] = col_data.get("rent_1br_city", 1200)
        else:
            transactions = []
        
        sim_feed = simulate_vtc(transactions, vtc_profile)
        vtc_summary = calculate_vtc_summary(sim_feed)
        vtc_recommendations = get_vtc_recommendations(sim_feed, vtc_profile)
        
        col_data = get_cost_of_living(country, city) if country and city else None
        if col_data:
            from data_module import convert_to_eur
            currency = col_data.get("currency", "EUR")
            raw_expenses = sum([
                col_data["rent_1br_city"],
                col_data["groceries_monthly"],
                col_data["utilities_monthly"],
                col_data["transport_monthly"],
                col_data["internet_monthly"]
            ])
            if currency != "EUR":
                monthly_expenses = convert_to_eur(raw_expenses, currency)
            else:
                monthly_expenses = raw_expenses
        else:
            monthly_expenses = salary * 0.7
        
        seed = 42 if st.session_state.demo_mode else None
        mc_results = run_monte_carlo(
            base_salary=salary,
            base_expenses=monthly_expenses,
            variables={
                "upskill_boost": [0, 0.15, 0.25],
                "expense_reduction": [0, 0.1, 0.2],
                "side_income": [0, 200, 500]
            },
            num_sims=100,
            seed=seed
        )
        
        st.session_state.sim_results = {
            "sim_feed": sim_feed,
            "vtc_summary": vtc_summary,
            "vtc_recommendations": vtc_recommendations,
            "mc_results": mc_results,
            "monthly_expenses": monthly_expenses
        }
        st.session_state.simulation_run = True
        st.rerun()


def display_results(country, city, salary, savings, vtc_profile):
    """Display simulation results with improved layout"""
    
    results = st.session_state.sim_results
    vtc_summary = results["vtc_summary"]
    mc_results = results["mc_results"]
    sim_feed = results["sim_feed"]
    
    st.header("Simulation Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        approval_rate = vtc_summary.get("approval_rate", 0)
        delta_text = f"+{approval_rate - 70:.0f}%" if approval_rate >= 70 else f"{approval_rate - 70:.0f}%"
        st.metric("VTC Approval Rate", f"{approval_rate:.0f}%", delta=delta_text)
    
    with col2:
        top_path = mc_results.get("top_paths", [{}])[0]
        success_prob = top_path.get("approval_prob", 0) * 100
        st.metric("Success Probability", f"{success_prob:.0f}%", delta="Strong" if success_prob >= 75 else "Moderate")
    
    with col3:
        potential_savings = vtc_summary.get("potential_savings", 0)
        st.metric("VTC Savings", f"EUR {potential_savings:,.0f}", delta="Protected" if potential_savings > 0 else None)
    
    with col4:
        projected = top_path.get("total_savings_12m", 0)
        st.metric("12-Month Projection", f"EUR {projected:,.0f}", delta="On track" if projected >= 11208 else "Build more")
    
    declined_txs = [tx for tx in sim_feed if tx.get("status") == "Declined"]
    if declined_txs:
        st.markdown(f"""
        <div class="alert-card alert-warning">
            <strong>⚠ VTC Alert:</strong> {len(declined_txs)} transaction(s) would be declined. 
            This protects EUR {sum(tx.get('amount', 0) for tx in declined_txs):,.0f} from potential overspending.
        </div>
        """, unsafe_allow_html=True)
    
    result_tabs = st.tabs([
        "📊 Transaction Feed", 
        "🔀 Alternative Paths",
        "📈 Monte Carlo"
    ])
    
    with result_tabs[0]:
        display_echowallet_feed(sim_feed, vtc_summary, vtc_profile)
    
    with result_tabs[1]:
        display_alternative_paths(mc_results, salary, results["monthly_expenses"])
    
    with result_tabs[2]:
        display_monte_carlo_viz(mc_results)


def display_echowallet_feed(sim_feed, vtc_summary, vtc_profile):
    """Display the EchoWallet transaction feed"""
    
    st.subheader("EchoWallet: VTC Transaction Simulation")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown(f"**VTC Profile:** {vtc_profile.capitalize()}")
        st.markdown(f"**Rules Applied:** {VTC_RULES[vtc_profile]['description']}")
    
    with col2:
        approved = vtc_summary.get("approved_count", 0)
        declined = vtc_summary.get("declined_count", 0)
        st.markdown(f"**Approved:** {approved} | **Declined:** {declined}")
    
    st.divider()
    
    for tx in sim_feed[:8]:
        status_class = {
            "Approved": "status-approved",
            "Declined": "status-declined",
            "Flagged": "status-flagged"
        }.get(tx.get("status", ""), "")
        
        col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1.5])
        
        with col1:
            st.markdown(f"### {tx.get('icon', '💳')}")
        
        with col2:
            st.markdown(f"**{tx.get('tx', 'Transaction')}**")
            st.caption(f"{tx.get('category', 'other').capitalize()} | {tx.get('location', 'domestic').capitalize()}")
        
        with col3:
            st.markdown(f"### EUR {tx.get('amount', 0):,.0f}")
        
        with col4:
            st.markdown(f'<span class="{status_class}">{tx.get("status", "Pending")}</span>', unsafe_allow_html=True)
            if tx.get("vtc_action"):
                action_text = tx["vtc_action"][:50] + "..." if len(tx.get("vtc_action", "")) > 50 else tx.get("vtc_action", "")
                st.caption(action_text)


def display_alternative_paths(mc_results, salary, expenses):
    """Display Monte Carlo alternative paths"""
    
    st.subheader("Alternative Financial Paths")
    st.markdown("Based on Monte Carlo simulation with 100 scenarios:")
    
    paths = mc_results.get("top_paths", [])
    
    if not paths:
        st.warning("No paths generated. Try running the simulation again.")
        return
    
    cols = st.columns(min(3, len(paths)))
    
    for i, (col, path) in enumerate(zip(cols, paths[:3])):
        with col:
            color = ["#48bb78", "#4299e1", "#ed8936"][i] if i < 3 else "#718096"
            
            st.markdown(f"""
            <div style="background: {color}22; padding: 1.5rem; border-radius: 10px; border-left: 4px solid {color};">
                <h4 style="color: {color}; margin-bottom: 0.5rem;">{path.get('path_name', 'Path ' + str(i+1))}</h4>
                <p style="font-size: 2rem; font-weight: bold; margin: 0;">{path.get('approval_prob', 0)*100:.0f}%</p>
                <p style="color: #666; font-size: 0.9rem;">Success Probability</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown(f"**Monthly Savings:** EUR {path.get('monthly_savings', 0):,.0f}")
            st.markdown(f"**12-Month Total:** EUR {path.get('total_savings_12m', 0):,.0f}")


def display_monte_carlo_viz(mc_results):
    """Display Monte Carlo visualization"""
    
    st.subheader("Monte Carlo Distribution")
    
    outcomes = mc_results.get("all_outcomes", [])
    if outcomes:
        df = pd.DataFrame(outcomes)
        
        fig = px.scatter(
            df,
            x="salary",
            y="total_savings_12m",
            color="approval_prob",
            size="stability_score",
            color_continuous_scale="Viridis",
            labels={
                "salary": "Effective Salary (EUR)",
                "total_savings_12m": "12-Month Savings (EUR)",
                "approval_prob": "Success Prob"
            }
        )
        fig.update_layout(title="Monte Carlo Outcomes Distribution")
        st.plotly_chart(fig, use_container_width=True)
    
    stats = mc_results.get("statistics", {})
    st.markdown(f"""
    **Simulation Statistics:**
    - Simulations Run: {stats.get('total_simulations', 0)}
    - Visa Fund Success Rate: {stats.get('visa_fund_success_rate', 0):.0f}%
    - Average Success Probability: {stats.get('avg_approval_prob', 0)*100:.0f}%
    """)


def display_audio_guidance(country, city, vtc_summary, mc_results, salary, savings):
    """Display audio guidance section"""
    
    st.subheader("Audio Guidance from Your Financial Guardian")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; text-align: center;">
        <h3 style="margin-bottom: 0.5rem;">📞 Incoming Call...</h3>
        <p>From: Your Financial Guardian ({country}, Ahead)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if st.button("Generate Audio Guidance", type="primary", use_container_width=True):
        with st.spinner("Generating personalized guidance..."):
            try:
                guidance_text = generate_guardian_guidance(
                    country=country,
                    city=city,
                    vtc_summary=vtc_summary,
                    monte_carlo_results=mc_results,
                    user_salary=salary,
                    user_savings=savings,
                    use_ai=True
                )
                
                audio_bytes = generate_audio_guidance(guidance_text, include_watermark=True)
                
                if audio_bytes:
                    st.session_state.guidance_audio = audio_bytes
                    st.session_state.guidance_text = guidance_text
                    st.session_state.audio_generated = True
                    st.rerun()
                else:
                    st.warning("Audio generation unavailable. Displaying text guidance:")
                    st.info(guidance_text)
            except Exception as e:
                st.error(f"Guidance generation failed. Using fallback text mode.")
                fallback_text = f"Welcome to {city}, {country}. Based on your profile, your success probability is strong. Consider the VTC recommendations to optimize your spending."
                st.info(fallback_text)
    
    if st.session_state.get("audio_generated") and st.session_state.get("guidance_audio"):
        st.audio(st.session_state.guidance_audio, format="audio/mp3")
        
        duration = estimate_audio_duration(st.session_state.get("guidance_text", ""))
        st.caption(f"Estimated duration: {duration:.0f} seconds")
        
        with st.expander("View Guidance Transcript"):
            st.markdown(st.session_state.get("guidance_text", ""))
    
    st.divider()
    
    st.markdown("""
    <div class="disclaimer">
        <strong>Ethics Notice:</strong> This audio guidance is generated by AI for planning purposes only. 
        It includes a watermark identifying it as a simulated tool. No personal data is stored.
    </div>
    """, unsafe_allow_html=True)


def display_nft_section(country, city, vtc_summary, mc_results):
    """Display NFT minting section"""
    
    st.subheader("Mobility Passport NFT")
    
    st.markdown("""
    Mint a testnet NFT summarizing your financial readiness. 
    This NFT serves as a verifiable credential of your simulation results.
    """)
    
    top_path = mc_results.get("top_paths", [{}])[0]
    success_prob = top_path.get("approval_prob", 0.75)
    
    metadata = create_mobility_passport_metadata(
        user_id="anon_user",
        country=country,
        city=city,
        success_probability=success_prob,
        vtc_optimized=True,
        approval_rate=vtc_summary.get("approval_rate", 75),
        projected_savings=top_path.get("total_savings_12m", 0),
        best_path=top_path.get("path_name", "Balanced Growth")
    )
    
    preview = get_nft_preview_card(metadata)
    
    tier_colors = {
        "Gold": "#ffd700",
        "Silver": "#c0c0c0",
        "Bronze": "#cd7f32",
        "Starter": "#718096"
    }
    tier_color = tier_colors.get(preview["tier"], "#718096")
    
    st.markdown(f"""
    <div class="nft-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h3 style="margin: 0;">Mobility Passport - {preview["title"]}</h3>
            <span style="background: {tier_color}; padding: 0.25rem 0.75rem; border-radius: 20px; 
                         font-weight: bold; color: #1a365d;">{preview["tier"]}</span>
        </div>
        <p style="color: #a0aec0; margin: 0.5rem 0;">{preview["tier_description"]}</p>
        <hr style="border-color: #4a5568;">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
            <div>
                <p style="color: #a0aec0; margin: 0; font-size: 0.8rem;">Destination</p>
                <p style="margin: 0; font-size: 1.2rem;">{preview["city"]}, {preview["country"]}</p>
            </div>
            <div>
                <p style="color: #a0aec0; margin: 0; font-size: 0.8rem;">Success Rate</p>
                <p style="margin: 0; font-size: 1.2rem;">{preview["success_prob"]}</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    web3_status = check_web3_availability()
    if web3_status.get("connected"):
        st.success("Connected to Polygon Amoy Testnet")
    else:
        st.info("Preview Mode - Connect wallet to mint")
    
    wallet_address = st.text_input(
        "Wallet Address (optional)",
        placeholder="0x...",
        help="Enter your Ethereum wallet address for testnet minting"
    )
    
    if st.button("Prepare NFT Mint", type="primary", use_container_width=True):
        if wallet_address and wallet_address.startswith("0x"):
            tx_data = prepare_mint_transaction(wallet_address, metadata)
            st.success("NFT Mint Prepared!")
            with st.expander("NFT Metadata (JSON)"):
                st.json(metadata)
        else:
            st.warning("Enter a valid wallet address (starting with 0x) or view preview below")
            with st.expander("Preview NFT Metadata"):
                st.json(metadata)


def display_export_section(country, city, salary, savings, vtc_summary, mc_results, sim_feed, recommendations):
    """Display PDF export section"""
    
    st.subheader("Export Financial Roadmap")
    
    st.markdown("""
    Download a comprehensive PDF report of your financial simulation results including:
    - Executive summary with key metrics
    - VTC simulation breakdown  
    - Alternative path analysis
    - Personalized recommendations
    """)
    
    if st.button("Generate PDF Report", type="primary", use_container_width=True):
        with st.spinner("Generating PDF..."):
            try:
                pdf_bytes = generate_financial_roadmap_pdf(
                    country=country,
                    city=city,
                    user_salary=salary,
                    user_savings=savings,
                    vtc_summary=vtc_summary,
                    monte_carlo_results=mc_results,
                    sim_feed=sim_feed,
                    recommendations=recommendations
                )
                
                filename = get_pdf_filename(country, city)
                
                st.download_button(
                    label="📥 Download PDF Roadmap",
                    data=pdf_bytes,
                    file_name=filename,
                    mime="application/pdf",
                    type="secondary",
                    use_container_width=True
                )
                
                st.success(f"PDF generated: {filename}")
            except Exception as e:
                st.error("PDF generation failed. Please try again.")


def display_data_preview(country, city):
    """Display data preview before simulation with RAG-powered insights"""
    
    st.header("Data Preview")
    
    rag = get_rag_retriever()
    rag_status = rag.get_status()
    
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        if rag_status.get("initialized"):
            if rag_status.get("fallback_mode"):
                st.info(f"RAG System: Keyword Mode ({rag_status.get('num_documents', 0)} docs indexed)")
            else:
                st.success(f"RAG System: Vector Search Active ({rag_status.get('num_documents', 0)} docs)")
        else:
            st.warning("RAG System: Initializing...")
    
    with col2:
        st.caption("Data Sources: Numbeo + World Bank (Cross-Verified)")
    
    with col3:
        st.caption(f"Vector Store: {rag_status.get('vector_store_type', 'N/A')}")
    
    st.divider()
    
    visa_info = get_visa_requirements(country)
    if visa_info:
        with st.expander("Visa Requirements", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Visa Types:** {', '.join(visa_info.get('visa_types', []))}")
                st.markdown(f"**Processing Time:** {visa_info.get('processing_time_weeks', 'N/A')} weeks")
            with col2:
                st.markdown(f"**Blocked Account:** {visa_info.get('blocked_account', 0):,}")
                st.markdown(f"**Health Insurance:** {'Required' if visa_info.get('health_insurance_required') else 'Optional'}")
    
    st.divider()
    
    col_data = get_cost_of_living(country, city) if country and city else None
    wb_data = get_world_bank_data(country) if country else None
    
    if not col_data or not wb_data:
        st.warning("Data not available for selected location")
        return
    
    confidence = calculate_confidence_score(col_data, wb_data)
    currency = col_data.get("currency", "EUR")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Cost of Living: {city}")
        
        expenses = {
            "Rent (1BR City Center)": col_data.get("rent_1br_city", 0),
            "Groceries": col_data.get("groceries_monthly", 0),
            "Utilities": col_data.get("utilities_monthly", 0),
            "Transport": col_data.get("transport_monthly", 0),
            "Internet": col_data.get("internet_monthly", 0),
        }
        
        df = pd.DataFrame([
            {"Category": k, "Amount": v} for k, v in expenses.items()
        ])
        
        fig = px.pie(
            df, 
            values="Amount", 
            names="Category",
            title=f"Monthly Expenses ({currency})"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader(f"Economic Indicators: {country}")
        
        st.metric("GDP per Capita", f"${wb_data.get('gdp_per_capita', 0):,.0f}")
        st.metric("Inflation Rate", f"{wb_data.get('inflation_rate', 0):.1f}%")
        st.metric("Unemployment", f"{wb_data.get('unemployment_rate', 0):.1f}%")
        
        st.caption(f"Data Confidence: {confidence*100:.0f}% (Cross-verified)")


if __name__ == "__main__":
    main()
