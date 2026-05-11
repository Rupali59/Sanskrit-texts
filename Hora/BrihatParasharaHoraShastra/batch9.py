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

# Ch 84: last 3 missing (23, 24, 26)
patch_b2(B+'BPHS_084.json', {
  23: (
    "The food offerings (Naivedya) for the nine planets in order are: Jaggery-rice (Gudanna), Payasa (milk-rice pudding), Havishya (cooked offering), Kshira-Shashtika (milk rice), Dadhi-Odana (curd rice), Havis-Churna (powdered offering), meat (Mamsa), and Chitra-Anna (mixed/coloured food).",
    "नव ग्रहों के लिए क्रमशः नैवेद्य इस प्रकार हैं: गुड़ान्न, पायस, हविष्य, क्षीरषाष्टिक, दध्योदन, हविश्चूर्ण, मांस और चित्रान्न।"
  ),
  24: (
    "One should offer food in this planetary sequence to Brahmins — or whatever is available, according to one's capacity — with due honour and respect.",
    "ग्रहों के क्रमानुसार इस प्रकार का भोजन ब्राह्मणों को देना चाहिए — अथवा सामर्थ्यानुसार जो भी उपलब्ध हो — सत्कारपूर्वक।"
  ),
  26: (
    "Whoever (planet) is afflicted at any time, that very planet should be worshipped with great effort. The Creator (Brahma) has granted this boon to these planets: 'Those who are worshipped shall bestow blessings on the worshippers.'",
    "जो ग्रह जब भी पीड़ित हो, उस ग्रह की यत्नपूर्वक पूजा करनी चाहिए। ब्रह्मा ने इन ग्रहों को वरदान दिया है: 'जो पूजे जाएँगे, वे पूजक को (कल्याण से) पूजेंगे।'"
  ),
})

# Ch 83 — Putra-Bhava (children) — Sarpa-Shapa (snake curse) yogas
patch_b2(B+'BPHS_083.json', {
  7: (
    "When the Guru (Jupiter), Lagna Lord, 7th lord, and 5th lord are all weak, one should predict childlessness (Anapatya).",
    "जब गुरु, लग्नेश, दारेश (सप्तमेश) और पुत्रस्थानाधिप — ये सभी बलहीन हों, तब अनपत्यता (सन्तानहीनता) का फल कहना चाहिए।"
  ),
  8: (
    "When the Sun, Mars, Rahu, and Saturn are strong and placed in the 5th house, and the planet of children (Jupiter, Putrakāraka) is weak — childlessness results from a serpent's curse (Sarpa-Shapa).",
    "जब सूर्य, मंगल, राहु और शनि बलवान होकर पुत्र भाव में हों, और पुत्रकारक निर्बल हो — तब सर्पशाप से सन्तानहानि होती है।"
  ),
  9: (
    "When Rahu is in the 5th house and aspected by Mars, or when (the 5th lord) is in a Mars-owned sign — there is loss of children due to a serpent's curse (Sarpa-Shapa).",
    "जब पुत्र भाव में राहु हो और मंगल उसे देखता हो, अथवा (पुत्रेश) कुजक्षेत्र में हो — तब सर्पशाप के कारण पुत्रहानि होती है।"
  ),
  10: (
    "When the 5th lord is conjoined with Rahu, and Saturn is in the 5th house conjoined with or aspected by the Moon — there is loss of children due to a serpent's curse.",
    "जब पुत्रेश राहु से युक्त हो, और पुत्र भाव में शनि हो तथा चन्द्रमा से युक्त या दृष्ट हो — तब सर्पशाप से पुत्रहानि होती है।"
  ),
})
