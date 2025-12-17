"""
EchoWorld Nexus - AI Financial Guardian for Global Mobility
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import json

from data_module import (
    get_cost_of_living, get_cities, get_world_bank_data,
    calculate_confidence_score, get_monthly_expenses, SAMPLE_TRANSACTIONS,
    TRANSACTION_CATEGORIES, VTC_RULES
)
from vtc_engine import (
    simulate_vtc, calculate_vtc_summary, get_vtc_recommendations,
    generate_vtc_guardian_message
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
</style>
""", unsafe_allow_html=True)

if "simulation_run" not in st.session_state:
    st.session_state.simulation_run = False
if "sim_results" not in st.session_state:
    st.session_state.sim_results = None
if "audio_generated" not in st.session_state:
    st.session_state.audio_generated = False


def main():
    st.markdown('<h1 class="main-header">EchoWorld Nexus</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="tagline">Simulate your abroad finances securely—get audio guidance from your future self, '
        'powered by Visa controls and DeFi insights.</p>',
        unsafe_allow_html=True
    )
    
    with st.sidebar:
        st.header("Your Profile")
        
        country = st.selectbox(
            "Destination Country",
            ["Germany", "Japan"],
            help="Select your target destination country"
        )
        
        cities = get_cities(country)
        city = st.selectbox("Destination City", cities)
        
        st.divider()
        
        st.subheader("Financial Information")
        
        col_data = get_cost_of_living(country, city)
        default_salary = col_data.get("avg_salary_tech", 4000) if col_data else 4000
        
        if country == "Japan":
            salary_eur = st.number_input(
                "Expected Monthly Salary (€)",
                min_value=1000,
                max_value=20000,
                value=int(default_salary * 0.0067),
                step=100,
                help="Your expected monthly salary in EUR"
            )
        else:
            salary_eur = st.number_input(
                "Expected Monthly Salary (€)",
                min_value=1000,
                max_value=20000,
                value=int(default_salary),
                step=100,
                help="Your expected monthly salary in EUR"
            )
        
        current_savings = st.number_input(
            "Current Savings (€)",
            min_value=0,
            max_value=100000,
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
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("Run Financial Simulation", type="primary", use_container_width=True):
            run_simulation(
                country, city, salary_eur, current_savings, 
                vtc_profile, uploaded_file, use_sample
            )
    
    with col2:
        col_data = get_cost_of_living(country, city)
        wb_data = get_world_bank_data(country)
        if col_data and wb_data:
            confidence = calculate_confidence_score(col_data, wb_data)
            st.metric("Data Confidence", f"{confidence*100:.0f}%", help="Cross-verified accuracy")
    
    if st.session_state.simulation_run and st.session_state.sim_results:
        display_results(country, city, salary_eur, current_savings, vtc_profile)
    else:
        display_data_preview(country, city)
    
    st.divider()
    st.markdown(
        '<div class="disclaimer">' + get_ethical_disclaimer() + '</div>',
        unsafe_allow_html=True
    )


def run_simulation(country, city, salary, savings, vtc_profile, uploaded_file, use_sample):
    """Run the full financial simulation"""
    
    with st.spinner("Running financial simulation..."):
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            transactions = df.to_dict('records')
        elif use_sample:
            transactions = SAMPLE_TRANSACTIONS.copy()
            col_data = get_cost_of_living(country, city)
            if col_data and country == "Germany":
                transactions[0]["amount"] = col_data.get("rent_1br_city", 1200)
        else:
            transactions = []
        
        sim_feed = simulate_vtc(transactions, vtc_profile)
        vtc_summary = calculate_vtc_summary(sim_feed)
        vtc_recommendations = get_vtc_recommendations(sim_feed, vtc_profile)
        
        col_data = get_cost_of_living(country, city)
        if col_data:
            if country == "Germany":
                monthly_expenses = sum([
                    col_data["rent_1br_city"],
                    col_data["groceries_monthly"],
                    col_data["utilities_monthly"],
                    col_data["transport_monthly"],
                    col_data["internet_monthly"]
                ])
            else:
                monthly_expenses = sum([
                    col_data["rent_1br_city"] * 0.0067,
                    col_data["groceries_monthly"] * 0.0067,
                    col_data["utilities_monthly"] * 0.0067,
                    col_data["transport_monthly"] * 0.0067,
                    col_data["internet_monthly"] * 0.0067
                ])
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
            f"€{potential_savings:,.0f}",
            delta="Protected" if potential_savings > 0 else None
        )
    
    with col4:
        projected = top_path.get("total_savings_12m", 0)
        st.metric(
            "12-Month Projection",
            f"€{projected:,.0f}",
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
            st.caption(f"{tx['category'].capitalize()} • {tx['location'].capitalize()}")
        
        with col3:
            st.markdown(f"### €{tx['amount']:,.0f}")
        
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
        fig.update_layout(yaxis_title="Amount (€)", legend_title="Status")
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
            
            st.markdown(f"**Monthly Savings:** €{path.get('monthly_savings', 0):,.0f}")
            st.markdown(f"**12-Month Total:** €{path.get('total_savings_12m', 0):,.0f}")
            st.markdown(f"*{path.get('path_description', '')}*")
            
            if st.button(f"Simulate {path.get('path_name', 'Path')}", key=f"path_{i}"):
                st.info(f"Re-running simulation with {path.get('path_description', 'this configuration')}...")
    
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
                "salary": "Effective Salary (€)",
                "total_savings_12m": "12-Month Savings (€)",
                "approval_prob": "Success Prob"
            }
        )
        fig.update_layout(title="Monte Carlo Outcomes Distribution")
        st.plotly_chart(fig, use_container_width=True)


def display_audio_guidance(country, city, vtc_summary, mc_results, salary, savings):
    """Display audio guidance section"""
    
    st.subheader("Audio Guidance from Your Financial Guardian")
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; border-radius: 15px; color: white; text-align: center;">
        <h3 style="margin-bottom: 0.5rem;">Incoming Call...</h3>
        <p>From: Your Financial Guardian ({}, Ahead)</p>
    </div>
    """.format(country), unsafe_allow_html=True)
    
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
            <h3 style="margin: 0;">🌍 {preview["title"]}</h3>
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
        st.caption(f"Data Sources: Numbeo + World Bank (Cross-Verified)")
    
    with col3:
        st.caption(f"Vector Store: {rag_status.get('vector_store_type', 'N/A')}")
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(f"Cost of Living: {city}")
        
        currency = col_data.get("currency", "EUR")
        
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
        if country == "Germany":
            visa_fund = "€11,208"
        else:
            visa_fund = "¥2,000,000 (~€13,400)"
        st.metric("Visa Fund Proof Required", visa_fund)
    
    with col2:
        min_salary = col_data.get("min_salary_tech", 0)
        if country == "Japan":
            st.metric("Min Tech Salary", f"¥{min_salary:,}")
        else:
            st.metric("Min Tech Salary", f"€{min_salary:,}")
    
    with col3:
        ppp = col_data.get("ppp_index", 0)
        st.metric("PPP Index", f"{ppp:.2f}", help="Purchasing Power Parity relative to reference")


if __name__ == "__main__":
    main()
