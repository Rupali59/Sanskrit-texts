import json

def patch(filepath, schema_a_updates=None, schema_b_updates=None):
    """
    schema_a_updates: {chap_num_int: {shloka_number_str: (eng, hin)}}
    schema_b_updates: {shlok_number_int: (eng, hin)}
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    changed = 0

    if 'chapters' in data and schema_a_updates:
        for ch in data['chapters']:
            cnum = ch.get('number')
            if cnum not in schema_a_updates:
                continue
            upd = schema_a_updates[cnum]
            for s in ch.get('shlokas', []):
                key = str(s.get('number', s.get('shlok_number', '')))
                if key in upd:
                    eng, hin = upd[key]
                    if eng and not s.get('english_meaning'):
                        s['english_meaning'] = eng; changed += 1
                    if hin and not s.get('hindi_meaning'):
                        s['hindi_meaning'] = hin

    elif schema_b_updates:
        for s in data.get('shlokas', []):
            key = s.get('shlok_number', s.get('number'))
            if key in schema_b_updates:
                eng, hin = schema_b_updates[key]
                if eng and not s.get('english'):
                    s['english'] = eng; changed += 1
                if hin and not s.get('hindi'):
                    s['hindi'] = hin

    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  [✓] {filepath}: {changed} injected")

BASE = '/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra/chapters/'

# ─── BPHS_012 — Tanu Bhava Phala (Results of the 1st house) ─────────────────
# Shlokas 11-15: Bodily marks, wounds from planets in specific body parts
patch(BASE + 'BPHS_012.json', schema_a_updates={12: {
    '११': (
        "Wise astrologers should also always predict the same results from the Moon. Now I shall speak of scars and marks (Vrana Chihna) on the body of the native.",
        "बुद्धिमान ज्योतिषियों को चन्द्रमा से भी सदा इसी प्रकार का फल कहना चाहिए। अब मैं जातक के शरीर पर व्रण (घाव) और चिह्नों के बारे में बताता हूँ।"
    ),
    '१२': (
        "From the first Drekkana (0°–10°) of the Lagna, the body parts signified in order are: head, eyes, ears, nose, cheeks, chin, and face.",
        "लग्न के प्रथम द्रेष्काण (०°–१०°) से क्रमशः ये अंग जाने जाते हैं: शिर, नेत्र, कर्ण, नासिका, कपोल, ठुड्डी (हनु) और मुख।"
    ),
    '१३': (
        "When the Lagna falls in the middle Drekkana (10°–20°), the body parts indicated in order are: neck, shoulders, arms, sides (flanks), heart, chest, and navel.",
        "लग्न मध्य द्रेष्काण (१०°–२०°) में होने पर क्रमशः ये अंग होते हैं: कण्ठ, कंधे, भुजाएँ, पार्श्व (बगल), हृदय, वक्ष (क्रोड) और नाभि।"
    ),
    '१४': (
        "In the third Drekkana (20°–30°) of the Lagna, the body parts indicated in order are: bladder (Vasti), genitals, anus, scrotum, thighs, knees, calves, and feet — and the left side of the body.",
        "लग्न के तृतीय द्रेष्काण (२०°–३०°) में क्रमशः ये अंग होते हैं: वस्ति (मूत्राशय), लिंग, गुदा, मुष्क (वृषण), ऊरू (जाँघ), जानु (घुटने), जंघा और पाद (पैर) — ये वाम (बाएँ) अंग जानने चाहिए।"
    ),
    '१५': (
        "In whatever body part a malefic planet is located (in the relevant Drekkana), a scar (Vrana) or wound should be predicted there. If malefics are associated with benefics, a birthmark (Lakshma) should be predicted by the wise astrologer.",
        "जिस अंग भाग में (सम्बंधित द्रेष्काण में) पाप ग्रह स्थित हो, वहाँ व्रण (घाव/निशान) का फल कहें। यदि पाप ग्रह बुध आदि शुभ ग्रहों के साथ हों, तो बुद्धिमान ज्योतिषी को वहाँ 'लक्ष्म' (शुभ चिह्न/तिल) बताना चाहिए।"
    ),
}})

# ─── BPHS_014 — Graha Shanti (Pacification ritual, continued) ────────────────
patch(BASE + 'BPHS_014.json', schema_a_updates={14: {
    '१६': (
        "Using the Tryambaka Mantra (Mahamrityunjaya Mantra), one should offer oblations of Samidha (sacred wood), ghee, and Charu (cooked offerings) into the sacred fire — 1008 times, or 108 times, according to one's capacity.",
        "त्र्यम्बक मन्त्र (महामृत्युंजय मन्त्र) से समिधा, आज्य (घी) और चरू की आहुति देनी चाहिए — सामर्थ्यानुसार सहस्राधिक अष्टोत्तर (१००८) अथवा अष्टोत्तरशत (१०८) बार।"
    ),
    '१७': (
        "Or one may also perform the Homa 28 times according to one's capacity. A Tila (sesame seed) Homa should also be performed with the Mrityunjaya Mantra.",
        "अथवा सामर्थ्यानुसार अट्ठाईस (२८) बार भी होम कर सकते हैं। मृत्युंजय मन्त्र से तिल का होम भी करवाना चाहिए।"
    ),
    '१८': (
        "After that, offering the Svishtha-Krit oblation (concluding fire offering), one should perform the sacred bathing (Abhisheka). Afterward, Brahmins should be fed a meal. In this way, peace and well-being (Shanti) are attained.",
        "तत्पश्चात् स्विष्टकृत् आहुति देकर अभिषेक कराना चाहिए। इसके बाद ब्राह्मणों को भोजन कराएँ। इस प्रकार शान्ति की प्राप्ति होती है।"
    ),
}})

# ─── BPHS_025 — Putra Bhava (5th house / children) ───────────────────────────
patch(BASE + 'BPHS_025.json', schema_a_updates={25: {
    '१६': (
        "When the Lagna Lord is in the 10th house, the native becomes honored by the king, is a master of wealth, renowned, charitable, and intelligent.",
        "लग्नेश दशम भाव में हो तो जातक राजमान्य, धनाधिप, ख्यातिप्राप्त, दानशील और बुद्धिमान होता है।"
    ),
}})

print("Done with ch 12, 14, 25.")
