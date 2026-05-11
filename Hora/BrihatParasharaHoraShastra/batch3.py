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

patch_a(B+'BPHS_087.json', 87, {
  '६': (
    "With the Tryambaka (Mahamrityunjaya) Mantra one should worship diligently. The Acharya should invoke the deity with Varuna Mantras and perform the ritual worship.",
    "त्र्यम्बक मन्त्र (महामृत्युंजय) से निरन्तर पूजा करनी चाहिए। आचार्य को वारुण मन्त्रों से देवता का आवाहन करके पूजा करनी चाहिए।"
  ),
  '७': (
    "One should recite the Rig-Vedic hymns: 'Imam Me Varuna', 'Tattva Yami', 'Tvanno Agne', and 'Satvam Na' — each in sequence for the worship of Lord Varuna.",
    "'इमं मे वरुण', 'तत्त्वा यामी', 'त्वन्नोऽग्ने' और 'सत्वं नः' — इन ऋचाओं का क्रमशः जप करना चाहिए।"
  ),
  '९': (
    "After reciting the Purusha Sukta, one should also chant 'Krishanu Rudra'. Then one should have the Abhisheka (consecrated bathing) of Lord Shankara and the worship of the Navagrahas performed.",
    "पुरुष सूक्त का पाठ करके 'कृण्वन रुद्र' का जप करना चाहिए। तत्पश्चात् भगवान शंकर का अभिषेक और ग्रह-पूजा करानी चाहिए।"
  ),
  '१०': (
    "The auspicious Samidhas (sacred wood) for the fire sacrifice are: Ashvattha (Peepal), Palasha (Flame of the Forest), Khadira (Acacia), Apamarga (Prickly Chaff), Pippala, Udumbara (Cluster Fig), Shami, Durva grass, and Kusha grass respectively.",
    "होम के लिए शुभ समिधाएँ हैं: अश्वत्थ, पलाश, खदिर, अपामार्ग, पिप्पल, उदुम्बर, शमी, दूर्वा और कुश — क्रमशः।"
  ),
  '११': (
    "108 oblations (or 28, separately for each planet) should be offered into the fire according to the prescribed ritual method.",
    "विधिपूर्वक अग्नि में एक सौ आठ (१०८) अथवा अट्ठाईस (२८) आहुतियाँ प्रत्येक ग्रह के लिए पृथक-पृथक देनी चाहिए।"
  ),
  '१२': (
    "With the Tryambaka Mantra one should offer sesame seeds, and with Vyahritis (sacred utterances) other oblations. The planetary Homa should be performed according to the prescribed rules — thereafter, peace and well-being are attained.",
    "त्र्यम्बक मन्त्र से तिल और व्याहृतियों से अन्य द्रव्यों की आहुति देनी चाहिए। विधिपूर्वक ग्रह-होम करने पर क्षेम (कल्याण) की प्राप्ति होती है।"
  ),
})
