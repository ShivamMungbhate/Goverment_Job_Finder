# Sahayak - Government Scheme Finder

Sahayak  is an expert Indian government policy advisor and social welfare consultant app built using Python, Streamlit, and Groq LLM API. It helps citizens discover central and state government schemes, subsidies, pensions, and entitlements they qualify for.

## Features
- **👤 Applier Profile Card**: Fill out name, email, mobile, government ID, and upload a profile picture to dynamically generate a digital Sahayak Identity Card.
- **📋 Eligibility Inputs**: Simple structured input form collecting demographics, location, financial, education, employment, family, and daily life needs.
- **📑 Demo Presets**: Quickly load preset profiles (Ramesh Kumar - Farmer, Sunita Devi - Widow, Aarav Ansari - Student) to test the app instantly in Simulation Mode without an API Key.
- **🤖 Groq API Integration**: Queries state-of-the-art models like `llama-3.3-70b-specdec` using a fine-tuned consultant prompt.
- **📥 Download Reports**: Export generated advisory reports in Markdown/Text formats.

## Setup Instructions

1. **Clone or navigate to the directory**:
   ```bash
   cd C:\Users\shiva\.gemini\antigravity\scratch\sahayak
   ```

2. **Install dependencies**:
   Make sure you have python installed. Then run:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit application**:
   ```bash
   streamlit run app.py
   ```

4. **Access the application**:
   Open [http://localhost:8501](http://localhost:8501) in your browser.

5. **API Key Setup**:
   Enter your **Groq API Key** in the sidebar. If you do not have one, select a preset in the sidebar and click **Dhoondhein Schemes** to run in Simulation Mode.
