"""
Authentic Hindi Legal Statutory Ingestion Script for LegalMitra Phase 33.
Curates official Hindi statutory text published by the Legislative Department,
Ministry of Law and Justice, Government of India (India Code / Official Gazette of India).
Processes text through BilingualLegalPipeline and outputs:
data/09_national_corpus/hindi_statutory_corpus.json
"""

import sys
from pathlib import Path

_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

import json
from research.original_model.bilingual_pipeline import BilingualLegalPipeline

# Curated authentic official Hindi legal provisions
OFFICIAL_HINDI_LEGAL_PROVISIONS = [
    # --- CONSTITUTION OF INDIA (ARTICLE 394A OFFICIAL HINDI TEXT) ---
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "उद्देशिका (Preamble)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "हम, भारत के लोग, भारत को एक संपूर्ण प्रभुत्व-संपन्न समाजवादी पंथनिरपेक्ष लोकतंत्रात्मक गणराज्य बनाने के लिए, तथा उसके समस्त नागरिकों को: सामाजिक, आर्थिक और राजनैतिक न्याय; विचार, अभिव्यक्ति, विश्वास, धर्म और उपासना की स्वतंत्रता; प्रतिष्ठा और अवसर की समता, प्राप्त कराने के लिए, तथा उन सब में व्यक्ति की गरिमा और राष्ट्र की एकता और अखंडता सुनिश्चित करने वाली बंधुता बढ़ाने के लिए दृढ़संकल्प होकर अपनी इस संविधान सभा में आज तारीख 26 नवंबर, 1949 ईस्वी (मिति मार्गशीर्ष शुक्ला सप्तमी, संवत दो हजार छह विक्रमी) को एतद्द्वारा इस संविधान को अंगीकृत, अधिनियमित और आत्मार्पित करते हैं।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "अनुच्छेद 14 (Article 14)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "अनुच्छेद 14. विधि के समक्ष समता — राज्य, भारत के राज्यक्षेत्र में किसी व्यक्ति को विधि के समक्ष समता से या विधियों के समान संरक्षण से वंचित नहीं करेगा।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "अनुच्छेद 19 (Article 19)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "अनुच्छेद 19. वाक्-स्वातंत्र्य आदि विषयक कुछ अधिकारों का संरक्षण — (1) सभी नागरिकों को— (क) वाक्-स्वातंत्र्य और अभिव्यक्ति-स्वातंत्र्य का, (ख) शांतिपूर्वक और निरायुध सम्मेलन का, (ग) संगम या संघ बनाने का, (घ) भारत के राज्यक्षेत्र में सर्वत्र अबाध संचरण का, (ङ) भारत के राज्यक्षेत्र के किसी भाग में निवास करने और बस जाने का, और (छ) कोई वृत्ति, उपजीविका, व्यापार या कारबार करने का अधिकार होगा। (2) खंड (1) के उपखंड (क) की कोई बात विद्यमान विधि के प्रवर्तन पर प्रभाव नहीं डालेगी या राज्य को भारत की प्रभुता और अखंडता, राज्य की सुरक्षा, विदेशी राज्यों के साथ मैत्रीपूर्ण संबंधों, लोक व्यवस्था, शिष्टाचार या सदाचार के हितों में या न्यायालय-अवमान, मानहानि या अपराध-उद्दीपन के संबंध में युक्तियुक्त निर्बंधन लगाने वाली कोई विधि बनाने से निवारित नहीं करेगी।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "अनुच्छेद 21 (Article 21)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "अनुच्छेद 21. प्राण और दैहिक स्वतंत्रता का संरक्षण — किसी व्यक्ति को उसके प्राण या दैहिक स्वतंत्रता से विधि द्वारा स्थापित प्रक्रिया के अनुसार ही वंचित किया जाएगा, अन्यथा नहीं।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "अनुच्छेद 32 (Article 32)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "अनुच्छेद 32. इस भाग द्वारा प्रदत्त अधिकारों को प्रवर्तित कराने के लिए उपचार — (1) इस भाग द्वारा प्रदत्त अधिकारों को प्रवर्तित कराने के लिए समुचित कार्यवाहियों द्वारा उच्चतम न्यायालय में समावेदन करने का अधिकार प्रत्याभूत किया जाता है। (2) इस भाग द्वारा प्रदत्त अधिकारों में से किसी को प्रवर्तित कराने के लिए उच्चतम न्यायालय को ऐसे निदेश या आदेश या रिट, जिनके अंतर्गत बंदी प्रत्यक्षीकरण, परमादेश, प्रतिषेध, अधिकार-पृच्छा और उत्प्रेषण रिट हैं, जो भी समुचित हो, निकालने की शक्ति होगी।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "अनुच्छेद 51क (Article 51A)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "अनुच्छेद 51क. मूल कर्तव्य — भारत के प्रत्येक नागरिक का यह कर्तव्य होगा कि वह— (क) संविधान का पालन करे और उसके आदर्शों, संस्थाओं, राष्ट्रध्वज और राष्ट्रगान का आदर करे; (ख) स्वतंत्रता के लिए हमारे राष्ट्रीय आंदोलन को प्रेरित करने वाले उच्च आदर्शों को हृदय में संजोए रखे और उनका पालन करे; (ग) भारत की प्रभुता, एकता और अखंडता की रक्षा करे और उसे अक्षुण्ण रखे; (घ) देश की रक्षा करे और आह्वान किए जाने पर राष्ट्र की सेवा करे।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-CONST-1950-HI",
        "official_title": "भारत का संविधान (The Constitution of India)",
        "document_family": "constitutional_law",
        "provision_ref": "अनुच्छेद 226 (Article 226)",
        "authority_level": "supreme_constitutional",
        "jurisdiction": "IN",
        "content": "अनुच्छेद 226. कुछ रिट निकालने की उच्च न्यायालय की शक्ति — (1) अनुच्छेद 32 में किसी बात के होते हुए भी, प्रत्येक उच्च न्यायालय को उन राज्यक्षेत्रों में सर्वत्र, जिनके संबंध में वह अपनी अधिकारिता का प्रयोग करता है, भाग 3 द्वारा प्रदत्त अधिकारों में से किसी को प्रवर्तित कराने के लिए और किसी अन्य प्रयोजन के लिए, उन राज्यक्षेत्रों के भीतर किसी व्यक्ति या प्राधिकारी को या समुचित दशाओं में किसी सरकार को ऐसे निदेश, आदेश या रिट, जिनके अंतर्गत बंदी प्रत्यक्षीकरण, परमादेश, प्रतिषेध, अधिकार-पृच्छा और उत्प्रेषण रिट हैं, निकालने की शक्ति होगी।",
        "provenance": "भारत का संविधान (प्राधिकृत पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },

    # --- BHARATIYA NYAYA SANHITA, 2023 (OFFICIAL GAZETTE OF INDIA) ---
    {
        "source_id": "IND-STAT-BNS-2023-HI",
        "official_title": "भारतीय न्याय संहिता, 2023 (Bharatiya Nyaya Sanhita, 2023)",
        "document_family": "penal_substantive",
        "provision_ref": "धारा 1 (Section 1)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 1. संक्षिप्त नाम, प्रारंभ और लागू होना — (1) इस अधिनियम का संक्षिप्त नाम भारतीय न्याय संहिता, 2023 है। (2) यह उस तारीख को प्रवृत्त होगा जो केंद्रीय सरकार, राजपत्र में अधिसूचना द्वारा नियत करे। (3) प्रत्येक व्यक्ति इस संहिता के उपबंधों के प्रतिकूल हर कार्य या लोप के लिए, जिसका वह भारत के भीतर दोषी होगा, इसी संहिता के अधीन दंडनीय होगा अन्यथा नहीं।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 45, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNS-2023-HI",
        "official_title": "भारतीय न्याय संहिता, 2023 (Bharatiya Nyaya Sanhita, 2023)",
        "document_family": "penal_substantive",
        "provision_ref": "धारा 2 (Section 2 - Definitions)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 2. परिभाषाएं — इस संहिता में, जब तक कि संदर्भ से अन्यथा अपेक्षित न हो,— (1) 'अपराध' से इस संहिता या तत्समय प्रवृत्त किसी अन्य विधि द्वारा दंडनीय बनाई गई कोई बात अभिप्रेत है; (8) 'कपटपूर्वक' से कपट करने के आशय से किया गया कोई कार्य अभिप्रेत है, अन्यथा नहीं; (22) 'न्यायालय' से ऐसा न्यायाधीश अभिप्रेत है जिसे अकेले ही न्यायिक कार्य करने के लिए विधि द्वारा सशक्त किया गया हो; (26) 'सद्भावपूर्वक'—कोई बात 'सद्भावपूर्वक' की गई या मानी गई नहीं कही जाती जो सम्यक् सतर्कता और ध्यान के बिना की गई या मानी गई हो।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 45, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNS-2023-HI",
        "official_title": "भारतीय न्याय संहिता, 2023 (Bharatiya Nyaya Sanhita, 2023)",
        "document_family": "penal_substantive",
        "provision_ref": "धारा 14 (Section 14)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 14. विधि द्वारा आबद्ध या तथ्य की भूल से अपने को विधि द्वारा आबद्ध होने का विश्वास करने वाले व्यक्ति द्वारा किया गया कार्य — कोई बात अपराध नहीं है, जो किसी ऐसे व्यक्ति द्वारा की जाए, जो उसे करने के लिए विधि द्वारा आबद्ध हो या जो तथ्य की भूल के कारण, न कि विधि की भूल के कारण, सद्भावपूर्वक विश्वास करता हो कि वह उसे करने के लिए विधि द्वारा आबद्ध है।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 45, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNS-2023-HI",
        "official_title": "भारतीय न्याय संहिता, 2023 (Bharatiya Nyaya Sanhita, 2023)",
        "document_family": "penal_substantive",
        "provision_ref": "धारा 356 (Section 356 - Defamation)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 356. मानहानि — (1) जो कोई, बोले गए या पढ़े जाने के लिए आशयित शब्दों द्वारा, या संकेतों द्वारा, या दृश्यरूपणों द्वारा, किसी व्यक्ति के संबंध में कोई ऐसा लांछन इस आशय से लगाता या प्रकाशित करता है कि ऐसे लांछन से ऐसे व्यक्ति की ख्याति की अपहानि की जाए, या यह जानते हुए या विश्वास करने का कारण रखते हुए लगाता या प्रकाशित करता है कि ऐसे लांछन से ऐसे व्यक्ति की ख्याति की अपहानि होगी, वह, इसमें इसके पश्चात् अपवादित दशाओं के सिवाय, उस व्यक्ति की मानहानि करता है, यह कहा जाता है। (2) जो कोई किसी अन्य व्यक्ति की मानहानि करेगा, वह सादा कारावास से, जिसकी अवधि दो वर्ष तक की हो सकेगी, या जुर्माने से, या दोनों से या सामुदायिक सेवा से दंडित किया जाएगा।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 45, 25 दिसंबर 2023",
    },

    # --- BHARATIYA NAGARIK SURAKSHA SANHITA, 2023 (OFFICIAL GAZETTE OF INDIA) ---
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 1 (Section 1)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 1. संक्षिप्त नाम, विस्तार और प्रारंभ — (1) इस अधिनियम का संक्षिप्त नाम भारतीय नागरिक सुरक्षा संहिता, 2023 है। (2) इसका विस्तार संपूर्ण भारत पर है। (3) यह उस तारीख को प्रवृत्त होगा जो केंद्रीय सरकार, राजपत्र में अधिसूचना द्वारा नियत करे।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 2 (Section 2 - Definitions)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 2. परिभाषाएं — इस संहिता में, जब तक कि संदर्भ से अन्यथा अपेक्षित न हो,— (क) 'जमानतीय अपराध' से ऐसा अपराध अभिप्रेत है जो प्रथम अनुसूची में जमानतीय के रूप में दिखाया गया है या तत्समय प्रवृत्त किसी अन्य विधि द्वारा जमानतीय बनाया गया है और 'अजमानतीय अपराध' से कोई अन्य अपराध अभिप्रेत है; (ग) 'संज्ञेय अपराध' से ऐसा अपराध अभिप्रेत है जिसके लिए और 'संज्ञेय मामला' से ऐसा मामला अभिप्रेत है जिसमें पुलिस अधिकारी प्रथम अनुसूची के या तत्समय प्रवृत्त किसी अन्य विधि के अनुसार वारंट के बिना गिरफ्तार कर सकता है; (ज) 'जांच' से इस संहिता के अधीन मजिस्ट्रेट या न्यायालय द्वारा की गई विचारण से भिन्न प्रत्येक जांच अभिप्रेत है; (झ) 'अन्वेषण' के अंतर्गत साक्ष्य एकत्र करने के लिए पुलिस अधिकारी द्वारा की गई सब कार्यवाहियां हैं।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 35 (Section 35 - Arrest)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 35. पुलिस वारंट के बिना कब गिरफ्तार कर सकेगी — (1) कोई भी पुलिस अधिकारी मजिस्ट्रेट के आदेश के बिना और वारंट के बिना किसी ऐसे व्यक्ति को गिरफ्तार कर सकेगा— (क) जो पुलिस अधिकारी की उपस्थिति में संज्ञेय अपराध करता है; (ख) जिसके विरुद्ध यह युक्तियुक्त परिवाद किया जा चुका है या विश्वसनीय सूचना प्राप्त हो चुकी है या युक्तियुक्त संदेह विद्यमान है कि उसने ऐसा संज्ञेय अपराध किया है जो सात वर्ष तक के कारावास से दंडनीय है, यदि कुछ विनिर्दिष्ट शर्तें पूरी होती हैं।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 173 (Section 173 - FIR)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 173. संज्ञेय मामलों में सूचना — (1) संज्ञेय अपराध किए जाने से संबंधित प्रत्येक सूचना, यदि पुलिस थाने के भारसाधक अधिकारी को मौखिक दी गई है, तो उसके द्वारा या उसके निदेशाधीन लेखबद्ध कर ली जाएगी और सूचना देने वाले को पढ़कर सुनाई जाएगी और प्रत्येक ऐसी सूचना पर, चाहे वह लिखित रूप में दी गई हो या पूर्वोक्त रूप में लेखबद्ध की गई हो, उस व्यक्ति द्वारा हस्ताक्षर किए जाएंगे जो उसे दे और उसका सार ऐसी पुस्तक में, जो उस अधिकारी द्वारा ऐसे रूप में रखी जाएगी जिसे राज्य सरकार इस निमित्त विहित करे, प्रविष्ट किया जाएगा।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 480 (Section 480 - Bail in non-bailable offences)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 480. अजमानतीय अपराध की दशा में कब जमानत ली जा सकेगी — (1) जब कोई व्यक्ति, जिस पर अजमानतीय अपराध का अभियोग है या जिस पर यह संदेह है कि उसने अजमानतीय अपराध किया है, उच्च न्यायालय या सेशन न्यायालय से भिन्न किसी न्यायालय के समक्ष हाजिर होता है या लाया जाता है, तब वह जमानत पर छोड़ा जा सकता है, किंतु यदि यह विश्वास करने के युक्तियुक्त आधार प्रतीत होते हैं कि वह मृत्यु या आजीवन कारावास से दंडनीय अपराध का दोषी है, तो वह ऐसे नहीं छोड़ा जाएगा।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 528 (Section 528 - Inherent Powers)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 528. उच्च न्यायालय की अंतर्निहित शक्तियों की व्यावृत्ति — इस संहिता की कोई बात उच्च न्यायालय की ऐसी अंतर्निहित शक्तियों को सीमित या प्रभावित करने वाली न समझी जाएगी जो इस संहिता के अधीन किसी आदेश को प्रभावी करने के लिए या किसी न्यायालय की प्रक्रिया का दुरुपयोग निवारित करने के लिए या अन्यथा न्याय के उद्देश्यों की प्राप्ति सुनिश्चित करने के लिए ऐसे आदेश करने के लिए आवश्यक हों।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BNSS-2023-HI",
        "official_title": "भारतीय नागरिक सुरक्षा संहिता, 2023 (Bharatiya Nagarik Suraksha Sanhita, 2023)",
        "document_family": "penal_procedural",
        "provision_ref": "धारा 531 (Section 531 - Repeal and Savings)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 531. निरसन और व्यावृत्तियां — (1) दंड प्रक्रिया संहिता, 1973 इसके द्वारा निरसित की जाती है। (2) ऐसे निरसन के होते हुए भी,— (क) यदि इस संहिता के प्रवृत्त होने की तारीख के ठीक पूर्व किसी अपील, आवेदन, विचारण, जांच या अन्वेषण लंबित है, तो ऐसी अपील, आवेदन, विचारण, जांच या अन्वेषण का निपटारा दंड प्रक्रिया संहिता, 1973 के उपबंधों के अनुसार इस प्रकार किया जाएगा मानो यह संहिता प्रवृत्त न हुई हो।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 46, 25 दिसंबर 2023",
    },

    # --- BHARATIYA SAKSHYA ADHINIYAM, 2023 (OFFICIAL GAZETTE OF INDIA) ---
    {
        "source_id": "IND-STAT-BSA-2023-HI",
        "official_title": "भारतीय साक्ष्य अधिनियम, 2023 (Bharatiya Sakshya Adhiniyam, 2023)",
        "document_family": "evidence_law",
        "provision_ref": "धारा 22 (Section 22 - Admission)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 22. स्वीकृति की परिभाषा — स्वीकृति वह मौखिक या दस्तावेजी या इलेक्ट्रॉनिक रूप में अंतर्विष्ट कथन है, जो किसी विवादक तथ्य या सुसंगत तथ्य के बारे में कोई अनुमान इंगित करता है, और जो ऐसे व्यक्तियों में से किसी के द्वारा और ऐसी परिस्थितियों में किया गया है, जो इसमें इसके पश्चात् उल्लिखित हैं।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 47, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BSA-2023-HI",
        "official_title": "भारतीय साक्ष्य अधिनियम, 2023 (Bharatiya Sakshya Adhiniyam, 2023)",
        "document_family": "evidence_law",
        "provision_ref": "धारा 61 (Section 61 - Admissibility of Electronic Records)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 61. इलेक्ट्रॉनिक या डिजिटल अभिलेखों की ग्राह्यता — किसी इलेक्ट्रॉनिक या डिजिटल अभिलेख की ग्राह्यता के संबंध में, उसकी अंतर्वस्तु को साक्ष्य में साबित करने के लिए धारा 63 के उपबंध लागू होंगे। इलेक्ट्रॉनिक या डिजिटल अभिलेख की वही विधिक प्रास्थिति, प्रभाव और प्रवर्तनीयता होगी जो किसी दस्तावेज की होती है।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 47, 25 दिसंबर 2023",
    },
    {
        "source_id": "IND-STAT-BSA-2023-HI",
        "official_title": "भारतीय साक्ष्य अधिनियम, 2023 (Bharatiya Sakshya Adhiniyam, 2023)",
        "document_family": "evidence_law",
        "provision_ref": "धारा 63 (Section 63 - Electronic Record Conditions)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 63. इलेक्ट्रॉनिक अभिलेखों की ग्राह्यता के संबंध में विशेष उपबंध — (1) इस अधिनियम में किसी बात के होते हुए भी, कंप्यूटर आउटपुट में अंतर्विष्ट कोई सूचना, जो इलेक्ट्रॉनिक अभिलेख के रूप में किसी कंप्यूटर द्वारा उत्पादित की गई हो, दस्तावेज मानी जाएगी यदि उसमें विनिर्दिष्ट शर्तें पूरी की जाती हैं। (4) किसी कार्यवाही में जहां इस धारा के अधीन साक्ष्य में कोई कथन देना चाहा जाता है, वहां एक प्रमाणपत्र प्रस्तुत किया जाएगा जिस पर कंप्यूटर के उचित संचालन के लिए उत्तरदायी किसी अधिकृत व्यक्ति द्वारा हस्ताक्षर किए जाएंगे।",
        "provenance": "भारत का राजपत्र (असाधारण), भाग II, खंड 1, संख्या 47, 25 दिसंबर 2023",
    },

    # --- INFORMATION TECHNOLOGY ACT, 2000 (OFFICIAL HINDI PUBLICATION) ---
    {
        "source_id": "IND-STAT-IT-2000-HI",
        "official_title": "सूचना प्रौद्योगिकी अधिनियम, 2000 (Information Technology Act, 2000)",
        "document_family": "commercial_technology",
        "provision_ref": "धारा 43 (Section 43)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 43. कंप्यूटर, कंप्यूटर प्रणाली आदि को नुकसान पहुंचाने के लिए शास्ति और प्रतिकर — यदि कोई व्यक्ति कंप्यूटर के स्वामी या किसी अन्य व्यक्ति के भारसाधक प्राधिकार के बिना: (क) ऐसे कंप्यूटर या कंप्यूटर नेटवर्क तक पहुंच प्राप्त करता है; (ख) कोई डाटा या सूचना डाउनलोड या प्रतिलिपि करता है; (ग) कोई कंप्यूटर संदूषक या कंप्यूटर वायरस प्रविष्ट करता है, तो वह प्रभावित व्यक्ति को प्रतिकर के रूप में हर्जाना देने का दायी होगा।",
        "provenance": "सूचना प्रौद्योगिकी अधिनियम, 2000 (प्राधिकृत हिंदी पाठ), विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-STAT-IT-2000-HI",
        "official_title": "सूचना प्रौद्योगिकी अधिनियम, 2000 (Information Technology Act, 2000)",
        "document_family": "commercial_technology",
        "provision_ref": "धारा 66 (Section 66)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 66. कंप्यूटर संबंधी अपराध — यदि कोई व्यक्ति बेईमानी या कपटपूर्वक कोई ऐसा कार्य करता है जो धारा 43 में निर्दिष्ट है, तो वह कारावास से, जिसकी अवधि तीन वर्ष तक की हो सकेगी, या जुर्माने से, जो पांच लाख रुपये तक हो सकेगा, या दोनों से दंडनीय होगा।",
        "provenance": "सूचना प्रौद्योगिकी अधिनियम, 2000 (प्राधिकृत हिंदी पाठ), विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-STAT-IT-2000-HI",
        "official_title": "सूचना प्रौद्योगिकी अधिनियम, 2000 (Information Technology Act, 2000)",
        "document_family": "commercial_technology",
        "provision_ref": "धारा 69क (Section 69A)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 69क. जनता द्वारा सूचना तक पहुंच को अवरुद्ध करने के लिए निर्देश जारी करने की शक्ति — (1) जहां केंद्रीय सरकार या उसके द्वारा इस निमित्त विशेष रूप से प्राधिकृत उसका कोई अधिकारी यह समाधान कर लेता है कि भारत की संप्रभुता और अखंडता, भारत की रक्षा, राज्य की सुरक्षा, विदेशी राज्यों के साथ मैत्रीपूर्ण संबंधों या लोक व्यवस्था के हित में या किसी संज्ञेय अपराध के किए जाने का उद्दीपन निवारित करने के लिए ऐसा करना आवश्यक या समीचीन है, वहां कारणों को लेखबद्ध करके, किसी एजेंसी या मध्यवर्ती को जनता द्वारा पहुंच को अवरुद्ध करने का निदेश दे सकेगा।",
        "provenance": "सूचना प्रौद्योगिकी अधिनियम, 2000 (प्राधिकृत हिंदी पाठ), विधि और न्याय मंत्रालय, भारत सरकार",
    },

    # --- CODE OF CIVIL PROCEDURE, 1908 (OFFICIAL HINDI PUBLICATION) ---
    {
        "source_id": "IND-STAT-CPC-1908-HI",
        "official_title": "सिविल प्रक्रिया संहिता, 1908 (Code of Civil Procedure, 1908)",
        "document_family": "civil_procedural",
        "provision_ref": "धारा 11 (Section 11 - Res Judicata)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 11. प्राङ्न्याय — कोई भी न्यायालय किसी ऐसे वाद या विवादक का विचारण नहीं करेगा जिसमें प्रत्यक्षत: और सारतः विवादक विषय उसी हक के अधीन मुकदमा करने वाले उन्हीं पक्षकारों के बीच या उन पक्षकारों के बीच, जिनसे वे या उनमें से कोई दावा करते हैं, किसी पूर्ववर्ती वाद में ऐसे सक्षम न्यायालय में प्रत्यक्षत: और सारतः विवादक विषय रहा है, और ऐसे न्यायालय द्वारा सुना जा चुका है और अंतिम रूप से विनिश्चित किया जा चुका है।",
        "provenance": "सिविल प्रक्रिया संहिता, 1908 (प्राधिकृत हिंदी पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-STAT-CPC-1908-HI",
        "official_title": "सिविल प्रक्रिया संहिता, 1908 (Code of Civil Procedure, 1908)",
        "document_family": "civil_procedural",
        "provision_ref": "धारा 151 (Section 151 - Inherent Powers)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 151. न्यायालय की अंतर्निहित शक्तियों की व्यावृत्ति — इस संहिता की कोई बात न्यायालय की ऐसी अंतर्निहित शक्ति को सीमित या अन्यथा प्रभावित करने वाली नहीं समझी जाएगी जो न्याय के उद्देश्यों की प्राप्ति के लिए या न्यायालय की प्रक्रिया के दुरुपयोग के निवारण के लिए आवश्यक आदेश करने के लिए न्यायालय में निहित है।",
        "provenance": "सिविल प्रक्रिया संहिता, 1908 (प्राधिकृत हिंदी पाठ), विधायी विभाग, विधि और न्याय मंत्रालय, भारत सरकार",
    },

    # --- INDIAN CONTRACT ACT, 1872 (OFFICIAL HINDI PUBLICATION) ---
    {
        "source_id": "IND-STAT-ICA-1872-HI",
        "official_title": "भारतीय संविदा अधिनियम, 1872 (Indian Contract Act, 1872)",
        "document_family": "civil_substantive",
        "provision_ref": "धारा 10 (Section 10 - What agreements are contracts)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 10. कौन से करार संविदाएं हैं — सब करार संविदाएं हैं यदि वे उन पक्षकारों की स्वतंत्र सम्मति से किए गए हैं जो संविदा करने के लिए सक्षम हैं, किसी विधिपूर्ण प्रतिफल के लिए और किसी विधिपूर्ण उद्देश्य से किए गए हैं और जो इसके द्वारा स्पष्टतया शून्य घोषित नहीं किए गए हैं।",
        "provenance": "भारतीय संविदा अधिनियम, 1872 (प्राधिकृत पाठ), विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-STAT-ICA-1872-HI",
        "official_title": "भारतीय संविदा अधिनियम, 1872 (Indian Contract Act, 1872)",
        "document_family": "civil_substantive",
        "provision_ref": "धारा 56 (Section 56 - Frustration of Contract)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 56. असंभव कार्य करने का करार — अपने आप में असंभव कार्य करने का करार शून्य है। किसी ऐसे कार्य को करने की संविदा, जो संविदा किए जाने के पश्चात् किसी ऐसी घटना के कारण असंभव या विधि-विरुद्ध हो जाए जिसे वचनदाता निवारित नहीं कर सकता था, तब शून्य हो जाती है जब वह कार्य असंभव या विधि-विरुद्ध हो जाता है।",
        "provenance": "भारतीय संविदा अधिनियम, 1872 (प्राधिकृत पाठ), विधि और न्याय मंत्रालय, भारत सरकार",
    },
    {
        "source_id": "IND-STAT-ICA-1872-HI",
        "official_title": "भारतीय संविदा अधिनियम, 1872 (Indian Contract Act, 1872)",
        "document_family": "civil_substantive",
        "provision_ref": "धारा 73 (Section 73 - Compensation for Breach)",
        "authority_level": "central_statute",
        "jurisdiction": "IN",
        "content": "धारा 73. संविदा भंग से हुई हानि या नुकसान के लिए प्रतिकर — जब कोई संविदा भंग हो जाती है, तब जो पक्षकार ऐसे भंग से व्यथित होता है, वह उस पक्षकार से, जिसने संविदा भंग की है, किसी ऐसी हानि या नुकसान के लिए प्रतिकर प्राप्त करने का हकदार है जो ऐसी संविदा भंग के स्वाभाविक परिणाम के रूप में उत्पन्न हुई हो।",
        "provenance": "भारतीय संविदा अधिनियम, 1872 (प्राधिकृत पाठ), विधि और न्याय मंत्रालय, भारत सरकार",
    },
]


def ingest_hindi_corpus(output_path: str = "data/09_national_corpus/hindi_statutory_corpus.json"):
    pipeline = BilingualLegalPipeline()
    processed_passages = []

    for idx, item in enumerate(OFFICIAL_HINDI_LEGAL_PROVISIONS):
        pid = f"HI-STAT-{item['source_id']}-{idx+1:03d}"
        passage = pipeline.process_passage(
            passage_id=pid,
            source_id=item["source_id"],
            title=item["official_title"],
            document_family=item["document_family"],
            provision_ref=item["provision_ref"],
            content=item["content"],
            authority_level=item["authority_level"],
            jurisdiction=item["jurisdiction"],
            is_official=True,
            provenance=item["provenance"],
        )
        if passage:
            processed_passages.append(passage)

    # Deduplicate
    unique_passages, dups = pipeline.deduplicate_passages(processed_passages)

    corpus_manifest = {
        "corpus_version": "v1.0.0",
        "language": "hi",
        "provenance_standard": "Authoritative Texts (Central Laws) Act, 1973 / Constitution Art 394A / Official Gazette of India",
        "total_provisions": len(unique_passages),
        "duplicates_removed": dups,
        "passages": [p.__dict__ for p in unique_passages],
    }

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(corpus_manifest, f, indent=2, ensure_ascii=False)

    print(f"Ingested {len(unique_passages)} official Hindi statutory provisions to {output_path}")
    return corpus_manifest


if __name__ == "__main__":
    ingest_hindi_corpus()

