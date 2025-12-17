# EchoWorld Nexus - AI Financial Guardian for Global Mobility

## Overview

EchoWorld Nexus is an AI-powered financial guardian simulator that helps users plan their international relocation finances. The application simulates financial scenarios with Visa Transaction Controls (VTC), Monte Carlo alternative paths, RAG-powered data insights, audio guidance, and DeFi NFT features.

**Tagline:** "Simulate your abroad finances securely—get audio guidance from your future self, powered by Visa controls and DeFi insights."

## Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| `app.py` | Main Streamlit dashboard integrating all features |
| `data_module.py` | Cost of living data for Germany/Japan, VTC rules, World Bank indicators |
| `rag_module.py` | RAG (Retrieval-Augmented Generation) system with FAISS vector store |
| `vtc_engine.py` | Visa Transaction Controls simulation with approval/decline logic |
| `monte_carlo_engine.py` | Monte Carlo simulation for alternative financial paths |
| `ai_guidance.py` | OpenAI integration for personalized financial guidance with RAG context |
| `tts_module.py` | Text-to-speech audio guidance with ethical watermarks (gTTS) |
| `nft_module.py` | Polygon testnet Mobility Passport NFT minting |
| `pdf_export.py` | PDF export for financial roadmap reports (ReportLab) |

### Data Flow

1. User inputs financial profile (salary, savings, destination)
2. RAG system retrieves relevant cost of living and visa data
3. VTC engine simulates transaction approvals/declines
4. Monte Carlo engine generates alternative financial paths
5. AI generates personalized audio guidance using RAG context
6. User can export PDF report or mint NFT passport

## Features

- **2 Countries Supported:** Germany (Berlin, Munich), Japan (Tokyo, Osaka)
- **VTC Profiles:** Standard, Conservative, Flexible
- **RAG-Powered Data:** Cross-verified Numbeo + World Bank data with confidence scoring
- **Audio Guidance:** TTS with ethical disclaimers
- **Monte Carlo:** 100 simulations, 1-3 alternative paths
- **NFT Minting:** Polygon Amoy testnet support
- **PDF Export:** Comprehensive financial roadmap

## Configuration

### Environment Variables

- `OPENAI_API_KEY` - Required for AI guidance and vector embeddings (RAG)
- Without API key, app falls back to template guidance and keyword search

### Running the App

```bash
streamlit run app.py --server.port 5000
```

## Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python 3.11
- **AI/ML:** OpenAI GPT-5, LangChain, FAISS
- **Audio:** gTTS
- **DeFi:** Web3.py (Polygon Amoy)
- **PDF:** ReportLab
- **Data Viz:** Plotly

## Recent Changes

- **Dec 2024:** Initial MVP with all core features
- RAG system with fallback to keyword search
- VTC simulation with 3 profile types
- Monte Carlo with salary/expense/side-income variables
- NFT minting preparation for Polygon testnet

## User Preferences

- Clean, modern UI with gradient accents
- Privacy-first: no data stored, ethical watermarks in audio
- Cross-verified data with confidence scoring
