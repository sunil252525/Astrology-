import streamlit as st
from fpdf import FPDF

# 1. पेज कॉन्फ़िगरेशन
st.set_page_config(
    page_title="Complete Vedic Astrology & Numerology System",
    page_icon="🔮",
    layout="wide",
)

st.title("🔮 सम्पूर्ण ज्योतिष, न्यूमरोलॉजी एवं वास्तु विश्लेषण")
st.write(
    "नवजात बच्चे एवं व्यक्ति के जीवन के सभी 6 प्रमुख स्तंभों का सम्पूर्ण विवरण"
)

# 2. यूज़र इनपुट फॉर्म
with st.form("complete_astro_form"):
  col1, col2 = st.columns(2)
  with col1:
    name = st.text_input("पूरा नाम (Full Name)")
    dob = st.date_input("जन्म तिथि (Date of Birth)")
  with col2:
    tob = st.time_input("जन्म समय (Time of Birth)")
    pob = st.text_input("जन्म स्थान (Place of Birth)")

  submitted = st.form_submit_button("सम्पूर्ण ज्योतिष रिपोर्ट तैयार करें")


# 3. PDF जनरेट करने का फ़ंक्शन
def generate_complete_pdf(user_name, user_dob, user_tob, user_pob):
  pdf = FPDF()
  pdf.add_page()

  # Header
  pdf.set_font("Helvetica", "B", 16)
  pdf.cell(
      0, 10, "Comprehensive Astrology & Numerology Report", ln=True, align="C"
  )
  pdf.set_font("Helvetica", "I", 10)
  pdf.cell(
      0,
      6,
      f"Generated for: {user_name} | DOB: {user_dob} | Time: {user_tob} | Place: {user_pob}",
      ln=True,
      align="C",
  )
  pdf.ln(8)

  sections = [
      (
          "1. Numerology & Name Astrology",
          [
              "Mulank (Driver No.): Core personality based on birth date sum.",
              (
                  "Bhagyank (Destiny No.): Life direction based on total DOB"
                  " sum."
              ),
              (
                  "Namank (Name No.): Name balance with Mulank/Bhagyank for"
                  " smooth life path."
              ),
              "Lo Shu Grid: 3x3 Element grid balance (Water, Fire, Earth, Metal, Wood).",
              "Personal Year/Month: Mathematical forecasting of time cycles.",
          ],
      ),
      (
          "2. Vastu Shastra & Spatial Balance",
          [
              "Nursery Vastu: Ideal sleeping direction (North-East / Ishan Kon).",
              "Study Vastu: Facing direction while studying (East/North).",
              "Energy Corrections: Balancing home layout for overall well-being.",
          ],
      ),
      (
          "3. Natal Astrological Yogas & Doshas",
          [
              "Auspicious Yogas: Raj Yoga, Dhan Yoga, Gaja Kesari Yoga, Panch Mahapurusha Yogas.",
              "Doshas & Remedies: Gandmool, Kaal Sarp, Manglik, Pitri Dosh, Balarishta Dosh.",
          ],
      ),
      (
          "4. Vedic Rituals & Protection (Sanskars)",
          [
              "16 Sanskars: Jatakarma, Namakaran, Nishkramana, Annaprashana, Chudakarana, Karnavedha, Vidyarambha.",
              "Shanti Pujas: Gandmool Shanti, Mool Shanti, Navgraha Shanti, Rudri Path.",
              "Protective Measures: Ishta Devta identification, Gemstones (Life/Lucky), Rudraksha.",
          ],
      ),
      (
          "5. Past Life & Life Cycle Calculations",
          [
              "Past Life Karma: D-60 (Shashtiamsha Chart) & Pitri Rin analysis.",
              "Future Cycles: Vimshottari Dasha (120-year roadmap), Ashtakvarga, Gochar, Varshphal.",
          ],
      ),
      (
          "6. Samudrika Shastra & Body Features",
          [
              "Palmistry: Major lines (Life, Head, Heart, Fate) & Mount structures.",
              "Body Features: Assessment through moles, chakras, and physical lines.",
          ],
      ),
      (
          "Summary Checklist for Newborn",
          [
              "Vedic Panchang & Birth Chart (D1 to D60)",
              "Numerology Analysis (Mulank, Bhagyank, Namank, Lo Shu Grid)",
              "Dosha Analysis (Gandmool, Balarishta, Kaal Sarp)",
              "Ishta Devta, Kuldevta & Lucky Remedies",
              "Vastu Alignment for Bed & Study",
              "16 Sanskar Dates & Shanti Puja Checklist",
          ],
      ),
  ]

  for title, items in sections:
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, title, ln=True)
    pdf.set_font("Helvetica", "", 9)
    for item in items:
      pdf.multi_cell(0, 5, f"- {item}")
    pdf.ln(2)

  return bytes(pdf.output())


# 4. रिपोर्ट आउटपुट और डाउनलोड
if submitted:
  if not name or not pob:
    st.error("कृपया सभी विवरण भरें!")
  else:
    st.success(f"धन्यवाद {name}, आपकी विस्तृत ज्योतिष रिपोर्ट तैयार है!")

    pdf_bytes = generate_complete_pdf(name, dob, tob, pob)

    st.download_button(
        label="📥 सम्पूर्ण ज्योतिष एवं न्यूमरोलॉजी रिपोर्ट (PDF) डाउनलोड करें",
        data=pdf_bytes,
        file_name=f"{name}_Complete_Astrology_Report.pdf",
        mime="application/pdf",
    )
      
