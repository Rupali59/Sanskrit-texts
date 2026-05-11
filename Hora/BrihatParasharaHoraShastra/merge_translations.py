import json
import glob
import os
import re

def extract_first_number(s):
    s_str = str(s)
    matches = re.findall(r'\d+', s_str)
    return int(matches[0]) if matches else None

def main():
    base_dir = '/Users/rupali.b/Documents/GitHub/Youvan/texts/BrihatParasharaHoraShastra'
    target_dir = os.path.join(base_dir, 'chapters')

    # ── 1. Build translation map from all BPHS*.json source files ───────────
    # translations[chap_num][shloka_num] = {'english': ..., 'hindi': ...}
    translations = {}

    for sf in sorted(glob.glob(os.path.join(base_dir, 'BPHS*.json'))):
        with open(sf, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"  [!] JSON error: {sf}")
                continue

        for chapter in data.get('chapters', []):
            chap_num = extract_first_number(chapter.get('number', ''))
            if chap_num is None:
                continue
            translations.setdefault(chap_num, {})
            for shloka in chapter.get('shlokas', []):
                s_num = extract_first_number(
                    shloka.get('number', shloka.get('shlok_number', ''))
                )
                if s_num is None:
                    continue
                eng = shloka.get('english_meaning', shloka.get('english', ''))
                hin = shloka.get('hindi_meaning', shloka.get('hindi', ''))
                if eng or hin:
                    translations[chap_num][s_num] = {'english': eng, 'hindi': hin}

    print(f"Loaded translations for {len(translations)} chapters.")

    # ── 2. Inject into target chapter files ─────────────────────────────────
    updated = 0
    total = 0
    injected = 0

    for tf in sorted(glob.glob(os.path.join(target_dir, 'BPHS_*.json'))):
        with open(tf, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print(f"  [!] JSON error: {tf}")
                continue

        changed = False
        fname = os.path.basename(tf)

        if 'chapters' in data:
            # ── Schema A: nested chapters[] with shlokas[] ──────────────────
            # keys: number, text, english_meaning, hindi_meaning
            for chapter in data['chapters']:
                chap_num = extract_first_number(chapter.get('number', ''))
                chap_trans = translations.get(chap_num, {})
                for shloka in chapter.get('shlokas', []):
                    total += 1
                    s_num = extract_first_number(
                        shloka.get('number', shloka.get('shlok_number', ''))
                    )
                    if s_num not in chap_trans:
                        continue
                    t = chap_trans[s_num]
                    if t['english'] and not shloka.get('english_meaning'):
                        shloka['english_meaning'] = t['english']
                        changed = True
                        injected += 1
                    if t['hindi'] and not shloka.get('hindi_meaning'):
                        shloka['hindi_meaning'] = t['hindi']
                        changed = True

        else:
            # ── Schema B: flat shlokas[] at root ────────────────────────────
            # keys: shlok_number, sanskrit, hindi, english
            m = re.search(r'BPHS_(\d+)', fname)
            if not m:
                continue
            chap_num = int(m.group(1))
            chap_trans = translations.get(chap_num, {})

            if not chap_trans:
                print(f"  [!] No translations found in source for chapter {chap_num}")
                continue

            for shloka in data.get('shlokas', []):
                total += 1
                s_num = extract_first_number(
                    shloka.get('shlok_number', shloka.get('number', ''))
                )
                if s_num not in chap_trans:
                    continue
                t = chap_trans[s_num]
                if t['english'] and not shloka.get('english'):
                    shloka['english'] = t['english']
                    changed = True
                    injected += 1
                if t['hindi'] and not shloka.get('hindi'):
                    shloka['hindi'] = t['hindi']
                    changed = True

        if changed:
            with open(tf, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            updated += 1
            print(f"  [✓] Updated: {fname}")

    print(f"\nDone. Files updated: {updated}, shlokas scanned: {total}, translations injected: {injected}")

if __name__ == '__main__':
    main()
