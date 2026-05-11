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
  11: (
    "Saturn (Arka-Suta) should be depicted as having the brilliance of blue sapphire (Indranila), holding a trident (Shoola), with a boon-giving gesture, riding a vulture (Gridhra), and holding a bow and arrows.",
    "शनि (अर्कसुत) को इन्द्रनील-मणि की कान्ति वाला, शूल और धनुष-बाण धारण किए, वरद मुद्रा में, गृध्र (गिद्ध) पर आरूढ़ चित्रित करना चाहिए।"
  ),
  12: (
    "Rahu should be depicted as having a terrifying face (Karala-vadana), holding a sword (Khadga), shield (Charma), and trident (Shoola), with a boon-giving gesture, seated on a lion, and dark blue in colour.",
    "राहु को भयंकर मुख (करालवदन) वाला, खड्ग, चर्म और शूल धारण किए, वर देने वाली मुद्रा में, सिंहारूढ़ और नीलवर्ण चित्रित करना चाहिए।"
  ),
  13: (
    "The Ketus should be depicted as smoky-coloured (Dhumra), two-armed (Dvibahu), each holding a mace (Gada), with distorted/fearsome faces (Vikritanana), seated on vultures (Gridhra), and always in a boon-giving posture.",
    "केतुओं को धूम्र वर्ण, द्विबाहु, गदाधारी, विकृत मुख वाले, गृध्रासीन और सदा वरप्रद मुद्रा में चित्रित करना चाहिए।"
  ),
  14: (
    "All planetary images should be made wearing crowns (Kiriti). They are shown as givers of blessings to the world. Learned men always make them 108 finger-breadths (Angulas) in height.",
    "सभी ग्रह-प्रतिमाएँ किरीट (मुकुट) धारण किए हुई बनानी चाहिए। वे लोककल्याण के दाता हैं। विद्वान लोग सदा इन्हें एक सौ आठ (१०८) अंगुल ऊँचा बनाते हैं।"
  ),
  16: (
    "Whatever material, food, or thing is liked by each planet — that very thing should be offered to that planet by the worshipper with a devoted mind.",
    "जिस ग्रह को जो द्रव्य, अन्न और जो वस्तु प्रिय हो — वही वस्तु भक्तियुक्त चित्त से उस ग्रह को अर्पित करनी चाहिए।"
  ),
})
