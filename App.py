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


# 3. FPDF2 का उपयोग करके PDF बनाने का सही फ़ंक्शन
def generate_pdf(user_name, user_dob, user_tob, user_pob):
  pdf = FPDF()
  pdf.add_page()

  # शीर्षक (Title)
  pdf.set_font("Helvetica", "B", 18)
  pdf.cell(0, 15, text="Astrology Report", new_x="LMARGIN", new_y="NEXT", align="C")
  pdf.ln(10)

  # विवरण जोड़ने का फ़ंक्शन
  pdf.set_font("Helvetica", "", 12)
  pdf.cell(0, 10, text=f"Name: {user_name}", new_x="LMARGIN", new_y="NEXT")
  pdf.cell(0, 10, text=f"Date of Birth: {user_dob}", new_x="LMARGIN", new_y="NEXT")
  pdf.cell(0, 10, text=f"Time of Birth: {user_tob}", new_x="LMARGIN", new_y="NEXT")
  pdf.cell(0, 10, text=f"Place of Birth: {user_pob}", new_x="LMARGIN", new_y="NEXT")

  pdf.ln(10)
  pdf.set_font("Helvetica", "I", 11)
  pdf.multi_cell(
      0,
      8,
      text=(
          "Prediction Summary:\nYour planetary positions show positive energy"
          " and progress. Focus on your goals and maintain a balanced"
          " routine."
      ),
  )

  # fpdf2 के नए वर्ज़न के लिए सही बाइट्स आउटपुट
  return bytes(pdf.output())


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
      
