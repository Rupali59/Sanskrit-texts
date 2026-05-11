import json
import re

def update_file(filepath, updates):
    """updates = {chapter_num: {shloka_num_str: (eng, hin)}}"""
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    changed = 0
    if 'chapters' in data:
        for chapter in data['chapters']:
            chap_num = chapter.get('number')
            if chap_num not in updates:
                continue
            chap_updates = updates[chap_num]
            for shloka in chapter.get('shlokas', []):
                s_key = str(shloka.get('number', shloka.get('shlok_number', '')))
                if s_key in chap_updates:
                    eng, hin = chap_updates[s_key]
                    if eng and not shloka.get('english_meaning'):
                        shloka['english_meaning'] = eng
                        changed += 1
                    if hin and not shloka.get('hindi_meaning'):
                        shloka['hindi_meaning'] = hin
    else:
        m = re.search(r'BPHS_(\d+)', filepath)
        if m:
            chap_num = int(m.group(1))
            if chap_num in updates:
                chap_updates = updates[chap_num]
                for shloka in data.get('shlokas', []):
                    s_key = str(shloka.get('shlok_number', shloka.get('number', '')))
                    if s_key in chap_updates:
                        eng, hin = chap_updates[chap_num][s_key] if chap_num in chap_updates else (None,None)
                        if eng and not shloka.get('english'):
                            shloka['english'] = eng
                            changed += 1
                        if hin and not shloka.get('hindi'):
                            shloka['hindi'] = hin

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [✓] {filepath}: {changed} translations injected")
    else:
        print(f"  [-] {filepath}: nothing changed")

BASE = '/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra/chapters/'

# ─── BPHS_002.json — Mula Nakshatra Shanti ritual ────────────────────────────
update_file(BASE + 'BPHS_002.json', {2: {
    '१४': (
        "For the propitiation of the presiding deities, one should perform a Homa (fire oblation) according to the prescribed rules — either 1008 times, 108 times, or simply 100 times, with a controlled mind and senses.",
        "देवाधिदेव (ईश) की प्रसन्नता के लिए यथाविधि होम करना चाहिए — सहस्राधिक अष्टोत्तर (१००८), अथवा शत (१०८), अथवा केवल सौ आहुतियाँ, जितनी सामर्थ्य हो, संयमित मन से।"
    ),
    '१५': (
        "For the pacification of death (Mrityu), one should recite the Tryambaka Mantra (Mahamrityunjaya). Then, with devotion, one should pray to the deity for the rite of sacred bathing (Abhisheka).",
        "मृत्यु के शमन के लिए त्र्यम्बक (महामृत्युंजय) मन्त्र का जप करना चाहिए। तत्पश्चात् श्रद्धापूर्वक अभिषेक के लिए देवता की प्रार्थना करनी चाहिए।"
    ),
    '१६': (
        "The Acharya (preceptor), who is well-versed in Mantras, should perform the sacred bathing (Abhisheka) of the Yajamana (host of the ritual) who is seated on a comfortable seat (Bhadrasana) along with his wife and sons.",
        "मन्त्रज्ञ आचार्य, पत्नी-पुत्र सहित भद्रासन पर बैठे यजमान का प्रेमपूर्वक अभिषेक करें।"
    ),
    '१७': (
        "After that, he should bathe (the image/idol) with two covered vessels (Kumbhas). The person being bathed should then wear white garments and be anointed with white sandalwood paste.",
        "तत्पश्चात् वस्त्र से आच्छादित दो कुम्भों से स्नान कराएँ। इसके बाद शुक्ल (सफेद) वस्त्र पहनाएँ और श्वेत चन्दन का अनुलेपन करें।"
    ),
    '१८': (
        "One should offer a milch-cow (Dhenu) to the Acharya according to one's capacity. Fees (Dakshina) should be given to the priests (Ritvijas), and Brahmins should be fed a meal.",
        "सामर्थ्यानुसार आचार्य को एक दुधारू गाय (धेनु) दान करनी चाहिए। ऋत्विजों को दक्षिणा देनी चाहिए और ब्राह्मणों को भोजन कराना चाहिए।"
    ),
    '१९': (
        "Whatever sin and misery rests in all my limbs — consume all of that, O Agni (Fire), and increase my prosperity (Lakshmi) and vitality (Pushti).",
        "जो भी पाप और दुःख मेरे सभी अंगों में बसे हैं, हे अग्नि! उन सबका भक्षण करो, और मेरी लक्ष्मी और पुष्टि की वृद्धि करो।"
    ),
    '२०': (
        "By reciting this very Mantra, one should properly gaze at (consecrate) the ghee (clarified butter). In this way, all the sins arising from Mula Nakshatra birth and snake-related curses are completely destroyed.",
        "इसी मन्त्र से घी को भलीभाँति देखना चाहिए (अभिमन्त्रित करना चाहिए)। इस प्रकार मूल जन्म और सर्पदोष से उत्पन्न समस्त पाप नष्ट हो जाते हैं।"
    ),
}})
