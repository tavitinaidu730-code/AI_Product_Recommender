import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import base64
# ====== Load Environment Variables ======
load_dotenv()

# ====== Configure Gemini API ======
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("❌ Google Gemini API key not found. Please add it to your .env file as GEMINI_API_KEY.")
    st.stop()

genai.configure(api_key=api_key)

# ====== Streamlit Page Config ======
st.set_page_config(page_title="AI Product Recommender", page_icon="🛒", layout="wide")

# ====== Custom CSS for Modern UI with Dark Background ======
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        background-color: #1a1a1a;  /* 🔹 Light black background */
        color: #f5f5f5;
    }

    .main-title {
        font-size: 40px;
        font-weight: 700;
        background: linear-gradient( to right,  #B9FADD, #4A7EF7, #0A418F);
        color: white;
        padding: 20px;
        border-radius: 12px;
        display: inline-block;
        text-align: center;
        box-shadow: 0 3px 15px rgba(0, 0, 0, 0.3);
    }

    .title-container {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 20px;
    }

    .logo {
        height: 2px;
        width: 2px;
    }

    .subtitle {
        text-align: center;
        color: #707070;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .response-title {
        color: #60A5FA;
        font-size: 22px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .response-box {
        background: #2e2e2e;
        border-radius: 15px;
        padding: 25px;
        margin-top: 30px;
        box-shadow: 0 3px 20px rgba(0,0,0,0.4);
        border-left: 6px solid #2563EB;
        max-width: 900px;
        margin-left: auto;
        margin-right: auto;
    }

    .footer {
        text-align: center;
        margin-top: 50px;
        font-size: 13px;
        color: #9ca3af;
    }

    hr {
        border: 0;
        height: 1px;
        background: #374151;
        margin-top: 10px;
        margin-bottom: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# ====== Header with Logo Space ======
logo_path = "company_logo.png"  # ensure this image exists

def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Encode logo if it exists
if os.path.exists(logo_path):
    logo_base64 = get_image_base64(logo_path)
    logo_html = f"<img src='data:image/png;base64,{logo_base64}' class='logo' />"
else:
    logo_html = "<div style='width:40px;height:40px;background:#333;border-radius:2px;'></div>"

# Title + Logo UI
st.markdown(f"""
    <style>
        .logo {{
            height: 40px;          /* 🔹 Adjust image size */
            width: auto;
        }}
        .main-title {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 25px;             /* 🔹 Space between logo and title */
            font-size: 42px;
            font-weight: 700;
            color: white;
            background-color: #2563EB; /* optional: background color for title bar */
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }}
    </style>

    <div class="main-title">
        {logo_html}
        AI Product Recommender Chatbot
    </div>
""", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Discover the perfect product based on your needs, preferences, and budget.</p>", unsafe_allow_html=True)
#st.markdown("<hr>", unsafe_allow_html=True)

# ====== Load Product Catalog ======
try:
    with open("products.json", "r") as f:
        products = json.load(f)
    for product in products:
        if isinstance(product.get("price"), (int, float)):
            product["price"] = f"${product['price']:,}"
except FileNotFoundError:
    st.error("❌ products.json not found. Please make sure it's in the same folder.")
    st.stop()

# ====== Input Section ======
#st.write("💬 Describe your need, product name, or use case — I'll recommend the best match!")
#query = st.text_input("", placeholder="Example: I need a laptop for video editing and gaming under $1200")

st.write("💬 Describe your need, product name, or use case — I'll recommend the best match!")
query = st.text_input(
    "Enter your query:", 
    placeholder="Example: I need a laptop for video editing and gaming under $1200",
    label_visibility="collapsed"
)

# ====== Response Section ======
if query:
    with st.spinner("🤖 Thinking... please wait..."):
        prompt = f"""
        You are an intelligent product recommender assistant.
        You have access to the following product catalog:
        {json.dumps(products, indent=2)}

        The user asked: "{query}"

        Analyze and classify the query as:
        1. Exact match (if product name is mentioned),
        2. Closest match (if features are described), or
        3. Application-based (if use case is described).

        Recommend best products from the catalog.
        Provide a short justification (2–3 sentences) explaining why it's the best fit.
        Include price and main features.
        """

        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)

    #st.markdown("<div class='response-box'>", unsafe_allow_html=True)
    st.markdown("<div class='response-title'>🧠 Recommended Product(s):</div>", unsafe_allow_html=True)
    st.markdown(response.text, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info("Please enter your product query above to get recommendations.")

# ====== Footer ======
st.markdown("<p class='footer'>💡 Designed By Taviti Naidu | IncubXperts </p>", unsafe_allow_html=True)
