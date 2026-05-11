import re
import json
import os

def parse_bphs(filename, start_chap, end_chap, output_dir):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find chapters
    chapter_pattern = re.compile(r'(अथ.*?ध्यायः\s*॥\s*(\d+|[०-९]+)\s*॥)')
    matches = list(chapter_pattern.finditer(content))
    
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    def convert_devanagari(num_str):
        # Convert to normal integer if it's devanagari
        dev_digits = '०१२३४५६७८९'
        std_digits = '0123456789'
        trans = str.maketrans(dev_digits, std_digits)
        return int(num_str.translate(trans))

    for i, match in enumerate(matches):
        header = match.group(1).strip()
        chap_num_str = match.group(2)
        chap_num = convert_devanagari(chap_num_str)
        
        start_idx = match.end()
        end_idx = matches[i+1].start() if i + 1 < len(matches) else len(content)
        
        chapter_content = content[start_idx:end_idx].strip()
        
        # Parse shlokas
        shloka_pattern = re.compile(r'(.*?)(॥\s*(\d+|[०-९]+)\s*॥)', re.DOTALL)
        shlokas = []
        
        for s_match in shloka_pattern.finditer(chapter_content):
            shloka_text = s_match.group(1).strip()
            shlok_num = s_match.group(3)
            
            # clean up multiple newlines or spaces if needed
            shloka_text = re.sub(r'\n{2,}', '\n', shloka_text).strip()
            
            shlokas.append({
                "number": shlok_num,
                "text": shloka_text,
                "english_meaning": "",
                "hindi_meaning": ""
            })
            
        # Chapter title
        title = header
        if title.startswith('अथ '):
            title = title[3:]
        elif title.startswith('अथ'):
            title = title[2:]
        title = title.split('॥')[0].strip()
        if title.startswith('ऽ'):
            title = title[1:]
        if title.startswith('ैक'): # For अथैक -> ैक
            title = 'ए' + title[2:] # Fix अथैक -> एक
        
        chapter_data = {
            "source": os.path.basename(filename),
            "header": header,
            "chapters": [
                {
                    "number": chap_num,
                    "title": title,
                    "shlokas": shlokas
                }
            ]
        }
        
        out_filename = os.path.join(output_dir, f"BPHS_{chap_num:03d}.json")
        with open(out_filename, 'w', encoding='utf-8') as out_f:
            json.dump(chapter_data, out_f, ensure_ascii=False, indent=2)
            
        print(f"Written {out_filename} with {len(shlokas)} shlokas")

parse_bphs('BPHS8190.md', 81, 90, 'chapters')
parse_bphs('BPHS9197.md', 91, 97, 'chapters')

