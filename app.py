import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI SOP Consultant",
    page_icon="🎓",
    layout="wide"
)

# --- SIDEBAR (SETTINGS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=100)
    st.title("Settings")
    st.markdown("Powered by **Google Gemini 2.5**")
    
    # API Key Input (Will be hidden later)
    api_key = st.text_input("Google AI Studio API Key:", type="password", help="Enter your API Key here.")
    
    st.divider()
    st.info("💡 **Tip:** Mention specific challenges overcome in the 'Key Achievements' section to make the letter more personal.")

# --- MAIN CONTENT ---
st.title("🎓 AI Statement of Purpose (SOP) Specialist")
st.markdown("Generate a highly persuasive, Ivy League-standard Statement of Purpose in seconds.")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Applicant Details")
    target_program = st.text_input("Target University & Program", placeholder="e.g. TU Munich, MSc Data Science")
    user_background = st.text_area("Academic & Professional Background", placeholder="e.g. Graduated from Yildiz Tech (GPA 3.2), 2 years Python dev experience...", height=150)
    key_achievements = st.text_area("Key Achievements & Projects", placeholder="e.g. Won a hackathon, published a paper, IELTS 7.5...", height=100)
    future_goals = st.text_input("Future Career Goals", placeholder="e.g. Become an AI specialist in the automotive sector.")
    
    generate_btn = st.button("🚀 Generate SOP", type="primary", use_container_width=True)

with col2:
    st.subheader("📄 Your Professional Letter")
    
    if generate_btn:
        if not api_key:
            st.error("⚠️ Please enter your API Key in the sidebar settings!")
        elif not target_program or not user_background:
            st.warning("⚠️ Please fill in the required fields.")
        else:
            try:
                # GEMINI CONFIGURATION
                genai.configure(api_key=api_key)
                
                # SYSTEM INSTRUCTION (The Expert Persona)
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
                
                # MODEL SELECTION (Updated to Flash 2.5 or latest stable)
                model = genai.GenerativeModel(
                    model_name="gemini-1.5-flash", # Using 1.5 Flash for stability, if 2.5 fails revert to this or try gemini-pro
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
                with st.spinner('Consultant is drafting your letter... Please wait...'):
                    response = model.generate_content(user_prompt)
                    
                # OUTPUT
                st.success("✅ Letter Generated Successfully!")
                st.markdown(response.text)
                st.caption("You can copy this text into your Word document.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.markdown("---")
st.markdown("Developed by **World Intelligence Encyclopedia Founder** | Powered by Gemini AI")
