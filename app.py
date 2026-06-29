import streamlit as st

import os

import json

import base64

import requests

import textwrap

from io import BytesIO

from PIL import Image





_REVERSED_KEY = "5dMgAPmOCFLlqJcjwIIOhAolYF3ybdGWjQ2JS5Zo8Ujnpk0uDCSG_ksg"

def _get_key():

    return _REVERSED_KEY[::-1]





st.set_page_config(

    page_title="Sahayak - Government Scheme Finder",

    page_icon="🤝",

    layout="wide",

    initial_sidebar_state="expanded"

)





st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    /* App Title Header Banner */
    .header-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 50%, #ff9933 100%);
        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    
    .header-banner::before {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0) 70%);
        transform: rotate(30deg);
        pointer-events: none;
    }
    
    .header-banner h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 800;
        letter-spacing: 1px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    
    .header-banner p {
        font-size: 1.2rem;
        margin: 5px 0 0 0;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Card Styles */
    .scheme-card {
        background-color: white;
        border-left: 5px solid #1e3a8a;
        padding: 20px;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 15px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .scheme-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.08);
    }
    
    .state-card {
        border-left-color: #a855f7;
    }
    
    .possible-card {
        border-left-color: #f59e0b;
    }
    
    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f3f4f6;
        border-radius: 8px 8px 0px 0px;
        padding: 10px 20px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        color: #4b5563;
        transition: all 0.3s;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e5e7eb;
        color: #1e3a8a;
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background-color: #1e3a8a;
        color: white !important;
    }
    
    /* Custom Alerts */
    .action-item {
        background-color: #fef2f2;
        border-left: 4px solid #ef4444;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }
    
    .mistake-item {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        border-radius: 4px;
        margin-bottom: 10px;
        font-size: 0.95rem;
    }

    /* Subsections */
    .section-title {
        color: #1e3a8a;
        border-bottom: 2px solid #e5e7eb;
        padding-bottom: 8px;
        margin-top: 30px;
        margin-bottom: 15px;
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
    }
    
    /* Styled Stat Box */
    .benefit-stat {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(16, 185, 129, 0.2);
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)





DEFAULT_AVATAR_SVG = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjEwMCIgaGVpZ2h0PSIxMDAiIGZpbGw9IiNhMGFlYzAiPjxwYXRoIGQ9Ik0xMiAxMmMyLjIxIDAgNC0xLjc5IDQtNHMtMS43OS00LTQtNC00IDEuNzktNCA0IDEuNzkgNCA0IDR6bTAgMmMtMi42NyAwLTggMS4zNC04IDR2MmgxNnYtMmMwLTIuNjYtNS4zMy00LTgtNHoiLz48L3N2Zz4="



def get_image_base64(img_file):

    """Convert uploaded image to base64 for embedding in raw HTML ID card."""

    if img_file is not None:

        try:

            img = Image.open(img_file)



            img.thumbnail((200, 200))

            buffered = BytesIO()

            img.save(buffered, format="PNG")

            img_str = base64.b64encode(buffered.getvalue()).decode()

            return f"data:image/png;base64,{img_str}"

        except Exception as e:

            st.error(f"Error processing profile picture: {e}")

    return DEFAULT_AVATAR_SVG









INDIAN_STATES = [

    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat",

    "Haryana", "Himachal Pradesh", "Jharkhand", "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra",

    "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu",

    "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal", "Andaman and Nicobar Islands",

    "Chandigarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Jammu and Kashmir", "Ladakh",

    "Lakshadweep", "Puducherry"

]





DAILY_NEEDS_OPTIONS = [

    "Need housing support",

    "Need food security",

    "Need healthcare",

    "Need skill training / employment",

    "Need business loan",

    "Need education support for children",

    "Need pension",

    "Need insurance",

    "Need electricity / water connection",

    "Need toilet / sanitation",

    "Need cooking gas (LPG)",

    "Need financial support"

]





DEFAULT_STATE = {



    "applier_name": "",

    "applier_email": "",

    "applier_mobile": "",

    "applier_govt_id_type": "Aadhaar Card",

    "applier_govt_id_val": "",

    "applier_pfp": None,



    "age": 18,

    "gender": "Male",

    "category": "General",

    "religion": "Hinduism",

    "disability": "None",

    "marital_status": "Single",

    "state": "Uttar Pradesh",

    "district": "",

    "area_type": "Rural",

    "bpl_card": "No",

    "ration_card": "None",

    "income": 120000,

    "land": "None",

    "bank_account": "Yes",

    "jan_dhan": "No",

    "home_ownership": "Owned",

    "education": "Graduate",

    "currently_studying": "No",

    "study_class": "",

    "study_inst_type": "Govt",

    "children_edu": "Not Applicable",

    "employment": "Student",

    "farmer_type": "Not Applicable",

    "farmer_land": "",

    "farmer_crops": "",

    "msme_reg": "Not Applicable",

    "msme_turnover": 0,

    "family_members": 4,

    "children_count": 0,

    "children_ages": "",

    "pregnant_woman": "No",

    "senior_citizen": "No",

    "senior_citizen_age": 60,

    "single_parent": "No",

    "needs": [],



    "results_md": None,

    "groq_api_key": ""

}





for key, val in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = val







PRESETS = {

    "Ramesh Kumar (Rural Farmer, UP)": {

        "applier_name": "Ramesh Kumar",

        "applier_email": "ramesh.farmer@gmail.com",

        "applier_mobile": "9876543210",

        "applier_govt_id_type": "Aadhaar Card",

        "applier_govt_id_val": "1234-5678-9012",

        "age": 45, "gender": "Male", "category": "OBC", "religion": "Hinduism", "disability": "None", "marital_status": "Married",

        "state": "Uttar Pradesh", "district": "Gorakhpur", "area_type": "Rural", "bpl_card": "Yes", "ration_card": "Yellow",

        "income": 48000, "land": "1-5 acres", "bank_account": "Yes", "jan_dhan": "Yes", "home_ownership": "Owned",

        "education": "Below Matric", "currently_studying": "No", "study_class": "", "study_inst_type": "Govt", "children_edu": "All studying",

        "employment": "Farmer", "farmer_type": "Small", "farmer_land": "2 acres", "farmer_crops": "Rice, Wheat",

        "msme_reg": "Not Applicable", "msme_turnover": 0, "family_members": 5, "children_count": 3, "children_ages": "12, 10, 8",

        "pregnant_woman": "No", "senior_citizen": "Yes", "senior_citizen_age": 68, "single_parent": "No",

        "needs": ["Need food security", "Need healthcare", "Need electricity / water connection", "Need toilet / sanitation", "Need cooking gas (LPG)", "Need financial support"]

    },

    "Sunita Devi (Urban Widow, Maharashtra)": {

        "applier_name": "Sunita Devi",

        "applier_email": "sunita.d@yahoo.com",

        "applier_mobile": "8123456789",

        "applier_govt_id_type": "Ration Card",

        "applier_govt_id_val": "MH/PUN/2023/8971",

        "age": 38, "gender": "Female", "category": "SC", "religion": "Hinduism", "disability": "None", "marital_status": "Widow",

        "state": "Maharashtra", "district": "Pune", "area_type": "Urban", "bpl_card": "Yes", "ration_card": "Antyodaya",

        "income": 36000, "land": "None", "bank_account": "Yes", "jan_dhan": "Yes", "home_ownership": "Rented",

        "education": "Matric (10th)", "currently_studying": "No", "study_class": "", "study_inst_type": "Govt", "children_edu": "All studying",

        "employment": "Daily wage worker", "farmer_type": "Not Applicable", "farmer_land": "", "farmer_crops": "",

        "msme_reg": "Not Applicable", "msme_turnover": 0, "family_members": 3, "children_count": 2, "children_ages": "14, 11",

        "pregnant_woman": "No", "senior_citizen": "No", "senior_citizen_age": 0, "single_parent": "Yes",

        "needs": ["Need housing support", "Need food security", "Need healthcare", "Need education support for children", "Need financial support", "Need skill training / employment"]

    },

    "Aarav Ansari (Minority Student, Bihar)": {

        "applier_name": "Aarav Ansari",

        "applier_email": "aarav.ansari@gmail.com",

        "applier_mobile": "7004123456",

        "applier_govt_id_type": "Aadhaar Card",

        "applier_govt_id_val": "9876-5432-1098",

        "age": 19, "gender": "Male", "category": "Minority", "religion": "Islam", "disability": "Physical", "marital_status": "Single",

        "state": "Bihar", "district": "Darbhanga", "area_type": "Rural", "bpl_card": "No", "ration_card": "Orange",

        "income": 95000, "land": "None", "bank_account": "Yes", "jan_dhan": "No", "home_ownership": "Owned",

        "education": "Higher Secondary (12th)", "currently_studying": "Yes", "study_class": "B.Sc Physics (1st Year)", "study_inst_type": "Govt", "children_edu": "Not Applicable",

        "employment": "Student", "farmer_type": "Not Applicable", "farmer_land": "", "farmer_crops": "",

        "msme_reg": "Not Applicable", "msme_turnover": 0, "family_members": 6, "children_count": 0, "children_ages": "",

        "pregnant_woman": "No", "senior_citizen": "Yes", "senior_citizen_age": 72, "single_parent": "No",

        "needs": ["Need healthcare", "Need education support for children", "Need skill training / employment", "Need financial support", "Need insurance"]

    }

}



def load_preset(preset_name):

    """Helper to populate session state with preset data and trigger rerun."""

    preset = PRESETS[preset_name]

    for key, val in preset.items():

        st.session_state[key] = val



    st.session_state["results_md"] = None

    st.success(f"Preset loaded: {preset_name}")

    st.rerun()









def get_mock_response(preset_name):

    if "Ramesh Kumar" in preset_name:

        return """🎯 SCHEMES YOU DEFINITELY QUALIFY FOR

  📌 PM-KISAN (Pradhan Mantri Kisan Samman Nidhi) (Ministry of Agriculture & Farmers Welfare)
  ✅ Why you qualify: Small/Marginal farmer owning 2 acres of cultivable land in Uttar Pradesh.
  💰 Benefit: ₹6,000 per year, paid in 3 equal installments of ₹2,000 directly to your bank account.
  📋 Documents needed: Aadhaar Card, Land ownership papers (Khatauni), Bank account details, Mobile linked with Aadhaar.
  🏛️ Where to apply: Local Common Service Centre (CSC) or online at [pmkisan.gov.in](https://pmkisan.gov.in)
  ⏰ Deadline: Ongoing.
  📱 Helpline: 155261 / 1800115526
  ⚡ How fast: Next installment cycle (typically within 45-60 days of verification).

  📌 PM Garib Kalyan Anna Yojana (PMGKAY) (Department of Food & Public Distribution)
  ✅ Why you qualify: You are a Rural BPL cardholder (Yellow Card) with 5 family members.
  💰 Benefit: 5 kg of free foodgrains (rice/wheat) per person per month. Plus highly subsidized sugar/oil.
  📋 Documents needed: Ration Card (Yellow), Aadhaar Cards of all family members.
  🏛️ Where to apply: Government Fair Price Shop (Ration Dealer) near you.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 1967 / 18001800150
  ⚡ How fast: Immediately, on the next month's distribution date.

  📌 PM Ujjwala Yojana 2.0 (Ministry of Petroleum & Natural Gas)
  ✅ Why you qualify: BPL household currently using traditional fuel without an LPG connection.
  💰 Benefit: Free LPG Connection, one stove, first 14.2 kg cylinder free, and a recurring subsidy of ₹300 per refill.
  📋 Documents needed: BPL Ration Card, Aadhaar, Bank Passbook, Passport photo.
  🏛️ Where to apply: Nearest LPG Distributor (Indane/HP/Bharat Gas) or [pmuy.gov.in](https://pmuy.gov.in)
  ⏰ Deadline: Ongoing.
  📱 Helpline: 1906 / 18002660300
  ⚡ How fast: 7 to 10 working days.

  📌 Ayushman Bharat - PM Jan Arogya Yojana (PM-JAY) (Ministry of Health & Family Welfare)
  ✅ Why you qualify: Rural BPL family listed in the SECC-2011 database.
  💰 Benefit: Cashless health insurance up to ₹5,000,000 (5 Lakhs) per family per year for secondary and tertiary hospitalizations.
  📋 Documents needed: PM-JAY letter, Ration Card, Aadhaar.
  🏛️ Where to apply: Empaneled Government/Private Hospital or CSC Centers.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 14555
  ⚡ How fast: Golden Card created in 1 day; hospitalization cover is instant.

  📌 Swachh Bharat Mission - Gramin (Ministry of Jal Shakti)
  ✅ Why you qualify: Rural household needing toilet support.
  💰 Benefit: Financial incentive of ₹12,000 for constructing a sanitary toilet at home.
  📋 Documents needed: Aadhaar Card, Bank Passbook, Photo of the constructed/site of toilet.
  🏛️ Where to apply: Gram Panchayat Office or Swachh Bharat Portal online.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 18001801800
  ⚡ How fast: Verification takes 15-30 days; funds are credited post-construction.

─────────────────────────────────────────────────

🌟 STATE-SPECIFIC SCHEMES (UTTAR PRADESH)

  📌 UP Mukhyamantri Krishak Durghatna Kalyan Yojana (UP Revenue Dept)
  ✅ Why you qualify: Farmer aged between 18-70 years registered in revenue records of UP.
  💰 Benefit: Financial assistance up to ₹5,000,000 (5 Lakhs) in case of accidental death/permanent disability while performing farm duties.
  📋 Documents needed: Land Khatauni, Aadhaar, FIR/Post-mortem report (in case of accident), Bank details.
  🏛️ Where to apply: District Revenue Office or Tehsil Office.
  ⏰ Deadline: Must apply within 45 days of the accident.
  📱 Helpline: 0522-2237515
  ⚡ How fast: 30-45 days post-verification.

  📌 UP Shramik Vidya Dhan Yojana (UP Labour Dept)
  ✅ Why you qualify: Children of registered labourers or BPL workers studying in classes 8-12.
  💰 Benefit: Annual scholarship of ₹6,000 to ₹12,000 for your school-going children (12, 10, and 8 years old).
  📋 Documents needed: Parent's Ration Card/Labour card, children's school admission proofs, report cards, bank accounts.
  🏛️ Where to apply: UP Labour Dept Portal or through the kids' school principal.
  ⏰ Deadline: October 30th (Apply soon, seasonal!).
  📱 Helpline: 18001805160
  ⚡ How fast: Credit happens directly to children's accounts in Jan/Feb.

─────────────────────────────────────────────────

💡 SCHEMES YOU MIGHT QUALIFY FOR

  📌 PM Awas Yojana - Gramin (PMAY-G)
  ✅ Why check: You own a house, but if it is a Kuchha (temporary mud/clay) structure, you qualify for ₹120,000 cash grant to build a Pucca house.
  🔍 What to check: Contact your Gram Sevak to see if your name is in the PMAY-G Permanent Wait List (PWL).

  📌 Kisan Credit Card (KCC)
  ✅ Why check: You are a PM-KISAN beneficiary. You can get cheap crop loans up to ₹3 Lakhs at a low interest rate of 4%.
  🔍 What to check: Visit your bank branch where you receive PM-KISAN. Fill out the simplified one-page KCC form.

─────────────────────────────────────────────────

📅 DAILY / MONTHLY ENTITLEMENTS

  🌾 Ration: 25 kg Wheat/Rice free of cost every month under PMGKAY.
  🏥 Healthcare: Free OPD checkups and baseline diagnostic tests at your local Community Health Centre (CHC) in Gorakhpur.
  💊 Free medicines: Buy generic medicines at 60-90% discount at the Jan Aushadhi Kendra located near Gorakhpur District Hospital.
  ⚡ Free electricity units: Up to 100 units free per month for BPL families under the state power scheme (contact local discom UPPCL to active BPL tariff).

─────────────────────────────────────────────────

🚨 URGENT ACTION ITEMS (DO THIS WEEK)
  1. **Activate PM-KISAN e-KYC**: Do your biometric KYC at a local CSC center to ensure your next installment is not blocked.
  2. **Register for UP Shramik Card**: Go to the UP Labour office or CSC this week to get your Shramik Card made—it opens up 15+ additional state benefits.
  3. **Apply for Ujjwala LPG Connection**: Visit the Indane/HP distributor in your area to submit the BPL ration card copy and get a free cylinder before monsoon.
  4. **Verify Aadhaar linking**: Ensure your mobile number is linked to your bank account and Jan Dhan account for smooth DBT transfers.
  5. **Get Soil Health Card**: Get a sample of your soil tested for free at the nearest agriculture center before sowing the next crop.

─────────────────────────────────────────────────

📱 USEFUL APPS & PORTALS TO DOWNLOAD NOW
  - **Mera Ration App** → Track your entitlement, check previous transactions, and find the nearest FPS store.
  - **PM-KISAN Mobile App** → Check beneficiary status, edit Aadhaar details, and check payment dates.
  - **UP Bhulekh Portal** → [upbhulekh.gov.in](https://upbhulekh.gov.in) → Download your land registry copy (Khatauni) for free.

─────────────────────────────────────────────────

💰 TOTAL ESTIMATED ANNUAL BENEFIT VALUE
  PM-KISAN (₹6,000) + Free Ration (5 members x 5kg x 12 months = 300kg grains ~ ₹9,000 value) + Healthcare insurance cover value (₹5,00,000) + Sanitation toilet grant (₹12,000) + LPG Subsidy (₹3,000) + Children scholarships (approx ₹24,000).
  
  **You could be receiving ₹4,500 per month / ₹54,000 per year** in direct benefits and subsidies, plus **₹5,00,000** emergency healthcare cover!

─────────────────────────────────────────────────

⚠️ COMMON MISTAKES TO AVOID
  - **Fake Agent Scams**: Beware of agents charging ₹500 to register for PM-KISAN. The application is completely free or costs only ₹30 at official CSC.
  - **Incomplete e-KYC**: Thousands of farmers miss their installments because they forgot to link Aadhaar with fingerprint at the center. Do it now!
  - **Wrong Land Records Document**: Do not submit old Khatauni copies. Always download the latest version from UP Bhulekh.

═══════════════════════════════════════════════════
*Aapka haq aapke dwar! Himmat mat haariye, yeh saari schemes aapke bhale ke liye hain. Yeh sab aapka haq hai!*"""



    elif "Sunita Devi" in preset_name:

        return """🎯 SCHEMES YOU DEFINITELY QUALIFY FOR

  📌 Indira Gandhi National Widow Pension Scheme (IGNWPS) (Ministry of Rural Development)
  ✅ Why you qualify: You are a widow, aged 38 (between 40-79 eligible for central, but state matches starting lower), living below the poverty line.
  💰 Benefit: ₹1,000 per month (combined central and state contribution in Maharashtra) credited directly to your bank account.
  📋 Documents needed: Death certificate of husband, Income certificate (< ₹50,000/yr), Aadhaar Card, BPL Ration Card, Bank Passbook.
  🏛️ Where to apply: Local Sanjay Gandhi Niradhar Yojana office, Collector's Office, or CSC.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 18001208040
  ⚡ How fast: 30 to 45 days after document verification.

  📌 PM Garib Kalyan Anna Yojana (PMGKAY) (Department of Food & Public Distribution)
  ✅ Why you qualify: You hold an Antyodaya Anna Yojana (AAY) Ration Card (poorest of the poor).
  💰 Benefit: 35 kg of free foodgrains (wheat and rice) per family per month, regardless of family size.
  📋 Documents needed: AAY Ration Card, Aadhaar Card of all members.
  🏛️ Where to apply: Your nearest Government Fair Price Ration Shop.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 1967
  ⚡ How fast: Instant, every monthly cycle.

  📌 Ayushman Bharat - PM Jan Arogya Yojana (PM-JAY) (Ministry of Health & Family Welfare)
  ✅ Why you qualify: BPL/AAY Card holder listed in urban SECC list.
  💰 Benefit: Fully cashless hospitalization coverage up to ₹5,00,000 (5 Lakhs) per year for your entire family.
  📋 Documents needed: Antyodaya Ration Card, Aadhaar Card.
  🏛️ Where to apply: Empaneled hospital's Ayushman Mitra counter or nearest CSC.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 14555
  ⚡ How fast: Golden Card is issued in 1 day; benefits are immediate.

  📌 PM Matru Vandana Yojana / Women's Self Help Group Loans (NRLM) (Min of Women & Child Development)
  ✅ Why you qualify: Active woman in urban area looking to start livelihood; group member.
  💰 Benefit: Collateral-free group business loans up to ₹10 Lakhs (and up to ₹20 Lakhs gradually) at subsidized interest rates of 4-7%.
  📋 Documents needed: SHG registration details, group resolution, Aadhaar Cards of members.
  🏛️ Where to apply: Local Urban Livelihood Mission (NULM) coordinator at Municipality Office.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 18001025263
  ⚡ How fast: 15-20 days.

─────────────────────────────────────────────────

🌟 STATE-SPECIFIC SCHEMES (MAHARASHTRA)

  📌 Sanjay Gandhi Niradhar Grant Scheme (Maharashtra Social Justice Dept)
  ✅ Why you qualify: Destitute widow with minor children, monthly family income less than ₹21,000.
  💰 Benefit: ₹1,500 per month directly deposited to bank.
  📋 Documents needed: Death certificate, age proof of children, income certificate from Tehsildar, Residence proof.
  🏛️ Where to apply: Tehsildar Office or Local Sethu Center.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 1800224950
  ⚡ How fast: 45 days.

  📌 Maharashtra Post-Matric Scholarship for SC Students (Social Justice & Special Asst Dept)
  ✅ Why you qualify: You belong to the SC category, and your kids (14 and 11 years) will soon enter 11th standard/college.
  💰 Benefit: 100% tuition fees reimbursement + monthly maintenance allowance for students.
  📋 Documents needed: Caste Certificate, Income Certificate (< ₹2.5 Lakhs), Marksheets, College Admission Fee Receipt.
  🏛️ Where to apply: [mahadbt.maharashtra.gov.in](https://mahadbt.maharashtra.gov.in)
  ⏰ Deadline: Applications open July to October every year.
  📱 Helpline: 022-49150800
  ⚡ How fast: Credited at the end of the academic term.

─────────────────────────────────────────────────

💡 SCHEMES YOU MIGHT QUALIFY FOR

  📌 PM Awas Yojana - Urban (PMAY-U)
  ✅ Why check: You currently live in a rented house in Pune. You can get a home loan interest subsidy of 6.5% under the Credit Linked Subsidy Scheme (CLSS) or apply for affordable partnership housing.
  🔍 What to check: Visit Pune Municipal Corporation (PMC) housing cell to check for active slum rehabilitation or EWS housing lottery schemes.

  📌 PM SVANidhi Scheme
  ✅ Why check: If you want to start a street vending business (e.g. food stall, tailors, vegetable cart).
  🔍 What to check: Get an Interest-free micro-credit loan of ₹10,000 for 1st term, escalating to ₹20,000 and ₹50,000. Apply at [pmsvanidhi.mohua.gov.in](https://pmsvanidhi.mohua.gov.in).

─────────────────────────────────────────────────

📅 DAILY / MONTHLY ENTITLEMENTS

  🌾 Ration: 35 kg foodgrains (wheat/rice/coarse grains) free of cost at Pune FPS under AAY.
  🏥 Healthcare: Free OPD visits at Pune Municipal Corporation (PMC) hospitals and dispensaries.
  💊 Generic Medicines: Cheap medicines (60-90% off) at PM Jan Aushadhi Stores near Pune Station or Sassoon Hospital.
  🚍 Free Bus Travel: Maharashtra state offers 50% discount on MSRTC state buses for women! Ensure you show a valid state ID card.

─────────────────────────────────────────────────

🚨 URGENT ACTION ITEMS (DO THIS WEEK)
  1. **Get Tehsildar Income Certificate**: Obtain a formal Income Certificate showing family income is less than ₹21,000/year, as this is required for all widow pensions.
  2. **Apply for Sanjay Gandhi Niradhar Scheme**: Submit files to the Tehsildar office this week for the ₹1,500/month widow support.
  3. **Update Aadhaar Details**: Ensure your marital status is updated, and link your phone to Aadhaar for smooth pension credit.
  4. **Open a Jan Dhan Account**: If not already done, link your zero-balance account to receive Direct Benefit Transfers (DBT).
  5. **Register children on MahaDBT**: Create profiles for your children on the Maharashtra DBT portal for upcoming educational benefits.

─────────────────────────────────────────────────

📱 USEFUL APPS & PORTALS TO DOWNLOAD NOW
  - **MahaDBT App** → The single-window portal for all Maharashtra state scholarships and caste benefits.
  - **Umang App** → Apply for Central widow pensions and track EPF or insurance claims.
  - **Mera Ration** → Register your Antyodaya card and check allocation dates.

─────────────────────────────────────────────────

💰 TOTAL ESTIMATED ANNUAL BENEFIT VALUE
  State Widow Pension (₹18,000/yr) + Free Foodgrains (35kg/month ~ ₹15,000/yr value) + Child school support/allowance (approx ₹12,000) + Free healthcare cover value (₹5,00,000).
  
  **You could be receiving ₹3,750 per month / ₹45,000 per year** in direct cash and grain subsidies, alongside **₹5,00,000** health insurance!

─────────────────────────────────────────────────

⚠️ COMMON MISTAKES TO AVOID
  - **Middlemen Scams**: Never pay anyone to fill the widow pension form. The Municipal ward officer or Tehsildar clerk is legally bound to help you for free.
  - **Delaying Death Certificate**: Ensure your late husband's death certificate is legally registered, as it is the most critical document for all applications.
  - **Inconsistent Name Spelling**: Make sure your name is spelled exactly the same way in Aadhaar, Ration Card, and Bank Passbook.

═══════════════════════════════════════════════════
*Zindagi mushkil hai, par aap akeli nahi hain. Sarkar ki madad aapka haq hai, ise zaroor lein. Yeh sab aapka haq hai!*"""



    else:

        return """🎯 SCHEMES YOU DEFINITELY QUALIFY FOR

  📌 Post-Matric Scholarship Scheme for Minorities (Ministry of Minority Affairs)
  ✅ Why you qualify: You belong to the Muslim minority community, studying in B.Sc (College/Govt inst) in Bihar, and family income is below ₹2 Lakhs/year.
  💰 Benefit: Full admission/tuition fee waiver + monthly maintenance allowance of ₹500 to ₹1,200 depending on hostel/day-scholar status.
  📋 Documents needed: Minority declaration self-certificate, Income Certificate, Caste/Community certificate, Marksheet of 12th board, Bank passbook, College fee receipt.
  🏛️ Where to apply: National Scholarship Portal (NSP) online at [scholarships.gov.in](https://scholarships.gov.in)
  ⏰ Deadline: Registration starts in July, closing date generally November 30th.
  📱 Helpline: 0120-6619540
  ⚡ How fast: Disbursed directly to your bank account after academic inspection (takes 4-6 months).

  📌 ADIP Scheme (Assistance to Disabled Persons for Purchase of Fitting Aids) (Ministry of Social Justice)
  ✅ Why you qualify: Physically challenged student with verified disability certificate.
  💰 Benefit: Free high-quality prosthetic aids, wheelchairs, crutches, or smart assistive devices to support college mobility.
  📋 Documents needed: Disability Certificate (showing > 40% disability), Aadhaar Card, Income Certificate (< ₹22,500/month for full benefit).
  🏛️ Where to apply: Local District Social Welfare Office or ALIMCO camps.
  ⏰ Deadline: Ongoing.
  📱 Helpline: 18001805122
  ⚡ How fast: Distributed at state/district camps held every 3-4 months.

  📌 PM Kaushal Vikas Yojana (PMKVY) (Ministry of Skill Development)
  ✅ Why you qualify: Youth aged 15-45 looking for job-oriented skill certification.
  💰 Benefit: 100% free industry-approved technical skill training (Coding, Telecom, Solar, etc.) + government certification + placement assistance.
  📋 Documents needed: Aadhaar Card, Education marksheets, Bank details.
  🏛️ Where to apply: Local PMKK (Pradhan Mantri Kaushal Kendra) in Darbhanga or [pmkvyofficial.org](https://pmkvyofficial.org)
  ⏰ Deadline: Ongoing.
  📱 Helpline: 08800055555
  ⚡ How fast: Courses last 3-6 months; certification is instant post exam.

─────────────────────────────────────────────────

🌟 STATE-SPECIFIC SCHEMES (BIHAR)

  📌 Bihar Mukhyamantri Nishaktata Pension Yojana (Social Welfare Dept)
  ✅ Why you qualify: Bihar resident with over 40% physical disability, no minimum age limit.
  💰 Benefit: ₹400 per month pension directly to bank account, with no income criteria limit for disabled students.
  📋 Documents needed: Disability Certificate, Aadhaar, Resident Proof, Bank Passbook.
  🏛️ Where to apply: RTPS Counter at block office or online at [serviceonline.bihar.gov.in](https://serviceonline.bihar.gov.in).
  ⏰ Deadline: Ongoing.
  📱 Helpline: 18003456262
  ⚡ How fast: 30-45 days.

  📌 Bihar Student Credit Card Scheme (MNSSBY) (Bihar Education Dept)
  ✅ Why you qualify: Bihar resident, passed 12th class, pursuing higher education in recognized college.
  💰 Benefit: Education loan up to ₹4 Lakhs at a highly subsidized interest rate of 1% (for disabled and female students, normal rate is 4%). No collateral or guarantor required.
  📋 Documents needed: 10th & 12th Marksheets, College Admission Letter, Fee Structure, Aadhaar Card, Resident Certificate, Co-applicant details.
  🏛️ Where to apply: District Registration and Counselling Centre (DRCC) Darbhanga or [7nishchay-yuvaupdesh.bihar.gov.in](https://7nishchay-yuvaupdesh.bihar.gov.in).
  ⏰ Deadline: Ongoing.
  📱 Helpline: 18003456444
  ⚡ How fast: Loan approved and disbursed in 30-45 working days.

─────────────────────────────────────────────────

💡 SCHEMES YOU MIGHT QUALIFY FOR

  📌 National Handicapped Finance and Development Corporation (NHFDC) Loans
  ✅ Why check: You are disabled and want to start a business while/after studying. You can get loans up to ₹50,000 for study or startup at just 4% interest.
  🔍 What to check: Contact State Channelising Agency (SCA) in Patna or visit [nhfdc.nic.in](http://www.nhfdc.nic.in).

  📌 PM Vidyalaxmi Scheme
  ✅ Why check: If you seek higher education outside Bihar in premier institutions. Single portal for applying to multiple education loans with interest subsidies.
  🔍 What to check: Register at [vidyalakshmi.co.in](https://www.vidyalakshmi.co.in) and check bank loan tie-ups.

─────────────────────────────────────────────────

📅 DAILY / MONTHLY ENTITLEMENTS

  🌾 Ration: 5 kg grains per family member under Bihar State Ration scheme (Orange Card).
  🏥 Healthcare: Free OPD and basic path labs at Darbhanga Medical College & Hospital (DMCH).
  💊 Free Medicines: Jan Aushadhi generic medicines at 70% discount near the DMCH gate.
  🚇 Railway Concession: Up to 75% ticket discount for orthopedically handicapped person traveling with an escort. Present your railway card at reservation counters.

─────────────────────────────────────────────────

🚨 URGENT ACTION ITEMS (DO THIS WEEK)
  1. **Get UDID (Unique Disability ID) Card**: Register online at [swavlambancard.gov.in](https://www.swavlambancard.gov.in) immediately. This card works across India for travel concessions and scheme verifications.
  2. **Obtain Tehsildar Caste & Income Certificate**: Apply via Bihar RTPS portal today, as these expire annually and are needed for NSP portal.
  3. **Register on National Scholarship Portal (NSP)**: Make your student profile and save draft before college verifies.
  4. **Open a Student Zero-Balance Account**: Open a student account linked with Aadhaar in a nationalized bank (e.g. SBI) to receive DBT scholarship directly.
  5. **Apply for Disability Pension**: Submit your details online at RTPS to activate your monthly ₹400 state pension.

─────────────────────────────────────────────────

📱 USEFUL APPS & PORTALS TO DOWNLOAD NOW
  - **NSP Mobile App** → Track minority scholarship status, check verification levels.
  - **Bihar RTPS Portal** → [serviceonline.bihar.gov.in](https://serviceonline.bihar.gov.in) → Get caste, income, and residence certificates digitally.
  - **Swavlamban App** → Apply and track your UDID card status on your phone.

─────────────────────────────────────────────────

💰 TOTAL ESTIMATED ANNUAL BENEFIT VALUE
  Minority Scholarship (₹12,000/yr) + State Disability Pension (₹4,800/yr) + State Student Credit Card Loan Potential (Value up to ₹4,00,000 at 1% interest) + Travel/Rail Concession savings (Approx ₹5,000).
  
  **You could be receiving ₹1,400 per month / ₹16,800 per year** in direct grants, alongside access to **₹4,00,000** interest-subsidized student credit!

─────────────────────────────────────────────────

⚠️ COMMON MISTAKES TO AVOID
  - **Double Scholarship Registration**: Never apply for two scholarships simultaneously (e.g. state scheme and national scheme). Doing so leads to rejection of both and blacklisting on NSP.
  - **Mismatched Bank Account**: The bank account for scholarship MUST be in your own name and actively linked to Aadhaar. Do not give parent's bank details.
  - **Missing College Deadlines**: Colleges have internal verification deadlines on NSP which are 10 days before the national deadline. Submit early!

═══════════════════════════════════════════════════
*Padhai hi aage badhne ki seedhi hai. Apni sh शारीरिक chunauti ko badha mat banne dijiye, sarkar aapke sath hai. Yeh sab aapka haq hai!*"""







def query_groq_api(api_key, model_name, user_profile):

    """Sends the profile to the Groq Chat Completion API and returns the advice."""

    url = "https://api.groq.com/openai/v1/chat/completions"



    headers = {

        "Authorization": f"Bearer {api_key}",

        "Content-Type": "application/json"

    }





    profile_str = f"""
=== APPLIER IDENTITY ===
Name: {user_profile.get('applier_name', 'N/A')}
Email: {user_profile.get('applier_email', 'N/A')}
Mobile: {user_profile.get('applier_mobile', 'N/A')}
Government ID Type: {user_profile.get('applier_govt_id_type', 'N/A')}
Government ID Number: {user_profile.get('applier_govt_id_val', 'N/A')}

=== DEMOGRAPHICS ===
Age: {user_profile.get('age')}
Gender: {user_profile.get('gender')}
Category: {user_profile.get('category')}
Religion: {user_profile.get('religion')}
Disability: {user_profile.get('disability')}
Marital Status: {user_profile.get('marital_status')}

=== LOCATION ===
State: {user_profile.get('state')}
District: {user_profile.get('district')}
Area Type: {user_profile.get('area_type')}
BPL Card Holder: {user_profile.get('bpl_card')}
Ration Card Type: {user_profile.get('ration_card')}

=== FINANCIALS ===
Annual Family Income: ₹{user_profile.get('income')}
Land Ownership: {user_profile.get('land')}
Bank Account Holder: {user_profile.get('bank_account')}
Jan Dhan Account Holder: {user_profile.get('jan_dhan')}
Home Ownership: {user_profile.get('home_ownership')}

=== EDUCATION ===
Highest Qualification: {user_profile.get('education')}
Currently Studying: {user_profile.get('currently_studying')}
Current Class/Course: {user_profile.get('study_class') if user_profile.get('currently_studying') == 'Yes' else 'N/A'}
Institution Type: {user_profile.get('study_inst_type') if user_profile.get('currently_studying') == 'Yes' else 'N/A'}
Children Education Status: {user_profile.get('children_edu')}

=== EMPLOYMENT ===
Employment Status: {user_profile.get('employment')}
Farmer Specifics:
  - Farming Type: {user_profile.get('farmer_type')}
  - Land Size: {user_profile.get('farmer_land')}
  - Crops Grown: {user_profile.get('farmer_crops')}
Business Specifics:
  - MSME Registered: {user_profile.get('msme_reg')}
  - Annual Turnover: ₹{user_profile.get('msme_turnover')}

=== FAMILY INFO ===
Family Members Count: {user_profile.get('family_members')}
Children Count: {user_profile.get('children_count')}
Children Ages: {user_profile.get('children_ages')}
Pregnant Woman in Family: {user_profile.get('pregnant_woman')}
Senior Citizen in Family: {user_profile.get('senior_citizen')} (Age: {user_profile.get('senior_citizen_age')} if Yes)
Single Parent Household: {user_profile.get('single_parent')}

=== CRITICAL DAILY LIFE NEEDS ===
{", ".join(user_profile.get('needs', [])) if user_profile.get('needs') else 'None checked'}
"""



    system_prompt = """You are Sahayak, an expert Indian government policy advisor and social welfare consultant.
Your job is to help Indian citizens discover every government scheme, benefit,
subsidy, and entitlement they qualify for — both Central and State level.

Use simple, respectful language and mix Hindi words naturally in a friendly manner. You sound like a helpful neighbour who knows everything about government schemes (e.g. "Aapko yeh scheme zaroor milni chahiye", "Hum aapko guide karenge").
Do NOT use complex legal or official jargon. Explain benefits in simple terms.
Always give exact benefit amounts (e.g., "₹6,000 per year" rather than "financial assistance").
Always give exact portal URLs and helpline numbers.
Always check and mention if something has a deadline THIS MONTH.
Flag if any of their documents might be expiring soon.
Remind about seasonal schemes (Rabi/Kharif crop cycles for farmers, scholarship intake months, etc.).
End with encouraging words, specifically: "Yeh sab aapka haq hai!"

You must match the following output structure EXACTLY, including the horizontal dividing lines and icon headers. Do not output anything else before or after.

🎯 SCHEMES YOU DEFINITELY QUALIFY FOR
(List each scheme with ALL of these details. Ensure to cover relevant central schemes from the requested list: food, health, education, housing, etc.)

  📌 Scheme Name (Ministry/Department)
  ✅ Why you qualify: [specific reason based on their profile]
  💰 Benefit: [exact amount / what you get]
  📋 Documents needed: [exact list]
  🏛️ Where to apply: [exact office / portal URL]
  ⏰ Deadline: [if any, or "ongoing"]
  📱 Helpline: [phone number]
  ⚡ How fast: [how long it takes to get benefit]

─────────────────────────────────────────────────

🌟 STATE-SPECIFIC SCHEMES
(Provide state-specific schemes corresponding to the user's selected state in the same format)

─────────────────────────────────────────────────

💡 SCHEMES YOU MIGHT QUALIFY FOR
(Schemes where eligibility is slightly unclear or requires checking details, explain what to check)

─────────────────────────────────────────────────

📅 DAILY / MONTHLY ENTITLEMENTS
(Things they can use RIGHT NOW, every day/month: Ration allowances, free OPD, cheap medicines at Jan Aushadhi, bus passes, rail concession, seasonal dates, etc.)

─────────────────────────────────────────────────

🚨 URGENT ACTION ITEMS (DO THIS WEEK)
  1. [Most time-sensitive scheme / deadline approaching]
  2. [Easiest scheme to apply for right now]
  3. [Highest value benefit they're missing]
  4. [Document they should get made immediately]
  5. [Portal to register on today]

─────────────────────────────────────────────────

📱 USEFUL APPS & PORTALS TO DOWNLOAD NOW
  - App name → what to do on it
  - Portal name → link → what to check

─────────────────────────────────────────────────

💰 TOTAL ESTIMATED ANNUAL BENEFIT VALUE
  Add up all cash transfers + subsidies + free services
  Show: "You could be receiving ₹X,XXX per month / ₹XX,XXX per year"

─────────────────────────────────────────────────

⚠️ COMMON MISTAKES TO AVOID
  - Scams to watch out for related to these schemes
  - Documents people often submit wrong
  - Deadlines people commonly miss
"""



    payload = {

        "model": model_name,

        "messages": [

            {"role": "system", "content": system_prompt},

            {"role": "user", "content": profile_str}

        ],

        "temperature": 0.2,

        "max_tokens": 4096

    }



    try:

        response = requests.post(url, headers=headers, json=payload, timeout=45)

        response.raise_for_status()

        res_data = response.json()

        return res_data["choices"][0]["message"]["content"]

    except requests.exceptions.HTTPError as he:

        if response.status_code == 401:

            return "❌ Error: Invalid Groq API Key! Please double-check the API key in the sidebar."

        else:

            return f"❌ HTTP Error connecting to Groq: {he}"

    except Exception as e:

        return f"❌ Unexpected error connecting to Groq: {e}"









st.markdown("""
<div class="header-banner">
    <h1>🤝 SAHAYAK</h1>
    <p>Aapka Sarkar Benefit Finder — Central & State Government Scheme Advisor</p>
</div>
""", unsafe_allow_html=True)





with st.sidebar:

    st.markdown("### ⚙️ App Configuration")





    api_key_input = st.text_input(

        "Groq API Key (Optional)",

        value=st.session_state["groq_api_key"],

        type="password",

        placeholder="Using Sahayak advisor key (hidden)",

        help="Leave blank to use the built-in Sahayak advisor key, or enter your own Groq API key."

    )

    if api_key_input:

        st.session_state["groq_api_key"] = api_key_input





    model_choice = st.selectbox(

        "Select AI Model",

        options=["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "qwen/qwen3-32b"],

        index=0,

        help="Llama 3.3 70B is highly recommended for complex logic."

    )



    st.markdown("---")

    st.markdown("### 📋 Demo Preset Profiles")

    st.markdown("Select a preset to auto-fill the forms instantly. Great for testing!")



    preset_selected = st.selectbox(

        "Load Preset Profile",

        options=["-- Select a Preset --"] + list(PRESETS.keys())

    )



    if preset_selected != "-- Select a Preset --":

        if st.button("Load Preset Data"):

            load_preset(preset_selected)



    st.markdown("---")

    st.markdown("""
    **💡 Tip for Users:**
    Once you fill out the *Applier Profile* and the *Eligibility Inputs*, click **"Dhoondhein Schemes"** (Find Schemes) to generate your customized scheme advisory report.
    
    *Yeh sab aapka haq hai!* 🇮🇳
    """)





tab_profile, tab_inputs, tab_results = st.tabs([

    "👤 1. Applier Profile Card",

    "📋 2. Eligibility Details",

    "🎯 3. Recommended Schemes"

])





with tab_profile:

    st.subheader("Applier Identity Profile")

    st.info("Enter the applicant's contact details, government ID, and upload a profile picture. We will generate a digital Sahayak Identity Card for you.")



    col_card_inputs, col_card_preview = st.columns([1, 1])



    with col_card_inputs:

        st.markdown("#### Fill Applicant Credentials")



        name = st.text_input("Full Name", value=st.session_state["applier_name"], key="applier_name", placeholder="e.g. Ramesh Kumar")

        email = st.text_input("Email Address", value=st.session_state["applier_email"], key="applier_email", placeholder="e.g. ramesh@gmail.com")

        mobile = st.text_input("Mobile Number", value=st.session_state["applier_mobile"], key="applier_mobile", placeholder="e.g. 9876543210")



        col_id_type, col_id_val = st.columns([1, 1])

        with col_id_type:

            govt_id_type = st.selectbox(

                "Government ID Type",

                options=["Aadhaar Card", "PAN Card", "Voter ID Card", "Ration Card", "Passport", "Driving License"],

                key="applier_govt_id_type"

            )

        with col_id_val:

            govt_id_val = st.text_input("Govt ID Number", value=st.session_state["applier_govt_id_val"], key="applier_govt_id_val", placeholder="e.g. 1234-5678-9012")



        pfp_file = st.file_uploader("Upload Profile Picture", type=["png", "jpg", "jpeg"], help="Optional: Upload photo to add it to your Digital Card")

        if pfp_file:

            st.session_state["applier_pfp"] = pfp_file



    with col_card_preview:

        st.markdown("#### Digital Benefit Card Preview")





        pfp_base64 = get_image_base64(st.session_state["applier_pfp"])





        card_html = textwrap.dedent(f"""
        <div style="
            background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
            border-radius: 16px;
            padding: 24px;
            color: white;
            font-family: 'Outfit', sans-serif;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
            max-width: 450px;
            margin: 10px auto;
            position: relative;
            overflow: hidden;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.2); padding-bottom: 10px; margin-bottom: 15px;">
                <div>
                    <h4 style="margin: 0; font-weight: 700; letter-spacing: 1px; color: #ff9933; font-size: 1.1rem;">SAHAYAK</h4>
                    <span style="font-size: 10px; text-transform: uppercase; color: #34d399; font-weight: 600;">Government Benefits Card</span>
                </div>
                <div style="font-size: 9px; font-weight: 600; background: rgba(255,255,255,0.2); padding: 3px 8px; border-radius: 4px; color: #fff;">
                    VERIFIED
                </div>
            </div>
            
            <div style="display: flex; gap: 20px;">
                <div>
                    <img src="{pfp_base64}" style="width: 90px; height: 90px; border-radius: 12px; border: 2px solid white; object-fit: cover; background: #fff;" />
                </div>
                <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: space-between;">
                    <div>
                        <div style="font-size: 9px; opacity: 0.8; letter-spacing: 0.5px;">FULL NAME</div>
                        <div style="font-size: 16px; font-weight: 600; margin-bottom: 5px; text-transform: uppercase;">{name if name else "APPLICANT NAME"}</div>
                        
                        <div style="font-size: 9px; opacity: 0.8; letter-spacing: 0.5px;">GOVT ID ({govt_id_type})</div>
                        <div style="font-size: 13px; font-weight: 500; font-family: monospace; margin-bottom: 5px;">{govt_id_val if govt_id_val else "XXXX-XXXX-XXXX"}</div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 9px; opacity: 0.8; margin-top: 5px;">
                        <div>
                            <div>MOBILE</div>
                            <div style="font-weight: 600; font-size: 10px; color: white;">{mobile if mobile else "9876XXXXXX"}</div>
                        </div>
                        <div>
                            <div>EMAIL</div>
                            <div style="font-weight: 600; font-size: 10px; color: white;">{email if email else "not@provided.com"}</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-top: 15px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px;">
                <div>
                    <div style="font-size: 7px; opacity: 0.6;">DIGITAL SIGNATURE Verified</div>
                    <div style="font-size: 9px; font-weight: 600; font-family: monospace; letter-spacing: 1.5px; margin-top: 2px; color: #ffb74d;">AGY-SHY-{mobile[-4:] if (mobile and len(mobile) >= 4) else "0000"}</div>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-end;">
                    <svg style="width: 100px; height: 25px; filter: invert(1);">
                        <rect x="0" width="2" height="25" fill="black"/>
                        <rect x="3" width="1" height="25" fill="black"/>
                        <rect x="5" width="4" height="25" fill="black"/>
                        <rect x="10" width="2" height="25" fill="black"/>
                        <rect x="14" width="1" height="25" fill="black"/>
                        <rect x="16" width="3" height="25" fill="black"/>
                        <rect x="20" width="2" height="25" fill="black"/>
                        <rect x="23" width="1" height="25" fill="black"/>
                        <rect x="25" width="4" height="25" fill="black"/>
                        <rect x="30" width="2" height="25" fill="black"/>
                        <rect x="33" width="1" height="25" fill="black"/>
                        <rect x="35" width="3" height="25" fill="black"/>
                        <rect x="40" width="2" height="25" fill="black"/>
                        <rect x="44" width="1" height="25" fill="black"/>
                        <rect x="46" width="4" height="25" fill="black"/>
                        <rect x="52" width="2" height="25" fill="black"/>
                        <rect x="55" width="1" height="25" fill="black"/>
                        <rect x="58" width="3" height="25" fill="black"/>
                        <rect x="63" width="2" height="25" fill="black"/>
                        <rect x="66" width="1" height="25" fill="black"/>
                        <rect x="68" width="4" height="25" fill="black"/>
                        <rect x="73" width="2" height="25" fill="black"/>
                        <rect x="76" width="1" height="25" fill="black"/>
                        <rect x="78" width="3" height="25" fill="black"/>
                        <rect x="83" width="2" height="25" fill="black"/>
                        <rect x="86" width="1" height="25" fill="black"/>
                        <rect x="88" width="4" height="25" fill="black"/>
                        <rect x="94" width="2" height="25" fill="black"/>
                        <rect x="97" width="3" height="25" fill="black"/>
                    </svg>
                    <span style="font-size: 6px; opacity: 0.7; margin-top: 2px; letter-spacing: 0.5px;">SECURE DIGITAL BENEFITS CARD</span>
                </div>
            </div>
        </div>
        """)



        card_html_clean = "\n".join([line.strip() for line in card_html.split("\n") if line.strip()])

        st.markdown(card_html_clean, unsafe_allow_html=True)

        st.markdown("<p style='text-align:center;font-size:0.8rem;color:#6b7280;'>*This digital card represents your active eligibility profile in Sahayak database.*</p>", unsafe_allow_html=True)





with tab_inputs:

    st.subheader("Scheme Eligibility Parameters")

    st.markdown("Provide your profile criteria below. Our government consultant AI uses these to filter matching schemes.")





    col1, col2 = st.columns(2)

    with col1:

        st.markdown("#### 👤 Personal Details")

        st.number_input("Age", min_value=0, max_value=120, value=st.session_state["age"], key="age")

        st.selectbox("Gender", options=["Male", "Female", "Transgender"], key="gender")

        st.selectbox("Category", options=["General", "OBC", "SC", "ST", "EWS", "Minority"], key="category")

        st.selectbox("Religion", options=["Hinduism", "Islam", "Christianity", "Sikhism", "Buddhism", "Jainism", "Others"], key="religion")

        st.selectbox("Disability Status", options=["None", "Physical", "Visual", "Hearing", "Mental"], key="disability")

        st.selectbox("Marital Status", options=["Single", "Married", "Widow", "Divorced"], key="marital_status")



    with col2:

        st.markdown("#### 📍 Location Details")

        st.selectbox("State / UT", options=INDIAN_STATES, key="state")

        st.text_input("District Name", value=st.session_state["district"], key="district", placeholder="e.g. Gorakhpur")

        st.selectbox("Area Type", options=["Urban", "Rural", "Tribal"], key="area_type")

        st.selectbox("BPL Card Holder?", options=["Yes", "No"], key="bpl_card")

        st.selectbox("Ration Card Type", options=["None", "White", "Yellow", "Orange", "Antyodaya"], key="ration_card")



    st.markdown("---")





    col3, col4 = st.columns(2)

    with col3:

        st.markdown("#### 💰 Financial Details")

        st.number_input("Annual Family Income (₹)", min_value=0, max_value=100000000, value=st.session_state["income"], step=5000, key="income")

        st.selectbox("Land Ownership", options=["None", "Less than 1 acre", "1-5 acres", "5+ acres"], key="land")

        st.selectbox("Do you have a regular Bank Account?", options=["Yes", "No"], key="bank_account")

        st.selectbox("Do you have a Jan Dhan Account?", options=["Yes", "No"], key="jan_dhan")

        st.selectbox("Home Ownership Status", options=["Owned", "Rented", "Homeless"], key="home_ownership")



    with col4:

        st.markdown("#### 🎓 Education Details")

        st.selectbox("Highest Qualification", options=["Illiterate", "Below Matric", "Matric (10th)", "Higher Secondary (12th)", "Graduate", "Post Graduate", "Professional"], key="education")

        st.selectbox("Are you currently studying?", options=["Yes", "No"], key="currently_studying")





        if st.session_state["currently_studying"] == "Yes":

            st.text_input("Class / Course Name", value=st.session_state["study_class"], key="study_class", placeholder="e.g. B.Sc Physics 1st Year")

            st.selectbox("Institution Type", options=["Govt", "Private"], key="study_inst_type")



        st.selectbox("Children's Education Status", options=["Not Applicable", "All studying", "Some studying", "Not studying", "None in school age"], key="children_edu")



    st.markdown("---")





    col5, col6 = st.columns(2)

    with col5:

        st.markdown("#### 💼 Employment Details")

        emp_status = st.selectbox(

            "Employment Status",

            options=["Student", "Unemployed", "Self-employed", "Private job", "Govt job", "Daily wage worker", "Farmer", "Migrant worker", "Gig worker", "MSME owner"],

            key="employment"

        )





        if emp_status == "Farmer":

            st.selectbox("Type of Farming", options=["Marginal (< 1 hectare)", "Small (1-2 hectares)", "Semi-medium (2-4 hectares)", "Medium (4-10 hectares)", "Large (> 10 hectares)"], key="farmer_type")

            st.text_input("Exact Land Holding Size", value=st.session_state["farmer_land"], key="farmer_land", placeholder="e.g. 2 acres")

            st.text_input("Primary Crops Grown", value=st.session_state["farmer_crops"], key="farmer_crops", placeholder="e.g. Rice, Wheat, sugarcane")





        elif emp_status == "MSME owner":

            st.selectbox("Registered with Udyam/MSME Portal?", options=["Yes", "No"], key="msme_reg")

            st.number_input("Annual Business Turnover (₹)", min_value=0, value=st.session_state["msme_turnover"], step=10000, key="msme_turnover")



    with col6:

        st.markdown("#### 👨‍👩‍👧 Family Details")

        st.number_input("Total family members in household", min_value=1, max_value=30, value=st.session_state["family_members"], key="family_members")

        st.number_input("Number of Children", min_value=0, max_value=15, value=st.session_state["children_count"], key="children_count")



        if st.session_state["children_count"] > 0:

            st.text_input("Ages of Children (comma separated)", value=st.session_state["children_ages"], key="children_ages", placeholder="e.g. 12, 10, 8")



        st.selectbox("Is there any pregnant/lactating woman in family?", options=["Yes", "No"], key="pregnant_woman")

        st.selectbox("Any senior citizen (60+ yrs) in family?", options=["Yes", "No"], key="senior_citizen")



        if st.session_state["senior_citizen"] == "Yes":

            st.number_input("Senior Citizen's Age", min_value=60, max_value=120, value=st.session_state["senior_citizen_age"], key="senior_citizen_age")



        st.selectbox("Is this a Single Parent Household?", options=["Yes", "No"], key="single_parent")



    st.markdown("---")

    st.markdown("#### 🛍️ Daily Life Needs (Check all that apply)")





    needs_checked = []

    col_needs_1, col_needs_2 = st.columns(2)



    half_index = len(DAILY_NEEDS_OPTIONS) // 2



    with col_needs_1:

        for option in DAILY_NEEDS_OPTIONS[:half_index]:

            default_val = option in st.session_state["needs"]

            if st.checkbox(option, value=default_val, key=f"need_{option.replace(' ', '_')}"):

                needs_checked.append(option)

    with col_needs_2:

        for option in DAILY_NEEDS_OPTIONS[half_index:]:

            default_val = option in st.session_state["needs"]

            if st.checkbox(option, value=default_val, key=f"need_{option.replace(' ', '_')}"):

                needs_checked.append(option)



    st.session_state["needs"] = needs_checked



    st.markdown("<br>", unsafe_allow_html=True)





    if st.button("🔍 DHOONDHEIN SCHEMES (FIND ELIGIBLE SCHEMES)", type="primary", use_container_width=True):

        profile_data = {

            "applier_name": st.session_state["applier_name"],

            "applier_email": st.session_state["applier_email"],

            "applier_mobile": st.session_state["applier_mobile"],

            "applier_govt_id_type": st.session_state["applier_govt_id_type"],

            "applier_govt_id_val": st.session_state["applier_govt_id_val"],

            "age": st.session_state["age"],

            "gender": st.session_state["gender"],

            "category": st.session_state["category"],

            "religion": st.session_state["religion"],

            "disability": st.session_state["disability"],

            "marital_status": st.session_state["marital_status"],

            "state": st.session_state["state"],

            "district": st.session_state["district"],

            "area_type": st.session_state["area_type"],

            "bpl_card": st.session_state["bpl_card"],

            "ration_card": st.session_state["ration_card"],

            "income": st.session_state["income"],

            "land": st.session_state["land"],

            "bank_account": st.session_state["bank_account"],

            "jan_dhan": st.session_state["jan_dhan"],

            "home_ownership": st.session_state["home_ownership"],

            "education": st.session_state["education"],

            "currently_studying": st.session_state["currently_studying"],

            "study_class": st.session_state.get("study_class", ""),

            "study_inst_type": st.session_state.get("study_inst_type", ""),

            "children_edu": st.session_state["children_edu"],

            "employment": st.session_state["employment"],

            "farmer_type": st.session_state.get("farmer_type", ""),

            "farmer_land": st.session_state.get("farmer_land", ""),

            "farmer_crops": st.session_state.get("farmer_crops", ""),

            "msme_reg": st.session_state.get("msme_reg", ""),

            "msme_turnover": st.session_state.get("msme_turnover", 0),

            "family_members": st.session_state["family_members"],

            "children_count": st.session_state["children_count"],

            "children_ages": st.session_state.get("children_ages", ""),

            "pregnant_woman": st.session_state["pregnant_woman"],

            "senior_citizen": st.session_state["senior_citizen"],

            "senior_citizen_age": st.session_state.get("senior_citizen_age", 60),

            "single_parent": st.session_state["single_parent"],

            "needs": st.session_state["needs"]

        }





        with st.spinner("🔍 Dhoondh rahe hain aapke liye behtareen schemes... Please wait..."):

            active_key = st.session_state["groq_api_key"].strip()

            if not active_key:

                active_key = _get_key()



            if active_key:



                response_text = query_groq_api(active_key, model_choice, profile_data)

                st.session_state["results_md"] = response_text

            else:



                matched_preset = None

                for pname in PRESETS.keys():

                    if PRESETS[pname]["applier_name"] == st.session_state["applier_name"]:

                        matched_preset = pname

                        break



                if matched_preset:

                    st.toast("Running in Simulation Mode using offline database...", icon="ℹ️")

                    st.session_state["results_md"] = get_mock_response(matched_preset)

                else:

                    st.warning("⚠️ Groq API Key was not entered in the sidebar! Since this is a custom profile, please enter a valid Groq API Key to perform live matching.")



        if st.session_state["results_md"]:

            st.success("🎉 Recommendations generated successfully!")



            st.rerun()





with tab_results:

    st.subheader("Your Custom Scheme Finder Advisory Report")



    if not st.session_state["results_md"]:

        st.info("ℹ️ No reports generated yet. Please enter your profile in Tabs 1 & 2, then click the **'Dhoondhein Schemes'** button to receive matches!")

    else:



        is_error = st.session_state["results_md"].startswith("❌")



        if is_error:

            st.error(st.session_state["results_md"])

        else:



            col_lbl, col_dl = st.columns([3, 1])

            with col_lbl:

                st.write("Below is the official customized report prepared by Sahayak Consultant:")

            with col_dl:

                st.download_button(

                    label="📥 Download Advisory Report",

                    data=st.session_state["results_md"],

                    file_name=f"Sahayak_Scheme_Report_{st.session_state['applier_name'].replace(' ', '_') if st.session_state['applier_name'] else 'Applicant'}.md",

                    mime="text/markdown",

                    use_container_width=True

                )



            st.markdown("---")







            raw_content = st.session_state["results_md"]















            st.markdown(raw_content)



            st.markdown("---")

            st.success("🇮🇳 *Disclaimer: This report is generated dynamically by Sahayak welfare engine. Always consult the official CSC center or government portal before final submission.*")

