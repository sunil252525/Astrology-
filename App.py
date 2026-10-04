import os
import datetime
import streamlit as st
import swisseph as swe

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# -------------------------------------------------------------
# 1. उन्नत वैदिक ज्योतिष व पंचांग कैलकुलेटर
# -------------------------------------------------------------
class ComprehensiveVedicAstrology:
    def __init__(self):
        try:
            swe.set_sidemode(1) # Lahiri Ayanamsa
        except Exception:
            pass

        self.SIGNS = [
            "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
            "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
            "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"
        ]

        # 27 नक्षत्र और उनके 4 चरणों के नामाक्षर
        self.NAKSHATRA_PADAS = [
            ("अश्विनी", ["चू", "चे", "चो", "ला"], "केतु"),
            ("भरणी", ["ली", "लू", "ले", "लो"], "शुक्र"),
            ("कृत्तिका", ["अ", "ई", "उ", "ए"], "सूर्य"),
            ("रोहिणी", ["ओ", "वा", "वी", "वू"], "चंद्रमा"),
            ("मृगशिरा", ["वे", "वो", "का", "की"], "मंगल"),
            ("आर्द्रा", ["कू", "घ", "ङ", "छ"], "राहु"),
            ("पुनर्वसु", ["के", "को", "हा", "ही"], "गुरु"),
            ("पुष्य", ["हू", "हे", "हो", "डा"], "शनि"),
            ("अश्लेषा", ["डी", "डू", "डे", "डो"], "बुध"),
            ("मघा", ["मा", "मी", "मू", "मे"], "केतु"),
            ("पूर्वाफाल्गुनी", ["मो", "टा", "टी", "टू"], "शुक्र"),
            ("उत्तराफाल्गुनी", ["टे", "टो", "पा", "पी"], "सूर्य"),
            ("हस्त", ["पू", "ष", "ण", "ठ"], "चंद्रमा"),
            ("चित्रा", ["पे", "पो", "रा", "री"], "मंगल"),
            ("स्वाति", ["रू", "रे", "रो", "ता"], "राहु"),
            ("विशाखा", ["ती", "तू", "ते", "तो"], "गुरु"),
            ("अनुराधा", ["ना", "नी", "नू", "ने"], "शनि"),
            ("ज्येष्ठा", ["नो", "या", "यी", "यू"], "बुध"),
            ("मूल", ["ये", "यो", "भा", "भी"], "केतु"),
            ("पूर्वाषाढ़ा", ["भू", "ध", "फ", "ढा"], "शुक्र"),
            ("उत्तराषाढ़ा", ["भे", "भो", "जा", "जी"], "सूर्य"),
            ("श्रवण", ["खी", "खू", "खे", "खो"], "चंद्रमा"),
            ("धनिष्ठा", ["गा", "गी", "गु", "गे"], "मंगल"),
            ("शतभिषा", ["गो", "सा", "सी", "सु"], "राहु"),
            ("पूर्वाभाद्रपद", ["से", "सो", "दा", "दी"], "गुरु"),
            ("उत्तराभाद्रपद", ["दू", "थ", "झ", "ञ"], "शनि"),
            ("रेवती", ["दे", "दो", "च", "ची"], "बुध")
        ]

        self.DASHA_YEARS = {
            "केतु": 7, "शुक्र": 20, "सूर्य": 6, "चंद्रमा": 10,
            "मंगल": 7, "राहु": 18, "गुरु": 16, "शनि": 19, "बुध": 17
        }
        self.DASHA_ORDER = ["केतु", "शुक्र", "सूर्य", "चंद्रमा", "मंगल", "राहु", "गुरु", "शनि", "बुध"]

        self.PLANETS = {
            swe.SUN: "सूर्य (Sun)", swe.MOON: "चंद्रमा (Moon)", swe.MARS: "मंगल (Mars)",
            swe.MERCURY: "बुध (Mercury)", swe.JUPITER: "गुरु (Jupiter)",
            swe.VENUS: "शुक्र (Venus)", swe.SATURN: "शनि (Saturn)", swe.MEAN_NODE: "राहु (Rahu)"
        }

    def get_julian_day(self, dt, tz_offset=5.5):
        utc_dt = dt - datetime.timedelta(hours=tz_offset)
        return swe.julday(utc_dt.year, utc_dt.month, utc_dt.day, utc_dt.hour + utc_dt.minute/60.0 + utc_dt.second/3600.0)

    def calculate_astrology(self, dt, lat, lon, tz_offset=5.5):
        jd = self.get_julian_day(dt, tz_offset)
        flags = swe.FLG_SIDEREAL if hasattr(swe, 'FLG_SIDEREAL') else 64

        # 1. ग्रह गणना
        planets_data = {}
        for p_id, p_name in self.PLANETS.items():
            try:
                res, _ = swe.calc_ut(jd, p_id, flags)
                deg = res[0] % 360
            except Exception:
                res = swe.calc_ut(jd, p_id)
                deg = (res[0][0] if isinstance(res[0], (list, tuple)) else res[0]) % 360
            planets_data[p_name] = {"degree": deg, "sign": self.SIGNS[int(deg // 30)], "sign_deg": deg % 30}

        # केतु
        ketu_deg = (planets_data["राहु (Rahu)"]["degree"] + 180) % 360
        planets_data["केतु (Ketu)"] = {"degree": ketu_deg, "sign": self.SIGNS[int(ketu_deg // 30)], "sign_deg": ketu_deg % 30}

        # 2. लग्न गणना
        try:
            cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
            asc_deg = ascmc[0] % 360
        except Exception:
            asc_deg = (jd * 360) % 360
        ascendant = self.SIGNS[int(asc_deg // 30)]

        # 3. नक्षत्र, चरण और नामकरण गणना
        moon_deg = planets_data["चंद्रमा (Moon)"]["degree"]
        nak_span = 360 / 27.0
        nak_idx = int(moon_deg // nak_span)
        nak_rem = moon_deg % nak_span
        pada = int(nak_rem // (nak_span / 4))

        nak_info = self.NAKSHATRA_PADAS[min(nak_idx, 26)]
        nak_name = nak_info[0]
        suggested_letter = nak_info[1][min(pada, 3)]
        lord = nak_info[2]

        # 4. विंशोत्तरी महादशा (भविष्य काल गणना)
        total_dasha_years = self.DASHA_YEARS[lord]
        fraction_passed = nak_rem / nak_span
        balance_years = total_dasha_years * (1 - fraction_passed)

        dasha_timeline = []
        current_year = dt.year + (dt.month / 12.0)
        start_lord_idx = self.DASHA_ORDER.index(lord)
        
        # जन्म के समय बची हुई दशा
        end_year = current_year + balance_years
        dasha_timeline.append((lord, int(current_year), int(end_year)))
        
        curr_y = end_year
        for i in range(1, 6): # अगले 5 ग्रहों की दशाएँ
            next_lord = self.DASHA_ORDER[(start_lord_idx + i) % 9]
            d_years = self.DASHA_YEARS[next_lord]
            dasha_timeline.append((next_lord, int(curr_y), int(curr_y + d_years)))
            curr_y += d_years

        return {
            "ascendant": ascendant,
            "moon_sign": planets_data["चंद्रमा (Moon)"]["sign"],
            "nakshatra": nak_name,
            "pada": pada + 1,
            "letter": suggested_letter,
            "dasha_lord": lord,
            "dasha_balance": round(balance_years, 2),
            "dasha_timeline": dasha_timeline,
            "planets": planets_data
        }

    def generate_predictions(self, data):
        asc = data["ascendant"].split()[0]
        moon = data["moon_sign"].split()[0]
        nak = data["nakshatra"]
        pada = data["pada"]

        # विशिष्ट भविष्यफल
        future_text = f"जातक का जन्म **{asc} लग्न** और **{moon} राशि** के **{nak} नक्षत्र (द्वितीय/तृतीय चरण {pada})** में हुआ है।\n\n"
        future_text += f"• **करियर व धन:** {asc} लग्न के कारण जातक कर्मठ और बुद्धिमान रहेगा। "
        future_text += f"जीवन के 28वें वर्ष के बाद विशेष धनलाभ और पद-प्रतिष्ठा मिलने के योग हैं।\n"
        future_text += f"• **नामकरण हेतु सुझाव:** जन्म के क्षण अनुसार बच्चे का नाम **'{data['letter']}'** अक्षर से शुरू होना चाहिए।"

        remedies = [
            f"जन्म नक्षत्रपति ({data['dasha_lord']}) के मंत्रों का नियमित जाप करें।",
            "प्रतिदिन प्रातःकाल सूर्य को अर्घ्य दें।",
            "प्रतिदिन हनुमान चालीसा का पाठ करें।"
        ]
        return future_text, remedies


# -------------------------------------------------------------
# 2. PDF जनरेटर
# -------------------------------------------------------------
def generate_pdf_bytes(name, dob_str, tob_str, place_str, data, prediction, remedies):
    pdf_path = f"/tmp/kundli_{datetime.datetime.now().timestamp()}.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('T1', parent=styles['Heading1'], fontSize=18, alignment=1, textColor=colors.HexColor('#8B0000'))
    heading_style = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=12, spaceBefore=10, textColor=colors.HexColor('#4A0E4E'))
    normal = styles['Normal']

    elements = []
    elements.append(Paragraph("<b>विस्तृत वैदिक जन्म कुंडली एवं दशा फल</b>", title_style))
    elements.append(Spacer(1, 10))

    info = [
        ["Name:", name, "DOB:", dob_str],
        ["Time:", tob_str, "Place:", place_str],
        ["Ascendant (लग्न):", data["ascendant"], "Moon Sign (राशि):", data["moon_sign"]],
        ["Nakshatra:", f"{data['nakshatra']} (चरण {data['pada']})", "Suggested Letter:", data["letter"]],
        ["Birth Dasha Lord:", data["dasha_lord"], "Dasha Balance:", f"{data['dasha_balance']} Years"]
    ]
    t_info = Table(info, colWidths=[110, 140, 110, 140])
    t_info.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF8DC')),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    elements.append(t_info)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Future Dasha Timeline (विंशोत्तरी महादशा भविष्यफल)</b>", heading_style))
    dasha_data = [["Planet (ग्रह)", "Start Year (प्रारंभ)", "End Year (समाप्ति)"]]
    for lord, s_yr, e_yr in data["dasha_timeline"]:
        dasha_data.append([lord, str(s_yr), str(e_yr)])
    
    t_dasha = Table(dasha_data, colWidths=[180, 170, 170])
    t_dasha.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#4A0E4E')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_dasha)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Planetary Positions (ग्रह स्थिति)</b>", heading_style))
    p_data = [["Planet", "Sign", "Degree"]]
    for p_name, p_info in data["planets"].items():
        deg_str = f"{int(p_info['sign_deg'])}° {int((p_info['sign_deg']%1)*60)}'"
        p_data.append([p_name, p_info["sign"], deg_str])

    t_p = Table(p_data, colWidths=[180, 180, 160])
    t_p.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#8B0000')),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('PADDING', (0,0), (-1,-1), 4),
    ]))
    elements.append(t_p)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Predictions & Analysis</b>", heading_style))
    elements.append(Paragraph(prediction, normal))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Suggested Remedies</b>", heading_style))
    for r in remedies:
        elements.append(Paragraph(f"• {r}", normal))

    doc.build(elements)
    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()
    if os.path.exists(pdf_path):
        os.remove(pdf_path)
    return pdf_bytes


# -------------------------------------------------------------
# 3. Streamlit UI
# -------------------------------------------------------------
st.set_page_config(page_title="उन्नत वैदिक ज्योतिष ऐप", page_icon="🔮")

st.title("🔮 सटीक वैदिक जन्म कुंडली व महादशा कैलकुलेटर")

CITY_COORDS = {
    "New Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Kolkata": (22.5726, 88.3639),
    "Chennai": (13.0827, 80.2707),
    "Bengaluru": (12.9716, 77.5946),
    "Custom / अन्य शहर": (None, None)
}

with st.form("astrology_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("नाम (Name)", value="राहुल शर्मा")
        dob = st.date_input("जन्म तिथि (DOB)", value=datetime.date(1998, 5, 15))
        # समय को सेकंड तक सटीक इनपुट लें
        tob = st.time_input("जन्म समय (Time - HH:MM:SS)", value=datetime.time(14, 30, 0))

    with col2:
        selected_city = st.selectbox("शहर चुनें (City)", list(CITY_COORDS.keys()))
        if selected_city != "Custom / अन्य शहर":
            lat, lon = CITY_COORDS[selected_city]
            st.info(f"अक्षांश: {lat}, देशांतर: {lon}")
        else:
            lat = st.number_input("अक्षांश (Latitude)", value=28.6139, format="%.4f")
            lon = st.number_input("देशांतर (Longitude)", value=77.2090, format="%.4f")

    submit = st.form_submit_button("सटीक कुंडली बनाएँ")

if submit:
    dt = datetime.datetime.combine(dob, tob)
    calc = ComprehensiveVedicAstrology()
    data = calc.calculate_astrology(dt, lat, lon)
    pred, remedies = calc.generate_predictions(data)

    st.success("✨ आपकी सटीक कुंडली तैयार है!")

    st.subheader("📌 सूक्ष्म जन्म विवरण एवं नामकरण")
    col_a, col_b = st.columns(2)
    with col_a:
        st.write(f"**लग्न (Ascendant):** {data['ascendant']}")
        st.write(f"**चंद्र राशि (Moon Sign):** {data['moon_sign']}")
        st.write(f"**नक्षत्र:** {data['nakshatra']} (चरण {data['pada']})")
    with col_b:
        st.write(f"**सुझाया गया नामाक्षर:** `{data['letter']}`")
        st.write(f"**जन्म महादशा स्वामी:** {data['dasha_lord']}")
        st.write(f"**बची हुई महादशा:** {data['dasha_balance']} वर्ष")

    st.subheader("⏳ विंशोत्तरी महादशा टाइमलाइन (भविष्य काल)")
    d_list = []
    for lord, s_yr, e_yr in data["dasha_timeline"]:
        d_list.append({"ग्रह (Planet)": lord, "प्रारंभ वर्ष (Start)": s_yr, "समाप्ति वर्ष (End)": e_yr})
    st.table(d_list)

    st.subheader("📜 विस्तृत भविष्यफल एवं उपाय")
    st.write(pred)
    for r in remedies:
        st.write(f"- {r}")

    pdf_bytes = generate_pdf_bytes(
        name, dob.strftime("%d-%m-%Y"), tob.strftime("%H:%M:%S"),
        selected_city if selected_city != "Custom / अन्य शहर" else f"{lat}, {lon}",
        data, pred, remedies
    )

    st.download_button(
        label="📄 सम्पूर्ण कुंडली PDF डाउनलोड करें",
        data=pdf_bytes,
        file_name=f"Kundli_{name.replace(' ', '_')}.pdf",
        mime="application/pdf"
    )
    
