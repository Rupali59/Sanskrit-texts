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
  71: (
    "A man who, out of pride and arrogance, disrespects Brahmins — due to that sin and a Brahmin's curse, he suffers loss of progeny.",
    "जो मनुष्य बल और अहंकार के कारण ब्राह्मणों का अपमान करता है — उस दोष तथा ब्रह्मशाप के कारण उसके सन्तति का नाश होता है।"
  ),
  72: (
    "When Rahu is in a Jupiter-owned sign in the 5th, and Jupiter, Saturn, and the Sun are there too, and the 9th lord is in the 8th — loss of children from a Brahmin's curse.",
    "जब पुत्र भाव में बृहस्पति की राशि में राहु हो, और गुरु, शनि तथा सूर्य भी वहाँ हों, और 9वें का स्वामी 8वें भाव में हो — तब ब्रह्मशाप से पुत्रहानि होती है।"
  ),
  73: (
    "When the 9th lord is in the 5th, the 5th lord is in an 8th-house sign (Nasha-Rashi), and conjoined with Jupiter, Mars, and Rahu — loss of children from a Brahmin's curse.",
    "जब 9वें का स्वामी 5वें भाव में हो, पुत्रेश नाश-राशि (8वें की राशि) में हो, और गुरु, मंगल और राहु से युक्त हो — तब ब्रह्मशाप से पुत्रहानि होती है।"
  ),
  74: (
    "When the 9th lord is debilitated, the 12th lord is in the 5th, and they are conjoined with or aspected by Rahu — loss of children from a Brahmin's curse.",
    "जब 9वें का स्वामी नीच हो, 12वें का स्वामी पुत्र भाव में हो, और वे राहु से युक्त या दृष्ट हों — तब ब्रह्मशाप से पुत्रहानि होती है।"
  ),
  78: (
    "When Saturn in the Lagna is conjoined with Jupiter, and Rahu is in the 9th or the 12th conjoined with Jupiter — loss of children from a Brahmin's curse.",
    "जब लग्न में शनि गुरु से युक्त हो, और 9वें या 12वें भाव में राहु गुरु से युक्त हो — तब ब्रह्मशाप से पुत्रहानि होती है।"
  ),
})
