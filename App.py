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
    {"rashi": "मेष (Aries)", "lord": "मंगल (Mars)", "letters": "च, चे, चो, ला, ली, लू, ले, लो, अ", "element": "अग्नि (Fire)", "manglik_risk": "उच्च (High)"},
    {"rashi": "वृषभ (Taurus)", "lord": "शुक्र (Venus)", "letters": "उ, ए, ओ, वा, वी, वू, वे, वो", "element": "पृथ्वी (Earth)", "manglik_risk": "मध्यम (Medium)"},
    {"rashi": "मिथुन (Gemini)", "lord": "बुध (Mercury)", "letters": "का, की, कू, घ, ङ, छ, के, को, हा", "element": "वायु (Air)", "manglik_risk": "सामान्य (Low)"},
    {"rashi": "कर्क (Cancer)", "lord": "चंद्रमा (Moon)", "letters": "ही, हू, हे, हो, डा, डी, डू, डे, डो", "element": "जल (Water)", "manglik_risk": "उच्च (High)"},
    {"rashi": "सिंह (Leo)", "lord": "सूर्य (Sun)", "letters": "मा, मी, मू, मे, मो, टा, टी, टू, टे", "element": "अग्नि (Fire)", "manglik_risk": "उच्च (High)"},
    {"rashi": "कन्या (Virgo)", "lord": "बुध (Mercury)", "letters": "टो, पा, पी, पू, ष, ण, ठा, पे, पो", "element": "पृथ्वी (Earth)", "manglik_risk": "सामान्य (Low)"},
    {"rashi": "तुला (Libra)", "lord": "शुक्र (Venus)", "letters": "रा, री, रू, रे, रो, ता, ती, तू, ते", "element": "वायु (Air)", "manglik_risk": "मध्यम (Medium)"},
    {"rashi": "वृश्चिक (Scorpio)", "lord": "मंगल (Mars)", "letters": "तो, ना, नी, नू, ने, नो, या, यी, यू", "element": "जल (Water)", "manglik_risk": "उच्च (High)"},
    {"rashi": "धनु (Sagittarius)", "lord": "गुरु (Jupiter)", "letters": "ये, यो, भा, भी, भू, धा, फा, ढा, भे", "element": "अग्नि (Fire)", "manglik_risk": "सामान्य (Low)"},
    {"rashi": "मकर (Capricorn)", "lord": "शनि (Saturn)", "letters": "भो, जा, जी, खी, खू, खे, खो, गा, गी", "element": "पृथ्वी (Earth)", "manglik_risk": "उच्च (High)"},
    {"rashi": "कुंभ (Aquarius)", "lord": "शनि (Saturn)", "letters": "गू, गे, गो, सा, सी, सू, से, सो, द", "element": "वायु (Air)", "manglik_risk": "उच्च (High)"},
    {"rashi": "मीन (Pisces)", "lord": "गुरु (Jupiter)", "letters": "दी, दू, थ, झ, ञ, दे, दो, चा, ची", "element": "जल (Water)", "manglik_risk": "सामान्य (Low)"}
]

PLANET_INFO = {
    1: {
        "planet": "सूर्य (Sun)",
        "traits": "नेतृत्व क्षमता, स्वाभिमान, शासन-प्रशासन में रुचि, आत्मविश्वासी व दृढ़ निश्चयी।",
        "health": "सिरदर्द, आंखों की कमजोरी, उच्च रक्तचाप, हृदय व हड्डियों की अड़चनें।",
        "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "gem": "माणिक्य (Ruby)",
        "remedy": "प्रातः सूर्य देव को तांबे के पात्र से जल अर्पण करें और गायत्री मंत्र जपें।",
        "lucky_day": "रविवार", "lucky_color": "लाल / नारंगी", "direction": "पूर्व"
    },
    2: {
        "planet": "चंद्रमा (Moon)",
        "traits": "भावुक, कल्पनाशील, सौम्य, रचनात्मक, चंचल मन व उच्च संवेदनशीलता।",
        "health": "मानसिक तनाव, अवसाद/डिप्रेशन, अनिद्रा, कफ व सर्दी-जुकाम।",
        "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        "gem": "मोती (Pearl)",
        "remedy": "सोमवार को शिवलिंग पर कच्चा दूध व जल चढ़ाएं। माता का नित्य आशीर्वाद लें।",
        "lucky_day": "सोमवार", "lucky_color": "सफेद / चांदी", "direction": "उत्तर-पश्चिम"
    },
    3: {
        "planet": "गुरु (Jupiter)",
        "traits": "ज्ञान, बौद्धिकता, धर्म-कर्म में आस्था, मार्गदर्शन करने में कुशल, महत्वाकांक्षी।",
        "health": "मोटापा, लीवर विकार, पेट के रोग, पाचन तंत्र में ढिलाई।",
        "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "gem": "पुखराज (Yellow Sapphire)",
        "remedy": "गुरुवार को मस्तक पर केसर/हल्दी का तिलक लगाएं। चना दाल का दान करें।",
        "lucky_day": "गुरुवार", "lucky_color": "पीला / सुनहरा", "direction": "उत्तर-पूर्व (ईशान)"
    },
    4: {
        "planet": "राहु (Rahu)",
        "traits": "अचानक सफलता, लीक से हटकर सोच, तीव्र बुद्धि, तकनीक में निपुणता व संघर्ष।",
        "health": "अचानक धन हानि, मानसिक भ्रम, अनिद्रा, त्वचा इंफेक्शन।",
        "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "gem": "गोमेद (Hessonite)",
        "remedy": "शनिवार को पक्षियों को बाजरा डालें व सफाई कर्मचारियों का सम्मान करें।",
        "lucky_day": "शनिवार", "lucky_color": "नीला / ग्रे", "direction": "दक्षिण-पश्चिम"
    },
    5: {
        "planet": "बुध (Mercury)",
        "traits": "तीव्र बुद्धि, व्यापारिक कौशल, मधुर वाणी, तार्किक क्षमता व तुरंत निर्णय लेना।",
        "health": "त्वचा रोग, तंत्रिका तंत्र (Nervous System) की कमजोरी, तनाव।",
        "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "gem": "पन्ना (Emerald)",
        "remedy": "बुधवार को गाय को हरा चारा खिलाएं और तुलसी का पौधा लगाएं।",
        "lucky_day": "बुधवार", "lucky_color": "हरा", "direction": "उत्तर"
    },
    6: {
        "planet": "शुक्र (Venus)",
        "traits": "विलासिता, कला, सौंदर्य प्रेम, सुख-सुविधाओं की लालसा, आकर्षक व्यक्तित्व।",
        "health": "डायबिटीज, किडनी विकार, हार्मोनल असंतुलन।",
        "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "gem": "हीरा (Diamond) / ओपल",
        "remedy": "शुक्रवार को सफेद मिठाई का दान करें और सुगंधित इत्र का प्रयोग करें।",
        "lucky_day": "शुक्रवार", "lucky_color": "सफेद / चमकीला", "direction": "दक्षिण-पूर्व"
    },
    7: {
        "planet": "केतु (Ketu)",
        "traits": "आध्यात्मिक झुकाव, गम्भीर शोध, रहस्यमय सोच, विश्लेषणात्मक व एकांतप्रिय।",
        "health": "जोड़ों व पैरों में दर्द, अलगाववाद, अज्ञात भय, त्वचा रोग।",
        "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "gem": "लहसुनिया (Cat's Eye)",
        "remedy": "चितकबरे कुत्ते को रोटी खिलाएं व गणेश जी की आराधना करें।",
        "lucky_day": "मंगलवार", "lucky_color": "चितकबरा / भूरा", "direction": "उत्तर-पश्चिम"
    },
    8: {
        "planet": "शनि (Saturn)",
        "traits": "कठिन परिश्रम, अनुशासन, न्यायप्रियता, धैर्य, संघर्ष के बाद स्थाई सफलता।",
        "health": "वातरोग, हड्डियों व जोड़ों का दर्द, आलस्य, स्नायु रोग।",
        "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्र्चराय नमः",
        "gem": "नीलम (Blue Sapphire)",
        "remedy": "शनिवार को पीपल के पेड़ के नीचे सरसों के तेल का दीपक जलाएं।",
        "lucky_day": "शनिवार", "lucky_color": "काला / गहरा नीला", "direction": "पश्चिम"
    },
    9: {
        "planet": "मंगल (Mars)",
        "traits": "साहस, पराक्रम, नेतृत्व, ऊर्जावान, भूमि-भवन प्राप्ति, तुरंत निर्णय।",
        "health": "रक्त विकार, चोट-चपेट, उच्च रक्तचाप, अत्यधिक क्रोध।",
        "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "gem": "मूंगा (Red Coral)",
        "remedy": "मंगलवार को सुंदरकांड या हनुमान चालीसा का पाठ करें व लाल वस्तुएं दान करें।",
        "lucky_day": "मंगलवार", "lucky_color": "लाल / सिंदूरी", "direction": "दक्षिण"
    }
}

LOSHU_PLANES = {
    "Mental Plane (4-9-2)": ([4, 9, 2], "तीव्र स्मृति, विश्लेषणात्मक क्षमता और रणनीतिक सोच।"),
    "Emotional Plane (3-5-7)": ([3, 5, 7], "सहानुभूति, आध्यात्मिक झुकाव व मजबूत अंतर्ज्ञान शक्ति।"),
    "Practical Plane (8-1-6)": ([8, 1, 6], "व्यावहारिक सोच, व्यावसायिक सफलता व संपत्ति का लाभ।"),
    "Thought Plane (4-3-8)": ([4, 3, 8], "दूरदर्शिता, दूरगामी योजनाएं व नई सोच का विकास।"),
    "Will Power Plane (9-5-1)": ([9, 5, 1], "दृढ़ इच्छाशक्ति, सफलता प्राप्त करने का अटूट जुनून।"),
    "Action Plane (2-7-6)": ([2, 7, 6], "तुरंत निर्णय लेना, ऊर्जावान निष्पादन और त्वरित परिणाम।"),
    "Raj Yoga 1 (4-5-6)": ([4, 5, 6], "अत्यंत शुभ! जीवन में राजयोग, धन-संपत्ति व स्थायित्व।"),
    "Raj Yoga 2 (2-5-8)": ([2, 5, 8], "भूमि-भवन सुख, रियल एस्टेट में भारी सफलता व आर्थिक मजबूती।")
}

MISSING_REMEDIES = {
    1: "तांबे के बर्तन से जल पीएं व प्रातः सूर्य देव को अर्घ्य दें।",
    2: "जल व्यर्थ न बहाएं। चांदी की चेन या कड़ा धारण करें।",
    3: "पीला रुमाल पास रखें। गुरुजनों एवं बड़ों का आदर करें।",
    4: "लकड़ी या तुलसी की माला पहनें। घर में हरे पौधे लगाएं।",
    5: "ग्रीन एवेंचुरिन क्रिस्टल या हरा धागा पहनें।",
    6: "सुगंधित इत्र और कलाई पर घड़ी पहनें। साफ-सफाई रखें।",
    7: "सफेद या हल्के रंग के कपड़े पहनें। बुजुर्गों की सेवा करें।",
    8: "ब्लैक टूरमैलिन या एमेथिस्ट पहनें। समय के पाबंद बनें।",
    9: "लाल रंग का उपयोग करें। मंदिर में निस्वार्थ सेवा करें।"
}

# ---------------------------------------------------------
# Helper Functions
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
    total = 0
    for char in clean_name:
        if char in CHALDEAN_MAP:
            total += CHALDEAN_MAP[char]
    return reduce_to_single_digit(total) if total > 0 else 0

def get_loshu_grid(dob_date):
    dob_str = dob_date.strftime("%d%m%Y")
    digits = [int(d) for d in dob_str if d != '0']
    grid = {i: [] for i in range(1, 10)}
    for d in digits:
        grid[d].append(d)
    return grid, set(digits)

def get_ascendant_and_rashi(birth_time, dob_date):
    total_minutes = birth_time.hour * 60 + birth_time.minute
    idx = (total_minutes // 120) % 12
    asc_data = RASHI_DATA[idx]
    
    # Rashi based on day calculation
    rashi_idx = (dob_date.day + dob_date.month) % 12
    rashi_data = RASHI_DATA[rashi_idx]
    
    return asc_data, rashi_data

def check_manglik_dosha(asc_data, mulank, bhagyank):
    manglik_houses = [1, 4, 7, 8, 12]
    # Synthetic astrological calculation for Manglik Kundali
    calc_house = ((mulank + bhagyank) * 3) % 12 + 1
    
    if calc_house in manglik_houses or asc_data['lord'] == "मंगल (Mars)":
        is_manglik = True
        status = "⚠️️ कुण्डली में मांगलिक दोष मौजूद है (Manglik Dosh Present)"
        details = f"आपकी जन्म लग्न/कुंडली गणना के अनुसार मंगल का प्रभाव भाव {calc_house} में पड़ता है। विवाह से पूर्व वर-कन्या की कुंडली मिलान आवश्यक है।"
        remedy = "मंगलवार का व्रत रखें, सुंदरकांड का पाठ करें, एवं हनुमान जी को चोला चढ़ाएं। उज्जैन में भात पूजा भी लाभदायक है।"
    else:
        is_manglik = False
        status = "✨ कुण्डली गैर-मांगलिक है (Non-Manglik Kundali)"
        details = "आपकी कुंडली में कोई गंभीर मांगलिक दोष नहीं पाया गया है। वैवाहिक जीवन के लिए यह शुभ संकेत है।"
        remedy = "सामान्य दैनिक पूजा-अर्चना एवं बड़ों का आशीर्वाद बनाए रखें।"
        
    return is_manglik, status, details, remedy

def generate_report_html(name, dob, tob, mulank, bhagyank, namank, asc_data, rashi_data, is_manglik, mang_status, mang_details, mang_remedy, missing_nums, conflicts):
    p_info = PLANET_INFO[mulank]
    b_info = PLANET_INFO[bhagyank]
    
    missing_html = ""
    if missing_nums:
        for num in sorted(missing_nums):
            missing_html += f"<li><b>अंक {num} ({PLANET_INFO[num]['planet']}):</b> {MISSING_REMEDIES[num]}</li>"
    else:
        missing_html = "<li>आपकी जन्म तिथि में सभी अंक मौजूद हैं।</li>"

    conflicts_html = ""
    if conflicts:
        for c in conflicts:
            conflicts_html += f"<div style='background-color: #fdedec; border-left: 5px solid #e74c3c; padding: 10px; margin-bottom: 10px; border-radius: 4px;'><b>⚠️ {html.escape(c['title'])}</b><br>{html.escape(c['desc'])}<br><b>उपाय:</b> {html.escape(c['remedy'])}</div>"
    else:
        conflicts_html = "<div style='background-color: #eafaf1; border-left: 5px solid #27ae60; padding: 10px; margin-bottom: 10px; border-radius: 4px;'>✨ मूलांक और भाग्यांक में कोई प्रत्यक्ष विरोधी संयोजन नहीं है।</div>"

    html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
        <meta charset="UTF-8">
        <title>सम्पूर्ण जन्मकुंडली व भविष्यफल रिपोर्ट</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #2C3E50; padding: 25px; line-height: 1.6; background-color: #fdfefe; }}
            h1 {{ text-align: center; color: #8E44AD; border-bottom: 3px solid #8E44AD; padding-bottom: 10px; margin-bottom: 20px; }}
            h2 {{ color: #2980B9; margin-top: 25px; border-bottom: 2px solid #BDC3C7; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 14px; }}
            td, th {{ padding: 10px; border: 1px solid #BDC3C7; text-align: left; }}
            th {{ background-color: #F2F4F4; color: #34495E; }}
            .mantra {{ background-color: #F4ECF7; padding: 12px; border-radius: 6px; font-weight: bold; text-align: center; font-size: 16px; margin: 10px 0; color: #5B2C6F; border: 1px dashed #8E44AD; }}
            .box {{ padding: 12px; border-radius: 6px; margin-bottom: 12px; }}
            .card {{ background: #ffffff; border: 1px solid #e0e0e0; padding: 15px; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }}
            @media print {{
                .no-print {{ display: none; }}
                body {{ padding: 0; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: right; margin-bottom: 20px;">
            <button onclick="window.print()" style="background-color: #8E44AD; color: white; border: none; padding: 12px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold;">🖨️ कुण्डली प्रिंट करें / PDF सेव करें</button>
        </div>
        
        <h1>🔮 वैदिक ज्योतिष एवं सम्पूर्ण जन्मकुंडली रिपोर्ट</h1>
        
        <table>
            <tr>
                <td><b>जातक का नाम:</b> {html.escape(name)}</td>
                <td><b>जन्म तिथि:</b> {dob.strftime('%d-%m-%Y')}</td>
            </tr>
            <tr>
                <td><b>जन्म समय:</b> {tob.strftime('%I:%M %p')}</td>
                <td><b>जन्म लग्न:</b> {asc_data['rashi']} (स्वामी: {asc_data['lord']})</td>
            </tr>
            <tr>
                <td><b>चंद्र राशि:</b> {rashi_data['rashi']}</td>
                <td><b>नामाक्षर (Name Letters):</b> <span style="color:#d35400; font-weight:bold;">{rashi_data['letters']}</span></td>
            </tr>
            <tr>
                <td><b>मूलांक (Driver):</b> {mulank} ({p_info['planet']})</td>
                <td><b>भाग्यांक (Conductor):</b> {bhagyank} ({b_info['planet']})</td>
            </tr>
            <tr>
                <td colspan="2"><b>नामांक (Name Number):</b> {namank} (Chaldean Method)</td>
            </tr>
        </table>

        <h2>1. मांगलिक दोष जाँच एवं विश्लेषण (Manglik Dosh Test)</h2>
        <div class="card" style="border-left: 5px solid {'#e74c3c' if is_manglik else '#27ae60'};">
            <h3>{mang_status}</h3>
            <p><b>विवरण:</b> {mang_details}</p>
            <p><b>सटीक निवारण/उपाय:</b> {mang_remedy}</p>
        </div>

        <h2>2. नामाक्षर एवं नामकरण (Baby / Name Suggestion)</h2>
        <div class="card">
            <p>ज्योतिषीय गणना के अनुसार आपके लिए सबसे शुभ और भाग्यशाली नाम निम्नलिखित अक्षरों से शुरू होने चाहिए:</p>
            <p style="font-size: 18px; color: #8E44AD; font-weight: bold;">👉 {rashi_data['letters']}</p>
            <p><i>इन्हीं अक्षरों पर नाम रखने से नामांक, राशि और ग्रहों में संतुलन बना रहता है।</i></p>
        </div>

        <h2>3. जीवन का सम्पूर्ण भविष्यफल (Detailed Horoscope Predictions)</h2>
        <div class="card">
            <h4>💼 करियर, नौकरी एवं व्यवसाय (Career & Business)</h4>
            <p>स्वामी ग्रह <b>{p_info['planet']}</b> तथा भाग्यांक स्वामी <b>{b_info['planet']}</b> के प्रभाव से आपके लिए <b>{p_info['direction']}</b> दिशा तथा {p_info['lucky_day']} के दिन शुरू किए गए कार्य विशेष सफलता दिलाएंगे। आप प्रशासनिक कार्यों, प्रबंधन, तकनीक या व्यापार में उच्च स्थान प्राप्त कर सकते हैं।</p>
            
            <h4>💰 धन, संपत्ति व आर्थिक स्थिति (Wealth & Finances)</h4>
            <p>आर्थिक दृष्टिकोण से जीवन में उतार-चढ़ाव के बाद मजबूती आएगी। <b>{p_info['gem']}</b> रत्न तथा <b>{p_info['lucky_color']}</b> रंग का उपयोग आर्थिक लाभ में वृद्धि करेगा।</p>
            
            <h4>❤️ वैवाहिक जीवन व संबंध (Marriage & Relationships)</h4>
            <p>पारिवारिक जीवन में सौहार्द बनाए रखने के लिए वाणी पर नियंत्रण रखें। मांगलिक स्थिति एवं ग्रहों के प्रभाव को संतुलित करने के लिए नियमित मंत्र जप अत्यंत फलदायी रहेगा।</p>

            <h4>🩺 स्वास्थ्य व जीवनशैली (Health & Vitality)</h4>
            <p><b>संभावित स्वास्थ्य चिंताएं:</b> {p_info['health']}</p>
        </div>

        <h2>4. अनुपस्थित अंक (Missing Numbers) एवं उपाय</h2>
        <ul>{missing_html}</ul>

        <h2>5. दोष एवं विरोधी योग विश्लेषण</h2>
        {conflicts_html}

        <h2>6. सर्व-उपाय, महामंत्र एवं सिद्ध रत्न</h2>
        <div class="card">
            <p><b>मूलांक {mulank} वैदिक बीज मंत्र:</b></p>
            <div class="mantra">{p_info['mantra']}</div>
            <p><b>दैनिक उपाय:</b> {p_info['remedy']}</p>
            
            <p><b>भाग्यांक {bhagyank} वैदिक बीज मंत्र:</b></p>
            <div class="mantra">{b_info['mantra']}</div>
            <p><b>दैनिक उपाय:</b> {b_info['remedy']}</p>

            <p><b>शुभ रत्न:</b> {p_info['gem']} | <b>शुभ रंग:</b> {p_info['lucky_color']} | <b>शुभ दिन:</b> {p_info['lucky_day']}</p>
        </div>
    </body>
    </html>
    """
    return html_content

# ---------------------------------------------------------
# Streamlit UI Layout
# ---------------------------------------------------------
st.title("🔮 वैदिक ज्योतिष एवं सम्पूर्ण जन्मकुंडली सॉफ्टवेयर")
st.markdown("### Complete Vedic Astrology, Kundali & Future Predictions Engine")
st.write("---")

st.sidebar.header("📋 जन्म विवरण दर्ज करें (Input Birth Details)")
user_name = st.sidebar.text_input("पूरा नाम (Full Name)", "Kusum")
dob_date = st.sidebar.date_input("जन्म तिथि (Date of Birth)", datetime.date(1990, 10, 25), min_value=datetime.date(1940, 1, 1))
tob_time = st.sidebar.time_input("जन्म समय (Time of Birth)", datetime.time(5, 45))

if st.sidebar.button("📊 सम्पूर्ण जन्मकुंडली व भविष्यफल देखें"):
    mulank = calculate_mulank(dob_date.day)
    bhagyank = calculate_bhagyank(dob_date)
    namank = calculate_namank(user_name)
    asc_data, rashi_data = get_ascendant_and_rashi(tob_time, dob_date)
    is_manglik, mang_status, mang_details, mang_remedy = check_manglik_dosha(asc_data, mulank, bhagyank)
    loshu_grid, present_digits = get_loshu_grid(dob_date)
    missing_nums = set(range(1, 10)) - present_digits
    day_name = dob_date.strftime("%A")

    conflicts = []
    pair = sorted([mulank, bhagyank])
    if pair == [1, 8]:
        conflicts.append({
            "title": "1 और 8 टकराव (सूर्य - शनि)",
            "desc": "पिता-पुत्र में मतभेद, करियर में अत्यधिक संघर्ष, सरकारी कार्यों में रुकावट।",
            "remedy": "सूर्य देव को नित्य जल दें, नीले कपड़े पहनने से बचें।"
        })
    elif pair == [2, 8]:
        conflicts.append({
            "title": "2 और 8 टकराव (विष योग - चंद्र शनि)",
            "desc": "अत्यधिक मानसिक तनाव, डिप्रेशन, कार्य में बार-बार अड़चनें।",
            "remedy": "सोमवार को शिवलिंग पर जलाभिषेक करें और महामृत्युंजय मंत्र पढ़ें।"
        })
    elif pair == [4, 9]:
        conflicts.append({
            "title": "4 और 9 टकराव (अंगारक योग - राहु मंगल)",
            "desc": "अचानक गुस्सा, दुर्घटना की आशंका, कानूनी अड़चनें।",
            "remedy": "हनुमान चालीसा का रोज पाठ करें। शांत रहें।"
        })

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔮 लग्न, राशि व नामाक्षर",
        "🔥 मांगलिक दोष जाँच",
        "🌟 सम्पूर्ण भविष्यफल (Prediction)",
        "🧩 अंकशास्त्र व लो-शू ग्रिड",
        "🌿 महा-उपाय व सिद्ध मंत्र"
    ])

    with tab1:
        st.subheader("1. जन्म पंचांग, राशि व शुभ नामाक्षर (Name Letters)")
        col1, col2, col3, col4 = st.columns(4)
    
