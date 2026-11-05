import streamlit as st
import os
from google import genai

# Page Config
st.set_page_config(
    page_title="EduPulse - AI Micro-Mentor",
    page_icon="🚀",
    layout="wide"
)

# --- NAVBAR / HEADER WITH MANDATORY STICKER ---
st.markdown("""
    <div style="background-color: #1e1e2f; padding: 12px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <h2 style="color: white; margin: 0; font-size: 22px;">🎓 EduPulse: AI Micro-Mentor</h2>
        <div style="background-color: #ff4b4b; color: white; padding: 6px 12px; border-radius: 6px; font-weight: bold; font-size: 13px;">
            ✨ Built For Ostad Presents YUNet AIgnite Buildathon 2026
        </div>
    </div>
""", unsafe_allow_html=True)

# --- SIDEBAR: API KEY & USER INPUTS ---
st.sidebar.header("⚙️ Configuration & Profile")
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

st.sidebar.subheader("Tell us about yourself")
current_skill = st.sidebar.text_input("Current Skills (e.g., Basic Python, HTML)", "Basic Python, HTML")
target_role = st.sidebar.text_input("Target Role/Goal (e.g., Full Stack Developer)", "Full Stack Developer")
learning_time = st.sidebar.slider("Daily Learning Time (Minutes)", 10, 60, 20)

# --- MAIN INTERFACE ---
st.write("### Bridge your skill gap with AI-powered personalized micro-learning!")

if st.button("🚀 Generate My AI Micro-Learning Plan & Analysis", type="primary"):
    if not api_key:
        st.error("⚠️ Please enter your Gemini API Key in the sidebar to proceed.")
    else:
        try:
            # Initialize Gemini Client using official google-genai SDK
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            Act as an expert AI career mentor and educator. 
            The user's current skills: {current_skill}
            Their target professional role: {target_role}
            Available daily study time: {learning_time} minutes.

            Provide a structured JSON-like response in clear markdown format containing:
            1. **Skill Gap Analysis:** What are they missing to reach their target role?
            2. **Today's 3-Step Micro-Lesson:** Tailored bite-sized steps they can finish in {learning_time} minutes.
            3. **Quick Practice Task:** A small hands-on challenge for today.
            """

            with st.spinner("🤖 AI Mentor is analyzing your profile and crafting your custom plan..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt
                )
                
                st.success("✨ Your Personalized Plan is Ready!")
                st.markdown(response.text)

        except Exception as e:
            st.error(f"An error occurred: {e}")

# --- INTERACTIVE AI TUTOR CHAT SECTION ---
st.divider()
st.subheader("💬 Ask AI Micro-Tutor (Instant Doubts Solving)")
user_question = st.text_input("Got stuck while learning? Ask any coding or concept question here:")

if st.button("Ask Tutor"):
    if not api_key:
        st.warning("Please provide your Gemini API Key in the sidebar first.")
    elif user_question:
        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Thinking..."):
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=f"Explain this simply and clearly for a student: {user_question}"
                )
                st.info(response.text)
        except Exception as e:
            st.error(f"Error: {e}")