import streamlit as st
import datetime
import html

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="सर्वश्रेष्ठ वैदिक ज्योतिष व अंकशास्त्र सॉफ्टवेयर",
    page_icon="🔮",
    layout="wide"
)

# Custom CSS for high contrast & clean UI
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
    .info-card {
        background-color: #111827;
        border-left: 4px solid #8b5cf6;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
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
    1: {
        "planet": "सूर्य (Sun)",
        "traits": "नेतृत्व क्षमता, स्वाभिमान, अनुशासन, निडरता",
        "careers": "सरकारी नौकरी, प्रशासनिक सेवा (IAS/IPS), राजनीति, प्रबंधन, मेडिकल/सर्जन",
        "dos": "समय का पाबंद रहें, प्रातः सूर्य देव को अर्घ्य दें, माता-पिता का सम्मान करें।",
        "donts": "अहंकार और अति-आत्मविश्वास से बचें, दूसरों का अनादर न करें।",
        "health": "सिरदर्द, आंखों की कमजोरी, हृदय संबंधी सजगता",
        "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "gem": "माणिक्य (Ruby)",
        "remedy": "प्रातः तांबे के लोटे से सूर्य देव को जल अर्पित करें।",
        "lucky_days": "रविवार, सोमवार",
        "lucky_colors": "लाल, नारंगी, सुनहरा",
        "lucky_nums": "1, 2, 3, 9",
        "direction": "पूर्व (East)"
    },
    2: {
        "planet": "चंद्रमा (Moon)",
        "traits": "भावुकता, कल्पनाशीलता, सौम्यता, रचनात्मकता",
        "careers": "कला, संगीत, लेखन, मरीन/नेवी, डेयरी/तरल पदार्थ व्यवसाय, साइकोलॉजी",
        "dos": "मानसिक शांति बनाए रखें, शिवलिंग की पूजा करें, बुजुर्गों का आशीर्वाद लें।",
        "donts": "अत्यधिक भावुक होकर फैसले न लें, तनाव व नकारात्मक सोच से दूर रहें।",
        "health": "मानसिक तनाव, कफ/सर्दी, पाचन विकार",
        "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        "gem": "मोती (Pearl)",
        "remedy": "प्रति सोमवार शिवलिंग पर कच्चा दूध व जल चढ़ाएं।",
        "lucky_days": "सोमवार, रविवार",
        "lucky_colors": "सफेद, चांदी, हल्का नीला",
        "lucky_nums": "1, 2, 4, 7",
        "direction": "उत्तर-पश्चिम (North-West)"
    },
    3: {
        "planet": "गुरु (Jupiter)",
        "traits": "ज्ञान, बौद्धिकता, मार्गदर्शन, न्यायप्रियता",
        "careers": "शिक्षा/प्रोफेसर, कानून/जज/वकील, सीए/फाइनेंस, कंसल्टेंसी, धर्म-अध्यात्म",
        "dos": "बड़ों और गुरुओं का सम्मान करें, हमेशा सीखते रहें, धार्मिक कार्य करें।",
        "donts": "दूसरों को नीचा दिखाने या ज्ञान का घमंड करने से बचें।",
        "health": "मोटापा, लीवर, डायबिटीज के प्रति सचेत रहें",
        "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "gem": "पुखराज (Yellow Sapphire)",
        "remedy": "गुरुवार को हल्दी या केसर का तिलक लगाएं और चने की दाल दान करें।",
        "lucky_days": "गुरुवार, मंगलवार",
        "lucky_colors": "पीला, केसरिया, सुनहरा",
        "lucky_nums": "1, 3, 5, 9",
        "direction": "उत्तर-पूर्व (North-East)"
    },
    4: {
        "planet": "राहु (Rahu)",
        "traits": "तीव्र बुद्धि, आउट-ऑफ-द-बॉक्स सोच, तकनीकी निपुणता",
        "careers": "आईटी/सॉफ्टवेयर, डेटा साइंस, रिसर्च, शेयर मार्केट, मीडिया, जासूसी/जांच",
        "dos": "तकनीक का सही इस्तेमाल करें, नियमबद्ध रहें, नियमित ध्यान लगाएं।",
        "donts": "शॉर्टकट, सट्टा, या गलत संगति में पड़ने से बचें।",
        "health": "अचानक तनाव, अनिद्रा, त्वचा संबंधी विकार",
        "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "gem": "गोमेद (Hessonite)",
        "remedy": "पक्षियों को नियमित बाजरा डालें और घर में स्वच्छता रखें।",
        "lucky_days": "शनिवार, बुधवार",
        "lucky_colors": "नीला, ग्रे, चितकबरा",
        "lucky_nums": "1, 4, 5, 6, 8",
        "direction": "दक्षिण-पश्चिम (South-West)"
    },
    5: {
        "planet": "बुध (Mercury)", "traits": "व्यापारिक कौशल, तार्किक सोच, मधुर वाणी, विश्लेषणात्मक क्षमता",
        "careers": "व्यापार/बिजनेस, बैंकिंग, मार्केटिंग, अकाउंट्स, एंकरिंग, पत्रकारिता",
        "dos": "वाणी पर संयम रखें, नेटवर्किंग बढ़ाएं, व्यापारिक हिसाब-किताब साफ़ रखें।",
        "donts": "जल्दबाज़ी में वादे न करें और झूठ बोलने से बचें।",
        "health": "तंत्रिका तंत्र कमजोरी, त्वचा रोग, मानसिक तनाव",
        "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "gem": "पन्ना (Emerald)",
        "remedy": "बुधवार को गाय को हरा चारा खिलाएं या हरी मूंग दान करें।",
        "lucky_days": "बुधवार, शुक्रवार",
        "lucky_colors": "हरा, हल्का पीला",
        "lucky_nums": "1, 3, 5, 6",
        "direction": "उत्तर (North)"
    },
    6: {
        "planet": "शुक्र (Venus)",
        "traits": "विलासिता, कलात्मकता, आकर्षण, सौंदर्य प्रेम",
        "careers": "फैशन, मीडिया/फिल्म, इंटीरियर डिजाइनिंग, लग्जरी गुड्स, ऑटोमोबाइल, टूरिज्म",
        "dos": "साफ़-सुथरे रहें, जीवनसाथी का सम्मान करें, अपनी कला को निखारें।",
        "donts": "अत्यधिक धन खर्च करने व लालच से बचें।",
        "health": "हार्मोनल असंतुलन, डायबिटीज, जल संबंधी विकार",
        "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "gem": "हीरा / ओपल (Opal)",
        "remedy": "सुगंधित इत्र का प्रयोग करें और शुक्रवार को मां लक्ष्मी की पूजा करें।",
        "lucky_days": "शुक्रवार, शुक्रवार",
        "lucky_colors": "सफेद, गुलाबी, सिल्वर",
        "lucky_nums": "5, 6, 8",
        "direction": "दक्षिण-पूर्व (South-East)"
    },
    7: {
        "planet": "केतु (Ketu)",
        "traits": "गहन आध्यात्मिक दृष्टिकोण, शोध विचार, गूढ़ ज्ञान",
        "careers": "शोधकर्ता/वैज्ञानिक, हीलिंग/आयुर्वेद, ज्योतिष, कोडिंग, योग शिक्षक",
        "dos": "आध्यात्मिक मार्ग से जुड़े रहें, असहायों की मदद करें।",
        "donts": "एकांतप्रियता के कारण अपनों से दूरी न बनाएं।",
        "health": "जोड़ों में दर्द, पैर में चोट, अज्ञात भय",
        "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "gem": "लहसुनिया (Cat's Eye)",
        "remedy": "आवारा कुत्तों को रोटी खिलाएं व बड़ों का आशीर्वाद लें।",
        "lucky_days": "मंगलवार, गुरुवार",
        "lucky_colors": "चितकबरा, हल्का पीला",
        "lucky_nums": "2, 3, 7",
        "direction": "उत्तर-पश्चिम (North-West)"
    },
    8: {
        "planet": "शनि (Saturn)",
        "traits": "कठिन परिश्रम, दृढ़ संकल्प, न्यायप्रियता, धैर्य",
        "careers": "रियल एस्टेट/प्रॉपर्टी, कंस्ट्रक्शन, इंजीनियरिंग, जज/कानून, माइनिंग, ऑयल व गैस",
        "dos": "मेहनती और ईमानदार रहें, अधीनस्थों का सम्मान करें, समय का पालन करें।",
        "donts": "आलस्य न करें, किसी का हक न मारें और गलत मार्ग न चुनें।",
        "health": "हड्डियों/जोड़ों का दर्द, वात रोग, नसों की समस्या",
        "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्र्चराय नमः",
        "gem": "नीलम (Blue Sapphire)",
        "remedy": "शनिवार को पीपल के नीचे तेल का दीपक जलाएं और हनुमान जी की सेवा करें।",
        "lucky_days": "शनिवार, शुक्रवार",
        "lucky_colors": "काला, गहरा नीला, ग्रे",
        "lucky_nums": "3, 5, 6, 8",
        "direction": "पश्चिम (West)"
    },
    9: {
        "planet": "मंगल (Mars)",
        "traits": "अतुल्य साहस, ऊर्जा, पराक्रम, नेतृत्व",
        "careers": "सेना/पुलिस, स्पोर्ट्स, रियल एस्टेट, सर्जन, फायर फाइटिंग, माइनिंग",
        "dos": "ऊर्जा का सही उपयोग करें, योग-व्यायाम करें, भाइयों की मदद करें।",
        "donts": "क्रोध और जल्दबाज़ी से बचें, वाहन सावधानी से चलाएं।",
        "health": "रक्त संबंधी विकार, चोट-चपेट, बीपी",
        "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "gem": "मूंगा (Red Coral)",
        "remedy": "प्रति मंगलवार हनुमान चालीसा का पाठ करें और गुड़/चना दान करें।",
        "lucky_days": "मंगलवार, रविवार",
        "lucky_colors": "लाल, सिंदूरी, केसरिया",
        "lucky_nums": "1, 3, 9",
        "direction": "दक्षिण (South)"
    }
}

MISSING_REMEDIES = {
    1: "तांबे के पात्र से पानी पीएं और सूर्य देव को जल दें।",
    2: "चांदी की वस्तु पास रखें या गले में पहनें।",
    3: "माथे पर हल्दी का तिलक लगाएं और पीला रुमाल पास रखें।",
    4: "घर में तुलसी का पौधा लगाएं और बाजरा पक्षियों को दें।",
    5: "हरा धागा कलाई पर बांधें और गाय को हरा चारा खिलाएं।",
    6: "सुगंधित इत्र/परफ्यूम लगाएं और सफेद वस्त्र पहनें।",
    7: "कुत्तों को रोटी खिलाएं और बुजुर्गों की सेवा करें।",
    8: "शनिवार को पीपल के नीचे सरसों के तेल का दीपक जलाएं।",
    9: "लाल रंग का रुमाल पास रखें और हनुमान जी की आराधना करें।"
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
        return True, "⚠ कुण्डली में मांगलिक दोष मौजूद है", f"लग्न व अंक गणना के अनुसार मंगल का प्रभाव भाव {calc_house} में है। विवाह से पूर्व कुंडली मिलान अत्यंत आवश्यक है।", "मंगलवार का व्रत रखें, हनुमान चालीसा व सुंदरकांड का पाठ करें।"
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
        <title>सम्पूर्ण जन्मकुंडली व भविष्यफल रिपोर्ट</title>
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #1f2937; padding: 25px; line-height: 1.6; background: #fff; }}
            h1 {{ text-align: center; color: #6b21a8; border-bottom: 3px solid #6b21a8; padding-bottom: 10px; margin-bottom: 20px; }}
            h2 {{ color: #4c1d95; border-bottom: 1px solid #ddd; padding-bottom: 5px; margin-top: 25px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 20px; }}
            td, th {{ border: 1px solid #cbd5e1; padding: 12px; text-align: left; }}
            th {{ background: #f1f5f9; color: #0f172a; }}
            .card {{ border: 1px solid #e2e8f0; padding: 18px; border-radius: 8px; margin-top: 15px; background: #fafafa; }}
            .highlight {{ color: #16a34a; font-weight: bold; }}
            .alert {{ color: #dc2626; font-weight: bold; }}
            ul {{ padding-left: 20px; }}
            li {{ margin-bottom: 8px; }}
        </style>
    </head>
    <body>
        <h1>🔮 वैदिक ज्योतिष एवं सम्पूर्ण जन्मकुंडली रिपोर्ट</h1>
        <table>
            <tr><td><b>नाम:</b> {html.escape(name)}</td><td><b>जन्म तिथि:</b> {dob.strftime('%d-%m-%Y')}</td></tr>
            <tr><td><b>समय:</b> {tob.strftime('%I:%M %p')}</td><td><b>जन्म लग्न:</b> {asc_data['rashi']}</td></tr>
            <tr><td><b>चंद्र राशि:</b> {rashi_data['rashi']}</td><td><b>शुभ नामाक्षर:</b> {rashi_data['letters']}</td></tr>
            <tr><td><b>मूलांक:</b> {mulank} ({p_info['planet']})</td><td><b>भाग्यांक:</b> {bhagyank} ({b_info['planet']})</td></tr>
            <tr><td><b>नामांक:</b> {namank}</td><td><b>मांगलिक स्थिति:</b> {mang_status}</td></tr>
        </table>

        <h2>💼 1. करियर, भविष्य व क्या बनना चाहिए?</h2>
        <div class="card">
            <p><b>सर्वश्रेष्ठ करियर क्षेत्र:</b> {p_info['careers']}</p>
            <p><b>व्यक्तित्व एवं गुण:</b> मूलांक {mulank} ({p_info['planet']}) के प्रभाव से आपमें {p_info['traits']} हैं। वही भाग्यांक {bhagyank} ({b_info['planet']}) आपके जीवन की दिशा तय करता है।</p>
        </div>

        <h2>👍 2. क्या करें और क्या न करें (Do's & Don'ts)</h2>
        <div class="card">
            <p><b>क्या करना चाहिए (Do's):</b> {p_info['dos']}</p>
            <p><b>क्या नहीं करना चाहिए (Don'ts):</b> <span class="alert">{p_info['donts']}</span></p>
        </div>

        <h2>📅 3. जीवन के मुख्य चरण</h2>
        <div class="card">
            <ul>
                <li><b>बाल्यकाल व शिक्षा (1-18 वर्ष):</b> शिक्षा और सीखने का मुख्य चरण रहेगा। बौद्धिक विकास तीव्र होगा।</li>
                <li><b>युवावस्था व करियर (19-32 वर्ष):</b> करियर स्थापित करने का समय। संघर्ष के बाद बड़ी सफलता प्राप्त होगी।</li>
                <li><b>स्वर्ण काल व स्थायित्व (33+ वर्ष):</b> समाज में सम्मान, वित्तीय मजबूती, गृह-वाहन का पूर्ण सुख मिलेगा।</li>
            </ul>
        </div>

        <h2>🎨 4. शुभ रंग, दिन, अंक व दिशा</h2>
        <table>
            <tr><th>श्रेणी</th><th>विवरण</th></tr>
            <tr><td><b>शुभ अंक</b></td><td>{p_info['lucky_nums']}</td></tr>
            <tr><td><b>शुभ दिन</b></td><td>{p_info['lucky_days']}</td></tr>
            <tr><td><b>शुभ रंग</b></td><td>{p_info['lucky_colors']}</td></tr>
            <tr><td><b>शुभ दिशा</b></td><td>{p_info['direction']}</td></tr>
            <tr><td><b>शुभ रत्न</b></td><td>{p_info['gem']}</td></tr>
        </table>

        <h2>🌿 5. महा-उपाय व सिद्ध मंत्र</h2>
        <div class="card">
            <p><b>बीज मंत्र:</b> <code>{p_info['mantra']}</code></p>
            <p><b>दैनिक महा-उपाय:</b> {p_info['remedy']}</p>
        </div>

        <h2>❌ 6. अनुपस्थित अंक (Missing Numbers) एवं उपाय</h2>
        <div class="card">
            <ul>{missing_html}</ul>
        </div>
    </body>
    </html>
    """

# ---------------------------------------------------------
# UI Layout
# ---------------------------------------------------------
st.title("🔮 वैदिक ज्योतिष एवं सम्पूर्ण जन्मकुंडली सॉफ्टवेयर")
st.caption("Complete Vedic Astrology, Numerology, Lo Shu Grid & Future Predictions Engine")

st.sidebar.header("📋 जन्म विवरण दर्ज करें")
user_name = st.sidebar.text_input("पूरा नाम (Full Name)", "Khushwant")

dob_date = st.sidebar.date_input(
    "जन्म तिथि (Date of Birth)",
    value=datetime.date(2019, 1, 8),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)

tob_time = st.sidebar.time_input("जन्म समय (Time of Birth)", datetime.time(11, 12))

# Calculations Execution
mulank = calculate_mulank(dob_date.day)
bhagyank = calculate_bhagyank(dob_date)
namank = calculate_namank(user_name)
asc_data, rashi_data = get_ascendant_and_rashi(tob_time, dob_date)
is_manglik, mang_status, mang_details, mang_remedy = check_manglik_dosha(asc_data, mulank, bhagyank)
loshu_grid, present_digits = get_loshu_grid(dob_date)
missing_nums = set(range(1, 10)) - present_digits

p_info = PLANET_INFO[mulank]
b_info = PLANET_INFO[bhagyank]

# Tabs UI
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔮 मुख्य पहचान",
    "💼 करियर व भविष्यफल",
    "👍 क्या करें / क्या न करें",
    "🎨 शुभ अंक व रंग",
    "🌿 महा-उपाय व मंत्र"
])

with tab1:
    st.subheader("1. ज्योतिषीय व अंकशास्त्र पहचान")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("जन्म लग्न", asc_data['rashi'].split()[0], f"स्वामी: {asc_data['lord'].split()[0]}")
    c2.metric("चंद्र राशि", rashi_data['rashi'].split()[0], f"तत्व: {rashi_data['element']}")
    c3.metric("मूलांक", str(mulank), p_info['planet'].split()[0])
    c4.metric("भाग्यांक", str(bhagyank), b_info['planet'].split()[0])

    st.markdown("---")
    st.success(f"👉 **शुभ नामाक्षर (Name Letters):** **{rashi_data['letters']}**")
    st.info(f"👉 **नामांक (Name Number):** **{namank}**")
    
    st.markdown("---")
    if is_manglik:
        st.error(f"### {mang_status}")
    else:
        st.success(f"### {mang_status}")
    st.write(f"**विवरण:** {mang_details}")

with tab2:
    st.subheader("2. करियर, भविष्य व क्या बनना चाहिए?")
    st.markdown(f"**🎯 सर्वश्रेष्ठ करियर क्षेत्र:**")
    st.success(p_info['careers'])
    
    st.markdown(f"**🌟 व्यक्तित्व एवं गुण:**")
    st.write(f"मूलांक **{mulank} ({p_info['planet']})** के प्रभाव से आपमें **{p_info['traits']}** हैं। वही भाग्यांक **{bhagyank} ({b_info['planet']})** आपके जीवन के अंतिम लक्ष्य और सफलता को निर्धारित करता है।")

    st.markdown("---")
    st.subheader("📅 आने वाले जीवन के चरण")
    st.markdown("""
    * **बाल्यकाल व शिक्षा (1-18 वर्ष):** सीखने और बौद्धिक विकास का मुख्य समय रहेगा।
    * **युवावस्था व करियर (19-32 वर्ष):** करियर की नींव रखी जाएगी। शुरुआती मेहनत के बाद बड़ा मुकाम मिलेगा।
    * **स्वर्ण काल व स्थायित्व (33+ वर्ष):** समाज में मान-प्रतिष्ठा, अपना घर, गाड़ी और वित्तीय मजबूती प्राप्त होगी।
    """)

with tab3:
    st.subheader("3. क्या करना चाहिए और क्या नहीं करना चाहिए?")
    col_a, col_b = st.columns(2)
    with col_a:
        st.success("### ✅ क्या करना चाहिए (Do's)")
        st.write(p_info['dos'])
    with col_b:
        st.error("### ❌ क्या नहीं करना चाहिए (Don'ts)")
        st.write(p_info['donts'])

    st.markdown("---")
    st.warning(f"🩺 **स्वास्थ्य संबंधी सजगता:** {p_info['health']}")

with tab4:
    st.subheader("4. शुभ अंक, रंग, दिन व दिशा")
    k1, k2, k3 = st.columns(3)
  
