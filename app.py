import os
import itertools
import streamlit as st
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="BNXT.ai PPT Generator",
    page_icon="🤖",
    layout="wide"
)

# =====================================================
# LOGIN SYSTEM
# =====================================================

USERNAME = "himanshu.singh@frugaltestingin.com"
PASSWORD = "himanshu@2026"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:gray;'>BNXT.ai PPT Generator</p>", unsafe_allow_html=True)
    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        email = st.text_input("📧 Email", placeholder="Enter your email")
        password = st.text_input("🔑 Password", type="password", placeholder="Enter your password")

        if st.button("Login", use_container_width=True):
            if email == USERNAME and password == PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("❌ Invalid email or password.")

    st.stop()

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:
    st.markdown("### 🤖 BNXT.ai Tool")
    st.markdown(f"👤 **{USERNAME}**")
    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# =====================================================
# LOAD API KEYS
# =====================================================

try:
    keys_string = st.secrets["GEMINI_API_KEYS"]
except Exception:
    load_dotenv()
    keys_string = os.getenv("GEMINI_API_KEYS", "")

API_KEYS = [k.strip() for k in keys_string.split(",") if k.strip()]

if not API_KEYS:
    st.error("❌ No Gemini API keys found. Add GEMINI_API_KEYS in secrets or .env")
    st.stop()

KEY_CYCLE = itertools.cycle(API_KEYS)

# =====================================================
# GEMINI HELPER
# =====================================================

def ask(prompt):
    last_error = None
    for _ in range(len(API_KEYS)):
        api_key = next(KEY_CYCLE)
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.5-flash")
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            last_error = e
            continue
    return f"All API keys failed. Last error: {last_error}"

# =====================================================
# OCR via Gemini Vision (no Tesseract needed)
# =====================================================

def extract_text_from_image(uploaded_img):
    api_key = next(KEY_CYCLE)
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
    img = Image.open(uploaded_img)
    response = model.generate_content([
        "Extract all the text from this image exactly as it appears. Return only the raw text, no explanation.",
        img
    ])
    return response.text or ""

# =====================================================
# CHAIN
# =====================================================

def run_chain(prospect, competitor, mail, progress_bar, status_text):

    status_text.text("🔍 Step 1/4 — Researching prospect & competitor...")
    progress_bar.progress(10)

    prompt1 = f"""
the {prospect} our prospect and they have a competitor {competitor}

research about both on web

Uploaded mail content:

{mail}

Compare:

- company overview
- services
- strengths
- weaknesses
- opportunities
- key differences
"""
    out1 = ask(prompt1)
    progress_bar.progress(30)

    status_text.text("📊 Step 2/4 — Generating 10-slide PPT content...")

    prompt2 = f"""
give me content for 10 page ppt to send to {prospect}

which says how bnxt.ai helped {competitor}

in ai integration and automation

Keep every slide separate

Slide1:

Slide2:

Slide3:

Slide4:

Slide5:

Slide6:

Slide7:

Slide8:

Slide9:

Slide10:
"""
    out2 = ask(prompt2)
    progress_bar.progress(55)

    status_text.text("📈 Step 3/4 — Making it detailed & number-oriented...")

    prompt3 = f"""
this is too generic

give detailed analysis

not surface level

keep it number oriented

Use this content:

{out2}
"""
    out3 = ask(prompt3)
    progress_bar.progress(78)

    status_text.text("✉️ Step 4/4 — Drafting outreach message...")

    prompt4 = f"""
draft me a humanized msg without emdash

to send with this ppt

to come on meet

Prospect:

{prospect}

Context:

{out1}
"""
    out4 = ask(prompt4)
    progress_bar.progress(100)
    status_text.text("✅ Done!")

    return {"step1": out1, "step2": out2, "step3": out3, "step4": out4}

# =====================================================
# MAIN UI
# =====================================================

st.title("🤖 BNXT.ai PPT Generator")
st.markdown("Upload a prospect's email screenshot + fill details to generate PPT content & outreach message.")
st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    prospect = st.text_input("🏢 Prospect Company Name", placeholder="e.g. Acme Corp")
with col2:
    competitor = st.text_input("⚔️ Competitor Company Name", placeholder="e.g. RivalCo")

uploaded_image = st.file_uploader(
    "📎 Upload Mail Screenshot (JPG / PNG)",
    type=["jpg", "jpeg", "png"]
)

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=False, width=400)

st.markdown("---")

if st.button("🚀 Generate", use_container_width=True):

    if not prospect.strip():
        st.warning("⚠️ Please enter Prospect Company Name.")
        st.stop()
    if not competitor.strip():
        st.warning("⚠️ Please enter Competitor Company Name.")
        st.stop()
    if uploaded_image is None:
        st.warning("⚠️ Please upload a mail screenshot.")
        st.stop()

    progress_bar = st.progress(0)
    status_text = st.empty()

    status_text.text("🖼️ Extracting text from image...")
    progress_bar.progress(5)

    try:
        mail_text = extract_text_from_image(uploaded_image)
    except Exception as e:
        st.error(f"❌ Image text extraction failed: {e}")
        st.stop()

    with st.expander("📄 Extracted Mail Text", expanded=False):
        st.write(mail_text or "(No text found in image)")

    results = run_chain(prospect, competitor, mail_text, progress_bar, status_text)

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍 Research & Comparison",
        "📊 PPT Content (Draft)",
        "📈 PPT Content (Detailed)",
        "✉️ Outreach Message"
    ])

    with tab1:
        st.markdown("### Prospect vs Competitor Research")
        st.write(results["step1"])
        st.download_button("⬇️ Download", data=results["step1"], file_name="research.txt", mime="text/plain")

    with tab2:
        st.markdown("### 10-Slide PPT Content (Draft)")
        st.write(results["step2"])
        st.download_button("⬇️ Download", data=results["step2"], file_name="ppt_draft.txt", mime="text/plain")

    with tab3:
        st.markdown("### 10-Slide PPT Content (Detailed)")
        st.write(results["step3"])
        st.download_button("⬇️ Download", data=results["step3"], file_name="ppt_detailed.txt", mime="text/plain")

    with tab4:
        st.markdown("### Outreach Message")
        st.write(results["step4"])
        st.download_button("⬇️ Download", data=results["step4"], file_name="outreach.txt", mime="text/plain")