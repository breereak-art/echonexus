# EchoWorld Nexus - AI Financial Guardian for Global Mobility

## Overview
EchoWorld Nexus is a comprehensive Streamlit-based financial simulation tool that helps users plan international relocations. It provides AI-powered guidance, Visa Transaction Controls (VTC) simulation, Monte Carlo financial projections, and blockchain-based credential verification.

## Recent Changes (December 19, 2025 - Phase 1: Community Launch)
- **Reddit-Style Community Platform Phase 1**: New "🌍 Community" tab with posts, comments, and likes
- **Core Social Features**:
  - Create posts with title, content, and category
  - Comment on posts with real-time threading
  - Like/unlike posts and comments
  - Browse posts filtered by category
  - Display names for anonymity/flexibility
- **Categories Available**: General, Visa & Immigration, Cost of Living, Job Market, Relocation Tips, Language & Culture, Safety & Health
- **Storage**: Phase 1 uses session state (in-memory). Phase 2 will add persistent database storage
- **Next**: Phase 2 will add persistent storage, user profiles, and karma/reputation system

### Previous Session Changes (December 19, 2025)
- **Real-Time API Integration**: Added World Bank economic indicators API
- **Live Currency Exchange**: Integrated Frankfurter API for real-time forex rates
- **Intelligent Fallbacks**: All APIs gracefully fallback to hardcoded data if requests fail
- **API Functions Added**:
  - `get_world_bank_indicator()` - Fetches GDP, inflation, unemployment
  - `get_currency_exchange_rate()` - Real-time currency conversion via Frankfurter
  - `update_world_bank_data_live()` - Batch updates for economic data
  - `update_exchange_rates_live()` - Batch updates for forex rates
- **Future-Ready**: Structured for Travel Buddy AI Visa API integration (when key available)
- **Zero Dependencies**: Uses only `requests` (already installed)

## Previous Changes (December 18, 2025)
- **Professional UI Redesign**: Complete visual overhaul with modern dark-themed hero cards
- **New Color Palette**: Gradient accents (indigo/violet), clean typography with Inter font
- **Enhanced Hero Cards**: Dark gradient backgrounds with colored top borders and shadows
- **Improved Proof of Funds**: Dynamic coloring (green/red) based on funding status
- **Polished Components**: Rounded cards, better spacing, modern button styling
- **Tab Styling**: Clean tab navigation with hover effects
- **Chat UI**: Updated chat bubbles with gradient backgrounds

### Previous Updates (December 17, 2025)
- **UI Overhaul**: Restructured from 6 tabs to 3 focused tabs for better demo flow
- **Hero Dashboard**: Added 4 key metrics at the top (Data Confidence, PoF, Salary, VTC)
- **Proof of Funds Verification**: New PoF feature with progress bar and visa risk alerts
- **PPP Toggle**: Interactive purchasing power parity visualization
- **Judge Demo Mode**: Pre-seeded deterministic simulation for hackathon demos
- **Ethics Badges**: Prominent privacy/ethics indicators in sidebar
- **Error Handling**: Improved fallbacks for API failures
- **Deterministic Monte Carlo**: Optional seed parameter for reproducible results

## Project Architecture

### Core Modules
- `app.py` - Main Streamlit application with 3 focused tabs and hero dashboard
- `data_module.py` - Cost of living data for 12 countries, visa requirements, PPP indexes
- `vtc_engine.py` - Local VTC transaction simulation
- `vtc_api.py` - Visa VTC Sandbox API client integration
- `monte_carlo_engine.py` - Financial path simulation with 100 scenarios (deterministic option)
- `ai_guidance.py` - OpenAI-powered personalized guidance generation
- `tts_module.py` - Google TTS audio guidance with ethical watermarks
- `rag_module.py` - RAG-powered data retrieval using LangChain + FAISS

### Feature Modules
- `collaborative.py` - Multi-user collaborative budget planning
- `voice_input.py` - Voice transcription and conversational AI
- `visualization_3d.py` - Three.js 3D data visualization
- `dao_governance.py` - DAO governance and NFT minting for mainnet/testnet
- `nft_module.py` - Mobility Passport NFT metadata and minting
- `pdf_export.py` - PDF report generation

## Supported Countries (12 Total)
Germany, Japan, United States, United Kingdom, Canada, Australia, Netherlands, Singapore, France, Spain, UAE, Portugal

## Key Features

### 1. Financial Simulation (Tab 1: Simulate & Optimize)
- Hero dashboard with 4 key metrics
- Proof of Funds verification with visa risk alerts
- PPP-adjusted salary visualization
- Monte Carlo analysis with 100 scenarios
- VTC transaction control simulation
- Step indicator for guided flow

### 2. Voice & Guidance (Tab 2)
- Chat assistant for financial queries
- Audio guidance from "Financial Guardian"
- Quick question shortcuts

### 3. Export & Advanced (Tab 3)
- PDF roadmap export
- NFT Passport minting (testnet/mainnet)
- Collaborative budget planning
- DAO governance features

## Environment Variables
- `OPENAI_API_KEY` - For AI guidance and voice transcription
- `VISA_VTC_SANDBOX_KEY` - Optional: For live VTC API (sandbox mode works without)

## Running the Application
```bash
streamlit run app.py --server.port 5000 --server.address 0.0.0.0 --server.headless true
```

## Demo Mode
Click "Judge Demo Mode" in the sidebar to:
- Pre-seed deterministic data for consistent demos
- Automatically set optimal demo parameters
- Ensure reproducible Monte Carlo results

## Technology Stack
- **Frontend**: Streamlit with custom CSS styling
- **Data Visualization**: Plotly
- **AI/ML**: OpenAI GPT, LangChain, FAISS for RAG
- **Blockchain**: Web3.py, Polygon (Amoy testnet / Mainnet)
- **Audio**: Google TTS (gTTS)
- **PDF**: ReportLab

## User Preferences
- Modern, clean UI with gradient styling
- Privacy-first: No personal data storage
- Ethical AI: Watermarked audio guidance
- Cross-verified data from multiple sources
