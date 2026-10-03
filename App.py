import datetime
from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer
import streamlit as st

st.set_page_config(page_title="सम्पूर्ण वैदिक कुंडली", page_icon="🔮")
st.title("🔮 सम्पूर्ण वैदिक जन्मकुण्डली रिपोर्ट")


def generate_pdf(name, dob, tob, pob):
  buffer = BytesIO()
  doc = SimpleDocTemplate(
      buffer,
      pagesize=A4,
      rightMargin=36,
      leftMargin=36,
      topMargin=36,
      bottomMargin=36,
  )

  styles = getSampleStyleSheet()

  title_style = ParagraphStyle(
      "TitleStyle",
      parent=styles["Heading1"],
      fontSize=18,
      leading=22,
      textColor=colors.HexColor("#800000"),
      alignment=1,  # Center
      spaceAfter=6,
  )

  subtitle_style = ParagraphStyle(
      "SubTitleStyle",
      parent=styles["Normal"],
      fontSize=10,
      leading=14,
      textColor=colors.HexColor("#444444"),
      alignment=1,
      spaceAfter=15,
  )

  section_style = ParagraphStyle(
      "SectionStyle",
      parent=styles["Heading2"],
      fontSize=12,
      leading=16,
      textColor=colors.HexColor("#800000"),
      spaceBefore=12,
      spaceAfter=6,
  )

  body_style = ParagraphStyle(
      "BodyStyle",
      parent=styles["BodyText"],
      fontSize=10,
      leading=14,
      textColor=colors.HexColor("#222222"),
      spaceAfter=6,
  )

  story = []

  # Header
  story.append(
      Paragraph(
          "FULL VEDIC ASTROLOGY &amp; HOROSCOPE REPORT", title_style
      )
  )
  story.append(
      Paragraph(
          "Detailed Panchang, Kundali, Health, Vastu, Numerology &amp; Remedies"
          " Analysis",
          subtitle_style,
      )
  )
  story.append(
      HRFlowable(
          width="100%",
          thickness=1.5,
          color=colors.HexColor("#800000"),
          spaceAfter=15,
      )
  )

  # Basic Info
  info_text = f"<b>Subject:</b> {name} | <b>DOB:</b> {dob} | <b>Time:</b> {tob} | <b>Place:</b> {pob}<br/><b>Lagna:</b> Pisces (Meena) | <b>Rashi:</b> Capricorn (Makar) | <b>Nakshatra:</b> Shravana (Pad 2)"
  story.append(Paragraph(info_text, body_style))
  story.append(Spacer(1, 10))

  # 1. Panchang
  story.append(
      Paragraph(
          "1. VEDIC PANCHANG &amp; PLANETARY POSITIONS (D1 KUNDALI)",
          section_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Lagna Lord (Jupiter):</b> Placed in 9th House (Bhagya Sthan) -"
          " Grants wisdom, luck, and higher learning.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Sun (10th House):</b> Digbali in Sagittarius - Indicates"
          " government favor, leadership, and high status.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Moon (11th House):</b> In Shravana Nakshatra - Emotional,"
          " sharp memory, and artistic capability.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Saturn (10th House):</b> Long-term hard work leading to"
          " immense success and property gains.",
          body_style,
      )
  )
  story.append(Spacer(1, 10))

  # 2. Health
  story.append(
      Paragraph("2. HEALTH &amp; MEDICAL ASTROLOGY ANALYSIS", section_style)
  )
  story.append(
      Paragraph(
          "• <b>Cold, Phlegm &amp; ENT:</b> Vulnerable to seasonal cold,"
          " congestion, and sinus during childhood. Avoid cold items.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Digestive System:</b> Sensitive stomach due to Jupiter in"
          " Scorpio. Fresh, light, warm food recommended.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Bones &amp; Joints:</b> Requires adequate Calcium, Vit-D, and"
          " morning sunlight exposure.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Vision &amp; Focus:</b> Limit screen time (mobile/tablet) to"
          " prevent eye strain.",
          body_style,
      )
  )
  story.append(Spacer(1, 10))

  # 3. Dosha
  story.append(
      Paragraph("3. DOSHAS, YOGAS &amp; REMEDIAL MEASURES", section_style)
  )
  story.append(
      Paragraph(
          "• <b>Gandmool Dosha:</b> ABSENT (Born in Shravana Nakshatra). No"
          " puja required.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Kaal Sarp Dosha:</b> Mild Partial Anant Kaal Sarp. Remedy:"
          " Offer water/milk on Shivling and recite 'Om Namah Shivaya'.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Auspicious Yogas:</b> Gajakesari Yoga (High intelligence) &amp;"
          " Amal Kirti Yoga (Career success).",
          body_style,
      )
  )
  story.append(Spacer(1, 10))

  # 4. Vastu & Numerology
  story.append(
      Paragraph("4. NUMEROLOGY &amp; VASTU GUIDELINES", section_style)
  )
  story.append(
      Paragraph(
          "• <b>Driver No. (Mulank):</b> 8 (Saturn) - Hardworking, disciplined,"
          " steady nature.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Conductor No. (Bhagyank):</b> 2 (Moon) - Creative,"
          " compassionate, artistic.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Sleeping Direction:</b> Head facing East or South.", body_style
      )
  )
  story.append(
      Paragraph(
          "• <b>Study Vastu:</b> Study desk in Ishan Kon (North-East), facing"
          " East while studying.",
          body_style,
      )
  )
  story.append(
      Paragraph(
          "• <b>Lucky Colors:</b> Yellow, Light Blue, Cream, White, Light"
          " Green.",
          body_style,
      )
  )

  doc.build(story)
  buffer.seek(0)
  return buffer.getvalue()


with st.form("astro_form"):
  name = st.text_input("Name", value="Gurttam Kumar")
  dob = st.date_input("DOB", value=datetime.date(2019, 1, 8))
  tob = st.time_input("Time", value=datetime.time(11, 15))
  pob = st.text_input("Place", value="Faridabad")
  btn = st.form_submit_button("Generate Kundali PDF")

if btn:
  pdf_bytes = generate_pdf(name, dob, tob, pob)
  st.success("✅ PDF Successfully Generated!")
  st.download_button(
      "📥 Download Complete Kundali PDF",
      pdf_bytes,
      file_name="Gurttam_Kundali_Report.pdf",
      mime="application/pdf",
  )
  
