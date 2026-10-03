import datetime
from fpdf import FPDF
import streamlit as st

st.set_page_config(
    page_title="Detailed Vedic Kundali Engine", page_icon="🔮", layout="wide"
)
st.title("🔮 सम्पूर्ण वैदिक जन्मकुंडली, स्वास्थ्य व जीवन विश्लेषण")


class DetailedVedicPDF(FPDF):

  def header(self):
    self.set_font("Helvetica", "B", 14)
    self.cell(
        0,
        10,
        "COMPREHENSIVE VEDIC ASTROLOGY & HOROSCOPE REPORT",
        ln=True,
        align="C",
    )
    self.set_font("Helvetica", "I", 9)
    self.cell(
        0,
        5,
        "Detailed Panchang, Kundali, Health, Remedies & Career Analysis Engine",
        ln=True,
        align="C",
    )
    self.line(10, 26, 200, 26)
    self.ln(6)

  def footer(self):
    self.set_y(-15)
    self.set_font("Helvetica", "I", 8)
    self.cell(
        0,
        10,
        f"Page {self.page_no()}/{{nb}} - Confidential Vedic Report",
        align="C",
    )


def generate_full_report(name, dob, tob, pob):
  pdf = DetailedVedicPDF()
  pdf.alias_nb_pages()
  pdf.add_page()
  pw = pdf.w - 2 * pdf.l_margin

  # Header Info
  pdf.set_fill_color(240, 243, 246)
  pdf.rect(10, 28, pw, 22, "F")
  pdf.set_font("Helvetica", "B", 10)
  pdf.set_xy(12, 30)
  pdf.cell(90, 6, f"Subject: {name}", ln=False)
  pdf.cell(90, 6, f"Date of Birth: {dob}", ln=True)
  pdf.set_x(12)
  pdf.cell(90, 6, f"Time of Birth: {tob}", ln=False)
  pdf.cell(90, 6, f"Place of Birth: {pob}", ln=True)
  pdf.set_x(12)
  pdf.cell(90, 6, "Lagna / Ascendant: Pisces (Meena)", ln=False)
  pdf.cell(90, 6, "Ayanamsha: Lahiri", ln=True)
  pdf.ln(8)

  # 1. Panchang
  pdf.set_font("Helvetica", "B", 12)
  pdf.set_text_color(180, 50, 20)
  pdf.cell(
      pw, 8, "1. VEDIC PANCHANG & PLANETARY POSITIONS (D1 KUNDALI)", ln=True
  )
  pdf.set_text_color(0, 0, 0)

  items = [
      (
          "Birth Nakshatra",
          (
              "Shravana Nakshatra (Pad 2) - Lorded by Moon. Emotional &"
              " intuitive mindset."
          ),
      ),
      (
          "Sun & Moon Signs",
          (
              "Sun in Sagittarius (10th House) / Moon in Capricorn (11th"
              " House)."
          ),
      ),
      (
          "Lagna Lord",
          "Jupiter in 9th House (Scorpio) creating auspicious Raj Yoga.",
      ),
  ]
  for t, v in items:
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(45, 5, f"- {t}:", ln=False)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(pw - 45, 5, v)

  pdf.ln(4)

  # 2. Health
  pdf.set_font("Helvetica", "B", 12)
  pdf.set_text_color(180, 50, 20)
  pdf.cell(
      pw, 8, "2. HEALTH & BODY VULNERABILITY ANALYSIS (MEDICAL ASTRO)", ln=True
  )
  pdf.set_text_color(0, 0, 0)

  health = [
      (
          "Cold, Phlegm & ENT",
          (
              "Vulnerable to seasonal cold, sinus, and congestion during"
              " childhood."
          ),
      ),
      (
          "Digestive System",
          (
              "Jupiter placement requires fresh, warm food to avoid sluggish"
              " digestion."
          ),
      ),
      (
          "Bones & Joints",
          (
              "Saturn influence requires adequate Calcium, Vit-D, and regular"
              " sunlight."
          ),
      ),
  ]
  for t, v in health:
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(pw, 5, f"[+] {t}", ln=True)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(pw, 5, v)
    pdf.ln(1.5)

  pdf.ln(4)

  # 3. Yogas & Doshas
  pdf.set_font("Helvetica", "B", 12)
  pdf.set_text_color(180, 50, 20)
  pdf.cell(pw, 8, "3. DOSHAS, YOGAS & REMEDIAL MEASURES", ln=True)
  pdf.set_text_color(0, 0, 0)

  yogas = [
      ("Gandmool Dosha", "ABSENT - Birth in Shravana Nakshatra."),
      (
          "Kaal Sarp Dosha",
          (
              "PARTIAL - Recite Maha Mrityunjaya Mantra & offer silver snake in"
              " water."
          ),
      ),
      (
          "Raj Yoga & Wealth",
          (
              "Gaja Kesari Yoga & 10th House Saturn indicate high leadership &"
              " property wealth."
          ),
      ),
  ]
  for t, v in yogas:
    pdf.set_font("Helvetica", "B", 9.5)
    pdf.cell(45, 5, f"[*] {t}:", ln=False)
    pdf.set_font("Helvetica", "", 9.5)
    pdf.multi_cell(pw - 45, 5, v)

  return bytes(pdf.output())


# Streamlit Form
with st.form("astro_form"):
  name = st.text_input("Name", value="Gurttam")
  dob = st.date_input("DOB", value=datetime.date(2019, 1, 8))
  tob = st.time_input("TOB", value=datetime.time(11, 15))
  pob = st.text_input("POB", value="Faridabad")
  sub = st.form_submit_button("Generate Full Kundali Report")

if sub:
  pdf_bytes = generate_full_report(name, dob, tob, pob)
  st.success("विस्तृत कुंडली तैयार है!")
  st.download_button(
      "📥 सम्पूर्ण कुंडली PDF डाउनलोड करें",
      pdf_bytes,
      file_name="Full_Kundali_Report.pdf",
      mime="application/pdf",
  )
    
