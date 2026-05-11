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
  51: (
    "Now I will explain the yogas arising from a sibling's curse (Bhratru-Shapa). Knowing these, the wise person should make effort to protect progeny.",
    "अब मैं भ्रातृशाप से उत्पन्न होने वाले योगों को बताऊँगा। इन्हें जानकर बुद्धिमान पुरुष को अपत्य (सन्तान) की रक्षा के लिए यत्न करना चाहिए।"
  ),
  55: (
    "When the Lagna lord is in the 12th house, Mars is in the 5th, and the 5th lord is in the 8th along with malefics — loss of children from a sibling's curse.",
    "जब लग्नेश 12वें भाव में हो, मंगल 5वें भाव में हो, और पुत्रेश पाप ग्रहों सहित 8वें भाव में हो — तब भ्रातृशाप से पुत्रहानि होती है।"
  ),
  56: (
    "When the Lagna is hemmed between malefics, the 5th house is also between malefics, and the Lagna lord and 5th lord are both in bad houses — loss of children from a sibling's curse.",
    "जब लग्न पापकर्तरी में हो, पुत्र भाव भी पाप ग्रहों के मध्य हो, और लग्नेश तथा पुत्रेश दोनों दुःस्थ हों — तब भ्रातृशाप से पुत्रहानि होती है।"
  ),
  57: (
    "When the 10th lord is in the 3rd house (Bhratru-sthana) conjoined with malefics or benefics, and Mars is in the 5th house — loss of children from a sibling's curse.",
    "जब 10वें का स्वामी भ्रातृ भाव (3) में पाप या शुभ ग्रहों से युक्त हो, और मंगल पुत्र भाव में हो — तब भ्रातृशाप से पुत्रहानि होती है।"
  ),
  58: (
    "When a Mercury-owned sign is in the 5th house with Saturn and Rahu, and the 12th house shows a sibling indicator — there is loss of children from a sibling's curse.",
    "जब 5वें भाव में बुध की राशि में शनि और राहु हों, और 12वें भाव में भ्रातृ-सूचक हो — तब भ्रातृशाप से पुत्रहानि होती है।"
  ),
})
