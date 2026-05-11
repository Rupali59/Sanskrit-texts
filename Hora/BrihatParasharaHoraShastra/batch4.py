import json

def patch_a(fp, chap_num, updates):
    with open(fp) as f: data = json.load(f)
    c = 0
    for ch in data['chapters']:
        if ch['number'] != chap_num: continue
        for s in ch['shlokas']:
            k = str(s.get('number', s.get('shlok_number','')))
            if k in updates and not s.get('english_meaning'):
                s['english_meaning'], s['hindi_meaning'] = updates[k]; c+=1
    if c:
        with open(fp,'w') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(f"{fp}: {c} injected")

B='/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra/chapters/'

# Ch 90 — Sankranti-Janma Shanti (ritual for those born at solar ingress)
patch_a(B+'BPHS_090.json', 90, {
  '३': (
    "For the pacification of this defect (Sankranti-birth dosha), one should perform a Navagraha sacrifice. The eastern part of the house should be smeared with cow-dung.",
    "इस दोष की शान्ति के लिए नवग्रह यज्ञ करना चाहिए। घर के पूर्वी भाग को गोबर से लीप देना चाहिए।"
  ),
  '४': (
    "In this beautifully adorned space, a heap of rice grains (Vrihi) should be prepared — measuring five Dronas of grain and half of that in husked rice.",
    "सुसज्जित स्थान पर पाँच द्रोण धान्य (अनाज) और उसके आधे परिमाण में तण्डुल (चावल) से अनाज का ढेर (ब्रीहिराशि) बनाना चाहिए।"
  ),
  '६': (
    "First reciting the Punyahavachana (auspicious declaration), one should then select the Acharya — one who is knowledgeable in Dharma, well-versed in Mantras, and expert in Shanti rites.",
    "पहले पुण्याहवाचन करके, धर्मज्ञ, मन्त्रतत्त्वज्ञ और शान्तिकर्म में निपुण आचार्य का वरण (चुनाव) करना चाहिए।"
  ),
  '७': (
    "In the twelve zodiac signs (Rashi positions), unblemished and beautiful Kumbhas (water vessels) should be placed, filled with water from sacred tirthas, along with herbs and fresh leaves.",
    "बारह राशियों के स्थानों पर निर्दोष और सुन्दर कुम्भ (घट) स्थापित करने चाहिए, जो तीर्थ-जल से भरे हों और जिनमें ओषधियाँ और पल्लव (पत्ते) हों।"
  ),
  '८': (
    "Pancha-Gavya (the five cow-products: milk, curd, ghee, urine, and dung) should be placed inside, the vessel wrapped with a pair of cloths, and a small plate covered with a fine cloth placed on top of the Kumbha.",
    "उसमें पंचगव्य (दूध, दही, घी, गोमूत्र और गोबर) डालकर जोड़े वस्त्र से लपेट दें, और कुम्भ के ऊपर सूक्ष्म वस्त्र से ढका एक पात्र रखें।"
  ),
})
