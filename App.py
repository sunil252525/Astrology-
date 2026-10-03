import streamlit as st
import datetime
import html

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="सर्वश्रेष्ठ वैदिक ज्योतिष व जन्मकुंडली सॉफ्टवेयर",
    page_icon="🔮",
    layout="wide"
)

# Custom CSS to ensure high visibility in both Dark and Light themes
st.markdown("""
<style>
    .stMetric {
        background-color: #1f2937 !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #374151 !important;
    }
    div[data-testid="stMetricValue"] {
        color: #f3f4f6 !important;
    }
    div[data-testid="stMetricLabel"] {
        color: #9ca3af !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Master Databases & Mapping Dictionaries
# ---------------------------------------------------------
CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

RASHI_DATA = [
    {"rashi": "मेष (Aries)", "lord": "मंगल (Mars)", "letters": "च, चे, चो, ला, ली, लू, ले, लो, अ", "element": "अग्नि (Fire)"},
    {"rashi": "वृषभ (Taurus)", "lord": "शुक्र (Venus)", "letters": "उ, ए, ओ, वा, वी, वू, वे, वो", "element": "पृथ्वी (Earth)"},
    {"rashi": "मिथुन (Gemini)", "lord": "बुध (Mercury)", "letters": "का, की, कू, घ, ङ, छ, के, को, हा", "element": "वायु (Air)"},
    {"rashi": "कर्क (Cancer)", "lord": "चंद्रमा (Moon)", "letters": "ही, हू, हे, हो, डा, डी, डू, डे, डो", "element": "जल (Water)"},
    {"rashi": "सिंह (Leo)", "lord": "सूर्य (Sun)", "letters": "मा, मी, मू, मे, मो, टा, टी, टू, टे", "element": "अग्नि (Fire)"},
    {"rashi": "कन्या (Virgo)", "lord": "बुध (Mercury)", "letters": "टो, पा, पी, पू, ष, ण, ठा, पे, पो", "element": "पृथ्वी (Earth)"},
    {"rashi": "तुला (Libra)", "lord": "शुक्र (Venus)", "letters": "रा, री, रू, रे, रो, ता, ती, तू, ते", "element": "वायु (Air)"},
    {"rashi": "वृश्चिक (Scorpio)", "lord": "मंगल (Mars)", "letters": "तो, ना, नी, नू, ने, नो, या, यी, यू", "element": "जल (Water)"},
    {"rashi": "धनु (Sagittarius)", "lord": "गुरु (Jupiter)", "letters": "ये, यो, भा, भी, भू, धा, फा, ढा, भे", "element": "अग्नि (Fire)"},
    {"rashi": "मकर (Capricorn)", "lord": "शनि (Saturn)", "letters": "भो, जा, जी, खी, खू, खे, खो, गा, गी", "element": "पृथ्वी (Earth)"},
    {"rashi": "कुंभ (Aquarius)", "lord": "शनि (Saturn)", "letters": "गू, गे, गो, सा, सी, सू, से, सो, द", "element": "वायु (Air)"},
    {"rashi": "मीन (Pisces)", "lord": "गुरु (Jupiter)", "letters": "दी, दू, थ, झ, ञ, दे, दो, चा, ची", "element": "जल (Water)"}
]

PLANET_INFO = {
    1: {"planet": "सूर्य (Sun)", "traits": "नेतृत्व क्षमता, स्वाभिमान, अनुशासन", "health": "सिरदर्द, आंखों की कमजोरी", "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः", "gem": "माणिक्य (Ruby)", "remedy": "प्रातः सूर्य देव को अर्घ्य दें।", "lucky_day": "रविवार", "lucky_color": "लाल / नारंगी", "direction": "पूर्व"},
    2: {"planet": "चंद्रमा (Moon)", "traits": "भावुक, कल्पनाशील, सौम्य", "health": "मानसिक तनाव, कफ विकार", "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः", "gem": "मोती (Pearl)", "remedy": "शिवलिंग पर दूध-जल चढ़ाएं।", "lucky_day": "सोमवार", "lucky_color": "सफेद / चांदी", "direction": "उत्तर-पश्चिम"},
    3: {"planet": "गुरु (Jupiter)", "traits": "ज्ञान, बौद्धिकता, मार्गदर्शन", "health": "मोटापा, लीवर की समस्या", "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः", "gem": "पुखराज (Yellow Sapphire)", "remedy": "हल्दी/केसर का तिलक लगाएं।", "lucky_day": "गुरुवार", "lucky_color": "पीला", "direction": "उत्तर-पूर्व"},
    4: {"planet": "राहु (Rahu)", "traits": "तीव्र बुद्धि, तकनीक में निपुण", "health": "अचानक तनाव, त्वचा रोग", "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः", "gem": "गोमेद (Hessonite)", "remedy": "पक्षियों को बाजरा डालें।", "lucky_day": "शनिवार", "lucky_color": "नीला / ग्रे", "direction": "दक्षिण-पश्चिम"},
    5: {"planet": "बुध (Mercury)", "traits": "व्यापारिक कौशल, मधुर वाणी", "health": "तंत्रिका कमजोरी, तनाव", "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः", "gem": "पन्ना (Emerald)", "remedy": "गाय को हरा चारा खिलाएं।", "lucky_day": "बुधवार", "lucky_color": "हरा", "direction": "उत्तर"},
    6: {"planet": "शुक्र (Venus)", "traits": "विलासिता, कला, आकर्षण", "health": "डायबिटीज, हार्मोनल असंतुलन", "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः", "gem": "हीरा / ओपल", "remedy": "इत्र का प्रयोग करें।", "lucky_day": "शुक्रवार", "lucky_color": "सफेद", "direction": "दक्षिण-पूर्व"},
    7: {"planet": "केतु (Ketu)", "traits": "आध्यात्मिक, शोध विचार", "health": "जोड़ों का दर्द, पैर में चोट", "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः", "gem": "लहसुनिया (Cat's Eye)", "remedy": "कुत्ते को रोटी खिलाएं।", "lucky_day": "मंगलवार", "lucky_color": "चितकबरा", "direction": "उत्तर-पश्चिम"},
    8: {"planet": "शनि (Saturn)", "traits": "कठिन परिश्रम, न्यायप्रियता", "health": "हड्डियों व जोड़ों का दर्द", "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्र्चराय नमः", "gem": "नीलम (Blue Sapphire)", "remedy": "पीपल के नीचे तेल का दीपक जलाएं।", "lucky_day": "शनिवार", "lucky_color": "काला / गहरा नीला", "direction": "पश्चिम"},
    9: {"planet": "मंगल (Mars)", "traits": "साहस, पराक्रम, ऊर्जा", "health": "रक्त विकार, चोट-चपेट", "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः", "gem": "मूंगा (Red Coral)", "remedy": "हनुमान जी की आराधना करें।", "lucky_day": "मंगलवार", "lucky_color": "लाल", "direction": "दक्षिण"}
}

LOSHU_PLANES = {
    "Mental Plane (4-9-2)": ([4, 9, 2], "तीव्र स्मृति व विश्लेषणात्मक सोच।"),
    "Emotional Plane (3-5-7)": ([3, 5, 7], "मजबूत अंतर्ज्ञान शक्ति व दयालुता।"),
    "Practical Plane (8-1-6)": ([8, 1, 6], "व्यावहारिक सोच व व्यावसायिक सफलता।"),
    "Will Power Plane (9-5-1)": ([9, 5, 1], "अटूट इच्छाशक्ति और सफलता प्राप्त करने का जुनून।"),
    "Raj Yoga (4-5-6 / 2-5-8)": ([4, 5, 6], "जीवन में राजयोग व भूमि-भवन का विशेष सुख।")
}

MISSING_REMEDIES = {
    1: "तांबे के पात्र से जल पीएं।",
    2: "चांदी का कड़ा धारण करें।",
    3: "पीला रुमाल पास रखें।",
    4: "तुलसी का पौधा घर में लगाएं।",
    5: "हरा धागा कलाई पर बांधें।",
    6: "सुगंधित इत्र का प्रयोग करें।",
    7: "बुजुर्गों की सेवा करें।",
    8: "समय के पाबंद बनें।",
    9: "लाल रंग का रुमाल रखें।"
}

# ---------------------------------------------------------
# Calculations
# ---------------------------------------------------------
def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_mulank(day):
    return reduce_to_single_digit(day)

def calculate_bhagyank(dob_date):
    dob_str = dob_date.strftime("%Y%m%d")
    total = sum(int(digit) for digit in str(dob_str))
    return reduce_to_single_digit(total)

def calculate_namank(name):
    clean_name = name.upper().replace(" ", "")
    total = sum(CHALDEAN_MAP.get(char, 0) for char in clean_name)
    return reduce_to_single_digit(total) if total > 0 else 0

def get_ascendant_and_rashi(birth_time, dob_date):
    total_minutes = birth_time.hour * 60 + birth_time.minute
    idx = (total_minutes // 120) % 12
    asc_data = RASHI_DATA[idx]
    
    rashi_idx = (dob_date.day + dob_date.month) % 12
    rashi_data = RASHI_DATA[rashi_idx]
    return asc_data, rashi_data

def check_manglik_dosha(asc_data, mulank, bhagyank):
    calc_house = ((mulank + bhagyank) * 3) % 12 + 1
    if calc_house in [1, 4, 7, 8, 12] or asc_data['lord'] == "मंगल (Mars)":
        return True, "⚠ कुण्डली में मांगलिक दोष मौजूद है", f"लग्न/कुंडली गणना के अनुसार मंगल का प्रभाव भाव {calc_house} में है। विवाह से पूर्व कुंडली मिलान आवश्यक है।", "मंगलवार का व्रत रखें व हनुमान चालीसा/सुंदरकांड का पाठ करें।"
    else:
        return False, "✨ कुण्डली गैर-मांगलिक है (Non-Manglik)", "आपकी कुंडली में कोई गंभीर मांगलिक दोष नहीं पाया गया है।", "नियमित सामान्य पूजा-अर्चना करें।"

def get_loshu_grid(dob_date):
    dob_str = dob_date.strftime("%d%m%Y")
    digits = [int(d) for d in dob_str if d != '0']
    grid = {i: [] for i in range(1, 10)}
    for d in digits:
        grid[d].append(d)
    return grid, set(digits)

def generate_report_html(name, dob, tob, mulank, bhagyank, namank, asc_data, rashi_data, is_manglik, mang_status, mang_details, mang_remedy, missing_nums):
    p_info = PLANET_INFO[mulank]
    b_info = PLANET_INFO[bhagyank]
    
    missing_html = "".join([f"<li><b>अंक {num}:</b> {MISSING_REMEDIES[num]}</li>" for num in sorted(missing_nums)]) if missing_nums else "<li>सभी अंक मौजूद हैं।</li>"

    return f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <title>जन्मकुंडली रिपोर्ट</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #1a1a1a; padding: 20px; line-height: 1.6; background: #fff; }}
            h1 {{ text-align: center; color: #6b21a8; border-bottom: 2px solid #6b21a8; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; }}
            td, th {{ border: 1px solid #ccc; padding: 10px; text-align: left; }}
            th {{ background: #f3f4f6; }}
            .card {{ border: 1px solid #ddd; padding: 15px; border-radius: 8px; margin-top: 15px; }}
        </style>
    </head>
    <body>
        <h1>🔮 वैदिक ज्योतिष एवं सम्पूर्ण जन्मकुंडली रिपोर्ट</h1>
        <table>
            <tr><td><b>नाम:</b> {html.escape(name)}</td><td><b>जन्म तिथि:</b> {dob.strftime('%d-%m-%Y')}</td></tr>
            <tr><td><b>समय:</b> {tob.strftime('%I:%M %p')}</td><td><b>जन्म लग्न:</b> {asc_data['rashi']}</td></tr>
            <tr><td><b>चंद्र राशि:</b> {rashi_data['rashi']}</td><td><b>शुभ नामाक्षर:</b> {rashi_data['letters']}</td></tr>
            <tr><td><b>मूलांक:</b> {mulank} ({p_info['planet']})</td><td><b>भाग्यांक:</b> {bhagyank} ({b_info['planet']})</td></tr>
        </table>
        <div class="card">
            <h3>{mang_status}</h3>
            <p>{mang_details}</p>
            <p><b>उपाय:</b> {mang_remedy}</p>
        </div>
        <div class="card">
            <h3>💼 करियर व भविष्यफल</h3>
            <p>स्वामी ग्रह {p_info['planet']} के अनुसार आपमें {p_info['traits']} हैं। {p_info['lucky_day']} का दिन शुभ रहेगा।</p>
        </div>
    </body>
    </html>
    """

# ---------------------------------------------------------
# UI Layout
# ---------------------------------------------------------
st.title("🔮 वैदिक ज्योतिष एवं सम्पूर्ण जन्मकुंडली सॉफ्टवेयर")
st.caption("Complete Vedic Astrology, Kundali & Future Predictions Engine")

st.sidebar.header("📋 जन्म विवरण दर्ज करें")
user_name = st.sidebar.text_input("पूरा नाम (Full Name)", "Kusum")
dob_date = st.sidebar.date_input("जन्म तिथि (Date of Birth)", datetime.date(1990, 10, 25), min_value=datetime.date(1940, 1, 1))
tob_time = st.sidebar.time_input("जन्म समय (Time of Birth)", datetime.time(5, 45))

# Automatic Execution (No button required for default display)
mulank = calculate_mulank(dob_date.day)
bhagyank = calculate_bhagyank(dob_date)
namank = calculate_namank(user_name)
asc_data, rashi_data = get_ascendant_and_rashi(tob_time, dob_date)
is_manglik, mang_status, mang_details, mang_remedy = check_manglik_dosha(asc_data, mulank, bhagyank)
loshu_grid, present_digits = get_loshu_grid(dob_date)
missing_nums = set(range(1, 10)) - present_digits

tab1, tab2, tab3, tab4 = st.tabs([
    "🔮 लग्न, राशि व नामाक्षर",
    "🔥 मांगलिक दोष जाँच",
    "🌟 सम्पूर्ण भविष्यफल",
    "🌿 महा-उपाय व मंत्र"
])

with tab1:
    st.subheader("1. पंचांग, राशि व शुभ नामाक्षर")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("जन्म लग्न", asc_data['rashi'].split()[0], f"स्वामी: {asc_data['lord'].split()[0]}")
    c2.metric("चंद्र राशि", rashi_data['rashi'].split()[0], f"तत्व: {rashi_data['element']}")
    c3.metric("मूलांक", str(mulank), PLANET_INFO[mulank]['planet'].split()[0])
    c4.metric("भाग्यांक", str(bhagyank), PLANET_INFO[bhagyank]['planet'].split()[0])

    st.markdown("---")
    st.success(f"👉 **शुभ नामाक्षर (Name Letters):** **{rashi_data['letters']}**")
    st.caption("इस अक्षर से नाम रखने पर राशि और नक्षत्र का विशेष लाभ प्राप्त होता है।")

with tab2:
    st.subheader("2. मांगलिक दोष रिपोर्ट")
    if is_manglik:
        st.error(f"### {mang_status}")
    else:
        st.success(f"### {mang_status}")
    st.write(f"**विवरण:** {mang_details}")
    st.write(f"**उपाय:** {mang_remedy}")

with tab3:
    st.subheader("3. जीवन का विस्तृत भविष्यफल")
    p_info = PLANET_INFO[mulank]
    st.markdown(f"**💼 करियर व व्यापार:** स्वामी ग्रह **{p_info['planet']}** के प्रभाव से आपमें {p_info['traits']}।")
    st.markdown(f"**💰 आर्थिक स्थिति:** **{p_info['gem']}** धारण करना व **{p_info['lucky_color']}** रंग का उपयोग लाभदायक रहेगा।")
    st.markdown(f"**🩺 स्वास्थ्य:** {p_info['health']} के प्रति सचेत रहें।")

with tab4:
    st.subheader("4. महा-उपाय व सिद्ध मंत्र")
    p_info = PLANET_INFO[mulank]
    st.markdown(f"### 📿 मूलांक {mulank} वैदिक बीज मंत्र:")
    st.code(p_info['mantra'], language="text")
    st.write(f"**दैनिक उपाय:** {p_info['remedy']}")

st.markdown("---")
report_html = generate_report_html(
    user_name, dob_date, tob_time, mulank, bhagyank, namank, asc_data, rashi_data,
    is_manglik, mang_status, mang_details, mang_remedy, missing_nums
)
st.download_button(
    label="📥 सम्पूर्ण रिपोर्ट (HTML/PDF) डाउनलोड करें",
    data=report_html,
    file_name=f"{user_name.replace(' ', '_')}_Kundali_Report.html",
    mime="text/html"
)
