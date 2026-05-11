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
  59: (
    "When the Lagna lord is in the 3rd house (Bhratru-sthana), the 3rd lord is in the 5th, and the Lagna, 3rd, and 5th houses are all afflicted by malefics — loss of children from a sibling's curse.",
    "जब लग्नेश भ्रातृ भाव (3) में हो, भ्रातृस्थानाधिप पुत्र भाव में हो, और लग्न, भ्रातृ और पुत्र भाव तीनों पाप ग्रहों से पीड़ित हों — तब भ्रातृशाप से पुत्रहानि होती है।"
  ),
  67: (
    "When the 5th lord is obscured (lost) and Saturn is in the Lagna or 7th house, and the Lagna lord is conjoined with Mercury — there too, progeny is lost.",
    "जब पुत्रेश अस्त हो (लुप्त हो) और शनि लग्न या सप्तम भाव में हो, और लग्नेश बुध से युक्त हो — तब भी सन्ततिक्षय (पुत्र-नाश) होता है।"
  ),
  68: (
    "When the 11th lord is in the Lagna conjoined with the 12th lord, and the Moon, Mercury, and Mars are in the 5th house — there too, progeny is lost.",
    "जब 11वें का स्वामी 12वें के स्वामी के साथ लग्न में हो, और पुत्र भाव में चन्द्रमा, बुध और मंगल हों — तब भी सन्ततिक्षय होता है।"
  ),
  69: (
    "For the pacification of this defect, one should perform worship of Lord Vishnu (Vishnu-Sthapana). One should also have wells, ponds, and reservoirs (Vapi-Kupa-Tadaga) dug for the benefit of sons and relatives.",
    "इस दोष के निवारण के लिए विष्णु-स्थापन (विष्णु-पूजा) करनी चाहिए। पुत्र और बन्धुओं के लाभ के लिए वापी (बावड़ी), कूप (कुआँ) और तड़ाग (तालाब) भी खुदवाने चाहिए।"
  ),
  70: (
    "Through this, his children will flourish and his wealth will increase. In this manner, based on planetary combinations, the wise astrologer should prescribe peace-rituals.",
    "इससे उसके पुत्रों में वृद्धि होगी और सम्पत्ति बढ़ेगी। इस प्रकार ग्रह-योग के अनुसार विचक्षण (कुशल) ज्योतिषी को शान्ति करानी चाहिए।"
  ),
})
