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

patch_b2(B+'BPHS_083.json', {
  14: (
    "When Mars is in the 5th house (Putra-sthana) in a Mars-owned sign, and the 5th lord is conjoined with Rahu, and they are aspected or conjoined by benefics — loss of children from a serpent's curse.",
    "जब पुत्रभाव में मंगल की राशि में मंगल हो, पुत्रेश राहु से युक्त हो और वे शुभ ग्रहों से दृष्ट या युक्त हों — तब सर्पशाप से पुत्रहानि होती है।"
  ),
  15: (
    "When the Sun, Saturn, and Mars are in the 5th house, and the Lagna lord and 5th lord (Putra-Lagnesha) are both weak — loss of children from a serpent's curse.",
    "जब पुत्र भाव में सूर्य, शनि और मंगल हों, और पुत्र व लग्न दोनों के स्वामी निर्बल हों — तब सर्पशाप से पुत्रहानि होती है।"
  ),
  16: (
    "When the Lagna lord is conjoined with Rahu, the 5th lord is conjoined with Mars, and the Putra-Karaka (Jupiter) is also conjoined with Rahu — loss of children from a serpent's curse.",
    "जब लग्नेश राहु से युक्त हो, पुत्रेश मंगल से युक्त हो, और पुत्रकारक (गुरु) भी राहु से युक्त हो — तब सर्पशाप से पुत्रहानि होती है।"
  ),
  17: (
    "Having thus determined childlessness through planetary combinations, one should undertake Naga-Puja (serpent worship) for the pacification of this curse.",
    "इस प्रकार ग्रह-योग के आधार पर अनपत्यता जानकर, उस दोष के निवारण के लिए नागपूजा (सर्पपूजा) प्रारम्भ करनी चाहिए।"
  ),
  18: (
    "One should have a golden image of the Naga (serpent deity) made — with both the male and female forms — and worship it with prescribed rituals in order to get rid of this defect.",
    "दोष-निवारण के लिए नाग का सुवर्णमय (सोने का) युगल रूप (नर-नारी सहित) बनवाकर, विधिपूर्वक उसकी पूजा करनी चाहिए।"
  ),
})
