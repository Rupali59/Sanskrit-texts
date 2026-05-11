import json

def patch_b2(fp, updates):
    """Schema B variant: number (int), english_meaning/hindi_meaning"""
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
  5: (
    "These planetary images should be drawn on cloth by learned Brahmins using their respective colours as described earlier, or with the respective directional pigments and decorative substances.",
    "इन ग्रह-प्रतिमाओं को विद्वान ब्राह्मणों द्वारा पूर्वोक्त अपने-अपने रंगों से, अथवा अपनी-अपनी दिशाओं के उपयुक्त रंगों और सजावटी द्रव्यों से, वस्त्र पर बनाना चाहिए।"
  ),
  6: (
    "The Sun (Divakara) should be depicted as seated on a lotus (Padmasana), holding lotuses in his hands, radiant like a lotus petal, riding a chariot drawn by seven horses, and having two arms.",
    "सूर्य (दिवाकर) को पद्मासन पर बैठा, हाथों में कमल लिए, कमल-दल के समान कान्तिमान, सप्ताश्व-रथ पर आरूढ़ और द्विभुज चित्रित करना चाहिए।"
  ),
  7: (
    "The Moon (Vidhu) should be depicted as white-complexioned, wearing white garments, riding a chariot of ten horses, adorned with white ornaments, holding a mace (Gada), and having two arms.",
    "चन्द्रमा (विधु) को श्वेत वर्ण, श्वेत वस्त्रधारी, दशाश्व-रथारूढ़, श्वेत आभूषणों से सज्जित, गदा धारण किए और द्विभुज चित्रित करना चाहिए।"
  ),
  8: (
    "Mars (Mangala) should be depicted as wearing red garland and garments, holding a Shakti (spear), Shoola (trident), and Gada (mace), with a boon-giving gesture, four-armed, and riding a ram (Mesha).",
    "मंगल को लाल माला और लाल वस्त्र पहने, शक्ति, शूल और गदा धारण किए, वरद मुद्रा में, चतुर्भुज और मेष (भेड़) पर सवार चित्रित करना चाहिए।"
  ),
  9: (
    "Mercury (Budha) should be depicted as wearing yellow garland and garments, shining like the Karnikara flower, holding a sword, shield, and mace, seated on a lion, and with a boon-giving gesture.",
    "बुध को पीली माला और पीले वस्त्र धारण किए, कर्णिकार-पुष्प के समान चमकते, खड्ग, चर्म और गदा लिए, सिंहासीन और वरद मुद्रा में चित्रित करना चाहिए।"
  ),
})
