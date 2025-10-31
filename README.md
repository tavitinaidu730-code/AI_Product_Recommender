# 🛍️ AI Product Recommender Chatbot (Google Gemini)

A lightweight chatbot that recommends products from a JSON catalog using Google's Gemini AI.

---

## 🚀 Setup

1. Clone or extract the folder:
   ```bash
   cd AI_Product_Recommender_Gemini
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

4. Get your free Gemini API key:
   👉 https://aistudio.google.com/app/apikey

5. Enter the API key and ask:
   - “Show me Acer Nitro 5”
   - “Laptop for gaming and editing under $1200”
   - “Laptop for students”

---

## 🧠 Features
- Handles 3 query types (exact, feature, use-case)
- Suggests 1–2 products with explanation
- Lightweight UI with Streamlit
- Uses Google Gemini (no paid API)
