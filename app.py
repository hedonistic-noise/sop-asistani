import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI SOP Consultant Pro",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS HACK (TEMİZLİK MODU) ---
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            section[data-testid="stSidebar"] {display: none;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- APP VARIABLES ---
# Buradaki Şifre, müşteriye 499 TL ödeme yapınca maille gidecek olan şifre olmalı.
PATRON_SIFRESI_TEST = "PROUPGRADE499" 
# Buraya Shopier/PayTR/Iyzico'dan oluşturacağın 499 TL'lik ürünün linkini koy!
PAYMENT_LINK = "https://shopier.com/pro-academic-sop-499tl" 

if 'model_name' not in st.session_state:
    st.session_state['model_name'] = "gemini-1.5-flash"

# --- MAIN CONTENT ---
st.title("🎓 AI Statement of Purpose (SOP) Specialist")
st.markdown("Generate a highly persuasive, Ivy League-standard Statement of Purpose in seconds.")
st.markdown("---")

# FİYATLANDIRMA VE PLAN SEÇİMİ
st.subheader("Choose Your Plan:")

col_plan1, col_plan2 = st.columns(2)

with col_plan1:
    st.markdown("### 🥉 Basic (Flash) Plan")
    st.markdown("**:green[199 TL]** (~6 USD)")
    st.markdown("- Fast, error-free letter.")
    st.markdown("- Basic academic tone.")
    st.button("Continue with Basic Model", on_click=lambda: st.session_state.update(model_name="gemini-1.5-flash"), use_container_width=True)

with col_plan2:
    st.markdown("### 🥇 Pro (Academic) Plan")
    st.markdown("**:orange[499 TL]** (~16 USD)")
    st.markdown("- **Gemini 1.5 Pro** for deep analysis.")
    st.markdown("- High acceptance rate potential, persuasive narrative.")
    # Ödeme Linki, Müşteriyi doğrudan Shopier'a yönlendirir.
    st.markdown(f'<a href="{PAYMENT_LINK}" target="_blank"><button style="background-color: #FFA500; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; width: 100%;">Upgrade to Pro (499 TL) ➡️</button></a>', unsafe_allow_html=True)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Applicant Details")
    target_program = st.text_input("Target University & Program", placeholder="e.g. TU Munich, MSc Data Science")
    user_background = st.text_area("Academic & Professional Background", placeholder="e.g. Graduated from Yildiz Tech (GPA 3.2), 2 years Python dev experience...", height=150)
    key_achievements = st.text_area("Key Achievements & Projects", placeholder="e.g. Won a hackathon, published a paper, IELTS 7.5...", height=100)
    future_goals = st.text_input("Future Career Goals", placeholder="e.g. Become an AI specialist in the automotive sector.")
    
    st.markdown("### 🔑 Pro Code Activation")
    # PREMIUM ERİŞİM KODU KUTUSU
    premium_code_input = st.text_input("Enter Pro Access Code:", type="password", help="Enter the code received after 499 TL payment.")
    
    generate_btn = st.button(f"🚀 Generate Letter with {st.session_state['model_name'].split('-')[-1].upper()}", type="primary", use_container_width=True)

with col2:
    st.subheader("📄 Your Professional Letter")
    
    # KULLANILAN MODELİ GÖSTERME
    st.markdown(f"**Current Model:** **:blue[{st.session_state['model_name'].split('-')[-1].upper()}]**")
    
    if generate_btn:
        if "GOOGLE_API_KEY" in st.secrets:
            api_key = st.secrets["GOOGLE_API_KEY"]
        else:
            st.error("🚨 Admin Config Error: API Key not found in Secrets.")
            st.stop()

        if not target_program or not user_background:
            st.warning("⚠️ Please fill in the required fields.")
        else:
            try:
                # KOD KONTROLÜ VE MODEL GÜNCELLEMESİ
                model_to_use = st.session_state['model_name']
                
                # SADECE TEST İÇİN KULLANILACAK ŞİFRE KONTROLÜ
                if premium_code_input == PATRON_SIFRESI_TEST: 
                    model_to_use = "gemini-1.5-pro"
                    st.success("✅ PRO Model Activated! Generating a superior quality letter...")
                
                # GEMINI CONFIGURATION
                genai.configure(api_key=api_key)
                
                # SYSTEM INSTRUCTION
                system_instruction = """
                Role: You are a Senior Academic Admissions Consultant with 20+ years of experience in Ivy League admissions.
                Objective: Write a highly persuasive, unique, and professional Statement of Purpose (SOP).
                Tone: Academic, Professional, Persuasive, Authentic. No AI cliches.
                Structure:
                1. Hook (Engaging opening)
                2. Academic Background (Connected to the field)
                3. Professional Experience (Real world application)
                4. Why This University? (Specific alignment)
                5. Future Goals & Conclusion.
                Language: Write in flawless C1/C2 Academic English.
                """
                
                # MODEL SELECTION (Seçilen modeli kullanıyoruz)
                model = genai.GenerativeModel(
                    model_name=model_to_use, 
                    system_instruction=system_instruction
                )
                
                # USER PROMPT
                user_prompt = f"""
                Target Program: {target_program}
                User Background: {user_background}
                Key Achievements: {key_achievements}
                Future Goals: {future_goals}
                """
                
                # LOADING SPINNER
                with st.spinner(f'Consultant is drafting your letter using the {model_to_use.split("-")[-1].upper()} model... Please wait...'):
                    response = model.generate_content(user_prompt)
                    
                # OUTPUT
                st.success("✅ Letter Generated Successfully!")
                st.markdown(response.text)
                st.info("ℹ️ Copy this text and paste it into Microsoft Word for final formatting.")
                
            except Exception as e:
                st.error(f"An error occurred. Check your API access limits or contact support: {e}")

# --- FOOTER ---
st.markdown("---")
st.caption("Developed by **World Intelligence Encyclopedia Founder**")
