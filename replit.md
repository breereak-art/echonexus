# EchoWorld Nexus - AI Financial Guardian for Global Mobility

## Overview
EchoWorld Nexus is a comprehensive Streamlit-based financial simulation tool that helps users plan international relocations. It provides AI-powered guidance, Visa Transaction Controls (VTC) simulation, Monte Carlo financial projections, and blockchain-based credential verification.

## Recent Changes (December 2024)
- Expanded to 12 countries with comprehensive PPP and visa requirement data
- Added VTC Sandbox API integration for real-time transaction testing
- Implemented multi-user collaborative budgeting features
- Added voice input for conversational financial guidance
- Created Three.js visualization dashboard for immersive data exploration
- Added DAO governance for decentralized mobility communities

## Project Architecture

### Core Modules
- `app.py` - Main Streamlit application with 6 feature tabs
- `data_module.py` - Cost of living data for 12 countries, visa requirements, PPP indexes
- `vtc_engine.py` - Local VTC transaction simulation
- `vtc_api.py` - Visa VTC Sandbox API client integration
- `monte_carlo_engine.py` - Financial path simulation with 100 scenarios
- `ai_guidance.py` - OpenAI-powered personalized guidance generation
- `tts_module.py` - Google TTS audio guidance with ethical watermarks
- `rag_module.py` - RAG-powered data retrieval using LangChain + FAISS

### New Feature Modules
- `collaborative.py` - Multi-user collaborative budget planning
- `voice_input.py` - Voice transcription and conversational AI
- `visualization_3d.py` - Three.js 3D data visualization
- `dao_governance.py` - DAO governance and NFT minting for mainnet/testnet

### Supporting Modules
- `nft_module.py` - Mobility Passport NFT metadata and minting
- `pdf_export.py` - PDF report generation

## Supported Countries (12 Total)
1. Germany (Berlin, Munich, Frankfurt)
2. Japan (Tokyo, Osaka)
3. United States (New York, San Francisco, Austin)
4. United Kingdom (London, Manchester)
5. Canada (Toronto, Vancouver)
6. Australia (Sydney, Melbourne)
7. Netherlands (Amsterdam, Rotterdam)
8. Singapore
9. France (Paris, Lyon)
10. Spain (Barcelona, Madrid)
11. UAE (Dubai, Abu Dhabi)
12. Portugal (Lisbon, Porto)

## Key Features

### 1. Financial Simulation
- Monte Carlo analysis with 100 scenarios
- VTC transaction control simulation
- Multi-path savings projections

### 2. VTC Sandbox API
- Real-time transaction authorization testing
- Session-based transaction history
- Analytics and reporting

### 3. Collaborative Planning
- Multi-user budget sharing
- Income-based expense splitting
- Invite code system for partners/family

### 4. Voice Assistant
- Text-based conversational interface
- Intent parsing for financial queries
- Context-aware responses

### 5. 3D Visualization
- Global cost comparison map
- 3D bar charts for cost analysis
- Monte Carlo path visualization
- VTC transaction flow diagrams

### 6. DAO Governance
- Community creation and management
- Proposal creation and voting
- NFT passport minting (testnet/mainnet)
- Voting power based on NFT tier

## Environment Variables
- `OPENAI_API_KEY` - For AI guidance and voice transcription
- `VISA_VTC_SANDBOX_KEY` - Optional: For live VTC API (sandbox mode works without)

## Running the Application
```bash
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

## Technology Stack
- **Frontend**: Streamlit with custom CSS styling
- **Data Visualization**: Plotly, Three.js
- **AI/ML**: OpenAI GPT, LangChain, FAISS for RAG
- **Blockchain**: Web3.py, Polygon (Amoy testnet / Mainnet)
- **Audio**: Google TTS (gTTS)
- **PDF**: ReportLab

## User Preferences
- Modern, clean UI with gradient styling
- Privacy-first: No personal data storage
- Ethical AI: Watermarked audio guidance
- Cross-verified data from multiple sources
