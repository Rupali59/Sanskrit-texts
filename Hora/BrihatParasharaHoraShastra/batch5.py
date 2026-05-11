import json, re

def patch_b(fp, chap_num, updates):
    """Schema B: flat shlokas[] with shlok_number key"""
    with open(fp) as f: data = json.load(f)
    c = 0
    for s in data.get('shlokas', []):
        k = s.get('shlok_number', s.get('number'))
        if k in updates and not s.get('english'):
            s['english'], s['hindi'] = updates[k]; c+=1
    if c:
        with open(fp,'w') as f: json.dump(data,f,ensure_ascii=False,indent=2)
    print(f"{fp}: {c} injected")

B='/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra/chapters/'

patch_b(B+'BPHS_090.json', 90, {
  9: (
    "The presiding deity (Adhi-daivata) and secondary deity (Pratyadhi-daivata) images should be installed there. The presiding deity of the Sun is Agni (fire), and that of the Moon is Water (Jala).",
    "वहाँ अधिदेवता और प्रत्यधिदेवता सहित प्रतिमा स्थापित करनी चाहिए। सूर्य का अधिदेव अग्नि है और चन्द्रमा का प्रत्यधिदेव जल है।"
  ),
  11: (
    "Then, preceded by the Vyahritis (Bhur-Bhuvah-Svah), worship should be performed with each planet's respective Mantra; and the chief image should be worshipped with the Tryambaka (Mahamrityunjaya) Mantra.",
    "तत्पश्चात् व्याहृतियों (भूर्भुवः स्वः) सहित प्रत्येक ग्रह के अपने-अपने मन्त्र से पूजा करनी चाहिए; और प्रधान प्रतिमा की पूजा त्रैयम्बक (महामृत्युंजय) मन्त्र से करनी चाहिए।"
  ),
  12: (
    "Sun worship should be performed with the Mantra 'Utsurya'; Moon worship with the Mantra 'Apyayasva' — each planet in this manner with its prescribed Mantra.",
    "'उत्सूर्य' मन्त्र से सूर्य-पूजा और 'आप्यायस्व' मन्त्र से चन्द्र-पूजा करनी चाहिए — इसी प्रकार प्रत्येक ग्रह के लिए उसके विहित मन्त्र से पूजा करें।"
  ),
  13: (
    "Using sixteen Upacharas or at minimum five, one should touch the principal image while reciting the Mrityunjaya Mantra.",
    "षोडश उपचारों से, अथवा कम से कम पाँच उपचारों से, मृत्युंजय मन्त्र का उच्चारण करते हुए प्रधान प्रतिमा का स्पर्श करना चाहिए।"
  ),
  14: (
    "One should chant the Mantra 1008 times, or 108 times, or 28 times — according to one's capacity.",
    "सामर्थ्यानुसार मन्त्र का एक सहस्र आठ (१००८), अथवा एक सौ आठ (१०८), अथवा अट्ठाईस (२८) बार जप करना चाहिए।"
  ),
})
