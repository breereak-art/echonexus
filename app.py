"""
EchoWorld Nexus - AI Financial Guardian for Global Mobility
Main Streamlit Application with Advanced Features
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import json
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
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem 0;
    }
    .tagline {
        text-align: center;
        color: #666;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .status-approved {
        color: #48bb78;
        font-weight: bold;
    }
    .status-declined {
        color: #f56565;
        font-weight: bold;
    }
    .status-flagged {
        color: #ed8936;
        font-weight: bold;
    }
    .nft-card {
        background: linear-gradient(135deg, #1a365d 0%, #2d3748 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        border: 2px solid #4fd1c5;
    }
    .disclaimer {
        background-color: #f7fafc;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #4299e1;
        font-size: 0.85rem;
        color: #4a5568;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
    }
    .user-message {
        background-color: #e2e8f0;
        text-align: right;
    }
    .guardian-message {
        background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
        border-left: 4px solid #667eea;
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


def main():
    st.markdown('<h1 class="main-header">EchoWorld Nexus</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Simulate your abroad finances securely—get audio guidance from your future self, '
        'powered by Visa controls and DeFi insights. Now supporting 12+ countries!</p>',
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.header("Your Profile")
        
        countries = get_countries()
        country = st.selectbox(
            "Destination Country",
            countries,
            help="Select your target destination country"
        )
        
        cities = get_cities(country)
        city = st.selectbox("Destination City", cities)
        
        st.divider()
        
        st.subheader("Financial Information")
        
        col_data = get_cost_of_living(country, city)
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
            value=5000,
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
    
    main_tabs = st.tabs([
        "Financial Simulation",
        "VTC Sandbox API",
        "Collaborative Planning",
        "Voice Assistant",
        "3D Visualization",
        "DAO Governance"
    ])
    
    with main_tabs[0]:
        display_simulation_tab(country, city, salary_eur, current_savings, vtc_profile, uploaded_file, use_sample)
    
    with main_tabs[1]:
        display_vtc_api_tab(vtc_profile)
    
    with main_tabs[2]:
        display_collaborative_tab(country, city)
    
    with main_tabs[3]:
        display_voice_assistant_tab(country, city)
    
    with main_tabs[4]:
        display_3d_visualization_tab(country, city)
    
    with main_tabs[5]:
        display_dao_governance_tab(country, city)
    
    st.divider()
    st.markdown(
        '<div class="disclaimer">' + get_ethical_disclaimer() + '</div>',
        unsafe_allow_html=True
    )


def display_simulation_tab(country, city, salary, savings, vtc_profile, uploaded_file, use_sample):
    """Display main financial simulation tab"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Run Financial Simulation", type="primary", use_container_width=True):
            run_simulation(
                country, city, salary, savings, 
                vtc_profile, uploaded_file, use_sample
            )
    
    with col2:
        col_data = get_cost_of_living(country, city)
        wb_data = get_world_bank_data(country)
        if col_data and wb_data:
            confidence = calculate_confidence_score(col_data, wb_data)
            st.metric("Data Confidence", f"{confidence*100:.0f}%", help="Cross-verified accuracy")
    
    if st.session_state.simulation_run and st.session_state.sim_results:
        display_results(country, city, salary, savings, vtc_profile)
    else:
        display_data_preview(country, city)


def display_vtc_api_tab(vtc_profile):
    """Display VTC Sandbox API testing tab"""
    
    st.header("Visa VTC Sandbox API")
    st.markdown("Test real-time transaction control with the Visa VTC Sandbox API")
    
    api_status = get_vtc_api_status()
    
    if api_status.get("sandbox_mode"):
        st.info(api_status.get("message", "Simulation mode active"))
    else:
        st.success(api_status.get("message", "Live API connected"))
    
    if api_status.get("last_error"):
        st.error(f"Last API Error: {api_status['last_error']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("API Status", "Connected" if api_status["api_available"] else "Offline")
    with col2:
        mode_label = "Simulation" if api_status["sandbox_mode"] else "Live Sandbox"
        st.metric("Mode", mode_label)
    with col3:
        st.metric("Session", "Active" if api_status["session_active"] else "Inactive")
    
    st.divider()
    
    st.subheader("Test Transaction")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        tx_amount = st.number_input("Amount (EUR)", min_value=1, max_value=10000, value=500)
    
    with col2:
        tx_category = st.selectbox("Category", list(TRANSACTION_CATEGORIES.keys()))
    
    with col3:
        tx_location = st.selectbox("Location", ["domestic", "international"])
    
    merchant_name = st.text_input("Merchant Name", value="Test Merchant")
    
    if st.button("Submit to VTC API", type="primary"):
        client = get_vtc_client()
        rules = VTC_RULES.get(vtc_profile, VTC_RULES["standard"])
        
        result = client.authorize_transaction(
            amount=tx_amount,
            category=tx_category,
            location=tx_location,
            merchant_name=merchant_name,
            rules=rules
        )
        
        if result.get("status") == "approved":
            st.success(f"Transaction APPROVED - Auth Code: {result.get('authorization_code')}")
        else:
            st.error(f"Transaction DECLINED - Reason: {result.get('decline_reason')}")
        
        st.json(result)
    
    st.divider()
    
    st.subheader("Transaction History")
    client = get_vtc_client()
    history = client.get_transaction_history()
    
    if history:
        df = pd.DataFrame(history)
        st.dataframe(df, use_container_width=True)
        
        analytics = client.get_analytics()
        if analytics.get("success"):
            summary = analytics.get("summary", {})
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Transactions", summary.get("total_transactions", 0))
            with col2:
                st.metric("Approved", summary.get("approved", 0))
            with col3:
                st.metric("Declined", summary.get("declined", 0))
            with col4:
                st.metric("Total Blocked", f"EUR {summary.get('total_blocked_amount', 0):,.0f}")
    else:
        st.info("No transactions yet. Submit a test transaction above.")
    
    if st.button("Reset Session"):
        client.reset_session()
        st.success("Session reset successfully")
        st.rerun()


def display_collaborative_tab(country, city):
    """Display collaborative budgeting features"""
    
    st.header("Collaborative Mobility Planning")
    st.markdown("Plan your move together with partners, family, or friends")
    
    if st.session_state.collab_budget is None:
        st.subheader("Create a Shared Budget")
        
        col1, col2 = st.columns(2)
        
        with col1:
            budget_name = st.text_input("Budget Name", value=f"Move to {city} Together")
            creator_name = st.text_input("Your Name", value="Partner A")
            creator_income = st.number_input("Your Monthly Income (EUR)", min_value=1000, max_value=50000, value=4000)
        
        with col2:
            target_date = st.date_input("Target Move Date")
            savings_goal = st.number_input("Savings Goal (EUR)", min_value=5000, max_value=100000, value=20000)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Create Budget", type="primary"):
                manager = get_collab_manager()
                budget = manager.create_budget(
                    name=budget_name,
                    creator_name=creator_name,
                    destination_country=country,
                    destination_city=city,
                    target_move_date=str(target_date),
                    creator_income=creator_income,
                    savings_goal=savings_goal
                )
                st.session_state.collab_budget = budget
                st.success("Collaborative budget created!")
                st.rerun()
        
        with col2:
            if st.button("Load Demo Budget"):
                budget = create_demo_collaborative_budget(country, city)
                st.session_state.collab_budget = budget
                st.success("Demo budget loaded!")
                st.rerun()
    
    else:
        budget = st.session_state.collab_budget
        manager = get_collab_manager()
        
        overview = manager.get_budget_overview(budget.budget_id)
        
        st.subheader(f"Budget: {overview.get('budget_name', 'N/A')}")
        st.markdown(f"**Destination:** {overview.get('destination', 'N/A')} | **Target Date:** {overview.get('target_move_date', 'N/A')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Members", overview.get("num_members", 0))
        with col2:
            st.metric("Combined Income", f"EUR {overview.get('total_combined_income', 0):,.0f}")
        with col3:
            st.metric("Total Expenses", f"EUR {overview.get('total_shared_expenses', 0):,.0f}")
        with col4:
            progress = overview.get("progress_percent", 0)
            st.metric("Goal Progress", f"{progress:.0f}%")
        
        st.divider()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Members")
            for member in overview.get("members", []):
                st.markdown(f"**{member['name']}** ({member['role']}) - {member['contribution']:.0f}% contribution")
            
            st.markdown("---")
            st.markdown("**Add New Member**")
            new_name = st.text_input("Name", key="new_member_name")
            new_income = st.number_input("Income (EUR)", min_value=1000, value=3500, key="new_member_income")
            if st.button("Add Member"):
                manager.add_member(budget.budget_id, new_name, new_income)
                st.success(f"Added {new_name} to the budget")
                st.rerun()
        
        with col2:
            st.subheader("Shared Expenses")
            categories = overview.get("expense_categories", {})
            if categories:
                df = pd.DataFrame([
                    {"Category": k, "Amount": v} for k, v in categories.items()
                ])
                fig = px.pie(df, values="Amount", names="Category", title="Expense Distribution")
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("**Add Shared Expense**")
            exp_category = st.selectbox("Category", ["Housing", "Utilities", "Groceries", "Transport", "Other"])
            exp_desc = st.text_input("Description", key="exp_desc")
            exp_amount = st.number_input("Amount (EUR)", min_value=10, value=500, key="exp_amount")
            exp_split = st.selectbox("Split Type", ["equal", "income_based", "custom"])
            
            if st.button("Add Expense"):
                manager.add_shared_expense(
                    budget.budget_id,
                    exp_category,
                    exp_desc,
                    exp_amount,
                    "EUR",
                    exp_split
                )
                st.success(f"Added {exp_desc} expense")
                st.rerun()
        
        st.divider()
        
        invite_code = manager.generate_invite_code(budget.budget_id)
        st.info(f"Share this invite code with your partners: **{invite_code}**")
        
        if st.button("Clear Budget"):
            st.session_state.collab_budget = None
            st.rerun()


def display_voice_assistant_tab(country, city):
    """Display voice input and conversational assistant"""
    
    st.header("Conversational Financial Guardian")
    st.markdown("Chat with your Financial Guardian about your move")
    
    voice_status = check_voice_input_available()
    
    if voice_status.get("whisper_available"):
        st.success("Voice transcription available")
    else:
        st.info("Text chat mode - Configure OpenAI API for voice input")
    
    st.divider()
    
    conversation_manager = get_conversation_manager()
    conversation_manager.set_context(country=country, city=city)
    
    for msg in st.session_state.conversation_history:
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
    
    st.subheader("Quick Questions")
    
    quick_questions = [
        f"What's the rent in {city}?",
        f"Tell me about visa requirements for {country}",
        f"What salary can I expect in {country}?",
        "Compare different financial paths for me",
        "How can VTC help me save money?"
    ]
    
    cols = st.columns(3)
    for i, question in enumerate(quick_questions[:3]):
        with cols[i]:
            if st.button(question, key=f"quick_{i}"):
                result = conversation_manager.process_text_input(question)
                st.session_state.conversation_history.append({"role": "user", "text": question})
                st.session_state.conversation_history.append({"role": "guardian", "text": result.get("response", "")})
                st.rerun()


def display_3d_visualization_tab(country, city):
    """Display Three.js 3D visualization dashboard"""
    
    st.header("Immersive Data Exploration")
    st.markdown("Explore global mobility data in 3D")
    
    viz_type = st.selectbox(
        "Visualization Type",
        ["globe", "bars", "paths", "flow"],
        format_func=lambda x: {
            "globe": "Global Cost Map",
            "bars": "Cost Comparison 3D",
            "paths": "Savings Projections",
            "flow": "VTC Transaction Flow"
        }.get(x, x)
    )
    
    if st.session_state.sim_results:
        data = {
            "monte_carlo": st.session_state.sim_results.get("mc_results", {}),
            "transactions": st.session_state.sim_results.get("sim_feed", [])
        }
    else:
        data = {
            "monte_carlo": run_monte_carlo(base_salary=4000, base_expenses=2500),
            "transactions": SAMPLE_TRANSACTIONS
        }
    
    viz_config = get_visualization_for_streamlit(viz_type, data)
    
    st.divider()
    
    if viz_type == "globe":
        st.subheader("Global Cost Overview")
        
        countries_data = compare_countries_cost(get_countries())
        
        df = pd.DataFrame(countries_data)
        
        fig = px.scatter_geo(
            df,
            locations=[get_country_iso(c["country"]) for c in countries_data],
            size="monthly_cost_eur",
            color="ppp_index",
            hover_name="country",
            projection="natural earth",
            title="Cost of Living by Country (Circle Size = Monthly Cost)"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df[["country", "monthly_cost_eur", "ppp_index", "avg_tech_salary"]], use_container_width=True)
    
    elif viz_type == "bars":
        st.subheader("Cost Comparison")
        
        countries_data = compare_countries_cost(get_countries())
        df = pd.DataFrame(countries_data)
        
        fig = px.bar(
            df.sort_values("monthly_cost_eur"),
            x="country",
            y="monthly_cost_eur",
            color="ppp_index",
            title="Monthly Living Costs by Country (EUR)",
            color_continuous_scale="Viridis"
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "paths":
        st.subheader("Monte Carlo Savings Projections")
        
        mc_results = data["monte_carlo"]
        top_paths = mc_results.get("top_paths", [])
        
        if top_paths:
            fig = go.Figure()
            
            colors = ["#48bb78", "#4299e1", "#ed8936"]
            
            for i, path in enumerate(top_paths[:3]):
                months = list(range(13))
                savings = [path.get("monthly_savings", 0) * m for m in months]
                
                fig.add_trace(go.Scatter(
                    x=months,
                    y=savings,
                    mode='lines+markers',
                    name=path.get("path_name", f"Path {i+1}"),
                    line=dict(color=colors[i], width=3)
                ))
            
            fig.add_hline(y=11208, line_dash="dash", line_color="red", annotation_text="Visa Fund Target")
            
            fig.update_layout(
                title="12-Month Savings Projection by Path",
                xaxis_title="Months",
                yaxis_title="Cumulative Savings (EUR)"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    elif viz_type == "flow":
        st.subheader("VTC Transaction Flow")
        
        transactions = data["transactions"][:10]
        
        approved = sum(1 for t in transactions if t.get("status", "Approved") == "Approved")
        declined = len(transactions) - approved
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=["Incoming", "VTC Engine", "Approved", "Declined"],
                color=["#4299e1", "#9f7aea", "#48bb78", "#f56565"]
            ),
            link=dict(
                source=[0, 0, 1, 1],
                target=[1, 1, 2, 3],
                value=[len(transactions), 0, approved, declined]
            )
        )])
        
        fig.update_layout(title="Transaction Flow Through VTC")
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    with st.expander("Advanced 3D View (Three.js)"):
        st.markdown("Interactive 3D visualization requires WebGL support")
        st.info("The 3D globe and advanced visualizations are rendered using Three.js for immersive data exploration.")
        
        components.html(viz_config.get("html", ""), height=650, scrolling=False)


def display_dao_governance_tab(country, city):
    """Display DAO governance and NFT features"""
    
    st.header("Decentralized Mobility Community")
    st.markdown("Join or create a DAO for collective mobility planning")
    
    col1, col2 = st.columns(2)
    
    with col1:
        use_mainnet = st.toggle("Use Mainnet", value=False)
        if use_mainnet:
            st.warning("MAINNET: Real cryptocurrency will be used!")
    
    with col2:
        network = "Polygon Mainnet" if use_mainnet else "Polygon Amoy Testnet"
        st.info(f"Connected to: {network}")
    
    st.divider()
    
    if st.session_state.dao_community is None:
        st.subheader("Join or Create a Community")
        
        tab1, tab2 = st.tabs(["Create Community", "Join Existing"])
        
        with tab1:
            community_name = st.text_input("Community Name", value=f"{city} Global Movers DAO")
            wallet_address = st.text_input("Your Wallet Address", placeholder="0x...")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Create Community", type="primary"):
                    if wallet_address and wallet_address.startswith("0x"):
                        manager = get_dao_manager(use_mainnet=use_mainnet)
                        community = manager.create_community(
                            name=community_name,
                            destination_country=country,
                            destination_city=city,
                            creator_address=wallet_address
                        )
                        st.session_state.dao_community = community
                        st.success("Community created!")
                        st.rerun()
                    else:
                        st.error("Please enter a valid wallet address")
            
            with col2:
                if st.button("Load Demo Community"):
                    community = create_demo_community(country, city)
                    st.session_state.dao_community = community
                    st.success("Demo community loaded!")
                    st.rerun()
        
        with tab2:
            st.info("Enter the wallet address of a community to join, or use demo mode above.")
    
    else:
        community = st.session_state.dao_community
        manager = get_dao_manager(use_mainnet=use_mainnet)
        stats = manager.get_community_stats(community.community_id)
        
        st.subheader(f"Community: {stats.get('name', 'N/A')}")
        st.markdown(f"**Destination:** {stats.get('destination', 'N/A')}")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Members", stats.get("total_members", 0))
        with col2:
            st.metric("Proposals", stats.get("total_proposals", 0))
        with col3:
            st.metric("Active Votes", stats.get("active_proposals", 0))
        with col4:
            st.metric("Total Voting Power", stats.get("total_voting_power", 0))
        
        st.divider()
        
        tab1, tab2, tab3 = st.tabs(["Proposals", "Create Proposal", "Mint NFT Passport"])
        
        with tab1:
            st.subheader("Active Proposals")
            
            for proposal in community.proposals:
                with st.expander(f"{proposal.title} - {proposal.status.upper()}"):
                    st.markdown(proposal.description)
                    st.markdown(f"**Type:** {proposal.proposal_type}")
                    st.markdown(f"**Created:** {proposal.created_at[:10]}")
                    
                    total_votes = proposal.votes_for + proposal.votes_against + proposal.votes_abstain
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("For", proposal.votes_for)
                    with col2:
                        st.metric("Against", proposal.votes_against)
                    with col3:
                        st.metric("Abstain", proposal.votes_abstain)
                    
                    if proposal.status == "active":
                        vote_col1, vote_col2, vote_col3 = st.columns(3)
                        with vote_col1:
                            if st.button("Vote For", key=f"for_{proposal.proposal_id}"):
                                st.success("Vote recorded!")
                        with vote_col2:
                            if st.button("Vote Against", key=f"against_{proposal.proposal_id}"):
                                st.success("Vote recorded!")
                        with vote_col3:
                            if st.button("Abstain", key=f"abstain_{proposal.proposal_id}"):
                                st.success("Vote recorded!")
        
        with tab2:
            st.subheader("Create New Proposal")
            
            proposal_types = get_dao_proposal_types()
            
            p_title = st.text_input("Proposal Title")
            p_type = st.selectbox(
                "Proposal Type",
                [p["id"] for p in proposal_types],
                format_func=lambda x: next((p["name"] for p in proposal_types if p["id"] == x), x)
            )
            p_description = st.text_area("Description")
            p_duration = st.slider("Voting Duration (days)", 1, 14, 7)
            
            if st.button("Submit Proposal", type="primary"):
                if p_title and p_description:
                    demo_address = "0x" + "1" * 40
                    manager.create_proposal(
                        community_id=community.community_id,
                        creator_address=demo_address,
                        title=p_title,
                        description=p_description,
                        proposal_type=p_type,
                        voting_duration_days=p_duration
                    )
                    st.success("Proposal created!")
                    st.rerun()
                else:
                    st.error("Please fill in all fields")
        
        with tab3:
            st.subheader("Mint Mobility Passport NFT")
            
            st.markdown("Create an NFT representing your financial readiness for this move.")
            
            if st.session_state.sim_results:
                mc_results = st.session_state.sim_results.get("mc_results", {})
                vtc_summary = st.session_state.sim_results.get("vtc_summary", {})
                top_path = mc_results.get("top_paths", [{}])[0]
                success_prob = top_path.get("approval_prob", 0.75)
            else:
                success_prob = 0.75
                vtc_summary = {"approval_rate": 80}
                top_path = {"path_name": "Balanced Growth", "total_savings_12m": 10000}
            
            metadata = create_mobility_passport_metadata(
                user_id="user_" + str(hash(city))[:8],
                country=country,
                city=city,
                success_probability=success_prob,
                vtc_optimized=True,
                approval_rate=vtc_summary.get("approval_rate", 80),
                projected_savings=top_path.get("total_savings_12m", 10000),
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
                <h3 style="color: {tier_color};">Mobility Passport: {preview['tier']}</h3>
                <p><strong>Destination:</strong> {preview['city']}, {preview['country']}</p>
                <p><strong>Success Rate:</strong> {preview['success_prob']}</p>
                <p><strong>Projected Savings:</strong> {preview['savings']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            wallet_for_nft = st.text_input("Wallet Address for Minting", placeholder="0x...", key="nft_wallet")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Prepare Testnet Mint"):
                    if wallet_for_nft:
                        tx_data = prepare_mainnet_nft_mint(wallet_for_nft, metadata, use_mainnet=False)
                        st.json(tx_data)
                    else:
                        st.error("Enter wallet address")
            
            with col2:
                if use_mainnet:
                    if st.button("Prepare Mainnet Mint", type="primary"):
                        if wallet_for_nft:
                            tx_data = prepare_mainnet_nft_mint(wallet_for_nft, metadata, use_mainnet=True)
                            st.warning("MAINNET transaction - Review carefully!")
                            st.json(tx_data)
                        else:
                            st.error("Enter wallet address")
        
        if st.button("Leave Community"):
            st.session_state.dao_community = None
            st.rerun()


def get_country_iso(country_name):
    """Get ISO country code"""
    iso_map = {
        "Germany": "DEU",
        "Japan": "JPN",
        "United States": "USA",
        "United Kingdom": "GBR",
        "Canada": "CAN",
        "Australia": "AUS",
        "Netherlands": "NLD",
        "Singapore": "SGP",
        "France": "FRA",
        "Spain": "ESP",
        "UAE": "ARE",
        "Portugal": "PRT"
    }
    return iso_map.get(country_name, "")


def run_simulation(country, city, salary, savings, vtc_profile, uploaded_file, use_sample):
    """Run the full financial simulation"""
    
    with st.spinner("Running financial simulation..."):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            transactions = df.to_dict('records')
        elif use_sample:
            transactions = SAMPLE_TRANSACTIONS.copy()
            col_data = get_cost_of_living(country, city)
            if col_data:
                transactions[0]["amount"] = col_data.get("rent_1br_city", 1200)
        else:
            transactions = []
        
        sim_feed = simulate_vtc(transactions, vtc_profile)
        vtc_summary = calculate_vtc_summary(sim_feed)
        vtc_recommendations = get_vtc_recommendations(sim_feed, vtc_profile)
        
        col_data = get_cost_of_living(country, city)
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
        
        mc_results = run_monte_carlo(
            base_salary=salary,
            base_expenses=monthly_expenses,
            variables={
                "upskill_boost": [0, 0.15, 0.25],
                "expense_reduction": [0, 0.1, 0.2],
                "side_income": [0, 200, 500]
            },
            num_sims=100
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
    """Display simulation results"""
    
    results = st.session_state.sim_results
    vtc_summary = results["vtc_summary"]
    mc_results = results["mc_results"]
    sim_feed = results["sim_feed"]
    
    st.header("Simulation Results")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        approval_rate = vtc_summary.get("approval_rate", 0)
        st.metric(
            "VTC Approval Rate",
            f"{approval_rate:.0f}%",
            delta=f"{approval_rate - 70:.0f}% vs target" if approval_rate >= 70 else f"{approval_rate - 70:.0f}%"
        )
    
    with col2:
        top_path = mc_results.get("top_paths", [{}])[0]
        success_prob = top_path.get("approval_prob", 0) * 100
        st.metric(
            "Success Probability",
            f"{success_prob:.0f}%",
            delta="Strong" if success_prob >= 75 else "Moderate"
        )
    
    with col3:
        potential_savings = vtc_summary.get("potential_savings", 0)
        st.metric(
            "VTC Savings",
            f"EUR {potential_savings:,.0f}",
            delta="Protected" if potential_savings > 0 else None
        )
    
    with col4:
        projected = top_path.get("total_savings_12m", 0)
        st.metric(
            "12-Month Projection",
            f"EUR {projected:,.0f}",
            delta="On track" if projected >= 11208 else "Build more"
        )
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "EchoWallet Feed", 
        "Alternative Paths", 
        "Audio Guidance",
        "Mobility Passport NFT",
        "Export Roadmap"
    ])
    
    with tab1:
        display_echowallet_feed(sim_feed, vtc_summary, vtc_profile)
    
    with tab2:
        display_alternative_paths(mc_results, salary, results["monthly_expenses"])
    
    with tab3:
        display_audio_guidance(country, city, vtc_summary, mc_results, salary, savings)
    
    with tab4:
        display_nft_section(country, city, vtc_summary, mc_results)
    
    with tab5:
        display_export_section(country, city, salary, savings, vtc_summary, mc_results, sim_feed, results["vtc_recommendations"])


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
    
    for tx in sim_feed:
        status_class = {
            "Approved": "status-approved",
            "Declined": "status-declined",
            "Flagged": "status-flagged"
        }.get(tx["status"], "")
        
        col1, col2, col3, col4 = st.columns([0.5, 2, 1, 1.5])
        
        with col1:
            st.markdown(f"### {tx['icon']}")
        
        with col2:
            st.markdown(f"**{tx['tx']}**")
            st.caption(f"{tx['category'].capitalize()} | {tx['location'].capitalize()}")
        
        with col3:
            st.markdown(f"### EUR {tx['amount']:,.0f}")
        
        with col4:
            st.markdown(f'<span class="{status_class}">{tx["status"]}</span>', unsafe_allow_html=True)
            if tx.get("vtc_action"):
                st.caption(tx["vtc_action"][:50] + "..." if len(tx.get("vtc_action", "")) > 50 else tx.get("vtc_action", ""))
        
        st.divider()
    
    st.subheader("Category Breakdown")
    
    breakdown = vtc_summary.get("category_breakdown", {})
    if breakdown:
        df = pd.DataFrame([
            {
                "Category": cat.capitalize(),
                "Approved": data.get("approved", 0),
                "Declined": data.get("declined", 0)
            }
            for cat, data in breakdown.items()
        ])
        
        fig = px.bar(
            df, 
            x="Category", 
            y=["Approved", "Declined"],
            barmode="stack",
            color_discrete_map={"Approved": "#48bb78", "Declined": "#f56565"}
        )
        fig.update_layout(yaxis_title="Amount (EUR)", legend_title="Status")
        st.plotly_chart(fig, use_container_width=True)


def display_alternative_paths(mc_results, salary, expenses):
    """Display Monte Carlo alternative paths"""
    
    st.subheader("Alternative Financial Paths")
    
    st.markdown("Based on Monte Carlo simulation with 100 scenarios:")
    
    paths = mc_results.get("top_paths", [])
    
    cols = st.columns(len(paths))
    
    for i, (col, path) in enumerate(zip(cols, paths)):
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
            st.markdown(f"*{path.get('path_description', '')}*")
    
    st.divider()
    
    st.subheader("Path Comparison")
    st.markdown(compare_paths(paths))
    
    stats = mc_results.get("statistics", {})
    st.markdown(f"""
    **Simulation Statistics:**
    - Simulations Run: {stats.get('total_simulations', 0)}
    - Visa Fund Success Rate: {stats.get('visa_fund_success_rate', 0):.0f}%
    - Average Success Probability: {stats.get('avg_approval_prob', 0)*100:.0f}%
    """)
    
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


def display_audio_guidance(country, city, vtc_summary, mc_results, salary, savings):
    """Display audio guidance section"""
    
    st.subheader("Audio Guidance from Your Financial Guardian")
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; text-align: center;">
        <h3 style="margin-bottom: 0.5rem;">Incoming Call...</h3>
        <p>From: Your Financial Guardian ({country}, Ahead)</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    if st.button("Generate Audio Guidance", type="primary", use_container_width=True):
        with st.spinner("Generating personalized guidance..."):
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
                st.error("Failed to generate audio. Displaying text guidance instead.")
                st.info(guidance_text)
    
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
            <div>
                <p style="color: #a0aec0; margin: 0; font-size: 0.8rem;">VTC Optimized</p>
                <p style="margin: 0; font-size: 1.2rem;">{preview["vtc_optimized"]}</p>
            </div>
            <div>
                <p style="color: #a0aec0; margin: 0; font-size: 0.8rem;">Projected Savings</p>
                <p style="margin: 0; font-size: 1.2rem;">{preview["savings"]}</p>
            </div>
        </div>
        <hr style="border-color: #4a5568;">
        <p style="color: #4fd1c5; font-size: 0.9rem;">Recommended: {preview["path"]}</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("")
    
    col1, col2 = st.columns(2)
    
    with col1:
        wallet_address = st.text_input(
            "Wallet Address (optional)",
            placeholder="0x...",
            help="Enter your Ethereum wallet address for testnet minting"
        )
    
    with col2:
        web3_status = check_web3_availability()
        if web3_status.get("connected"):
            st.success("Connected to Polygon Amoy Testnet")
        else:
            st.info("Preview Mode - Connect wallet to mint")
    
    if st.button("Prepare NFT Mint", type="primary", use_container_width=True):
        if wallet_address and wallet_address.startswith("0x"):
            tx_data = prepare_mint_transaction(wallet_address, metadata)
            
            st.success("NFT Mint Prepared!")
            
            with st.expander("Minting Instructions"):
                for step, instruction in tx_data["instructions"].items():
                    st.markdown(f"**{step.upper()}:** {instruction}")
                
                st.markdown(f"**Faucet:** [{tx_data['faucet_url']}]({tx_data['faucet_url']})")
                st.markdown(f"**OpenSea Testnet:** [{tx_data['opensea_testnet']}]({tx_data['opensea_testnet']})")
            
            with st.expander("NFT Metadata (JSON)"):
                st.json(metadata)
        else:
            st.warning("Please enter a valid Ethereum wallet address (starting with 0x)")
            
            with st.expander("Preview NFT Metadata"):
                st.json(metadata)


def display_export_section(country, city, salary, savings, vtc_summary, mc_results, sim_feed, recommendations):
    """Display PDF export section"""
    
    st.subheader("Export Financial Roadmap")
    
    st.markdown("""
    Download a comprehensive PDF report of your financial simulation results. 
    This document includes:
    - Executive summary with key metrics
    - VTC simulation breakdown
    - Alternative path analysis
    - Personalized recommendations
    """)
    
    if st.button("Generate PDF Report", type="primary", use_container_width=True):
        with st.spinner("Generating PDF..."):
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
                label="Download PDF Roadmap",
                data=pdf_bytes,
                file_name=filename,
                mime="application/pdf",
                type="secondary",
                use_container_width=True
            )
            
            st.success(f"PDF generated: {filename}")


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
                st.markdown(f"**Language:** {visa_info.get('language_requirement', 'N/A')}")
            with col2:
                st.markdown(f"**Blocked Account:** {visa_info.get('blocked_account', 0):,}")
                st.markdown(f"**Health Insurance:** {'Required' if visa_info.get('health_insurance_required') else 'Optional'}")
                st.markdown(f"**Validity:** {visa_info.get('validity_months', 'N/A')} months")
    
    st.divider()
    
    with st.expander("Ask the Data (RAG Query)", expanded=False):
        rag_query = st.text_input(
            "Ask about cost of living, visa requirements, or salaries:",
            placeholder=f"e.g., What is the rent in {city}?",
            key="rag_query_input"
        )
        if rag_query:
            with st.spinner("Querying RAG system..."):
                result = query_cost_of_living(rag_query, country=country, city=city)
                
                if result.get("success") and result.get("results"):
                    st.markdown(f"**Confidence:** {result.get('confidence', 0)*100:.0f}% | **Mode:** {result.get('mode', 'unknown')}")
                    
                    for i, doc in enumerate(result["results"][:2], 1):
                        st.markdown(f"**Source {i}:** {doc.get('source', 'Unknown')}")
                        st.text(doc.get("content", "")[:500] + "..." if len(doc.get("content", "")) > 500 else doc.get("content", ""))
                else:
                    st.warning("No relevant data found. Try a different query.")
    
    st.divider()
    
    col_data = get_cost_of_living(country, city)
    wb_data = get_world_bank_data(country)
    
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
        st.metric("Income Level", wb_data.get("income_level", "N/A"))
        
        st.caption(f"Data Confidence: {confidence*100:.0f}% (Cross-verified)")
    
    st.divider()
    
    st.subheader("Key Financial Thresholds")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        visa_fund = col_data.get("visa_fund_proof", 0)
        if currency != "EUR":
            from data_module import convert_to_eur
            visa_fund_eur = convert_to_eur(visa_fund, currency)
            st.metric("Visa Fund Proof Required", f"{currency} {visa_fund:,}", help=f"≈ EUR {visa_fund_eur:,.0f}")
        else:
            st.metric("Visa Fund Proof Required", f"EUR {visa_fund:,}")
    
    with col2:
        min_salary = col_data.get("min_salary_tech", 0)
        st.metric("Min Tech Salary", f"{currency} {min_salary:,}")
    
    with col3:
        ppp = col_data.get("ppp_index", 0)
        st.metric("PPP Index", f"{ppp:.2f}", help="Purchasing Power Parity relative to reference")


if __name__ == "__main__":
    main()
