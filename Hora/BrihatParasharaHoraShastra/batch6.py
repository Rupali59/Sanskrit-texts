import json

def patch_b(fp, updates):
    with open(fp) as f: data = json.load(f)
    c = 0
    for s in data.get('shlokas', []):
        k = s.get('shlok_number', s.get('number'))
        if k in updates and not s.get('english'):
            s['english'], s['hindi'] = updates[k]; c+=1
    if c:
        with open(fp,'w') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(f"{fp}: {c} injected")

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

# Ch 90 last 3
patch_b(B+'BPHS_090.json', {
  15: (
    "To the west of the Kumbhas, one should prepare a Sthanda (sacred fire altar) and light the fire according to the Grihy ritual method.",
    "कुम्भों के पश्चिम में स्थण्डिल (यज्ञवेदी) बनाकर गृह्य-विधान के अनुसार अग्नि प्रज्वलित करनी चाहिए।"
  ),
  16: (
    "With the Tryambaka Mantra, oblations of Samidha, ghee, and Charu should be offered — 1008 times, or 108 times, according to one's capacity.",
    "त्र्यम्बक मन्त्र से समिधा, आज्य (घी) और चरू की आहुतियाँ देनी चाहिए — सामर्थ्यानुसार सहस्राधिक अष्टोत्तर (१००८) अथवा अष्टोत्तरशत (१०८) बार।"
  ),
  17: (
    "Or one may perform the Homa 28 times according to one's capacity. A Tila (sesame seed) Homa should also be performed with the Mrityunjaya Mantra.",
    "अथवा सामर्थ्यानुसार अट्ठाईस (२८) बार भी होम किया जा सकता है। मृत्युंजय मन्त्र से तिल का होम भी कराना चाहिए।"
  ),
})

# Ch 84 — Graha-Shanti-Adhyaya (planetary pacification iconography)
patch_a(B+'BPHS_084.json', 84, {
  '५': (
    "These (planetary images) should be drawn on cloth by learned Brahmins using their respective colours as described earlier, or using the respective directional pigments and decorative substances.",
    "इन (ग्रह-प्रतिमाओं) को विद्वान ब्राह्मणों को पूर्वोक्त अपने-अपने रंगों से, अथवा अपनी-अपनी दिशाओं के उपयुक्त रंगों और अलंकरण द्रव्यों से, वस्त्र पर बनाना चाहिए।"
  ),
  '६': (
    "The Sun (Divakara) should be depicted as: seated on a lotus (Padmasana), holding lotuses in his hands, with the brilliance of a lotus petal, riding a chariot drawn by seven horses (Saptashva), and having two arms.",
    "सूर्य (दिवाकर) का चित्रण इस प्रकार होना चाहिए: पद्मासन पर विराजित, हाथों में कमल धारण किए, कमल-दल के समान कान्ति वाले, सात अश्वों के रथ पर आरूढ़ और द्विभुज।"
  ),
})
