import streamlit as st
import datetime
import html

# ---------------------------------------------------------
# Page Configuration & Styling
# ---------------------------------------------------------
st.set_page_config(
    page_title="सर्वश्रेष्ठ संपूर्ण वैदिक ज्योतिष व अंकशास्त्र सॉफ्टवेयर",
    page_icon="🔮",
    layout="wide"
)

st.markdown("""
<style>
    .stMetric {
        background-color: #111827 !important;
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
# Master Mappings & Dictionaries
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

NUMEROLOGY_PREDICTIONS = {
    1: {
        "planet": "सूर्य (Sun)",
        "traits": "नेतृत्व, स्वाभिमान, निडरता, महत्वाकांक्षा और स्वतंत्र सोच।",
        "education": "प्रशासनिक पढ़ाई (IAS/IPS), लॉ, पॉलिटिक्स, मैनेजमेंट, और मेडिकल साइंस (सर्जन/डॉक्टर)। गणित व लीडरशिप विषयों में गहरी रुचि रहती है।",
        "marriage": "जीवनसाथी स्वाभिमानी, समझदार और आदर करने वाला मिलेगा। विवाह 25 से 28 वर्ष की आयु में शुभ रहता है।",
        "career": "सरकारी सेवा, उच्च प्रशासनिक पद, राजनीति, मैनेजमेंट, सोलर एनर्जी व बड़े व्यापार।",
        "health": "सिरदर्द, आंखों की समस्या, ब्लड प्रेशर और दिल की सेहत का ध्यान रखें।",
        "dos": "प्रातः सूर्य को जल दें, बड़ों का सम्मान करें, अनुशासन बनाएं।",
        "donts": "अहंकार, अत्यधिक गुस्सा और दूसरों पर हुक्म चलाने से बचें।",
        "mantra": "ॐ ह्रां ह्रीं ह्रौं सः सूर्याय नमः",
        "lucky_nums": "1, 2, 3, 9", "lucky_days": "रविवार, सोमवार", "lucky_colors": "लाल, नारंगी, सुनहरा", "direction": "पूर्व (East)"
    },
    2: {
        "planet": "चंद्रमा (Moon)",
        "traits": "सौम्यता, कल्पनाशीलता, भावुकता, कलात्मक विचार और शांतिप्रियता।",
        "education": "कला, साहित्य, संगीत, मनोविज्ञान (Psychology), नर्सिंग, मरीन/नेवी, डेयरी व होटल मैनेजमेंट। रचनात्मक विषयों में बहुत मन लगता है।",
        "marriage": "जीवनसाथी बेहद सुंदर, भावुक और परिवार की देखभाल करने वाला मिलेगा।",
        "career": "आर्ट्स, राइटिंग, साइकोलॉजी, डेयरी/लिक्विड बिज़नेस, नेवी, मर्चेंट नेवी व कंसल्टेंसी।",
        "health": "कफ, सर्दी-जुकाम, पेट के विकार और मानसिक तनाव (Overthinking) से सावधान रहें।",
        "dos": "शिवलिंग पर दूध-जल चढ़ाएं, मां का आशीर्वाद लें, पानी बर्बाद न करें।",
        "donts": "अत्यधिक भावुक होकर फैसले न लें, तनाव में अकेले रहने से बचें।",
        "mantra": "ॐ श्रां श्रीं श्रौं सः चंद्रमसे नमः",
        "lucky_nums": "1, 2, 4, 7", "lucky_days": "सोमवार, रविवार", "lucky_colors": "सफेद, चांदी, हल्का नीला", "direction": "उत्तर-पश्चिम (North-West)"
    },
    3: {
        "planet": "गुरु (Jupiter)",
        "traits": "ज्ञान, बौद्धिकता, दूरदर्शिता, संस्कार और न्यायप्रिय व्यवहार।",
        "education": "उच्च शिक्षा, कानून/न्यायपालिका (LL.B, Judge), सीए/फाइनेंस, टीचिंग/प्रोफेसरशिप, वेद-शास्त्र या रिसर्च। पढ़ाई में बच्चा हमेशा आगे रहता है।",
        "marriage": "जीवनसाथी सुशिक्षित, संस्कारी, धार्मिक और मार्गदर्शन करने वाला मिलता है। शादी के बाद भाग्य तेजी से चमकता है। 26 से 29 वर्ष में विवाह योग उत्तम है।",
        "career": "शिक्षक, जज, वकील, बैंक मैनेजर, सीए, आध्यात्मिक गुरु, परामर्शदाता (Consultant)।",
        "health": "मोटापा, लीवर की समस्या, डायबिटीज व कोलेस्ट्रॉल का ध्यान रखें।",
        "dos": "गुरुओं व माता-पिता का आदर करें, गुरुवार को चने की दाल या पीली वस्तु दान करें।",
        "donts": "ज्ञान का घमंड न करें, दूसरों को कमतर या अनपढ़ न समझें।",
        "mantra": "ॐ ग्रां ग्रीं ग्रौं सः गुरवे नमः",
        "lucky_nums": "1, 3, 5, 9", "lucky_days": "गुरुवार, मंगलवार", "lucky_colors": "पीला, केसरिया, सुनहरा", "direction": "उत्तर-पूर्व (North-East)"
    },
    4: {
        "planet": "राहु (Rahu)",
        "traits": "तीव्र बुद्धि, आउट-ऑफ-द-बॉक्स सोच, तकनीकी निपुणता और साहसिक कदम।",
        "education": "आईटी, कंप्यूटर साइंस, एआई/डेटा साइंस, इलेक्ट्रॉनिक्स, शेयर मार्केट, रिसर्च व एनिमेशन/गेमिंग। प्रैक्टिकल विषयों में विशेष रुचि रहती है।",
        "marriage": "विवाह अपरंपरागत या अचानक हो सकता है। जीवनसाथी व्यावहारिक और तेज बुद्धि वाला होता है।",
        "career": "सॉफ्टवेयर इंजीनियर, डेटा साइंटिस्ट, साइबर सिक्योरिटी, शेयर ब्रोकर, मीडिया, जासूसी।",
        "health": "अचानक बीमारियां, नसों में खिंचाव, अनिद्रा (Insomnia) व पाचन संबंधी दिक्कत।",
        "dos": "तकनीक का सही उपयोग करें, घर में सफाई रखें, पक्षियों को बाजरा दें।",
        "donts": "सट्टा, जुआ, शॉर्टकट और गलत संगति से पूरी तरह दूर रहें।",
        "mantra": "ॐ भ्रां भ्रीं भ्रौं सः राहवे नमः",
        "lucky_nums": "1, 4, 5, 6, 8", "lucky_days": "शनिवार, बुधवार", "lucky_colors": "नीला, ग्रे, चितकबरा", "direction": "दक्षिण-पश्चिम (South-West)"
    },
    5: {
        "planet": "बुध (Mercury)",
        "traits": "व्यापारिक बुद्धि, हाजिरजवाबी, तार्किक सोच, नेटवर्किंग व वाकपटुता।",
        "education": "कॉमर्स, बिजनेस एडमिनिस्ट्रेशन (MBA), बैंकिंग, एकाउंट्स, मास कम्यूनिकेशन, जर्नलिज्म व लैंग्वेजेस। व्यावहारिक व व्यापारिक पढ़ाई में टॉप करते हैं।",
        "marriage": "जीवनसाथी वाक्पटु, दोस्ताना व्यवहार वाला और खुशमिजाज मिलेगा। दांपत्य जीवन मित्रवत रहता है।",
        "career": "बिजनेसमैन, सीए, मार्केटर, एंकर, पत्रकार, ट्रेडर, स्टॉक एनालिस्ट, कमीशन एजेंट।",
        "health": "त्वचा रोग, एलर्जी, गले की समस्या व तंत्रिका तंत्र कमजोरी।",
        "dos": "बुधवार को गाय को हरा चारा खिलाएं, वाणी पर मधुरता रखें, व्यापार में ईमानदारी बरतें।",
        "donts": "झूठ बोलने, धोखाधड़ी करने और जल्दबाजी में वादे करने से बचें।",
        "mantra": "ॐ ब्रां ब्रीं ब्रौं सः बुधाय नमः",
        "lucky_nums": "1, 3, 5, 6", "lucky_days": "बुधवार, शुक्रवार", "lucky_colors": "हरा, हल्का पीला", "direction": "उत्तर (North)"
    },
    6: {
        "planet": "शुक्र (Venus)",
        "traits": "आकर्षण, कलात्मकता, सौंदर्य प्रेम, विलासिता और आधुनिक सोच।",
        "education": "फैशन डिजाइनिंग, इंटीरियर डिजाइनिंग, फिल्म/मीडिया, आर्किटेक्चर, ललित कला (Fine Arts), टूरिज्म, ऑटोमोबाइल व ब्यूटी/वेलनेस कोर्स।",
        "marriage": "जीवनसाथी अत्यंत आकर्षक, सुंदर, कलाप्रेमी और ऐश्वर्यप्रिय होगा। दांपत्य जीवन सुखद रहता है।",
        "career": "फैशन डिजाइनर, मॉडल, एक्टर, इंटीरियर डेकोरेटर, होटल ओनर, लग्जरी कार डीलर।",
        "health": "शुगर (डायबिटीज), हार्मोनल असंतुलन, किडनी या मूत्र विकार की संभावना।",
        "dos": "हमेशा साफ-सुथरे वस्त्र पहनें, इत्र का प्रयोग करें, महिलाओं का सम्मान करें।",
        "donts": "अत्यधिक कामुकता, फिजूलखर्ची और दिखावे में बहने से बचें।",
        "mantra": "ॐ द्रां द्रीं द्रौं सः शुक्राय नमः",
        "lucky_nums": "5, 6, 8", "lucky_days": "शुक्रवार", "lucky_colors": "सफेद, गुलाबी, सिल्वर", "direction": "दक्षिण-पूर्व (South-East)"
    },
    7: {
        "planet": "केतु (Ketu)",
        "traits": "गहन विश्लेषण, आध्यात्मिक दृष्टि, गूढ़ विद्या में रुचि और शोध प्रवृत्ति।",
        "education": "साइंस रिसर्च, बायोटेक्नोलॉजी, फिलॉसफी, एस्ट्रोलॉजी, आयुर्वेद/होम्योपैथी, योग साइंस व कोडिंग। विषय की गहराई में जाने का गुण होता है।",
        "marriage": "जीवनसाथी शांत, गंभीर और आध्यात्मिक प्रवृत्ति का मिलेगा।",
        "career": "रिसर्चर, साइंटिस्ट, डॉक्टर/हीलर, एस्ट्रोलॉजर, योग शिक्षक, डेटा विश्लेषक।",
        "health": "जोड़ों का दर्द, त्वचा रोग, पैर में चोट और बिना वजह चिंता/घबराहट।",
        "dos": "कुत्तों की सेवा करें, ध्यान-योग अपनाएं, धार्मिक पुस्तकों का अध्ययन करें।",
        "donts": "दुनिया से पूरी तरह कटकर एकांतवासी होने या अकेला रहने से बचें।",
        "mantra": "ॐ स्रां स्रीं स्रौं सः केतवे नमः",
        "lucky_nums": "2, 3, 7", "lucky_days": "मंगलवार, गुरुवार", "lucky_colors": "चितकबरा, हल्का पीला", "direction": "उत्तर-पश्चिम (North-West)"
    },
    8: {
        "planet": "शनि (Saturn)",
        "traits": "कठिन परिश्रम, अनुशासन, धैर्य, न्यायप्रियता व सहनशीलता।",
        "education": "सिविल/मैकेनिकल/माइनिंग इंजीनियरिंग, कानून (Law/Judiciary), रियल एस्टेट, इंफ्रास्ट्रक्चर, मेटलर्जी या पॉलिटिकल साइंस।",
        "marriage": "विवाह अक्सर थोड़ा परिपक्व (Late) आयु (28 से 32 वर्ष) में होता है। जीवनसाथी बेहद वफादार, कर्मठ, गंभीर और सुख-दुख में साथ निभाने वाला होता है।",
        "career": "रियल एस्टेट डेवलपर, प्रॉपर्टी बिज़नेस, जज, सिविल इंजीनियर, माइनिंग ओनर, ठेकेदार।",
        "health": "हड्डियों व नसों का दर्द, वात रोग, दांतों की समस्या और घुटनों की तकलीफ।",
        "dos": "शनिवार को पीपल के नीचे सरसों के तेल का दीपक जलाएं, मजदूरों व गरीबों की मदद करें।",
        "donts": "आलस्य न करें, किसी का हक न मारें और नशे/गलत काम से दूर रहें।",
        "mantra": "ॐ प्रां प्रीं प्रौं सः शनैश्र्चराय नमः",
        "lucky_nums": "3, 5, 6, 8", "lucky_days": "शनिवार, शुक्रवार", "lucky_colors": "काला, गहरा नीला, ग्रे", "direction": "पश्चिम (West)"
    },
    9: {
        "planet": "मंगल (Mars)",
        "traits": "ऊर्जा, अतुल्य साहस, पराक्रम, नेतृत्व और निडर स्वभाव।",
        "education": "डिफेंस/पुलिस साइंस, स्पोर्ट्स एकेडमिक्स, सर्जरी/मेडिकल, मैकेनिकल/इलेक्ट्रिकल इंजीनियरिंग, फायर फाइटिंग व रियल एस्टेट प्रबंधन।",
        "marriage": "जीवनसाथी ऊर्जावान, साहसी और तेज-तर्रार मिलेगा। मांगलिक स्थिति का विशेष ध्यान रखना होता है। गुस्सा काबू रखने से दांपत्य जीवन बहुत सुखद रहता है।",
        "career": "सेना/पुलिस अधिकारी, स्पोर्ट्स पर्सन, सर्जन, प्रॉपर्टी डीलर, बिल्डर, फायर ऑफिसर।",
        "health": "रक्त विकार, बीपी, चोट-चपेट, एसिडिटी व सिर में चोट की आशंका।",
        "dos": "हनुमान जी की उपासना करें, मंगलवार को गुड़-चना दान करें, भाइयों का सहयोग करें।",
        "donts": "अत्यधिक क्रोध, जल्दबाजी में वाहन चलाना और बहसबाज़ी से बचें।",
        "mantra": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "lucky_nums": "1, 3, 9", "lucky_days": "मंगलवार, रविवार", "lucky_colors": "लाल, सिंदूरी, केसरिया", "direction": "दक्षिण (South)"
    }
}

MISSING_REMEDIES = {
    1: "तांबे के बर्तन में पानी पीएं और प्रतिदिन सूर्य देव को जल अर्पित करें।",
    2: "चांदी का एक ठोस गोल टुकड़ा जेब में रखें या गले में चांदी की चेन पहनें।",
    3: "माथे पर रोज केसर/हल्दी का तिलक लगाएं और पीले रुमाल का प्रयोग करें।",
    4: "घर में तुलसी जी का पौधा लगाएं और पक्षियों को नियमित बाजरा/अनाज डालें।",
    5: "कलाई पर हरा धागा बांधें और गाय को बुधवार के दिन हरा चारा खिलाएं।",
    6: "प्रतिदिन हल्के सुगंधित इत्र/परफ्यूम का प्रयोग करें और सफेद वस्त्र पहनें।",
    7: "सड़क के आवारा कुत्तों को नियमित रोटी या बिस्कुट खिलाएं।",
    8: "शनिवार के दिन सरसों का तेल दान करें या पीपल के वृक्ष के नीचे दीया जलाएं।",
    9: "लाल रंग का रुमाल पास रखें और मंगलवार को हनुमान चालीसा का पाठ करें।"
}

# ---------------------------------------------------------
# Utility Calculations
# ---------------------------------------------------------
def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_namank(name):
    clean_name = name.upper().replace(" ", "")
    total = sum(CHALDEAN_MAP.get(char, 0) for char in clean_name)
    return reduce_to_single_digit(total) if total > 0 else 0

def check_manglik_dosha(asc_data, mulank, bhagyank):
    calc_house = ((mulank + bhagyank) * 3) % 12 + 1
    if calc_house in [1, 4, 7, 8, 12] or asc_data['lord'] == "मंगल (Mars)":
        return True, "⚠ कुण्डली में मांगलिक प्रभाव (Manglik Dosha) मौजूद है", f"लग्न एवं ग्रह गणना के अनुसार मंगल का प्रभाव भाव {calc_house} में आ रहा है। विवाह करते समय कुंडली मिलान अनिवार्य रूप से करें।", "प्रति मंगलवार हनुमान जी को सिंदूर चढ़ाएं, सुंदरकांड का पाठ करें और मंगल चंडिका स्तोत्र पढ़ें।"
    else:
        return False, "✨ कुण्डली गैर-मांगलिक है (Non-Manglik)", "आपकी कुंडली में कोई गंभीर मांगलिक दोष नहीं है। दांपत्य जीवन सामान्य व शुभ रहेगा।", "नियमित हनुमान चालीसा का पाठ करें।"

def check_name_compatibility(namank, mulank, bhagyank):
    friendly_map = {
        1: [1, 2, 3, 5, 9],
        2: [1, 2, 3, 5],
        3: [1, 2, 3, 5, 9],
        4: [1, 5, 6, 7, 8],
        5: [1, 2, 3, 5, 6],
        6: [5, 6, 8],
        7: [2, 3, 6, 7],
        8: [3, 5, 6],
        9: [1, 3, 5, 9]
    }
    if namank in friendly_map.get(mulank, []):
        return "उत्तम व अति-अनुकूल (Excellent Compatibility)", "यह नाम आपके मूलांक और भाग्यांक की ऊर्जाओं से पूरी तरह मेल खाता है। यह नाम आपके जीवन में प्रगति, यश और सफलता लाएगा।", "success"
    else:
        return "सामान्य/सुधार योग्य (Neutral or Mild Friction)", "यह नाम आपके मूलांक के साथ आंशिक संबंध बना रहा है। यदि जीवन में कार्य रुकावटें आएं तो नाम में स्पेलिंग बदलकर इसका नामांक बदल सकते हैं।", "warning"

# ---------------------------------------------------------
# Streamlit Main UI Workflow
# ---------------------------------------------------------
st.title("🔮 पूर्ण वैदिक ज्योतिष, अंकशास्त्र एवं भविष्यफल सॉफ्टवेयर")
st.caption("Complete Vedic Kundali, Astro-Numerology, Future Predictions, Career, Education & Marriage Guide")

st.markdown("---")

# Sidebar Steps
st.sidebar.header("📌 चरण 1: जन्म तिथि व समय डालें")
dob_date = st.sidebar.date_input("जन्म तिथि (DOB)", value=datetime.date(2019, 1, 8))
tob_time = st.sidebar.time_input("जन्म समय (Time)", datetime.time(11, 12))

# Calculations based ONLY on DOB and Time
mulank = reduce_to_single_digit(dob_date.day)
dob_str = dob_date.strftime("%Y%m%d")
bhagyank = reduce_to_single_digit(sum(int(d) for d in dob_str))

# Ascendant & Rashi Calc
total_minutes = tob_time.hour * 60 + tob_time.minute
asc_idx = (total_minutes // 120) % 12
asc_data = RASHI_DATA[asc_idx]

rashi_idx = (dob_date.day + dob_date.month) % 12
rashi_data = RASHI_DATA[rashi_idx]

is_manglik, mang_status, mang_details, mang_remedy = check_manglik_dosha(asc_data, mulank, bhagyank)

# Lo Shu missing numbers
digits = [int(d) for d in dob_str if d != '0']
present_digits = set(digits)
missing_nums = set(range(1, 10)) - present_digits

p_info = NUMEROLOGY_PREDICTIONS[mulank]
b_info = NUMEROLOGY_PREDICTIONS[bhagyank]

st.subheader("1️⃣ जन्म तिथि व समय से निकली प्राथमिक ज्योतिषीय गणना")

col1, col2, col3, col4 = st.columns(4)
col1.metric("जन्म लग्न (Ascendant)", asc_data['rashi'].split()[0], f"स्वामी: {asc_data['lord'].split()[0]}")
col2.metric("चंद्र राशि (Moon Sign)", rashi_data['rashi'].split()[0], f"तत्व: {rashi_data['element']}")
col3.metric("मूलांक (Driver)", str(mulank), p_info['planet'].split()[0])
col4.metric("भाग्यांक (Conductor)", str(bhagyank), b_info['planet'].split()[0])

st.success(f"👉 **ज्योतिषशास्त्र के अनुसार बच्चे का नामकरण करने हेतु शुभ नामाक्षर (Letter Suggestions):** **{rashi_data['letters']}**")

st.markdown("---")

st.sidebar.header("📌 चरण 2: रखा गया नाम दर्ज करें")
user_name = st.sidebar.text_input("रखा गया नाम (Full Name)", "Khushwant")

if user_name:
    namank = calculate_namank(user_name)
    compat_status, compat_desc, box_type = check_name_compatibility(namank, mulank, bhagyank)

    st.subheader(f"2️⃣ नाम विश्लेषण एवं संगतता (Name Analysis: {user_name})")
    n1, n2 = st.columns(2)
    n1.info(f"**नामांक (Name Number):** {namank}")
    if box_type == "success":
        n2.success(f"**नाम संगतता:** {compat_status}")
    else:
        n2.warning(f"**नाम संगतता:** {compat_status}")
    
    st.write(compat_desc)

    st.markdown("---")

    # Detailed Tabs Output
    t_astro, t_edu, t_marr, t_career, t_dos, t_remedies = st.tabs([
        "📜 कुण्डली व मूल पहचान",
        "📚 पढ़ाई व रुचि (Education)",
        "💍 विवाह व दांपत्य (Marriage)",
        "💼 करियर व धन (Career & Wealth)",
        "👍 क्या करें / क्या न करें (Do's & Don'ts)",
        "🌿 महा-उपाय व मंत्र (Remedies)"
    ])

    with t_astro:
        st.subheader("📜 कुण्डली व मूल पहचान")
        st.markdown(f"**व्यक्तिगत स्वभाव एवं गुण:** {p_info['traits']}")
        st.markdown(f"**मांगलिक स्थिति:** {mang_status}")
        st.write(mang_details)
        st.markdown(f"**भाग्यांक का प्रभाव:** भाग्यांक **{bhagyank} ({b_info['planet']})** जीवन के 28वें वर्ष के बाद विशेष भाग्य उन्नति देता है।")

    with t_edu:
        st.subheader("📚 पढ़ाई, किस चीज़ में रुचि होगी और किसमें रखें?")
        st.info(f"**मूलांक {mulank} ({p_info['planet']}) के अनुसार शिक्षा मार्गदर्शन:**")
        st.write(p_info['education'])
        st.markdown("""
        > **विशेष सलाह:** यदि बच्चा शुरुआती उम्र में चंचल रहे, तो उसकी रुचि के अनुसार व्यावहारिक पढ़ाई (Practical/Visual Learning) में लगाएं। दबाव डालने के बजाय उसकी प्राकृतिक रुचि वाले क्षेत्र में प्रेरित करें।
        """)

    with t_marr:
        st.subheader("💍 भविष्य में विवाह, जीवनसाथी व दांपत्य जीवन कैसा रहेगा?")
        st.success(f"**विवाह व जीवनसाथी भविष्यवाणी:**")
        st.write(p_info['marriage'])
        st.markdown(f"**मांगलिक उपाय (यदि लागू हो):** {mang_remedy}")

    with t_career:
        st.subheader("💼 भविष्य का करियर, कार्यक्षेत्र व धन-संपदा")
        st.success(f"**उत्कृष्ट करियर विकल्प:** {p_info['careers']}")
        
        c_col1, c_col2, c_col3 = st.columns(3)
        c_col1.metric("शुभ दिशा", p_info['direction'])
        c_col2.metric("शुभ दिन", p_info['lucky_days'])
        c_col3.metric("शुभ अंक", p_info['lucky_nums'])

    with t_dos:
        st.subheader("👍 क्या करना चाहिए और क्या नहीं करना चाहिए?")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            st.success("### ✅ क्या करना चाहिए (Do's)")
            st.write(p_info['dos'])
        with col_d2:
            st.error("### ❌ क्या नहीं करना चाहिए (Don'ts)")
            st.write(p_info['donts'])
        
        st.warning(f"🩺 **स्वास्थ्य सजगता:** {p_info['health']}")

    with t_remedies:
        st.subheader("🌿 सिद्ध महा-उपाय, मंत्र व Missing Number Remedies")
        st.markdown(f"**मूलांक {mulank} का सिद्ध बीज मंत्र:**")
        st.code(p_info['mantra'], language="text")
        
        st.markdown(f"**दैनिक मुख्य उपाय:** {p_info['dos']}")
        
        st.markdown("---")
        st.subheader("❌ अनुपस्थित अंकों के सरल उपाय (Missing Number Remedies)")
        if missing_nums:
            for num in sorted(missing_nums):
                st.write(f"* **अंक {num}:** {MISSING_REMEDIES[num]}")
        else:
            st.write("जन्म तिथि में सभी मुख्य अंक मौजूद हैं।")
            
