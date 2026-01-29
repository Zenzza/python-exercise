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
            "text": []
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

            indent = p.paragraph_format.left_indent
            indent_val = indent.cm if indent else 0.0
            data["indentation"].append(indent_val)

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
        diffs["Spacing Indentasi"]["A"] = f"{indent_a:.1f} cm"
        diffs["Spacing Indentasi"]["B"] = f"{indent_b:.1f} cm"
        diffs["Spacing Indentasi"]["Diff"] = f"{indent_a - indent_b:.1f} cm"

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


        def count_fmt(lst):
            return sum(1 for x in lst if x["bold"] or x["italic"] or x["underline"])
        
        fmt_a = count_fmt(data_a["formatting"])
        fmt_b = count_fmt(data_b["formatting"])
        
        diffs["Efek Pencetakan"]["A"] = f"{fmt_a} lines with effect"
        diffs["Efek Pencetakan"]["B"] = f"{fmt_b} lines with effect"
        diffs["Efek Pencetakan"]["Diff"] = f"{fmt_a - fmt_b} diff"

        text_a_full = " ".join(data_a["text"])
        text_b_full = " ".join(data_b["text"])
        
        matcher = difflib.SequenceMatcher(None, text_a_full.split(), text_b_full.split())
        
        typo_count = 0
        example_a = []
        example_b = []
        
        for tag, i1, i2, j1, j2 in matcher.get_opcodes():
            if tag == 'replace':
                a_segment = text_a_full.split()[i1:i2]
                b_segment = text_b_full.split()[j1:j2]
                if len(a_segment) == len(b_segment):
                    typo_count += len(a_segment)
                    if len(example_a) < 3: 
                        example_a.extend(a_segment)
                        example_b.extend(b_segment)
        
        diffs["Kesalahan Ketik"]["A"] = ", ".join(example_a) if example_a else "-"
        diffs["Kesalahan Ketik"]["B"] = ", ".join(example_b) if example_b else "-"
        diffs["Kesalahan Ketik"]["Diff"] = f"{typo_count} Kata"

        return diffs
