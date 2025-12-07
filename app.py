import streamlit as st
import google.generativeai as genai

# --- SAYFA AYARLARI ---
st.set_page_config(
    page_title="Pro SOP Oluşturucu",
    page_icon="🎓",
    layout="wide"
)

# --- YAN MENÜ (AYARLAR) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2991/2991148.png", width=100)
    st.title("Yönetim Paneli")
    st.markdown("Bu araç **Google Gemini** altyapısını kullanır.")
    
    # API Anahtarını buraya gireceksin
    api_key = st.text_input("Google AI Studio API Key:", type="password", help="API Key'ini buraya yapıştır.")
    
    st.divider()
    st.info("💡 İpucu: Müşterinin CV'sindeki en güçlü yanları 'Kilit Başarılar' kısmına ekle.")

# --- ANA EKRAN ---
st.title("🎓 Akademik Niyet Mektubu (SOP) Uzmanı")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📝 Müşteri Bilgileri")
    target_program = st.text_input("Hedef Üniversite ve Bölüm", placeholder="Örn: TU Munich, MSc Data Science")
    user_background = st.text_area("Eğitim ve İş Geçmişi", placeholder="Örn: Yıldız Teknik Bilgisayar mezunuyum, 2 yıl yazılımcı olarak çalıştım...", height=150)
    key_achievements = st.text_area("Kilit Başarılar & Projeler", placeholder="Örn: TÜBİTAK projesinde yer aldım, IELTS 7.5 aldım...", height=100)
    future_goals = st.text_input("Gelecek Hedefleri", placeholder="Örn: Otomotiv sektöründe yapay zeka uzmanı olmak.")
    
    generate_btn = st.button("🚀 Mektubu Oluştur", type="primary", use_container_width=True)

with col2:
    st.subheader("📄 Hazır Mektup")
    
    if generate_btn:
        if not api_key:
            st.error("⚠️ Lütfen sol menüden API Anahtarını girin!")
        elif not target_program or not user_background:
            st.warning("⚠️ Lütfen gerekli alanları doldurun.")
        else:
            try:
                # GEMINI AYARLARI
                genai.configure(api_key=api_key)
                
                # SİSTEM TALİMATI (SENİN İÇİN HAZIRLADIĞIM PERSONA)
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
                
                # MODELİ SEÇİYORUZ (Gemini 1.5 Flash - Hızlı ve Ucuz)
                model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",  # Adını 2.5 olarak güncelledik
    system_instruction=system_instruction
)
                
                # KULLANICI VERİLERİNİ BİRLEŞTİR
                user_prompt = f"""
                Target Program: {target_program}
                User Background: {user_background}
                Key Achievements: {key_achievements}
                Future Goals: {future_goals}
                """
                
                # YÜKLENİYOR EFEKTİ
                with st.spinner('Profesyonel danışman yazıyor... Lütfen bekleyin...'):
                    response = model.generate_content(user_prompt)
                    
                # SONUCU YAZDIR
                st.success("✅ Mektup Hazır!")
                st.markdown(response.text)
                st.caption("Bu metni kopyalayıp Word dosyasına yapıştırabilirsin.")
                
            except Exception as e:
                st.error(f"Bir hata oluştu: {e}")

# --- ALT BİLGİ ---
st.markdown("---")
st.markdown("Developed by **World Intelligence Encyclopedia Founder** | Powered by Gemini")