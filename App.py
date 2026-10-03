import streamlit as st
import datetime
import html

# Page Configuration
st.set_page_config(
    page_title="पूर्ण वैदिक ज्योतिष एवं अंकशास्त्र",
    page_icon="🔮",
    layout="wide"
)

# Databases
CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1, 'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3, 'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5, 'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7, 'F': 8, 'P': 8
}

RASHI_DATA = [
    {"rashi": "मेष (Aries)", "lord": "मंगल (Mars)", "letters": "च, चे, चो, ला, ली, लू, ले, लो, अ"},
    {"rashi": "वृषभ (Taurus)", "lord": "शुक्र (Venus)", "letters": "उ, ए, ओ, वा, वी, वू, वे, वो"},
    {"rashi": "मिथुन (Gemini)", "lord": "बुध (Mercury)", "letters": "का, की, कू, घ, ङ, छ, के, को, हा"},
    {"rashi": "कर्क (Cancer)", "lord": "चंद्रमा (Moon)", "letters": "ही, हू, हे, हो, डा, डी, डू, डे, डो"},
    {"rashi": "सिंह (Leo)", "lord": "सूर्य (Sun)", "letters": "मा, मी, मू, मे, मो, टा, टी, टू, टे"},
    {"rashi": "कन्या (Virgo)", "lord": "बुध (Mercury)", "letters": "टो, पा, पी, पू, ष, ण, ठा, पे, पो"},
    {"rashi": "तुला (Libra)", "lord": "शुक्र (Venus)", "letters": "रा, री, रू, रे, रो, ता, ती, तू, ते"},
    {"rashi": "वृश्चिक (Scorpio)", "lord": "मंगल (Mars)", "letters": "तो, ना, नी, नू, ने, नो, या, यी, यू"},
    {"rashi": "धनु (Sagittarius)", "lord": "गुरु (Jupiter)", "letters": "ये, यो, भा, भी, भू, धा, फा, ढा, भे"},
    {"rashi": "मकर (Capricorn)", "lord": "शनि (Saturn)", "letters": "भो, जा, जी, खी, खू, खे, खो, गा, गी"},
    {"rashi": "कुंभ (Aquarius)", "lord": "शनि (Saturn)", "letters": "गू, गे, गो, सा, सी, सू, से, सो, द"},
    {"rashi": "मीन (Pisces)", "lord": "गुरु (Jupiter)", "letters": "दी, दू, थ, झ, ञ, दे, दो, चा, ची"}
]

def reduce_to_single_digit(n):
    while n > 9:
        n = sum(int(digit) for digit in str(n))
    return n

def calculate_namank(name):
    clean_name = name.upper().replace(" ", "")
    total = sum(CHALDEAN_MAP.get(char, 0) for char in clean_name)
    return reduce_to_single_digit(total) if total > 0 else 0

st.title("🔮 पूर्ण वैदिक ज्योतिष एवं अंकशास्त्र विश्लेषक")

st.sidebar.header("Step 1: केवल जन्म विवरण डालें")
dob_date = st.sidebar.date_input("जन्म तिथि (DOB)", value=datetime.date(2019, 1, 8))
tob_time = st.sidebar.time_input("जन्म समय (Time)", datetime.time(11, 12))

# Step 1 Calculations
mulank = reduce_to_single_digit(dob_date.day)
dob_str = dob_date.strftime("%Y%m%d")
bhagyank = reduce_to_single_digit(sum(int(d) for d in dob_str))

# Ascendant & Rashi Calc
total_minutes = tob_time.hour * 60 + tob_time.minute
asc_idx = (total_minutes // 120) % 12
asc_data = RASHI_DATA[asc_idx]

rashi_idx = (dob_date.day + dob_date.month) % 12
rashi_data = RASHI_DATA[rashi_idx]

st.subheader("📌 आपकी जन्म कुंडली व अंकशास्त्र की प्राथमिक गणना")
c1, c2, c3, c4 = st.columns(4)
c1.metric("जन्म लग्न", asc_data['rashi'].split()[0])
c2.metric("चंद्र राशि", rashi_data['rashi'].split()[0])
c3.metric("मूलांक", str(mulank))
c4.metric("भाग्यांक", str(bhagyank))

st.success(f"👉 **ज्योतिष के अनुसार नाम रखने के लिए शुभ नामाक्षर:** **{rashi_data['letters']}**")

st.markdown("---")
st.sidebar.header("Step 2: रखा गया नाम डालें")
user_name = st.sidebar.text_input("रखा गया नाम (Full Name)", "Khushwant")

if user_name:
    namank = calculate_namank(user_name)
    st.subheader(f"📊 नाम विश्लेषण ({user_name}):")
    st.info(f"**नामांक (Name Number):** {namank}")
    
    # Compatibility
    if namank in [1, 3, 5, 6]:
        st.success("✅ यह नाम आपके मूलांक व भाग्यांक के अनुकूल और शुभ है।")
    else:
        st.warning("⚠️️ यह नाम सामान्य प्रभाव दे रहा है, नाम में स्पेलिंग बदलाव पर विचार कर सकते हैं।")
        
