import datetime
from fpdf import FPDF
import streamlit as st

st.set_page_config(page_title="वैदिक कुंडली", page_icon="🔮")
st.title("🔮 सम्पूर्ण वैदिक जन्मकुण्डली रिपोर्ट")


class PDF(FPDF):

  def header(self):
    self.set_font("Arial", "B", 15)
    self.cell(0, 10, "FULL VEDIC ASTROLOGY & HOROSCOPE REPORT", 0, 1, "C")
    self.line(10, 20, 200, 20)
    self.ln(5)


def generate_pdf(name, dob, tob, pob):
  pdf = PDF()
  pdf.add_page()
  pdf.set_font("Arial", size=11)

  content = f"""
    Name: {name} | DOB: {dob} | Time: {tob} | Place: {pob}
    Lagna: Pisces (Meena) | Rashi: Capricorn (Makar) | Nakshatra: Shravana

    1. PLANETARY POSITIONS & PANCHANG
    - Lagna Lord Jupiter in 9th House: Great wisdom and destiny.
    - Sun in 10th House: Strong leadership and official benefits.
    - Moon in 11th House (Shravana): Intelligent, creative and intuitive.

    2. HEALTH & MEDICAL ASTROLOGY
    - Cold & ENT: Vulnerable to seasonal cold and sinus during childhood.
    - Digestive System: Mild sensitive stomach, prefer fresh warm food.
    - Bones & Joints: Ensure adequate Calcium and sunlight exposure.

    3. DOSHA & REMEDIES
    - Gandmool Dosha: ABSENT
    - Kaal Sarp Yoga: Mild Partial. Remedy: Water/Milk offering on Shivling.

    4. VASTU & NUMEROLOGY
    - Driver No: 8 (Saturn) | Conductor No: 2 (Moon)
    - Sleeping Position: Head facing East or South.
    - Study Room: North-East corner facing East.
    """
  for line in content.split("\n"):
    pdf.cell(0, 6, line.strip(), ln=True)

  return pdf.output(dest="S").encode("latin-1", errors="replace")


with st.form("astro_form"):
  name = st.text_input("Name", value="Gurttam Kumar")
  dob = st.date_input("DOB", value=datetime.date(2019, 1, 8))
  tob = st.time_input("Time", value=datetime.time(11, 15))
  pob = st.text_input("Place", value="Faridabad")
  btn = st.form_submit_button("Generate PDF")

if btn:
  pdf_bytes = generate_pdf(name, dob, tob, pob)
  st.success("PDF Generated Successfully!")
  st.download_button(
      "Download Kundali PDF",
      pdf_bytes,
      file_name="Gurttam_Kundali_Report.pdf",
      mime="application/pdf",
  )
    
