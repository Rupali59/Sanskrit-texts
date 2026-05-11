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
  35: (
    "When Saturn is in the 11th house, the 4th house (Matru-sthana) has malefics, and the Moon is debilitated in the 5th — loss of children from a maternal curse.",
    "जब 11वें भाव में शनि हो, मातृ भाव (चतुर्थ) में पाप ग्रह हों, और चन्द्रमा पुत्र भाव में नीच हो — तब मातृशाप से पुत्रहानि होती है।"
  ),
  36: (
    "When the 5th lord is in a bad house (6th, 8th, 12th), the Lagna lord is in a debilitated sign, and the Moon is conjoined with malefics — loss of children from a maternal curse.",
    "जब पुत्रेश दुःस्थ (6, 8, 12वें) भाव में हो, लग्नेश नीच राशि में हो, और चन्द्रमा पाप ग्रहों से युक्त हो — तब मातृशाप से पुत्रहानि होती है।"
  ),
  37: (
    "When the 5th lord is in the 8th, 6th, or 12th house, the Moon is in a malefic navamsha, and both the Lagna and 5th are full of malefics — loss of children from a maternal curse.",
    "जब पुत्रेश 8, 6 या 12वें भाव में हो, चन्द्रमा पाप नवांश में हो, और लग्न तथा पुत्र भाव दोनों पाप ग्रहों से भरे हों — तब मातृशाप से पुत्रहानि होती है।"
  ),
  41: (
    "When the 6th and 8th lords are in the Lagna, the 12th lord is in the 5th, and Jupiter and Moon are conjoined with malefics — loss of children from a maternal curse.",
    "जब 6वें और 8वें के स्वामी लग्न में हों, 12वें का स्वामी पुत्र भाव में हो, और चन्द्रमा तथा गुरु पाप ग्रहों से युक्त हों — तब मातृशाप से पुत्रहानि होती है।"
  ),
  42: (
    "When the Lagna is hemmed between malefics, the waning Moon is in the 7th, and Rahu and Saturn are in the 4th and 5th — loss of children from a maternal curse.",
    "जब लग्न पाप ग्रहों के मध्य (पापकर्तरी) में हो, क्षीण चन्द्रमा सप्तम भाव में हो, और मातृ (4) तथा पुत्र (5) भाव में राहु और शनि हों — तब मातृशाप से पुत्रहानि होती है।"
  ),
})
