import difflib
import re
from docx import Document
from docx.shared import Pt

class ContentParser:
    def parse_docx(self, path):
        try:
            doc = Document(path)
        except Exception as e:
            return None

        data = {
            "paragraphs": [],
            "line_spacing": [],
            "numbering": [],
            "indentation": [],
            "formatting": [],
            "text": [],
            "words_with_fmt": [] 
        }

        for p in doc.paragraphs:
            text = p.text.strip()
            if not text:
                continue
            data["text"].append(text)

            spacing = p.paragraph_format.line_spacing
            if spacing is None:
                spacing = 1.0 
            data["line_spacing"].append(spacing)

            left = p.paragraph_format.left_indent
            first = p.paragraph_format.first_line_indent
            
            l_val = left.cm if left else 0.0
            f_val = first.cm if first else 0.0
            
            total_indent = l_val + f_val
            data["indentation"].append(total_indent)

            style_name = p.style.name
            num_format = "None"
            if "Bullet" in style_name:
                num_format = "Bullet"
            elif "List" in style_name:
                num_format = "Numbering"
            elif p._element.xpath('./w:pPr/w:numPr'):
                num_format = "Numbering/Bullet"
            
            if text.startswith("- ") or text.startswith("* "):
                num_format = "Manual Bullet"
            
            data["numbering"].append(num_format)

            para_fmt = {"bold": False, "italic": False, "underline": False}
            for run in p.runs:
                if run.bold:
                    para_fmt["bold"] = True
                if run.italic:
                    para_fmt["italic"] = True
                if run.underline:
                    para_fmt["underline"] = True
            
            if p.style.font.bold: para_fmt["bold"] = True
            if p.style.font.italic: para_fmt["italic"] = True
            if p.style.font.underline: para_fmt["underline"] = True

            data["formatting"].append(para_fmt)

            full_text = ""
            char_formats = []
            
            def_bold = p.style.font.bold or False
            def_italic = p.style.font.italic or False
            def_underline = p.style.font.underline or False

            for run in p.runs:
                r_text = run.text
                if not r_text: continue
                
                r_bold = run.bold if run.bold is not None else def_bold
                r_italic = run.italic if run.italic is not None else def_italic
                r_underline = bool(run.underline) if run.underline is not None else def_underline
                
                fmt = {"bold": r_bold, "italic": r_italic, "underline": r_underline}
                
                full_text += r_text
                char_formats.extend([fmt] * len(r_text))
            
            for match in re.finditer(r'\S+', full_text):
                start, end = match.span()
                w_text = match.group()
                
                if end > len(char_formats): end = len(char_formats)
                
                w_bold = any(char_formats[i]["bold"] for i in range(start, end))
                w_italic = any(char_formats[i]["italic"] for i in range(start, end))
                w_underline = any(char_formats[i]["underline"] for i in range(start, end))
                
                data["words_with_fmt"].append({
                    "text": w_text,
                    "bold": w_bold,
                    "italic": w_italic,
                    "underline": w_underline
                })

        return data

class DocumentComparator:
    def compare(self, data_a, data_b):
        diffs = {
            "Line Spacing": {"A": "", "B": "", "Diff": ""},
            "Bullet & Numbering": {"A": "", "B": "", "Diff": ""},
            "Spacing Indentasi": {"A": "", "B": "", "Diff": ""},
            "Efek Pencetakan": {"A": "", "B": "", "Diff": ""},
            "Kesalahan Ketik": {"A": "", "B": "", "Diff": ""}
        }

        def get_mode(lst):
            return max(set(lst), key=lst.count) if lst else 1.0
        
        spacing_a = get_mode(data_a["line_spacing"])
        spacing_b = get_mode(data_b["line_spacing"])
        diffs["Line Spacing"]["A"] = f"{spacing_a}"
        diffs["Line Spacing"]["B"] = f"{spacing_b}"
        try:
            val_a = float(spacing_a)
            val_b = float(spacing_b)
            diffs["Line Spacing"]["Diff"] = f"{val_a - val_b:.1f}"
        except:
            diffs["Line Spacing"]["Diff"] = "N/A"

        indent_a = get_mode(data_a["indentation"])
        indent_b = get_mode(data_b["indentation"])
        diffs["Spacing Indentasi"]["A"] = f"{indent_a:.2f} cm"
        diffs["Spacing Indentasi"]["B"] = f"{indent_b:.2f} cm"
        diffs["Spacing Indentasi"]["Diff"] = f"{indent_a - indent_b:.2f} cm"

        bullets_a = [b for b in data_a["numbering"] if b != "None"]
        bullets_b = [b for b in data_b["numbering"] if b != "None"]
        
        style_a = bullets_a[0] if bullets_a else "None"
        style_b = bullets_b[0] if bullets_b else "None"
        
        diffs["Bullet & Numbering"]["A"] = style_a
        diffs["Bullet & Numbering"]["B"] = style_b
        if style_a != style_b:
             diffs["Bullet & Numbering"]["Diff"] = "Beda Style"
        else:
             diffs["Bullet & Numbering"]["Diff"] = "Sama"


        words_a = data_a["words_with_fmt"]
        words_b = data_b["words_with_fmt"]
        
        text_a_list = [w["text"] for w in words_a]
        text_b_list = [w["text"] for w in words_b]

        matcher = difflib.SequenceMatcher(None, text_a_list, text_b_list)
        
        effect_diff_count = 0
        effect_details_a = []
        effect_details_b = []

        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'equal':
                for k in range(i2 - i1):
                    wa = words_a[i1 + k]
                    wb = words_b[j1 + k]
                    
                    eff_a = []
                    if wa["bold"]: eff_a.append("bold")
                    if wa["italic"]: eff_a.append("italic")
                    if wa["underline"]: eff_a.append("underline")
                    
                    eff_b = []
                    if wb["bold"]: eff_b.append("bold")
                    if wb["italic"]: eff_b.append("italic")
                    if wb["underline"]: eff_b.append("underline")
                    
                    is_diff = set(eff_a) != set(eff_b)
                    
                    if is_diff:
                        effect_diff_count += 1
                        str_a = f"{wa['text']} - {', '.join(eff_a) if eff_a else 'regular'}"
                        str_b = f"{wb['text']} - {', '.join(eff_b) if eff_b else 'regular'}"
                        
                        if len(effect_details_a) < 100: 
                            effect_details_a.append(str_a)
                            effect_details_b.append(str_b)

        diffs["Efek Pencetakan"]["A"] = ", ".join(effect_details_a) if effect_details_a else "-"
        diffs["Efek Pencetakan"]["B"] = ", ".join(effect_details_b) if effect_details_b else "-"
        diffs["Efek Pencetakan"]["Diff"] = f"{effect_diff_count} Efek"

        
        typo_count = 0
        example_a = []
        example_b = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                len_a = i2 - i1
                len_b = j2 - j1
                
                if len_a == len_b:
                    typo_count += len_a
                    if len(example_a) < 100: 
                        seg_a = text_a_list[i1:i2]
                        seg_b = text_b_list[j1:j2]
                        example_a.extend(seg_a)
                        example_b.extend(seg_b)
        
        diffs["Kesalahan Ketik"]["A"] = ", ".join(example_a) if example_a else "-"
        diffs["Kesalahan Ketik"]["B"] = ", ".join(example_b) if example_b else "-"
        diffs["Kesalahan Ketik"]["Diff"] = f"{typo_count} Kata"

        return diffs