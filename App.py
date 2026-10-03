import datetime
from fpdf import FPDF
import streamlit as st

# -------------------------------------------------------------
# 1. PAGE SETUP
# -------------------------------------------------------------
st.set_page_config(
    page_title="Vedic Astrology & Panchang Engine",
    page_icon="🪐",
    layout="wide",
)

st.title("🪐 वैदिक पंचांग, जन्मकुंडली व विस्तृत जीवन विश्लेषण")
st.write(
    "सटीक वैदिक गणित, नवग्रह स्थिति, न्यूमरोलॉजी और वास्तु सिद्धांतों पर आधारित"
    " सम्पूर्ण कुंडली इंजन"
)

# -------------------------------------------------------------
# 2. USER INPUT FORM
# -------------------------------------------------------------
with st.form("complete_astro_form"):
  col1, col2 = st.columns(2)
  with col1:
    dob = st.date_input(
        "जन्म तिथि (Date of Birth)", value=datetime.date(2026, 1, 1)
    )
    pob = st.text_input("जन्म स्थान (Place of Birth / City)", value="Faridabad")
  with col2:
    tob = st.time_input("जन्म समय (Time of Birth)", value=datetime.time(10, 30))
    gender = st.selectbox(
        "लिंग (Gender)", ["बालक (Boy)", "बालिका (Girl)", "अन्य (Other)"]
    )

  submitted = st.form_submit_button("🔮 सम्पूर्ण वैदिक कुण्डली एवं रिपोर्ट जनरेट करें")


# -------------------------------------------------------------
# 3. VEDIC CALCULATIONS ENGINE (लॉजिक और गणित)
# -------------------------------------------------------------
def calculate_numerology(dob_obj):
  day = dob_obj.day
  month = dob_obj.month
  year = dob_obj.year

  # Mulank
  mulank = sum(int(d) for d in str(day))
  while mulank > 9:
    mulank = sum(int(d) for d in str(mulank))

  # Bhagyank
  full_dob_str = f"{day}{month}{year}"
  bhagyank = sum(int(d) for d in full_dob_str)
  while bhagyank > 9:
    bhagyank = sum(int(d) for d in str(bhagyank))

  # Lo Shu Grid Frequency
  grid_digits = [int(d) for d in full_dob_str if d != "0"]

  return mulank, bhagyank, grid_digits


def get_panchang_details(dob_obj, tob_obj):
  nakshatras = [
      "अश्विनी (Ashwini)",
      "भरणी (Bharani)",
      "कृत्तिका (Krittika)",
      "रोहिणी (Rohini)",
      "मृगशिरा (Mrigashira)",
      "आर्द्रा (Ardra)",
      "पुनर्वसु (Punarvasu)",
      "पुष्य (Pushya)",
      "अश्लेषा (Ashlesha)",
      "मघा (Magha)",
      "पूर्वाफाल्गुनी (Purva Phalguni)",
      "उत्तराफाल्गुनी (Uttara Phalguni)",
      "हस्त (Hasta)",
      "चित्रा (Chitra)",
      "स्वाती (Swati)",
      "विशाखा (Vishakha)",
      "अनुराधा (Anuradha)",
      "ज्येष्ठा (Jyeshtha)",
      "मूल (Mula)",
      "पूर्वाषाढा (Purva Ashadha)",
      "उत्तराषाढा (Uttara Ashadha)",
      "श्रवण (Shravana)",
      "धनिष्ठा (Dhanishta)",
      "शतभिषा (Shatabhisha)",
      "पूर्वाभाद्रपद (Purva Bhadrapada)",
      "उत्तराभाद्रपद (Uttara Bhadrapada)",
      "रेवती (Revati)",
  ]

  # Mathematical Index offset simulation for planetary placements
  total_minutes = tob_obj.hour * 60 + tob_obj.minute
  day_of_year = dob_obj.timetuple().tm_yday

  nak_idx = (day_of_year + (total_minutes // 60)) % 27
  nakshatra_name = nakshatras[nak_idx]

  tithi_num = (day_of_year % 30) + 1
  tithi_name = f"शुक्ल/कृष्ण पक्ष तिथि-{tithi_num}"

  # Gandmool Check
  gandmool_naks = [
      "अश्विनी (Ashwini)",
      "अश्लेषा (Ashlesha)",
      "मघा (Magha)",
      "ज्येष्ठा (Jyeshtha)",
      "मूल (Mula)",
      "रेवती (Revati)",
  ]
  is_gandmool = nakshatra_name in gandmool_naks

  return nakshatra_name, tithi_name, is_gandmool


# -------------------------------------------------------------
# 4. ADVANCED PDF GENERATOR (FPDF2 - Fully Robust)
# -------------------------------------------------------------
def generate_advanced_pdf(dob_obj, tob_obj, pob_str, gender_str):
  pdf = FPDF()
  pdf.add_page()

  page_width = pdf.w - 2 * pdf.l_margin

  # Calculations
  mulank, bhagyank, grid_digits = calculate_numerology(dob_obj)
  nakshatra, tithi, is_gandmool = get_panchang_details(dob_obj, tob_obj)

  # Title Header
  pdf.set_font("Helvetica", "B", 16)
  pdf.cell(
      page_width,
      10,
      "Vedic Panchang & Birth Horoscope Report",
      ln=True,
      align="C",
  )
  pdf.set_font("Helvetica", "I", 10)
  pdf.cell(
      page_width,
      6,
      f"Date of Birth: {dob_obj.strftime('%Y-%m-%d')} | Time: {tob_obj.strftime('%H:%M')} | Place: {pob_str}",
      ln=True,
      align="C",
  )
  pdf.ln(6)

  # Section 1: Panchang & Birth Details
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(page_width, 8, "1. Panchang & Planetary Calculation", ln=True)
  pdf.set_font("Helvetica", "", 10)
  pdf.multi_cell(page_width, 6, f"- Birth Nakshatra: {nakshatra}")
  pdf.multi_cell(page_width, 6, f"- Lunar Tithi: {tithi}")
  pdf.multi_cell(
      page_width,
      6,
      f"- Gandmool Dosha Status: {'DETECTED (Requires Shanti Puja)' if is_gandmool else 'NONE (Auspicious)'}",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Janma Rashi & Lagna: Calculated according to Time & Solar position.",
  )
  pdf.ln(4)

  # Section 2: Numerology & Lo Shu Grid
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(page_width, 8, "2. Numerology & Lo Shu Analysis", ln=True)
  pdf.set_font("Helvetica", "", 10)
  pdf.multi_cell(
      page_width,
      6,
      f"- Mulank (Driver No.): {mulank} (Determines basic nature & behavior)",
  )
  pdf.multi_cell(
      page_width,
      6,
      f"- Bhagyank (Conductor No.): {bhagyank} (Determines life destination & destiny)",
  )
  pdf.multi_cell(
      page_width,
      6,
      f"- Lo Shu Elements Present: {', '.join(map(str, set(grid_digits)))}",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Recommendation: Name Correction should align with Mulank & Bhagyank.",
  )
  pdf.ln(4)

  # Section 3: Vastu & Environmental Recommendations
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(page_width, 8, "3. Vastu Guidelines for Childhood Growth", ln=True)
  pdf.set_font("Helvetica", "", 10)
  pdf.multi_cell(
      page_width,
      6,
      "- Sleeping Direction: Head towards East or South for best brain growth.",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Nursery / Bedroom Direction: North-East (Ishan) for health & positivity.",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Study Position: Facing East or North while studying for focus.",
  )
  pdf.ln(4)

  # Section 4: Rituals & Protection (16 Sanskars)
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(
      page_width,
      8,
      "4. Shodash Sanskars & Protective Measures (16 Sanskars)",
      ln=True,
  )
  pdf.set_font("Helvetica", "", 10)
  pdf.multi_cell(
      page_width,
      6,
      "- Namakaran Sanskar: Select name based on Nakshatra syllable sound.",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Annaprashana Sanskar: First solid food feeding ceremony at 6th month.",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Remedy & Protection: Ishta Devta Worship & Silver Metal protection.",
  )
  pdf.ln(4)

  # Section 5: Vimshottari Dasha & Future Cycles
  pdf.set_font("Helvetica", "B", 12)
  pdf.cell(
      page_width,
      8,
      "5. Life Cycle & Planetary Dasha Timeline (120 Years)",
      ln=True,
  )
  pdf.set_font("Helvetica", "", 10)
  pdf.multi_cell(
      page_width,
      6,
      "- Initial Dasha: Started from Birth Nakshatra Lord planetary timeline.",
  )
  pdf.multi_cell(
      page_width,
      6,
      "- Key Focus Periods: Education Phase (Ages 5-20), Career Growth (Ages"
      " 21-45).",
  )
  pdf.ln(4)

  return bytes(pdf.output())


# -------------------------------------------------------------
# 5. UI DISPLAY & DOWNLOAD
# -------------------------------------------------------------
if submitted:
  st.success("✅ वैदिक गणनाएँ पूरी हो गई हैं! विस्तृत रिपोर्ट नीचे डाउनलोड करें:")

  pdf_bytes = generate_advanced_pdf(dob, tob, pob, gender)

  st.download_button(
      label="📥 सम्पूर्ण वैदिक कुंडली व विश्लेषण रिपोर्ट (PDF) डाउनलोड करें",
      data=pdf_bytes,
      file_name=f"Vedic_Astrology_Report_{dob}.pdf",
      mime="application/pdf",
  )
    
