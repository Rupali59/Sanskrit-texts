import json

def patch_b2(fp, updates):
    with open(fp) as f: data = json.load(f)
    c = 0
    for s in data.get('shlokas', []):
        k = s.get('number')
        if k in updates and not s.get('english_meaning'):
            s['english_meaning'], s['hindi_meaning'] = updates[k]; c+=1
    if c:
        with open(fp,'w') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(f"{fp}: {c} injected")

B='/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra/chapters/'

patch_b2(B+'BPHS_084.json', {
  17: (
    "For the Sun one recites the Mantra 'Akrisnena'; for the Moon 'Imam Deva'; for Mars 'Agnir Murdha'; for Mercury 'Udbhudhyasva'; and the Brihaspati Mantra for Jupiter.",
    "सूर्य के लिए 'आकृष्णेन', चन्द्र के लिए 'इमं देवा', मंगल के लिए 'अग्निर्मूर्धा', बुध के लिए 'उद्बुध्यस्व' और गुरु के लिए 'बृहस्पते' मन्त्र का जप करना चाहिए।"
  ),
  18: (
    "For Venus one recites 'Annat Parishrutah'; for Saturn 'Shanno Devi'; for Rahu 'Kaya Nashchitra'; and for Ketu the mantra 'Ketum Krinvan' — in this prescribed sequence.",
    "शुक्र के लिए 'अन्नात् परिश्रुतः', शनि के लिए 'शन्नो देवी', राहु के लिए 'कया नश्चित्र' और केतु के लिए 'केतुं कृण्वन्' मन्त्र क्रमशः जपने चाहिए।"
  ),
  19: (
    "The number of Japa (repetitions) for each planet: Seven Rudras for the Sun, ten directions for the Moon, nine Nandas for Mars, nine Chandras for kings (Mercury), three Pakshas (fortnights) for Jupiter, eight Chandras for Venus, and seven Chandras for Saturn.",
    "ग्रहों के जप की संख्याएँ: सूर्य के लिए सात रुद्र, चन्द्र के लिए दस दिशाएँ (नन्दा), मंगल के लिए नव चन्द्र (नृपाः), बुध के लिए नव चन्द्र, गुरु के लिए तीन पक्ष, शुक्र के लिए आठ चन्द्र और शनि के लिए सात चन्द्र।"
  ),
  21: (
    "The Samidhas (sacred wood) for the nine planets in order are: Arka (Calotropis), Palasha, Khadira, Apamarga, Pippala, Udumbara, Shami, Durva grass, and Kusha grass.",
    "नव ग्रहों के लिए क्रमशः समिधाएँ हैं: अर्क (आक), पलाश, खदिर, अपामार्ग, पिप्पल, उदुम्बर, शमी, दूर्वा और कुश।"
  ),
  22: (
    "These should be offered mixed with honey and ghee, or with curd, or with milk — 108 or 28 oblations for each planet respectively.",
    "इन्हें मधु (शहद) और घी, अथवा दही, अथवा दूध के साथ मिलाकर प्रत्येक ग्रह के लिए एक सौ आठ (१०८) अथवा अट्ठाईस (२८) आहुतियाँ देनी चाहिए।"
  ),
})
