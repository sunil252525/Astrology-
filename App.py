import streamlit as st
import datetime
import html

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Vedic Astrology & Numerology Engine",
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

PLANET_INFO = {
    1: {
        "planet": "सूर्य (Sun)",
        "traits": "नेतृत्व, स्वाभिमान, ऊर्जा, स्वतंत्रता, ईगो।",
        "health": "सिरदर्द, आंखों की कमजोरी, उच्च रक्तचाप, हृदय संबंधी अड़चनें।",
        "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "gem": "माणिक्य (Ruby)",
        "remedy": "तांबे के लोटे से सूर्यदेव को जल दें। गायत्री मंत्र का पाठ करें।"
    },
    2: {
        "planet": "चंद्रमा (Moon)",
        "traits": "भावुकता, कल्पनाशीलता, सौम्यता, चंचल मन, संवेदनशीलता।",
        "health": "मानसिक तनाव, अवसाद/डिप्रेशन, अनिद्रा, सर्दी-जुकाम।",
        "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        "gem": "मोती (Pearl)",
        "remedy": "सोमवार को शिवलिंग पर कच्चा दूध व जल चढ़ाएं। माता का आशीर्वाद लें।"
    },
    3: {
        "planet": "गुरु (Jupiter)",
        "traits": "ज्ञान, परामर्श, अनुशासन, धर्म, महत्वाकांक्षा।",
        "health": "मोटापा, लीवर विकार, पेट के रोग, अति-विश्वास से हानि।",
        "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "gem": "पुखराज (Yellow Sapphire)",
        "remedy": "गुरुवार को केसर/हल्दी का तिलक लगाएं। चना दाल का दान करें।"
    },
    4: {
        "planet": "राहु (Rahu)",
        "traits": "अचानक बदलाव, लीक से हटकर सोच, संघर्ष, तीव्र बुद्धि।",
        "health": "अचानक धन हानि, मानसिक भ्रम, पाचन संबंधी विकार, कानूनी अड़चनें।",
        "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "gem": "गोमेद (Hessonite)",
        "remedy": "शनिवार को पक्षियों को बाजरा डालें। कोढ़ी/सफाई कर्मचारी की सेवा करें।"
    },
    5: {
        "planet": "बुध (Mercury)",
        "traits": "बुद्धि, व्यापार, वाणी, चपलता, तर्कशक्ति।",
        "health": "त्वचा रोग, तंत्रिका तंत्र (Nervous System) की कमजोरी, एकाग्रता की कमी।",
        "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "gem": "पन्ना (Emerald)",
        "remedy": "बुधवार को गाय को हरी घास खिलाएं। तुलसी जी में जल अर्पण करें।"
    },
    6: {
        "planet": "शुक्र (Venus)",
        "traits": "लक्जरी, कला, सौंदर्य, सुख-सुविधाएं, प्रेम।",
        "health": "डायबिटीज, किडनी विकार, अत्यधिक विलासिता से हानि।",
        "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "gem": "हीरा (Diamond) / ओपल",
        "remedy": "शुक्रवार को सफेद मिठाई या चावल का दान करें। सुगंधित इत्र का प्रयोग करें।"
    },
    7: {
        "planet": "केतु (Ketu)",
        "traits": "आध्यात्मिकता, शोध, विश्लेषणात्मक सोच, रहस्य, अकेलापन।",
        "health": "त्वचा इंफेक्शन, जोड़ों/पैरों में दर्द, अलगाववाद, धोखा मिलना।",
        "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "gem": "लहसुनिया (Cat's Eye)",
        "remedy": "चितकबरे कुत्ते को रोटी खिलाएं। गणेश अथर्वशीर्ष का पाठ करें।"
    },
    8: {
        "planet": "शनि (Saturn)",
        "traits": "कड़ी मेहनत, न्याय, ढिलाई/विलंब, संघर्ष, दीर्घकालिक सफलता।",
        "health": "वातरोग, हड्डियों व जोड़ों में दर्द, आलस्य, कार्यों में देरी।",
        "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्र्चराय नमः",
        "gem": "नीलम (Blue Sapphire)",
        "remedy": "शनिवार को सरसों के तेल का दीपक जलाएं। गरीबों व असहायों की मदद करें।"
    },
    9: {
        "planet": "मंगल (Mars)",
        "traits": "ऊर्जा, साहस, आक्रामकता, भूमि, भ्रातृ सुख।",
        "health": "रक्त संबंधी विकार, दुर्घटना/चोट, अत्यधिक गुस्सा, विवाद।",
        "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "gem": "मूंगा (Red Coral)",
        "remedy": "मंगलवार को सुंदरकांड या हनुमान चालीसा का पाठ करें। लाल मसूर दान करें।"
    }
}

LOSHU_PLANES = {
    "Mental Plane (4-9-2)": ([4, 9, 2], "तीव्र स्मृति, विश्लेषणात्मक क्षमता और कल्पनाशीलता।"),
    "Emotional Plane (3-5-7)": ([3, 5, 7], "सहानुभूति, आध्यात्मिक झुकाव व मजबूत अंतर्ज्ञान।"),
    "Practical Plane (8-1-6)": ([8, 1, 6], "व्यावहारिक सोच, व्यावसायिक सफलता व संपत्ति लाभ।"),
    "Thought Plane (4-3-8)": ([4, 3, 8], "दूरदर्शिता, दूरगामी योजनाएं व नई सोच।"),
    "Will Power Plane (9-5-1)": ([9, 5, 1], "दृढ़ इच्छाशक्ति, सफलता प्राप्त करने का जुनून।"),
    "Action Plane (2-7-6)": ([2, 7, 6], "तुरंत निर्णय लेना, ऊर्जावान निष्पादन।"),
    "Raj Yoga 1 (4-5-6)": ([4, 5, 6], "अत्यंत शुभ! जीवन में राजयोग, धन-संपत्ति व स्थिरता।"),
    "Raj Yoga 2 (2-5-8)": ([2, 5, 8], "भूमि-भवन सुख, रियल एस्टेट में सफलता व आर्थिक मजबूती।")
}

MISSING_REMEDIES = {
    1: "तांबे के बर्तन से जल पीएं व सूर्य देव को अर्घ्य दें।",
    2: "जल व्यर्थ न बहाएं। चांदी की चेन या कड़ा धारण करें।",
    3: "पीला रुमाल पास रखें। गुरुजनों का आदर करें।",
    4: "लकड़ी या तुलसी की माला पहनें। हरे पौधे लगाएं।",
    5: "ग्रीन एवेंचुरिन क्रिस्टल या हरा धागा पहनें।",
    6: "सुगंधित इत्र और कलाई पर घड़ी पहनें। साफ-सफाई रखें।",
    7: "सफेद या हल्के रंग के कपड़े पहनें। बुजुर्गों की सेवा करें।",
    8: "ब्लैक टूरमैलिन या एमेथिस्ट पहनें। समय के पाबंद बनें।",
    9: "लाल रंग का उपयोग करें। मंदिर में सेवा करें।"
}

RASHI_NAMES = [
    "मेष (Aries)", "वृषभ (Taurus)", "मिथुन (Gemini)", "कर्क (Cancer)",
    "सिंह (Leo)", "कन्या (Virgo)", "तुला (Libra)", "वृश्चिक (Scorpio)",
    "धनु (Sagittarius)", "मकर (Capricorn)", "कुंभ (Aquarius)", "मीन (Pisces)"
]

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

def get_approx_ascendant(birth_time):
    total_minutes = birth_time.hour * 60 + birth_time.minute
    index = (total_minutes // 120) % 12
    return RASHI_NAMES[index]

def generate_report_html(name, dob, tob, mulank, bhagyank, namank, ascendant, missing_nums, conflicts):
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
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Astrology Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; color: #2C3E50; padding: 20px; line-height: 1.6; }}
            h1 {{ text-align: center; color: #8E44AD; border-bottom: 2px solid #8E44AD; padding-bottom: 10px; }}
            h2 {{ color: #2980B9; margin-top: 20px; border-bottom: 1px solid #BDC3C7; padding-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
            td {{ padding: 8px; border: 1px solid #BDC3C7; }}
            .mantra {{ background-color: #F4ECF7; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; font-size: 16px; margin: 10px 0; }}
            @media print {{
                .no-print {{ display: none; }}
            }}
        </style>
    </head>
    <body>
        <div class="no-print" style="text-align: right; margin-bottom: 20px;">
            <button onclick="window.print()" style="background-color: #8E44AD; color: white; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; font-size: 16px;">🖨️ रिपोर्ट प्रिंट / PDF में सेव करें</button>
        </div>
        <h1>🔮 वैदिक ज्योतिष एवं अंकशास्त्र विस्तृत रिपोर्ट</h1>
        
        <table>
            <tr><td><b>नाम:</b> {html.escape(name)}</td><td><b>जन्म तिथि:</b> {dob.strftime('%d-%m-%Y')}</td></tr>
            <tr><td><b>जन्म समय:</b> {tob.strftime('%I:%M %p')}</td><td><b>अनुमानित लग्न:</b> {ascendant}</td></tr>
            <tr><td><b>मूलांक (Driver):</b> {mulank} ({p_info['planet']})</td><td><b>भाग्यांक (Conductor):</b> {bhagyank} ({b_info['planet']})</td></tr>
            <tr><td colspan="2"><b>नामांक (Name Number):</b> {namank}</td></tr>
        </table>

        <h2>1. मूलांक {mulank} विस्तृत विश्लेषण</h2>
        <p><b>विशेषता व प्रकृति:</b> {p_info['traits']}</p>
        <p><b>संभावित स्वास्थ्य समस्याएं:</b> {p_info['health']}</p>
        <p><b>उपयुक्त रत्न:</b> {p_info['gem']}</p>

        <h2>2. अनुपस्थित अंक (Missing Numbers) एवं उपाय</h2>
        <ul>{missing_html}</ul>

        <h2>3. दोष एवं विरोधी योग विश्लेषण</h2>
        {conflicts_html}

        <h2>4. महा-उपाय एवं वैदिक मंत्र</h2>
        <p><b>मूलांक {mulank} वैदिक बीज मंत्र:</b></p>
        <div class="mantra">{p_info['mantra']}</div>
        <p><b>दैनिक उपाय:</b> {p_info['remedy']}</p>
        
        <p><b>भाग्यांक {bhagyank} वैदिक बीज मंत्र:</b></p>
        <div class="mantra">{b_info['mantra']}</div>
        <p><b>दैनिक उपाय:</b> {b_info['remedy']}</p>
    </body>
    </html>
    """
    return html_content

# ---------------------------------------------------------
# Streamlit UI Layout
# ---------------------------------------------------------
st.title("🔮 वैदिक ज्योतिष एवं अंकशास्त्र कम्प्यूटेशनल सॉफ्टवेयर")
st.markdown("### Vedic Astrology, Numerology & Remedial Engine")
st.write("---")

st.sidebar.header("📋 जन्म विवरण दर्ज करें (Input Details)")
user_name = st.sidebar.text_input("पूरा नाम (Full Name)", "Sunil Kumar")
dob_date = st.sidebar.date_input("जन्म तिथि (Date of Birth)", datetime.date(1990, 10, 25), min_value=datetime.date(1940, 1, 1))
tob_time = st.sidebar.time_input("जन्म समय (Time of Birth)", datetime.time(5, 45))

if st.sidebar.button("📊 जन्मकुंडली व रिपोर्ट जनरेट करें"):
    mulank = calculate_mulank(dob_date.day)
    bhagyank = calculate_bhagyank(dob_date)
    namank = calculate_namank(user_name)
    ascendant = get_approx_ascendant(tob_time)
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
        "📊 मुख्य अंकशास्त्र (Numerology)",
        "🧩 लो-शू ग्रिड (Lo Shu Grid)",
        "🌌 पंचांग व लग्न (Ascendant)",
        "⚠️ दोष व योग (Doshas)",
        "🌿 महा-उपाय व मंत्र (Remedies)"
    ])

    with tab1:
        st.subheader("1. मूलभूत अंकशास्त्र विवरण (Key Numbers)")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("मूलांक (Driver)", mulank, f"ग्रह: {PLANET_INFO[mulank]['planet'].split()[0]}")
        col2.metric("भाग्यांक (Conductor)", bhagyank, f"ग्रह: {PLANET_INFO[bhagyank]['planet'].split()[0]}")
        col3.metric("नामांक (Name No)", namank, "Chaldean System")
        col4.metric("जन्म वार (Day)", day_name)

        st.markdown("---")
        st.write(f"### ☀️ मूलांक {mulank} ({PLANET_INFO[mulank]['planet']}) विस्तृत विश्लेषण:")
        st.write(f"**विशेषता व प्रकृति:** {PLANET_INFO[mulank]['traits']}")
        st.write(f"**संभावित स्वास्थ्य समस्याएं:** {PLANET_INFO[mulank]['health']}")
        st.write(f"**उपयुक्त रत्न:** {PLANET_INFO[mulank]['gem']}")

    with tab2:
        st.subheader("2. लो-शू ग्रिड 3x3 (Lo Shu Grid Diagram)")
        grid_pos = [[4, 9, 2], [3, 5, 7], [8, 1, 6]]
        col_g1, col_g2 = st.columns([1, 1])
        with col_g1:
            st.markdown("#### जन्म तिथि ग्रिड:")
            for row in grid_pos:
                r_str = " | ".join(["".join(str(x) for x in loshu_grid[cell]) if loshu_grid[cell] else " — " for cell in row])
                st.markdown(f"### `[ {r_str} ]` ")

        with col_g2:
            st.markdown("#### सक्रिय योग / प्लेन्स (Active Planes):")
            active_planes = 0
            for p_name, (nums, p_desc) in LOSHU_PLANES.items():
                if set(nums).issubset(present_digits):
                    st.success(f"✅ **{p_name}:** {p_desc}")
                    active_planes += 1
            if active_planes == 0:
                st.info("सामान्य ग्रिड संरचना - कोई विशिष्ट पूर्ण प्लेन योग नहीं है।")

        st.markdown("---")
        st.markdown("#### ❌ अनुपस्थित अंक (Missing Numbers) एवं उनके उपाय:")
        if missing_nums:
            for num in sorted(missing_nums):
                st.warning(f"**अंक {num} अनुपस्थित ({PLANET_INFO[num]['planet']}):** {MISSING_REMEDIES[num]}")
        else:
            st.success("आपकी जन्म तिथि में सभी अंक मौजूद हैं!")

    with tab3:
        st.subheader("3. पंचांग एवं लग्न विवरण (Panchang & Ascendant Details)")
        st.info(f"**अनुमानित जन्म लग्न (Approx Ascendant):** {ascendant}")
        st.write(f"**जन्म तिथि:** {dob_date.strftime('%d %B %Y')}")
        st.write(f"**जन्म समय:** {tob_time.strftime('%I:%M %p')}")

    with tab4:
        st.subheader("4. दोष एवं विरोधी संयोजन पहचान (Dosha Detector)")
        if conflicts:
            for c in conflicts:
                st.error(f"⚠️ **{c['title']}**\n\n**प्रभाव:** {c['desc']}\n\n**सटीक उपाय:** {c['remedy']}")
        else:
            st.success("✨ मूलांक और भाग्यांक में कोई प्रत्यक्ष अति-शत्रुता (Anti-combination) नहीं पाई गई।")

    with tab5:
        st.subheader("5. सर्व-उपाय, महामंत्र एवं समाधान (Remedies & Mantras)")
        st.markdown(f"### 📿 मूलांक {mulank} हेतु वैदिक बीज मंत्र:")
        st.code(PLANET_INFO[mulank]['mantra'], language="text")
        st.write(f"**दैनिक उपाय:** {PLANET_INFO[mulank]['remedy']}")

        st.markdown("---")
        st.markdown(f"### 📿 भाग्यांक {bhagyank} हेतु वैदिक बीज मंत्र:")
        st.code(PLANET_INFO[bhagyank]['mantra'], language="text")
        st.write(f"**दैनिक उपाय:** {PLANET_INFO[bhagyank]['remedy']}")

    st.markdown("---")
    report_html = generate_report_html(
        user_name, dob_date, tob_time, mulank, bhagyank, namank, ascendant,
        missing_nums, conflicts
    )
    st.download_button(
        label="📥 रिपोर्ट HTML/PDF फ़ॉर्मेट में डाउनलोड करें",
        data=report_html,
        file_name=f"{user_name.replace(' ', '_')}_Astrology_Report.html",
        mime="text/html"
    )

else:
    st.info("👈 कृपया बाएं (Sidebar) पैनल में अपना विवरण दर्ज करके **'जन्मकुंडली व रिपोर्ट जनरेट करें'** पर क्लिक करें।")
    
