import os
import datetime
import math
import streamlit as st
import swisseph as swe

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# 1. सम्पूर्ण पंचांग एवं वैदिक ज्योतिष कैलकुलेटर
# -------------------------------------------------------------
class VedicPanchangCalculator:
    def __init__(self):
        # Lahiri Ayanamsa Set
        try:
            if hasattr(swe, 'SIDM_LAHIRI'):
                swe.set_sidemode(swe.SIDM_LAHIRI)
            else:
                swe.set_sidemode(1)
        except Exception:
            pass

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

        self.TITHIS = [
            "प्रथमा (प्रतिपदा)", "द्वितीया", "तृतीया", "चतुर्थी", "पंचमी",
            "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी",
            "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा / अमावस्या"
        ]

        self.YOGAS = [
            "विष्कुम्भ", "प्रीति", "आयुष्मान", "सौभाग्य", "शोभन", "अतिगण्ड", "सुकर्मा",
            "धृति", "शूल", "गण्ड", "वृद्धि", "ध्रुव", "व्याघात", "हर्षण",
            "वज्र", "सिद्धि", "व्यतीपात", "वरीयान", "परिघ", "शिव", "सिद्ध",
            "साध्य", "शुभ", "शुक्ल", "ब्रह्म", "ऐन्द्र", "वैधृति"
        ]

        self.KARANAS = [
            "बव", "बालव", "कौलव", "तैतिल", "गर", "वणिज", "विष्टि (भद्रा)",
            "शकुनि", "चतुष्पाद", "नाग", "किंस्तुघ्न"
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

    def calculate_panchang_and_kundli(self, year, month, day, hour, minute, lat, lon, tz_offset=5.5):
        jd = self.datetime_to_julian(year, month, day, hour, minute, tz_offset)
        flags = swe.FLG_SIDEREAL if hasattr(swe, 'FLG_SIDEREAL') else 64

        # 1. ग्रहों की स्थिति गणना (Sidereal / निरयण)
        planet_positions = {}
        for p_id, p_name in self.PLANETS.items():
            try:
                res, _ = swe.calc_ut(jd, p_id, flags)
                deg = res[0] % 360
            except Exception:
                res = swe.calc_ut(jd, p_id)
                deg = (res[0][0] if isinstance(res[0], (list, tuple)) else res[0]) % 360

            sign_idx = int(deg // 30)
            sign_deg = deg % 30
            planet_positions[p_name] = {
                "degree": deg,
                "sign": self.SIGNS[sign_idx],
                "sign_degree": sign_deg
            }

        # केतु गणना
        rahu_deg = planet_positions["राहु (Rahu)"]["degree"]
        ketu_deg = (rahu_deg + 180) % 360
        planet_positions["केतु (Ketu)"] = {
            "degree": ketu_deg,
            "sign": self.SIGNS[int(ketu_deg // 30)],
            "sign_degree": ketu_deg % 30
        }

        # 2. पंचांग गणनाएं (Panchang Calculations)
        sun_deg = planet_positions["सूर्य (Sun)"]["degree"]
        moon_deg = planet_positions["चंद्रमा (Moon)"]["degree"]

        # A. तिथि calculation (1 तिथि = 12 अंश सूर्य-चंद्रमा का अंतर)
        diff_deg = (moon_deg - sun_deg) % 360
        tithi_num = int(diff_deg // 12) + 1
        paksha = "शुक्ल पक्ष" if tithi_num <= 15 else "कृष्ण पक्ष"
        tithi_idx = (tithi_num - 1) % 15
        tithi_name = f"{self.TITHIS[tithi_idx]} ({paksha})"

        # B. नक्षत्र calculation (1 नक्षत्र = 13° 20')
        nak_span = 360 / 27.0
        nak_idx = int(moon_deg // nak_span)
        nak_deg = moon_deg % nak_span
        pada = int(nak_deg // (nak_span / 4))
        nak_name, letter_list = self.NAKSHATRAS[min(nak_idx, 26)]
        suggested_letter = letter_list[min(pada, 3)]

        # C. योग calculation (सूर्य अंश + चंद्रमा अंश / 13° 20')
        total_deg = (sun_deg + moon_deg) % 360
        yoga_idx = int(total_deg // nak_span)
        yoga_name = self.YOGAS[min(yoga_idx, 26)]

        # D. करण calculation (1 तिथि में 2 करण)
        karana_num = int(diff_deg // 6)
        if karana_num == 0:
            karana_name = "किंस्तुघ्न"
        elif karana_num >= 57:
            karana_name = self.KARANAS[karana_num - 50]  # स्थिर करण
        else:
            karana_name = self.KARANAS[(karana_num - 1) % 7]  # चर करण

        # E. लग्न calculation
        try:
            cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
            asc_deg = ascmc[0] % 360
        except Exception:
            asc_deg = (jd * 360) % 360
        ascendant_sign = self.SIGNS[int(asc_deg // 30)]

        # F. वार (Day of week)
        dt = datetime.datetime(year, month, day)
        days_hindi = ["सोमवार", "मंगलवार", "बुधवार", "गुरुवार", "शुक्रवार", "शनिवार", "रविवार"]
        day_name = days_hindi[dt.weekday()]

        return {
            "panchang": {
                "vaar": day_name,
                "tithi": tithi_name,
                "nakshatra": f"{nak_name} (चरण {pada + 1})",
                "yoga": yoga_name,
                "karana": karana_name
            },
            "ascendant": ascendant_sign,
            "moon_sign": planet_positions["चंद्रमा (Moon)"]["sign"],
            "suggested_letter": suggested_letter,
            "planets": planet_positions
        }

    def generate_predictions_and_remedies(self, details):
        moon_sign = details["moon_sign"]
        nakshatra = details["panchang"]["nakshatra"]
        
        predictions = f"जातक का जन्म **{details['panchang']['tithi']}** तथा **{nakshatra}** में हुआ है। " \
                      f"चंद्र राशि **{moon_sign}** के प्रभाव से जातक बुद्धिमान, विचारशील और कार्यकुशल रहेगा। " \
                      f"जीवन में मध्यम आयु के पश्चात विशेष उन्नति के योग बनते हैं।"

        remedies = [
            "प्रतिदिन सूर्य देव को तांबे के पात्र से जल अर्पित करें।",
            "जन्म नक्षत्र के देवता की प्रसन्नता के लिए गायत्री मंत्र का 108 बार पाठ करें।",
            "प्रतिदिन हनुमान चालीसा का पाठ करना अत्यंत फलदायी होगा।",
            "माह में एक बार किसी गरीब या ब्राह्मण को अन्न का दान करें।"
        ]
        return predictions, remedies


# -------------------------------------------------------------
# 2. PDF जनरेटर
# -------------------------------------------------------------
def generate_pdf_bytes(name, dob_str, tob_str, place_str, details, prediction, remedies):
    pdf_path = f"/tmp/kundli_{datetime.datetime.now().timestamp()}.pdf"
    doc = SimpleDocTemplate(
        pdf_path, pagesize=letter,
        rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=18, alignment=1, spaceAfter=12, textColor=colors.HexColor('#8B0000'))
    heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=12, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor('#4A0E4E'))
    normal_style = styles['Normal']

    elements = []
    elements.append(Paragraph("<b>संपूर्ण पंचांग व वैदिक जन्म कुंडली</b>", title_style))
    elements.append(Spacer(1, 10))

    p = details["panchang"]
    personal_data = [
        ["Name:", name, "DOB:", dob_str],
        ["Time:", tob_str, "Place:", place_str],
        ["Ascendant:", details["ascendant"], "Moon Sign:", details["moon_sign"]],
        ["Day (वार):", p["vaar"], "Tithi (तिथि):", p["tithi"]],
        ["Nakshatra:", p["nakshatra"], "Yoga (योग):", p["yoga"]],
        ["Karana (करण):", p["karana"], "Name Letter:", details["suggested_letter"]]
    ]

    t_personal = Table(personal_data, colWidths=[110, 140, 110, 140])
    t_personal.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF8DC')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_personal)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Planetary Positions (निरयण ग्रह स्थिति)</b>", heading_style))
    planet_table_data = [["Planet", "Sign", "Degree"]]

    for planet, info in details["planets"].items():
        deg_str = f"{int(info['sign_degree'])}° {int((info['sign_degree']%1)*60)}'"
        planet_table_data.append([planet, info["sign"], deg_str])

    t_planets = Table(planet_table_data, colWidths=[180, 180, 160])
    t_planets.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.append(t_planets)
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Predictions (फलादेश)</b>", heading_style))
    elements.append(Paragraph(prediction, normal_style))
    elements.append(Spacer(1, 15))

    elements.append(Paragraph("<b>Remedies (उपाय)</b>", heading_style))
    for rem in remedies:
        elements.append(Paragraph(f"• {rem}", normal_style))

    doc.build(elements)

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return pdf_bytes


# -------------------------------------------------------------
# 3. Streamlit UI
# -------------------------------------------------------------
st.set_page_config(page_title="पंचांग एवं वैदिक ज्योतिष कुंडली", page_icon="📜")

st.title("📜 पंचांग एवं वैदिक जन्म कुंडली कैलकुलेटर")
st.write("जन्म विवरण दर्ज करें - पंचांग के 5 अंग (तिथि, वार, नक्षत्र, योग, करण) और ग्रहों की सटीक गणना प्राप्त करें।")

with st.form("panchang_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("नाम (Name)", value="राहुल शर्मा")
        dob = st.date_input("जन्म तिथि (Date of Birth)", value=datetime.date(1998, 5, 15))
        tob = st.time_input("जन्म समय (Time of Birth)", value=datetime.time(14, 30))
    with col2:
        place = st.text_input("जन्म स्थान (City)", value="New Delhi")
        lat = st.number_input("अक्षांश (Latitude)", value=28.6139, format="%.4f")
        lon = st.number_input("देशांतर (Longitude)", value=77.2090, format="%.4f")

    submit_btn = st.form_submit_button("पंचांग एवं कुंडली बनाएँ")

if submit_btn:
    calc = VedicPanchangCalculator()
    details = calc.calculate_panchang_and_kundli(
        dob.year, dob.month, dob.day, tob.hour, tob.minute, lat, lon
    )
    prediction, remedies = calc.generate_predictions_and_remedies(details)

    st.success("✨ पंचांग एवं कुंडली गणना सफलतापूर्वक पूर्ण हुई!")

    st.subheader("🗓️ पंचांग के 5 अंग (Birth Panchang)")
    p = details["panchang"]
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.write(f"**वार (Day):** {p['vaar']}")
        st.write(f"**तिथि (Tithi):** {p['tithi']}")
        st.write(f"**नक्षत्र (Nakshatra):** {p['nakshatra']}")
    with col_p2:
        st.write(f"**योग (Yoga):** {p['yoga']}")
        st.write(f"**करण (Karana):** {p['karana']}")
        st.write(f"**नामाक्षर (Suggested Letter):** `{details['suggested_letter']}`")

    st.subheader("🪐 ग्रहों की स्थिति (Planetary Degrees)")
    planet_data = []
    for p_name, p_info in details["planets"].items():
        deg_str = f"{int(p_info['sign_degree'])}° {int((p_info['sign_degree']%1)*60)}'"
        planet_data.append({"ग्रह (Planet)": p_name, "राशि (Sign)": p_info["sign"], "अंश (Degree)": deg_str})
    st.table(planet_data)

    st.subheader("📜 फलादेश एवं उपाय")
    st.write(prediction)
    for rem in remedies:
        st.write(f"- {rem}")

    pdf_data = generate_pdf_bytes(
        name, dob.strftime("%d-%m-%Y"), tob.strftime("%H:%M"), place,
        details, prediction, remedies
    )
    st.download_button(
        label="📄 पंचांग + कुंडली PDF डाउनलोड करें",
        data=pdf_data,
        file_name=f"Panchang_Kundli_{name.replace(' ', '_')}.pdf",
        mime="application/pdf"
        )
    
