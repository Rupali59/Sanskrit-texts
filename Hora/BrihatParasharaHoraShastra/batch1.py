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

B = '/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra/chapters/'

# Ch 86 — Darsha-Janma Shanti (Peace ritual for those born on new-moon day)
patch_a(B+'BPHS_086.json', 86, {
  '३': (
    "Into the vessel (Kalasha), one should also place the roots and bark of the Nimba (neem) tree. Five precious gems (Pancha-Ratna) should be placed inside, and the vessel should be wrapped with a pair of cloths.",
    "कलश में निम्ब (नीम) की जड़ें और छाल भी डालनी चाहिए। पाँच रत्न (पंचरत्न) डालकर उसे एक जोड़ी वस्त्र से लपेट देना चाहिए।"
  ),
  '४': (
    "Consecrating the vessel with the Vedic verses 'Sarve Samudra' and the three 'Apohistha' hymns, one should then place it in the fire-corner (south-east, Agni-kona).",
    "'सर्वे समुद्र' इस मन्त्र से तथा 'अपोहिष्ठा' की तीन ऋचाओं से कलश को अभिमन्त्रित कर, उसे अग्निकोण (दक्षिण-पूर्व) में स्थापित करना चाहिए।"
  ),
  '६': (
    "Using the Mantra 'Apyayasva' and thereafter the Savita Mantra, one should worship the deity with Upacharas (ritual offerings), and then perform the Homa (fire sacrifice).",
    "'आप्यायस्व' मन्त्र और तत्पश्चात् सवितृ मन्त्र से षोडशोपचार पूजा करके होम करना चाहिए।"
  ),
  '७': (
    "The learned and disciplined ritualist should offer Samidhas (sacred wood) and Charu (cooked oblation) into the fire in proper sequence — with the Savitri Mantra for Soma (Moon) and other Mantras for the other planetary deities.",
    "व्रती विद्वान को क्रमशः सवितृ मन्त्र से सोम (चन्द्रमा) और अन्य ग्रहों के लिए उनके मन्त्रों से समिधा और चरू की आहुति देनी चाहिए।"
  ),
})

# Ch 88 — Bhadrava / Durgayoga Shanti (Malefic yoga pacification)
patch_a(B+'BPHS_088.json', 88, {
  '३': (
    "Or, when astrologers have identified an auspicious Lagna and auspicious day, the householder should perform worship of the deities and a Yajana (fire sacrifice) for the planets.",
    "अथवा जब ज्योतिषियों द्वारा शुभ लग्न और शुभ दिन निर्धारित किया जाए, तब गृहस्थ को देवताओं की पूजा और ग्रहों का यजन करना चाहिए।"
  ),
  '४': (
    "One should perform the sacred bathing (Abhisheka) of Lord Shankara and light a ghee lamp in the Shiva temple. For longevity, circumambulation of the Ashvattha (Peepal) tree should also be done.",
    "शिव मन्दिर में भगवान शंकर का अभिषेक और घी का दीपक जलाना चाहिए। आयुर्वृद्धि के लिए अश्वत्थ (पीपल) वृक्ष की प्रदक्षिणा भी करनी चाहिए।"
  ),
})
