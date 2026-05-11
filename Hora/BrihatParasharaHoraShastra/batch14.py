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
  43: (
    "When the 8th lord is in the 5th, the 5th lord is in an 8th-house sign (Nasha-Rashi), and the Moon and the 4th lord are in bad houses — loss of children from a maternal curse.",
    "जब 8वें का स्वामी पुत्र भाव में हो, पुत्रेश नाश-राशि (8वें भाव की राशि) में हो, और चन्द्रमा तथा मातृपति (4वें का स्वामी) दुःस्थ हों — तब मातृशाप से पुत्रहानि होती है।"
  ),
  47: (
    "Having recognized such a yoga, the wise astrologer should conclude childlessness. Thereafter, for the protection of progeny, an excellent Shanti (peace ritual) should be performed.",
    "ऐसे योग को देखकर बुद्धिमान ज्योतिषी को अनपत्यता (सन्तानहीनता) जाननी चाहिए। तत्पश्चात् सन्तान-रक्षा के लिए उत्तम शान्तिकर्म करना चाहिए।"
  ),
  48: (
    "A pilgrimage and bath at Setu (Rameswaram) should be performed. The Gayatri Mantra should be recited 100,000 times. Planetary charity (Graha-Dana) should be made with silver vessels filled with milk — with great effort.",
    "सेतु (रामेश्वरम) में स्नान करना चाहिए। गायत्री मन्त्र का एक लाख जप करना चाहिए। प्रयत्नपूर्वक रजत-पात्र में दूध लेकर ग्रह-दान करना चाहिए।"
  ),
  49: (
    "Brahmins should be fed in the same manner. Circumambulation of the Ashvattha (Peepal) tree should be done with devotion — 1008 times.",
    "उसी प्रकार ब्राह्मणों को भोजन कराना चाहिए। भक्तियुक्त होकर अश्वत्थ (पीपल) वृक्ष की एक सहस्र आठ (१००८) बार प्रदक्षिणा करनी चाहिए।"
  ),
  50: (
    "O Great Goddess! Having done all this, liberation from the curse will surely occur. Afterwards, one will obtain a good son, and there will be growth of the family lineage.",
    "हे महादेवि! इस प्रकार करने पर शाप से मुक्ति होगी। इसके बाद उत्तम पुत्र की प्राप्ति होती है और कुल-वृद्धि होती है।"
  ),
})
