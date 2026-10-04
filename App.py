import os
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
        # Swiss Ephemeris में लाहिरी अयनंश (Sidereal Lahiri) सेट करें
        swe.set_sidemode(swe.SIDM_LAHIRI)
        
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
        """स्थानीय समय को UTC और फिर जुलियन डे (Julian Day) में बदलता है"""
        utc_hour = hour + minute / 60.0 - tz_offset
        julian_day = swe.julday(year, month, day, utc_hour)
        return julian_day

    def calculate_birth_details(self, year, month, day, hour, minute, lat, lon, tz_offset=5.5):
        jd = self.datetime_to_julian(year, month, day, hour, minute, tz_offset)
        
        # ग्रहों के स्थान (Sidereal / निरयण)
        planet_positions = {}
        flags = swe.FLG_SIDEREAL | swe.FLG_SPEED
        
        for p_id, p_name in self.PLANETS.items():
            res, _ = swe.calc_ut(jd, p_id, flags)
            deg = res[0] % 360
            sign_idx = int(deg // 30)
            sign_deg = deg % 30
            planet_positions[p_name] = {
                "degree": deg,
                "sign": self.SIGNS[sign_idx],
                "sign_degree": sign_deg
            }

        # केतु की गणना (राहु के ठीक 180 डिग्री विपरीत)
        rahu_deg = planet_positions["राहु (Rahu)"]["degree"]
        ketu_deg = (rahu_deg + 180) % 360
        planet_positions["केतु (Ketu)"] = {
            "degree": ketu_deg,
            "sign": self.SIGNS[int(ketu_deg // 30)],
            "sign_degree": ketu_deg % 30
        }

        # लग्न (Ascendant) गणना
        cusps, ascmc = swe.houses_ex(jd, lat, lon, b'P', flags)
        asc_deg = ascmc[0] % 360
        ascendant_sign = self.SIGNS[int(asc_deg // 30)]

        # चंद्रमा और नक्षत्र आधारित विवरण
        moon_deg = planet_positions["चंद्रमा (Moon)"]["degree"]
        nak_span = 360 / 27.0  # 13.3333... degrees
        nak_idx = int(moon_deg // nak_span)
        nak_deg = moon_deg % nak_span
        pada = int(nak_deg // (nak_span / 4))  # 0, 1, 2, 3
        
        nak_name, letter_list = self.NAKSHATRAS[nak_idx]
        suggested_letter = letter_list[pada]
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
        """संक्षिप्त फलादेश और उपाय उत्पन्न करता है"""
        moon_sign = details["moon_sign"]
        predictions = f"आपकी जन्म राशि **{moon_sign}** है। आप भावनात्मक और बुद्धिमान स्वभाव के व्यक्ति हैं। " \
                      f"करियर के दृष्टिकोण से आपको मध्यम से उच्च सफलता मिलेगी। जीवन में धैर्य बनाए रखना लाभकारी रहेगा।"
        
        remedies = [
            "प्रतिदिन सूर्य देव को तांबे के लोटे से जल अर्पित करें।",
            "गायत्री मंत्र का 108 बार जाप करें।",
            "प्रतिदिन हनुमान चालीसा का पाठ करना शुभ रहेगा।",
            "जरूरतमंदों को भोजन या वस्त्र दान करें।"
        ]
        return predictions, remedies


# -------------------------------------------------------------
# 2. PDF रिपोर्ट जनरेटर क्लास
# -------------------------------------------------------------
class PDFKundliGenerator:
    @staticmethod
    def create_pdf(filename, name, dob_str, tob_str, place_str, details, prediction, remedies):
        doc = SimpleDocTemplate(
            filename,
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle('TitleStyle', parent=styles['Heading1'], fontSize=20, alignment=1, spaceAfter=15, textColor=colors.HexColor('#8B0000'))
        heading_style = ParagraphStyle('HeadingStyle', parent=styles['Heading2'], fontSize=14, spaceBefore=10, spaceAfter=5, textColor=colors.HexColor('#4A0E4E'))
        normal_style = styles['Normal']
        normal_style.fontSize = 10
        normal_style.leading = 14

        elements = []

        # शीर्षक
        elements.append(Paragraph("<b>वैदिक ज्योतिष - जन्म कुंडली रिपोर्ट</b>", title_style))
        elements.append(Spacer(1, 10))

        # 1. व्यक्तिगत विवरण तालिका
        personal_data = [
            ["नाम (Name):", name, "जन्म तिथि (DOB):", dob_str],
            ["जन्म समय (Time):", tob_str, "जन्म स्थान (Place):", place_str],
            ["लग्न (Ascendant):", details["ascendant"], "चंद्र राशि (Moon Sign):", details["moon_sign"]],
            ["नक्षत्र (Nakshatra):", f"{details['nakshatra']} (चरण {details['pada']})", "सुझाया गया नामाक्षर:", details["suggested_letter"]]
        ]
        
        t_personal = Table(personal_data, colWidths=[120, 140, 120, 140])
        t_personal.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FFF8DC')),
            ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),
            ('PADDING', (0,0), (-1,-1), 6),
        ]))
        elements.append(t_personal)
        elements.append(Spacer(1, 15))

        # 2. ग्रहों की स्थिति तालिका
        elements.append(Paragraph("<b>ग्रहों की स्थिति (Planetary Positions)</b>", heading_style))
        planet_table_data = [["ग्रह (Planet)", "राशि (Sign)", "अंश (Degree)"]]
        
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

        # 3. फलादेश (Predictions)
        elements.append(Paragraph("<b>सामान्य फलादेश (General Predictions)</b>", heading_style))
        elements.append(Paragraph(prediction, normal_style))
        elements.append(Spacer(1, 15))

        # 4. ज्योतिषीय उपाय (Remedies)
        elements.append(Paragraph("<b>सुझाए गए उपाय (Suggested Remedies)</b>", heading_style))
        for rem in remedies:
            elements.append(Paragraph(f"• {rem}", normal_style))

        # PDF फाइल निर्माण
        doc.build(elements)
        print(f"\n[Success] PDF कुंडली सफलतापूर्वक तैयार हो गई है: {os.path.abspath(filename)}")


# -------------------------------------------------------------
# 4. मुख्य निष्पादन (Main Execution)
# -------------------------------------------------------------
if __name__ == "__main__":
    # उदाहरण डेटा (आप इसे User Input से बदल सकते हैं)
    name = "राहुल शर्मा"
    year, month, day = 1998, 5, 15
    hour, minute = 14, 30  # 2:30 PM
    lat, lon = 28.6139, 77.2090  # दिल्ली (Latitude, Longitude)
    
    dob_str = f"{day:02d}-{month:02d}-{year}"
    tob_str = f"{hour:02d}:{minute:02d}"
    place_str = "New Delhi, India"
    pdf_filename = f"Kundli_{name.replace(' ', '_')}.pdf"

    # कैलकुलेशन निष्पादित करें
    calc = VedicAstrologyCalculator()
    birth_details = calc.calculate_birth_details(year, month, day, hour, minute, lat, lon)
    prediction, remedies = calc.generate_predictions_and_remedies(birth_details)

    # PDF जनरेट करें
    PDFKundliGenerator.create_pdf(
        pdf_filename, name, dob_str, tob_str, place_str, 
        birth_details, prediction, remedies
      )
  
