import os
import datetime
import streamlit as st
import swisseph as swe

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# 1. वैदिक ज्योतिष कैलकुलेटर क्लास
# -------------------------------------------------------------
class VedicAstrologyCalculator:
    def __init__(self):
        # Lahiri Ayanamsa Safe Setup
        try:
            if hasattr(swe, 'SIDM_LAHIRI'):
                swe.set_sidemode(swe.SIDM_LAHIRI)
            else:
                swe.set_sidemode(1)  # 1 represents LAHIRI in swisseph C-library
        except Exception:
            pass  # Fallback gracefully
        
        self.SIGNS = [
            "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
            "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
            "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"
        ]
        
        self.NAKSHATRAS = [
            ("अश्विनी", ["चू", "चे", "चो", "ला"]), ("भरणी", ["ली", "लू", "ले", "लो"]),
            ("कृत्तिका", ["अ", "ई", "उ", "ए"]), ("रोहिणी", ["ओ", "वा", "वी", "वू"]),
            ("मृगशिरा", ["वे", "वो", "का", "की"]), ("आर्द्रा", ["कू", "घ", "ङ", "छ"]),
            ("पुनर्वसु", ["के", "को", "हा", "ही"]), ("पुष्य", ["हू", "हे", "हो", "डा"]),
            ("अश्लेषा", ["डी", "डू", "डे", "डो"]), ("मघा", ["मा", "मी", "मू", "मे"]),
            ("पूर्वाफाल्गुनी", ["मो", "टा", "टी", "टू"]), ("उत्तराफाल्गुनी", ["टे", "टो", "पा", "पी"]),
            ("हस्त", ["पू", "ष", "ण", "ठ"]), ("चित्रा", ["पे", "पो", "रा", "री"]),
            ("स्वाति", ["रू", "रे", "रो", "ता"]), ("विशाखा", ["ती", "तू", "ते", "तो"]),
            ("अनुराधा", ["ना", "नी", "नू", "ने"]), ("ज्येष्ठा", ["नो", "या", "यी", "यू"]),
            ("मूल", ["ये", "यो", "भा", "भी"]), ("पूर्वाषाढ़ा", ["भू", "ध", "फ", "ढा"]),
            ("उत्तराषाढ़ा", ["भे", "भो", "जा", "जी"]), ("श्रवण", ["खी", "खू", "खे", "खो"]),
            ("धनिष्ठा", ["गा", "गी", "गु", "गे"]), ("शतभिषा", ["गो", "सा", "सी", "सु"]),
            ("पूर्वाभाद्रपद", ["से", "सो", "दा", "दी"]), ("उत्तराभाद्रपद", ["दू", "थ", "झ", "ञ"]),
            ("रेवती", ["दे", "दो", "च", "ची"])
        ]

        self.PLANETS = {
            swe.SUN: "सूर्य (Sun)",
            swe.MOON: "चंद्रमा (Moon)",
            swe.MARS: "मंगल (Mars)",
            swe.MERCURY: "बुध (Mercury)",
            swe.JUPITER: "गुरु (Jupiter)",
            swe.VENUS: "शुक्र (Venus)",
            swe.SATURN: "शनि (Saturn)",
            swe.MEAN_NODE: "राहु (Rahu)"
        }

    def datetime_to_julian(self, year, month, day, hour, minute, tz_offset=5.5):
        utc_hour = hour + minute / 60.0 - tz_offset
        return swe.julday(year, month, day, utc_hour)

    def calculate_birth_details(self, year, month, day, hour, minute, lat, lon, tz_offset=5.5):
        jd = self.datetime_to_julian(year, month, day, hour, minute, tz_offset)
        
        planet_positions = {}
        flags = swe.FLG_SIDEREAL if hasattr(swe, 'FLG_SIDEREAL') else 64
        
        for p_id, p_name in self.PLANETS.items():
            try:
                res, _ = swe.calc_ut(jd, p_id, flags)
                deg = res[0] % 360
            except Exception:
                res = swe.calc_ut(jd, p_id)
                deg = res[0][0] % 360 if isinstance(res[0], (list, tuple)) else res[0] % 360

            sign_idx = int(deg // 30)
            sign_deg = deg % 30
            planet_positions[p_name] = {
                "degree": deg,
                "sign": self.SIGNS[sign_idx],
                "sign_degree": sign_deg
            }

        rahu_deg = planet_positions["राहु (Rahu)"]["degree"]
        ketu_deg = (rahu_deg + 180) % 360
        planet_positions["केतु (Ketu)"] = {
            "degree": ketu_deg,
            "sign": self.SIGNS[int(ketu_deg // 30)],
            "sign_degree": ketu_deg % 30
        }

        try:
            cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
            asc_deg = ascmc[0] % 360
        except Exception:
            asc_deg = (jd * 360) % 360
            
        ascendant_sign = self.SIGNS[int(asc_deg // 30)]

        moon_deg = planet_positions["चंद्रमा (Moon)"]["degree"]
        nak_span = 360 / 27.0
        nak_idx = int(moon_deg // nak_span)
        nak_deg = moon_deg % nak_span
        pada = int(nak_deg // (nak_span / 4))
        
        nak_name, letter_list = self.NAKSHATRAS[min(nak_idx, 26)]
        suggested_letter = letter_list[min(pada, 3)]
        moon_sign = planet_positions["चंद्रमा (Moon)"]["sign"]

        return {
            "ascendant": ascendant_sign,
            "moon_sign": moon_sign,
            "nakshatra": nak_name,
            "pada": pada + 1,
            "suggested_letter": suggested_letter,
            "planets": planet_positions
        }

    def generate_predictions_and_remedies(self, details):
        moon_sign = details["moon_sign"]
        predictions = f"आपकी जन्म राशि **{moon_sign}** है। आपका व्यक्तित्व प्रभावशाली है। " \
                      f"करियर और जीवन में मेहनत के बाद उच्च सफलता के योग हैं।"
        
        remedies = [
            "प्रतिदिन सूर्य देव को तांबे के लोटे से जल अर्पित करें।",
            "गायत्री मंत्र का जाप करें।",
            "प्रतिदिन हनुमान चालीसा का पाठ करें।",
            "ज़रूरतमंदों की सहायता करें।"
        ]
        return predictions, remedies


# -------------------------------------------------------------
# 2. PDF रिपोर्ट जनरेटर
# -------------------------------------------------------------
def generate_pdf_bytes(name, dob_str, tob_str, place_str, details, prediction, remedies):
    pdf_path = f"/tmp/kundli_{datetime.datetime.now().timestamp()}.pdf"
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, alignment=1, spaceAfter=15, textColor=colors.HexColor('#8B0000'))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor('#4A0E4E'))
    normal_style = styles['Normal']

    elements = []
    elements.append(Paragraph("<b>वैदिक ज्योतिष - जन्म कुंडली रिपोर्ट</b>", title_style))
    elements.append(Spacer(1, 10))

    personal_data = [
        ["Name:", name, "DOB:", dob_str],
        ["Time:", tob_str, "Place:", place_str],
        ["Ascendant:", details["ascendant"], "Moon Sign:", details["moon_sign"]],
        ["Nakshatra:", f"{details['nakshatra']} (Pada {details['pada']})", "Suggested Letter:", details["suggested_letter"]]
    ]
    
    t_personal = Table(personal_data, colWidths=[110, 140, 110, 140])
    t_personal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF8DC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    elements.append(t_personal)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Planetary Positions</b>", heading_style))
    planet_table_data = [["Planet", "Sign", "Degree"]]
    
    for planet, info in details["planets"].items():
        deg_str = f"{int(info['sign_degree'])}° {int((info['sign_degree']%1)*60)}'"
        planet_table_data.append([planet, info["sign"], deg_str])

    t_planets = Table(planet_table_data, colWidths=[180, 180, 160])
    t_planets.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_planets)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>General Predictions</b>", heading_style))
    elements.append(Paragraph(prediction, normal_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Suggested Remedies</b>", heading_style))
    for rem in remedies:
        elements.append(Paragraph(f"• {rem}", normal_style))

    doc.build(elements)
    
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
        
    return pdf_bytes


# -------------------------------------------------------------
# 3. Streamlit वेब यूज़र इंटरफ़ेस (UI)
# -------------------------------------------------------------
st.set_page_config(page_title="वैदिक ज्योतिष जन्म कुंडली", page_icon="🔮")

st.title("🔮 वैदिक ज्योतिष एवं जन्म कुंडली जनरेटर")
st.write("अपनी जन्म की जानकारी भरें और तुरंत विस्तृत कुंडली व PDF प्राप्त करें।")

with st.form("kundli_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("नाम (Name)", value="राहुल शर्मा")
        dob = st.date_input("जन्म तिथि (Date of Birth)", value=datetime.date(1998, 5, 15))
        tob = st.time_input("जन्म समय (Time of Birth)", value=datetime.time(14, 30))
    with col2:
        place = st.text_input("जन्म स्थान (City / Place)", value="New Delhi")
        lat = st.number_input("अक्षांश (Latitude)", value=28.6139, format="%.4f")
        lon = st.number_input("देशांतर (Longitude)", value=77.2090, format="%.4f")
    
    submit_btn = st.form_submit_button("कुंडली बनाएँ (Generate Kundli)")

if submit_btn:
    calc = VedicAstrologyCalculator()
    details = calc.calculate_birth_details(
        dob.year, dob.month, dob.day, tob.hour, tob.minute, lat, lon
    )
    prediction, remedies = calc.generate_predictions_and_remedies(details)

    st.success("✨ आपकी जन्म कुंडली सफलतापूर्वक तैयार हो गई है!")
    
    st.subheader("📌 मुख्य ज्योतिष विवरण")
    st.write(f"**लग्न (Ascendant):** {details['ascendant']}")
    st.write(f"**चंद्र राशि (Moon Sign):** {details['moon_sign']}")
    st.write(f"**नक्षत्र (Nakshatra):** {details['nakshatra']} (चरण {details['pada']})")
    st.write(f"**सुझाया गया नामाक्षर (Suggested Name Letter):** `{details['suggested_letter']}`")

    st.subheader("🪐 ग्रहों की स्थिति")
    planet_data = []
    for p_name, p_info in details["planets"].items():
        deg_str = f"{int(p_info['sign_degree'])}° {int((p_info['sign_degree']%1)*60)}'"
        planet_data.append({"ग्रह (Planet)": p_name, "राशि (Sign)": p_info["sign"], "अंश (Degree)": deg_str})
    st.table(planet_data)

    st.subheader("📜 सामान्य फलादेश एवं उपाय")
    st.write(prediction)
    for rem in remedies:
        st.write(f"- {rem}")

    # PDF Download Button
    pdf_data = generate_pdf_bytes(
        name, dob.strftime("%d-%m-%Y"), tob.strftime("%H:%M"), place,
        details, prediction, remedies
    )
    st.download_button(
        label="📄 कुंडली PDF डाउनलोड करें (Download PDF)",
        data=pdf_data,
        file_name=f"Kundli_{name.replace(' ', '_')}.pdf",
        mime="application/pdf"
        )
            
