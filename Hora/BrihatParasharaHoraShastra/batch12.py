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
  27: (
    "When the Sun, Mars, and Saturn are in the Lagna and 5th house, and Rahu and Jupiter are in the 8th and 12th — loss of children from a paternal curse.",
    "जब सूर्य, मंगल और शनि लग्न व पुत्र भाव में हों, और राहु तथा गुरु 8वें व 12वें भाव में हों — तब पितृशाप से पुत्रहानि होती है।"
  ),
  28: (
    "When the Sun is in the 8th from the Lagna, Saturn is in the 5th, the 5th lord is conjoined with Rahu, and the Lagna contains malefics — loss of children.",
    "जब सूर्य लग्न से अष्टम भाव में हो, शनि पुत्र भाव में हो, पुत्रेश राहु से युक्त हो, और लग्न में पाप ग्रह हों — तब पुत्रहानि होती है।"
  ),
  29: (
    "When the 12th lord is in the Lagna, the 8th lord is in the 5th, and the 9th lord (Pitru-sthana) is in the 8th — loss of children from a paternal curse.",
    "जब व्ययेश (12वें का स्वामी) लग्न भाव में हो, रन्ध्रेश (8वें का स्वामी) पुत्र राशि में हो, और पितृस्थानाधिप (9वें का स्वामी) 8वें भाव में हो — तब पितृशाप से पुत्रहानि होती है।"
  ),
  33: (
    "His family shall always grow with sons, grandsons, and other descendants. In this way, the wise astrologer should declare the results based on planetary combinations.",
    "उसके कुल में सदा पुत्र, पौत्र आदि की वृद्धि होती है। इस प्रकार विचक्षण (कुशल) ज्योतिषी को ग्रह-योग के आधार पर फल बताना चाहिए।"
  ),
  34: (
    "When the Moon (lord of 4th, mother) is the 5th lord and is debilitated or between malefics, and malefics are in the 4th and 5th houses — loss of children due to a maternal curse (Matru-Shapa).",
    "जब पुत्रस्थानाधिप चन्द्रमा नीच हो या पाप ग्रहों के मध्य में हो, और चतुर्थ तथा पंचम भाव में पाप ग्रह हों — तब मातृशाप से पुत्रहानि होती है।"
  ),
})
