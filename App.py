import os
from weasyprint import HTML, CSS

# 1. HTML सामग्री (दोनों जानकारियों का समावेशन)
html_content = """<!DOCTYPE html>
<html lang="hi">
<head>
    <meta charset="UTF-8">
    <title>संपूर्ण वैदिक ज्योतिष, अंकशास्त्र एवं सनातन कर्मकांड निर्देशिका</title>
    <style>
        @page {
            size: A4;
            margin: 1.5cm;
            @bottom-right {
                content: "पृष्ठ " counter(page) " / " counter(pages);
                font-family: 'FreeSerif', 'DejaVu Sans', serif;
                font-size: 9pt;
                color: #555;
            }
            @bottom-left {
                content: "वैदिक ज्योतिष एवं कर्मकांड निर्देशिका";
                font-family: 'FreeSerif', 'DejaVu Sans', serif;
                font-size: 9pt;
                color: #555;
            }
        }
        
        body {
            font-family: 'FreeSerif', 'DejaVu Sans', sans-serif;
            color: #222;
            line-height: 1.5;
            font-size: 10.5pt;
        }

        .header {
            text-align: center;
            border-bottom: 2px solid #8b0000;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }

        .header h1 {
            color: #8b0000;
            margin: 0;
            font-size: 22pt;
        }

        .header p {
            margin: 5px 0 0 0;
            font-size: 11pt;
            color: #444;
            font-weight: bold;
        }

        .section-title {
            background-color: #8b0000;
            color: #ffffff;
            padding: 6px 12px;
            font-size: 13pt;
            font-weight: bold;
            margin-top: 20px;
            margin-bottom: 10px;
            border-radius: 3px;
        }

        .subsection-title {
            color: #8b0000;
            font-size: 11.5pt;
            font-weight: bold;
            border-bottom: 1px solid #8b0000;
            padding-bottom: 3px;
            margin-top: 12px;
            margin-bottom: 6px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            margin: 10px 0;
            font-size: 9.5pt;
        }

        th, td {
            border: 1px solid #ccc;
            padding: 6px 8px;
            text-align: left;
            vertical-align: top;
        }

        th {
            background-color: #f2e6d9;
            color: #8b0000;
            font-weight: bold;
        }

        ul {
            margin: 5px 0 10px 20px;
            padding: 0;
        }

        li {
            margin-bottom: 4px;
        }

        .highlight-box {
            background-color: #fdf8f0;
            border-left: 4px solid #8b0000;
            padding: 10px 15px;
            margin: 12px 0;
        }

        .page-break {
            page-break-before: always;
        }

        .summary-box {
            background-color: #fff9e6;
            border: 1px solid #e6b800;
            padding: 12px;
            border-radius: 5px;
            margin-top: 15px;
        }
    </style>
</head>
<body>

    <div class="header">
        <h1>संपूर्ण वैदिक ज्योतिष, अंकशास्त्र एवं सनातन कर्मकांड निर्देशिका</h1>
        <p>ज्योतिष शास्त्र, अंकशास्त्र, वास्तु शास्त्र, नवजात शिशु संस्कार एवं कर्मकांड का संपूर्ण प्रामाणिक विवरण</p>
    </div>

    <!-- भाग 1: अंकशास्त्र, वास्तु एवं शिशु ज्योतिष विचार -->
    <div class="section-title">भाग 1: अंकशास्त्र, वास्तु एवं शिशु ज्योतिष विचार</div>

    <div class="subsection-title">1. अंकशास्त्र एवं नाम विज्ञान (Numerology & Name Astrology)</div>
    <ul>
        <li><strong>मूलांक (Driver Number):</strong> जन्म की तारीख का योग (जैसे 14 तारीख = 1+4 = 5), जो बच्चे का मूल स्वभाव बताता है।</li>
        <li><strong>भाग्यांक (Conductor / Destiny Number):</strong> पूरी जन्मतिथि (तारीख + महीना + साल) का योग, जो जीवन की दिशा और भाग्य दिखाता है।</li>
        <li><strong>नामांक (Name Number):</strong> बच्चे के नाम के अक्षरों का योग। इसे मूलांक/भाग्यांक के साथ संतुलित (Name Correction) किया जाता है ताकि जीवन में संघर्ष कम हो।</li>
        <li><strong>लो-शू ग्रिड (Lo Shu Grid):</strong> जन्मतिथि के अंकों को एक 3x3 के वर्गाकार ग्रिड में रखकर यह देखना कि जीवन में कौन से तत्व (जल, अग्नि, पृथ्वी, धातु, लकड़ी) मौजूद हैं और कौन से अनुपस्थित हैं।</li>
        <li><strong>पर्सनल ईयर/मंथ (Personal Year Calculation):</strong> हर साल बच्चे के जीवन में आने वाले सकारात्मक और नकारात्मक बदलावों की गणितीय गणना।</li>
    </ul>

    <div class="subsection-title">2. वास्तु शास्त्र एवं वातावरण संतुलन (Vastu Shastra)</div>
    <ul>
        <li><strong>बच्चे के शयनकक्ष की दिशा (Nursery Vastu):</strong> बच्चा किस दिशा में सोए (उत्तर-पूर्व/ईशान कोण पढ़ाई और स्वास्थ्य के लिए शुभ माना जाता है)।</li>
        <li><strong>अध्ययन कक्ष (Study Vastu):</strong> पढ़ाई करते समय चेहरा किस दिशा में हो (पूर्व या उत्तर)।</li>
        <li><strong>दिशा-दोष एवं निवारण:</strong> घर की किस दिशा का ऊर्जा संतुलन बच्चे की प्रगति या मानसिक स्थिति पर असर डाल रहा है।</li>
    </ul>

    <div class="subsection-title">3. जन्मकालीन वैदिक गणनाएँ एवं योग (Natal Astrological Yoga & Dosha)</div>
    <ul>
        <li><strong>शुभ योग:</strong>
            <ul>
                <li><strong>राजयोग:</strong> सफलता और पद-प्रतिष्ठा।</li>
                <li><strong>धन योग:</strong> आर्थिक समृद्धि।</li>
                <li><strong>गजकेसरी योग:</strong> बुद्धि और मान-सम्मान।</li>
                <li><strong>पंच महापुरुष योग:</strong> रुचक, भद्र, हंस, मालव्य, शश योग।</li>
            </ul>
        </li>
        <li><strong>अशुभ योग व दोष:</strong>
            <ul>
                <li><strong>गंडमूल दोष:</strong> जन्म नक्षत्र का दोष।</li>
                <li><strong>कालसर्प दोष:</strong> राहू-केतु के बीच सभी ग्रहों का आना।</li>
                <li><strong>मांगलिक दोष:</strong> विवाह और स्वभाव पर असर।</li>
                <li><strong>ग्रहण दोष / पितृ दोष:</strong> सूर्य/चंद्र या पूर्वजों से जुड़े दोष।</li>
                <li><strong>बालारिष्ट दोष:</strong> शैशवावस्था में स्वास्थ्य से जुड़े खतरे।</li>
            </ul>
        </li>
    </ul>

    <div class="subsection-title">4. कर्मकांड, संस्कार एवं सुरक्षा चक्र (Vedic Rituals & Sanskar)</div>
    <ul>
        <li><strong>षोडश संस्कार (16 Sanskars):</strong> जातकर्म, नामकरण, निष्क्रमण, अन्नप्राशन, चूड़ाकरण/मुंडन, कर्णवेध, विद्यारंभ एवं उपनयन (जनेऊ) संस्कार।</li>
        <li><strong>दोष शांति पूजा:</strong> गंडमूल शांति, मूल शांति, नवग्रह शांति, और रुद्रि-पाठ।</li>
        <li><strong>सुरक्षा कवच एवं रत्न विचार:</strong>
            <ul>
                <li><strong>इष्ट देव/देवी पहचान:</strong> बच्चे के जन्म के अनुसार जीवनभर रक्षा करने वाले देवता।</li>
                <li><strong>भाग्यशाली रत्न (Gemstones):</strong> जीवन रत्न (Life Stone), भाग्य रत्न (Lucky Stone), और कारक रत्न।</li>
                <li><strong>रुद्राक्ष एवं धातु:</strong> 1 मुखी, 4 मुखी, 5 मुखी रुद्राक्ष या तांबा/चांदी/सोना धारण करना।</li>
            </ul>
        </li>
    </ul>

    <div class="subsection-title">5. पूर्वजन्म (Past Life) और भावी जीवन चक्र</div>
    <ul>
        <li><strong>कर्म सिद्धांत एवं पूर्वजन्म (Past Life Karma):</strong> डी-60 (द्विषष्ट्यांश कुंडली) द्वारा संचित कर्मों का विश्लेषण एवं पितृ ऋण विचार।</li>
        <li><strong>भविष्यफल और समय चक्र:</strong> विंशोत्तरी महादशा / अंतर्दशा (120 वर्ष का सटीक समय-सारणी), अष्टकवर्ग एवं गोचर, तथा वर्षफल (Solar Return)।</li>
    </ul>

    <div class="subsection-title">6. समुद्र शास्त्र एवं अंग लक्षण (Samudrika Shastra / Palmistry)</div>
    <ul>
        <li><strong>हस्तरेखा (Palmistry):</strong> मुख्य रेखाएँ (जीवन, मस्तिष्क, हृदय, भाग्य) और पर्वतों (Mounts) की बनावट।</li>
        <li><strong>अंग लक्षण शास्त्र:</strong> शरीर के तिल, चक्र, रेखाओं और शारीरिक लक्षणों से भाग्य का आकलन।</li>
    </ul>

    <div class="summary-box">
        <strong>सारांश (Summary for a Newborn Child):</strong><br>
        नवजात बच्चे का संपूर्ण चार्ट/रिकॉर्ड निम्न बिंदुओं पर आधारित होता है:
        <ol>
            <li>वैदिक पंचांग एवं जन्म कुंडली (D1 से D60 तक)</li>
            <li>न्यूमरोलॉजी रिपोर्ट (मूलांक, भाग्यांक, नामांक व लो-शू ग्रिड)</li>
            <li>गंडमूल / बालारिष्ट / कालसर्प व अन्य दोष विचार</li>
            <li>इष्टदेव, कुलदेवता, शुभ रत्न, रंग व लकी नंबर</li>
            <li>वास्तु दिशा निर्देश (सोने व पढ़ाई का स्थान)</li>
            <li>16 संस्कारों की तिथि और शांति पूजा की सूची</li>
        </ol>
    </div>

    <div class="page-break"></div>

    <!-- भाग 2: संदर्भ निर्देशिका (PDF गाइड सामग्री) -->
    <div class="section-title">भाग 2: संपूर्ण वैदिक ज्योतिष एवं सनातन कर्मकांड निर्देशिका</div>

    <div class="subsection-title">1. ज्योतिष शास्त्र के तीन स्कंध (Branches)</div>
    <table>
        <tr>
            <th>स्कंध</th>
            <th>विवरण एवं क्षेत्र</th>
        </tr>
        <tr>
            <td><strong>1. सिद्धांत (Ganita / Astronomy)</strong></td>
            <td>ग्रहों की गति, स्थिति, सूर्य-चंद्र ग्रहण, नक्षत्र-मंडल तथा गणितीय काल-विभाग (युग, मन्वंतर, वर्ष, अयन, ऋतु, मास) की सूक्ष्म गणनाएँ।</td>
        </tr>
        <tr>
            <td><strong>2. संहिता (Mundane / Macro-Astrology)</strong></td>
            <td>सामूहिक घटनाएँ, प्राकृतिक आपदाएँ, मौसम, देश-दुनिया का भविष्य, कृषि, व्यापारिक मंदी-तेजी तथा मेदिनी ज्योतिष का अध्ययन।</td>
        </tr>
        <tr>
            <td><strong>3. होरा (Predictive / Natal)</strong></td>
            <td>व्यक्तिगत जन्म-कुंडली का अध्ययन, भविष्यफल, आयु, दशा, गोचर, तथा 16 वर्गीय कुंडलियों (षोडशवर्ग) का फलित विचार।</td>
        </tr>
        <tr>
            <td><strong>4. प्रश्न एवं मुहूर्त (Horary & Electional)</strong></td>
            <td>तात्कालिक प्रश्नों के उत्तर देने की विद्या (प्रश्न शास्त्र) तथा शुभ कार्यों हेतु काल-शोधन (मुहूर्त विज्ञान)।</td>
        </tr>
    </table>

    <div class="subsection-title">2. पंचांग के 5 मूलभूत अंग (Panchang)</div>
    <table>
        <tr>
            <th>अंग</th>
            <th>परिभाषा एवं आधार</th>
            <th>शास्त्रीय महत्व</th>
        </tr>
        <tr>
            <td><strong>1. तिथि (Tithi)</strong></td>
            <td>सूर्य और चंद्रमा के मध्य 12 अंश (Degrees) की दूरी। कुल 30 तिथियाँ (15 शुक्ल + 15 कृष्ण पक्ष)।</td>
            <td>कार्य सिद्धि, व्रत-पर्व एवं धार्मिक अनुष्ठानों का निर्धारण।</td>
        </tr>
        <tr>
            <td><strong>2. वार (Vaar)</strong></td>
            <td>सूर्योदय से अगले सूर्योदय तक का दिन (सोम से रवि तक 7 वार)।</td>
            <td>शारीरिक ऊर्जा, मानसिक शक्ति एवं कार्य की प्रकृति।</td>
        </tr>
        <tr>
            <td><strong>3. नक्षत्र (Nakshatra)</strong></td>
            <td>भचक्र के 27 तारामंडल (प्रत्येक 13°20') + 1 अभिजित नक्षत्र।</td>
            <td>दशा निर्धारण, नामकरण, चरित्र एवं मानसिक प्रकृति।</td>
        </tr>
        <tr>
            <td><strong>4. योग (Yoga)</strong></td>
            <td>सूर्य और चंद्रमा के देशांतर का जोड़ (कुल 27 योग)।</td>
            <td>भाग्य, स्वास्थ्य एवं विशिष्ट कर्मों का फल।</td>
        </tr>
        <tr>
            <td><strong>5. करण (Karana)</strong></td>
            <td>एक तिथि का आधा भाग (6 अंश)। कुल 11 करण (7 चर + 4 स्थिर)।</td>
            <td>तत्कालिक कार्य एवं अल्पकालिक बाधाओं का विचार।</td>
        </tr>
    </table>

    <div class="subsection-title">3. नवग्रह, 12 राशियां एवं 12 भाव (Houses)</div>
    <p><strong>नवग्रह (9 Planets):</strong> सूर्य (आत्मा), चंद्र (मन), मंगल (पराक्रम), बुध (बुद्धि), गुरु (ज्ञान/संतान), शुक्र (सुख/विवाह), शनि (कर्म/आयु), राहू (माया/भ्रम), केतु (मोक्ष/वैराग्य)।</p>
    
    <table>
        <tr>
            <th>भाव (House)</th>
            <th>प्रतिनिधित्व / जीवन के आयाम</th>
            <th>कारकतत्व</th>
        </tr>
        <tr><td>प्रथम (लग्न)</td><td>तन, स्वभाव, रूप-रंग, स्वास्थ्य, संपूर्ण व्यक्तित्व</td><td>सूर्य</td></tr>
        <tr><td>द्वितीय</td><td>धन, कुटुंब, वाणी, प्रारम्भिक शिक्षा, दाहिनी आंख</td><td>गुरु</td></tr>
        <tr><td>तृतीय</td><td>छोटे भाई-बहन, साहस, पराक्रम, छोटी यात्राएं, लेखन</td><td>मंगल</td></tr>
        <tr><td>चतुर्थ</td><td>माता, गृह-सुख, भूमि, भवन, वाहन, मानसिक शांति</td><td>चंद्रमा</td></tr>
        <tr><td>पंचम</td><td>संतान, बुद्धि, ज्ञान, पूर्व जन्म के पुण्य, प्रेम</td><td>गुरु</td></tr>
        <tr><td>षष्ठ</td><td>रोग, ऋण, शत्रु, प्रतिस्पर्धा, मामा, सेवा</td><td>मंगल, शनि</td></tr>
        <tr><td>सप्तम</td><td>विवाह, जीवनसाथी, साझेदारी, व्यापार, दैनिक रोजगार</td><td>शुक्र</td></tr>
        <tr><td>अष्टम</td><td>आयु, मृत्यु का कारण, गूढ़ विज्ञान, अचानक धन/बाधा</td><td>शनि</td></tr>
        <tr><td>नवम</td><td>धर्म, भाग्य, पिता, लंबी यात्राएं, गुरु, उच्च शिक्षा</td><td>गुरु, सूर्य</td></tr>
        <tr><td>दशम</td><td>कर्म, नौकरी, व्यापार, पद-प्रतिष्ठा, राज्य पक्ष</td><td>सूर्य, बुध, शनि</td></tr>
        <tr><td>एकादश</td><td>आय, लाभ, बड़े भाई-बहन, इच्छा पूर्ति, मित्र</td><td>गुरु</td></tr>
        <tr><td>द्वादश</td><td>व्यय (खर्च), मोक्ष, विदेश यात्रा, अस्पताल, शयन सुख</td><td>शनि, केतु</td></tr>
    </table>

    <div class="subsection-title">4. दशा एवं गोचर (Timing of Events)</div>
    <ul>
        <li><strong>विंशोत्तरी महादशा (120 वर्ष):</strong> जन्म नक्षत्र के आधार पर तय होती है। इसमें महादशा, अंतर्दशा, प्रत्यंतर्दशा और सूक्ष्म दशा से घटनाओं का सटीक समय ज्ञात किया जाता है।</li>
        <li><strong>गोचर (Transit):</strong> वर्तमान समय में ग्रहों की वास्तविक चाल। दशा आंतरिक परिस्थिति बनाती है तथा गोचर बाहरी परिस्थिति प्रदान कर घटना घटित करता है।</li>
        <li><strong>अष्टकवर्ग (Ashtakvarga System):</strong> 8 स्रोतों (7 ग्रह + लग्न) से प्राप्त शुभ-अशुभ बिंदुओं की गणितीय प्रणाली, जिससे किसी स्थान विशेष पर ग्रह का वास्तविक बल ज्ञात होता है।</li>
    </ul>

    <div class="subsection-title">5. शिशु जन्म पर आवश्यक वैदिक विचार एवं प्रक्रियाएँ</div>
    <ul>
        <li><strong>1. जन्म समय की शुद्धि (Birth Time Rectification):</strong> क्षितिज पर लग्न के अंशों एवं प्राण दशा से सही समय का मिलान।</li>
        <li><strong>2. इष्टकाल एवं स्पष्ट ग्रह सारणी:</strong> स्थानिक समय (Local Mean Time) के आधार पर लग्न एवं ग्रहों के स्पष्ट अंश ज्ञात करना।</li>
        <li><strong>3. नामाकरण अक्षर (Name Letter):</strong> बालक के जन्म नक्षत्र के चरण (Quarter) के आधार पर प्रथम अक्षर तय करना।</li>
        <li><strong>4. गंडमूल दोष विचार:</strong> 6 विशेष नक्षत्रों (अश्विनी, अश्लेषा, मघा, ज्येष्ठा, मूल, रेवती) में जन्म होने पर 27वें दिन गंडमूल शांति पूजन अनिवार्य है।</li>
        <li><strong>5. पाया विचार (Paya):</strong> चंद्रमा की भाव-स्थिति के आधार पर सोने (कष्टकारक), चाँदी (अति शुभ), तांबे (सामान्य/शुभ), या लोहे (संघर्षमय) का पाया तय होता है।</li>
        <li><strong>6. पंचक विचार:</strong> धनिष्ठा से रेवती तक के 5 नक्षत्रों में जन्म होने पर विशेष शांति विधान।</li>
        <li><strong>7. बालारिष्ट एवं अरिष्ट भंग:</strong> प्रथम 8-12 वर्षों में स्वास्थ्य या आयु पर किसी ग्रह का कोई विशेष अरिष्ट प्रभाव तो नहीं है।</li>
    </ul>

    <div class="subsection-title">6. षोडश संस्कार (16 Hindu Sacraments)</div>
    <table>
        <tr>
            <th>चरण</th>
            <th>संस्कार का नाम</th>
            <th>उद्देश्य एवं समय</th>
        </tr>
        <tr>
            <td>गर्भ-काल (Pre-Natal)</td>
            <td>1. गर्भाधान, 2. पुंसवन, 3. सीमंतोन्नयन</td>
            <td>उत्तम संतति प्राप्ति, गर्भ सुरक्षा एवं शिशु के मानसिक विकास हेतु।</td>
        </tr>
        <tr>
            <td>बाल्यकाल (Childhood)</td>
            <td>4. जातकर्म, 5. नामकरण, 6. निष्क्रमण, 7. अन्नप्राशन, 8. चूडाकरण (मुंडन), 9. कर्णवेध</td>
            <td>शिशु का नाल-च्छेदन, नाम-संस्कार, प्रथम गृह-आगमन, ठोस आहार, स्वच्छता एवं स्वास्थ्य रक्षा हेतु।</td>
        </tr>
        <tr>
            <td>विद्यारंभ (Education)</td>
            <td>10. विद्यारंभ, 11. उपनयन (जनेऊ), 12. वेदारंभ, 13. केशांत/समावर्तन</td>
            <td>अक्षर ज्ञान, गायत्री दीक्षा, संयमित ब्रह्मचर्य जीवन एवं शिक्षा की पूर्णता।</td>
        </tr>
        <tr>
            <td>गृहस्थ एवं अंत (Adult & Beyond)</td>
            <td>14. विवाह, 15. वानप्रस्थ/संन्यास, 16. अंत्येष्टि</td>
            <td>धर्म-अर्थ-काम की सिद्धि, समाज सेवा तथा आत्मा की शांति हेतु अंतिम संस्कार।</td>
        </tr>
    </table>

    <div class="subsection-title">7. षोडशवर्ग (16 Divisional Charts - सूक्ष्म विचार)</div>
    <ul>
        <li><strong>D-1 (लग्न):</strong> शारीरिक स्वरूप एवं जीवन का सामान्य खाका।</li>
        <li><strong>D-7 (सप्तमांश):</strong> संतान सुख, संतान की प्रगति एवं वंश वृद्धि।</li>
        <li><strong>D-9 (नवांश - Navamsha):</strong> विवाह, जीवनसाथी, धार्मिक झुकाव एवं आंतरिक बल (अत्यंत महत्वपूर्ण)।</li>
        <li><strong>D-10 (दशमांश):</strong> आजीविका, नौकरी, व्यापार, सफलता एवं उच्च पद।</li>
        <li><strong>D-12 (द्वादशांश):</strong> माता-पिता का सुख, उनका स्वास्थ्य एवं पितृ ऋण।</li>
        <li><strong>D-60 (द्विषष्ट्यांश):</strong> पूर्व जन्म के कर्म, सूक्ष्म संचित कर्म एवं अंतिम फलित।</li>
    </ul>

    <div class="subsection-title">8. पितृ ऋण, श्राद्ध एवं कुल परंपरा (Ancestor Rituals)</div>
    <ul>
        <li><strong>पितृ पक्ष एवं श्राद्ध कर्म:</strong> भाद्रपद पूर्णिमा से आश्विन अमावस्या (16 दिन) तक पूर्वजों का जल तर्पण, पिंड दान एवं ब्राह्मण भोजन कराना।</li>
        <li><strong>नित्य पंचमहायज्ञ:</strong> गृहस्थ जीवन में नित्य किए जाने वाले 5 यज्ञ - ब्रह्मयज्ञ (स्वाध्याय), देवयज्ञ (हवन), पितृयज्ञ (तर्पण), मनुष्ययज्ञ (अतिथि सेवा), और भूतयज्ञ (पशु-पक्षियों को भोजन)।</li>
        <li><strong>कुलदेवी / कुलदेवता पूजन:</strong> परिवार की वंश परंपरा की रक्षा हेतु विशेष अवसरों (विवाह, मुंडन, नवरात्रि) पर कुलदेवता का दर्शन व विशेष पूजन।</li>
        <li><strong>ग्रह शांति एवं दोष निवारण:</strong> कालसर्प योग, मांगलिक दोष, पितृ दोष, ग्रहण दोष आदि की शांति हेतु मंत्र जप, होम-हवन एवं दान विधान।</li>
    </ul>

    <div class="highlight-box">
        <strong>निष्कर्ष:</strong><br>
        वैदिक ज्योतिष एवं कर्मकांड केवल अंधविश्वास या भाग्यवादी दृष्टिकोण नहीं है, बल्कि यह आकाशगंगा के पिंडों, समय के प्रवाह और मनुष्य के कर्म सिद्धांत का एक अत्यंत परिष्कृत, वैज्ञानिक एवं आध्यात्मिक समन्वय है।
    </div>

</body>
</html>
"""

# 2. HTML फ़ाइल सेव करना एवं वीज़ीप्रिंट (WeasyPrint) से PDF बनाना
html_filename = "vedic_astrology_guide.html"
pdf_filename = "Vedic_Astrology_And_Numerology_Complete_Guide.pdf"

with open(html_filename, "w", encoding="utf-8") as f:
    f.write(html_content)

# WeasyPrint का उपयोग करके PDF उत्पन्न करें
HTML(html_filename).write_pdf(pdf_filename)

print(f"PDF सफलतापूर्वक बन गई है: {pdf_filename}")
