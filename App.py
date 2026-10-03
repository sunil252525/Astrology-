from fpdf import FPDF
import streamlit as st

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(
    page_title="Astrology App", page_icon="🔮", layout="centered"
)

st.title("🔮 ज्योतिष एवं कुंडली ऐप (Astrology App)")
st.subheader("अपनी जानकारी दर्ज करें और रिपोर्ट डाउनलोड करें")

# 2. यूज़र इनपुट फॉर्म
with st.form("astro_form"):
  name = st.text_input("पूरा नाम (Full Name)")
  dob = st.date_input("जन्म तिथि (Date of Birth)")
  tob = st.time_input("जन्म समय (Time of Birth)")
  pob = st.text_input("जन्म स्थान (Place of Birth)")

  submitted = st.form_submit_button("ज्योतिष रिपोर्ट तैयार करें")


# 3. FPDF2 का उपयोग करके PDF बनाने का फ़ंक्शन
def generate_pdf(user_name, user_dob, user_tob, user_pob):
  pdf = FPDF()
  pdf.add_page()

  # फ़ॉन्ट सेट करना (Standard Arial)
  pdf.set_font("Arial", "B", 18)

  # शीर्षक (Title)
  pdf.cell(0, 15, txt="Astrology Report", ln=True, align="C")
  pdf.ln(10)

  # विवरण जोड़ने का फ़ंक्शन
  pdf.set_font("Arial", "", 12)
  pdf.cell(0, 10, txt=f"Name: {user_name}", ln=True)
  pdf.cell(0, 10, txt=f"Date of Birth: {user_dob}", ln=True)
  pdf.cell(0, 10, txt=f"Time of Birth: {user_tob}", ln=True)
  pdf.cell(0, 10, txt=f"Place of Birth: {user_pob}", ln=True)

  pdf.ln(10)
  pdf.set_font("Arial", "I", 11)
  pdf.multi_cell(
      0,
      8,
      txt=(
          "Prediction Summary:\nYour planetary positions show positive energy"
          " and progress. Focus on your goals and maintain a balanced"
          " routine."
      ),
  )

  # PDF आउटपुट बाइट्स के रूप में प्राप्त करना
  return pdf.output(dest="S").encode("latin-1")


# 4. सबमिट होने पर PDF तैयार करना और डाउनलोड बटन दिखाना
if submitted:
  if not name or not pob:
    st.error("कृपया सभी फ़ील्ड भरें!")
  else:
    st.success(f"धन्यवाद {name}, आपकी रिपोर्ट तैयार है!")

    # PDF बनाना
    pdf_bytes = generate_pdf(name, dob, tob, pob)

    # Streamlit PDF डाउनलोड बटन
    st.download_button(
        label="📥 Astrology Report (PDF) डाउनलोड करें",
        data=pdf_bytes,
        file_name=f"{name}_Astrology_Report.pdf",
        mime="application/pdf",
    )
      
