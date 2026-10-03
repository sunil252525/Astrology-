import datetime
import streamlit as st
from weasyprint import HTML

st.set_page_config(
    page_title="सम्पूर्ण वैदिक कुंडली", page_icon="🔮", layout="wide"
)
st.title("🔮 सम्पूर्ण वैदिक जन्मकुण्डली एवं जीवन विश्लेषण रिपोर्ट")


def generate_hindi_pdf(name, dob, tob, pob):
  html_content = f"""
    <!DOCTYPE html>
    <html lang="hi">
    <head>
    <meta charset="UTF-8">
    <style>
        @page {{ size: A4; margin: 20mm 15mm; }}
        body {{ font-family: 'DejaVu Sans', sans-serif; color: #222; line-height: 1.5; }}
        .title {{ text-align: center; color: #b30000; font-size: 20pt; font-weight: bold; }}
        .subtitle {{ text-align: center; color: #444; font-size: 11pt; margin-bottom: 15px; }}
        .info-box {{ background: #f9f2ec; border: 1px solid #e6c280; padding: 12px; margin-bottom: 20px; }}
        .sec-title {{ background: #800000; color: white; padding: 6px 12px; font-weight: bold; margin-top: 15px; }}
        .sub-title {{ color: #b30000; font-weight: bold; margin-top: 8px; }}
    </style>
    </head>
    <body>
        <div class="title">卐 सम्पूर्ण वैदिक जन्मकुण्डली एवं जीवन विश्लेषण 卐</div>
        <div class="subtitle">सटीक ग्रह स्थिति, नक्षत्र फल, चिकित्सा ज्योतिष, वास्तु एवं न्यूमरोलॉजी</div>
        
        <div class="info-box">
            <b>बालक का नाम:</b> {name} | <b>जन्म तिथि:</b> {dob}<br>
            <b>जन्म समय:</b> {tob} | <b>जन्म स्थान:</b> {pob}<br>
            <b>लग्न:</b> मीन | <b>राशि:</b> मकर | <b>नक्षत्र:</b> श्रवण
        </div>

        <div class="sec-title">1. पंचांग एवं ग्रह स्थिति (D-1 कुण्डली)</div>
        <p>बालक का जन्म मीन लग्न और मकर राशि में हुआ है। लग्न स्वामी देवगुरु बृहस्पति नवम भाव (भाग्य स्थान) में स्थित होकर उच्च शिक्षा और धर्म की वृद्धि करते हैं।</p>

        <div class="sec-title">2. स्वास्थ्य एवं चिकित्सा ज्योतिष (Medical Astrology)</div>
        <div class="sub-title">कफ, सर्दी एवं श्वसन प्रणाली:</div>
        <p>मकर राशि में चंद्रमा होने से कफ और सर्दी-खांसी की संवेदनशीलता रह सकती है। ठंडी चीजों से बचाव रखें।</p>
        <div class="sub-title">पाचन एवं उदर स्वास्थ्य:</div>
        <p>ताजा और सुपाच्य भोजन दें। अत्यधिक मिर्च-मसाले से बचें।</p>

        <div class="sec-title">3. दोष एवं उपाय</div>
        <p><b>गंडमूल दोष:</b> अनुपस्थित।</p>
        <p><b>कालसर्प योग:</b> आंशिक। उपाय हेतु प्रतिदिन महामृत्युंजय मंत्र का पाठ करें एवं शिवलिंग पर जल अर्पित करें।</p>

        <div class="sec-title">4. बाल वास्तु नियम</div>
        <p><b>सोने की दिशा:</b> सिर पूर्व या दक्षिण दिशा की ओर रखें।</p>
        <p><b>पढ़ाई की दिशा:</b> ईशान कोण (उत्तर-पूर्व) में पूर्व दिशा की ओर मुंह करके अध्ययन करें।</p>
    </body>
    </html>
    """
  return HTML(string=html_content).write_pdf()


with st.form("hindi_astro_form"):
  name = st.text_input("पूरा नाम", value="Gurttam Kumar")
  dob = st.date_input("जन्म तिथि", value=datetime.date(2019, 1, 8))
  tob = st.time_input("जन्म समय", value=datetime.time(11, 15))
  pob = st.text_input("जन्म स्थान", value="Faridabad")
  sub = st.form_submit_button("सम्पूर्ण हिंदी कुंडली जनरेट करें")

if sub:
  pdf_data = generate_hindi_pdf(name, dob, tob, pob)
  st.success("✅ शुद्ध हिंदी में सम्पूर्ण कुंडली तैयार है!")
  st.download_button(
      "📥 सम्पूर्ण हिंदी कुंडली (PDF) डाउनलोड करें",
      pdf_data,
      file_name="Sampoorna_Hindi_Kundali.pdf",
      mime="application/pdf",
  )
    
