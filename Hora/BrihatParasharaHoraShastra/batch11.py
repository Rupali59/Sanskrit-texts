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
  19: (
    "Cows, land, sesame, gold, and other such things should be donated according to one's means. By doing so, through the grace of the Naga-Indra (Lord of Serpents), the family lineage flourishes.",
    "सामर्थ्यानुसार गाय, भूमि, तिल, सोना आदि का दान करना चाहिए। ऐसा करने पर नागेन्द्र की कृपा से कुल (वंश) में वृद्धि होती है।"
  ),
  20: (
    "When the Sun is in the 5th house debilitated or in Saturn's navamsha, with malefics on both sides — loss of children from a paternal curse (Pitru-Shapa).",
    "जब पुत्र भाव में सूर्य नीच राशि में या शनि के नवांश में हो, और दोनों ओर पाप ग्रह हों — तब पितृशाप से पुत्रहानि होती है।"
  ),
  24: (
    "When the 9th lord (Pitru-sthana lord) is in the 5th house, or the 5th lord is in the 10th house, and both the 5th and Lagna are filled with malefics — loss of children from a paternal curse.",
    "जब नवमेश (पितृस्थानाधिप) पुत्र भाव में हो, या पुत्रेश दशम भाव में हो, और पुत्र तथा लग्न दोनों पाप ग्रहों से भरे हों — तब पितृशाप से पुत्रहानि होती है।"
  ),
  25: (
    "When Mars is the 9th lord (Pitru-sthana) conjoined with the 5th lord, and malefics are in the Lagna, 5th house, and 9th house — destruction of progeny.",
    "जब मंगल नवमेश होकर पुत्रेश से युक्त हो, और लग्न, पुत्र और पितृ भाव में पाप ग्रह हों — तब सन्तति का नाश होता है।"
  ),
  26: (
    "When the 9th lord is in a bad house (6th, 8th, 12th), the Putra-Karaka is in a malefic sign, and the Lagna lord and 5th lord are both with malefics — loss of children from a paternal curse.",
    "जब नवमेश दुःस्थ (6, 8, 12वें) भाव में हो, पुत्रकारक पाप राशि में हो, और पुत्रेश तथा लग्नेश दोनों पाप ग्रहों के साथ हों — तब पितृशाप से पुत्रहानि होती है।"
  ),
})
