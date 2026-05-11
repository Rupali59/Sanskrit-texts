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

# Ch 89 — Eka-Nakshatra-Jata Shanti (ritual for those born in a Saturn-ruled nakshatra)
patch_a(B+'BPHS_089.json', 89, {
  '३': (
    "Avoiding the Rikta tithis (4th, 9th, 14th), Amavasya, and Vishti (Bhadra) Karana, one should perform the Shanti ritual at an appropriate time. An auspicious image of the relevant Nakshatra deity should be placed in the north-east (Ishana) direction of Saturn.",
    "रिक्ता तिथियों (4, 9, 14), अमावस्या और विष्टि (भद्रा) करण को छोड़कर, उचित समय पर शान्ति कर्म करना चाहिए। शनि की ईशान दिशा में उस नक्षत्र की शुभ प्रतिमा स्थापित करनी चाहिए।"
  ),
  '४': (
    "The Kalasha (sacred vessel) should be worshipped on top using the Mantra of that particular Nakshatra. Covering it with red cloth and wrapping it with a pair of cloths, one should set it up.",
    "उस नक्षत्र के मन्त्र से कलश के ऊपर पूजा करनी चाहिए। उसे लाल वस्त्र से ढककर और जोड़े वस्त्र से लपेटकर स्थापित करना चाहिए।"
  ),
  '५': (
    "Following the path prescribed in one's own Vedic branch (Shakha), one should perform the Agni-mukha (fire-facing) rite. Then, with that very Mantra, 108 oblations should be offered into the fire.",
    "अपनी-अपनी शाखा में उक्त विधान से अग्निमुख (अग्नि-संस्कार) करना चाहिए। पुनः उसी मन्त्र से एक सौ आठ (१०८) आहुतियाँ देनी चाहिए।"
  ),
  '६': (
    "Using Samidhas (wood), food (Anna), and ghee for each — up to the concluding Prayaschitta (expiation) oblation — one should perform the Abhisheka (sacred bathing). Then the Acharya (priest) should perform it for both (the parents and the child).",
    "प्रत्येक के लिए समिधा, अन्न और आज्य (घी) से प्रायश्चित्त तक आहुतियाँ देकर अभिषेक करना चाहिए। तत्पश्चात् आचार्य दोनों (बच्चे और माता-पिता) का अभिषेक करें।"
  ),
})

# Ch 87 — Shloka 4 & 5 (Krishna Chaturdashi Janma Shanti)
patch_a(B+'BPHS_087.json', 87, {
  '४': (
    "One should make a golden image of Lord Shiva weighing one Karsha (approx. 16g), or half or quarter of that, as per one's means — beautiful and pleasing to the eye.",
    "सोने की एक कर्ष (लगभग १६ ग्राम) तोल की शिव प्रतिमा बनानी चाहिए, या सामर्थ्यानुसार उसकी आधी या चौथाई तोल की — सुन्दर और मनोहर।"
  ),
  '५': (
    "The image should be adorned with a crescent moon crown (Balachandra Kirita), white garland and white garment; depicted as three-eyed (Tri-netra), seated on a bull (Vrisha), with one hand in a boon-granting gesture (Varada) and the other showing protection (Abhaya).",
    "प्रतिमा बालचन्द्र किरीट से अलंकृत, श्वेत माला और श्वेत वस्त्र से सज्जित हो; त्रिनेत्री, वृषभ पर आसीन, एक हाथ वरद मुद्रा में और दूसरा अभय मुद्रा में हो।"
  ),
})
