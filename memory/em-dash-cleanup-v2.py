#!/usr/bin/env python3
"""
Em-dash cleanup v2: toàn bộ sdn-onboard/*.md.

Khác v1: line-by-line processing, skip code blocks (```...```) để an toàn
cho content file đã fact-checked (17.0, 18.0, 19.0) có CLI output + log.
"""
import re
import glob
from pathlib import Path

PATTERNS = [
    # Header: "# X.Y —" → "# X.Y."
    (re.compile(r'^(#+ \d+\.\d+) — '), r'\1. '),
    (re.compile(r'^(#+ Phần \d+) — '), r'\1. '),
    # Metadata: "(phase — Rule N)" → "(phase theo Rule N)"
    (re.compile(r'\(architecture phase — Rule 10\)'), r'(architecture phase theo Rule 10)'),
    # Khối header: "**Khối:** X — Y" → "**Khối:** X, Y"
    (re.compile(r'(\*\*Khối:\*\*[^\n]+?) — ([^\n]+)'), r'\1, \2'),
    (re.compile(r'(\*\*Phần:\*\*[^\n]+?) — ([^\n]+)'), r'\1, \2'),
    # Placeholder: "*Placeholder — X" → "*Placeholder cho X"
    (re.compile(r'\*Placeholder — '), r'*Placeholder cho '),
    (re.compile(r'Placeholder — Phase B'), r'Placeholder cho Phase B'),
    # Parenthetical "(X — Y)" → "(X, Y)"
    (re.compile(r'\(([^)\n]{1,80}?) — ([^)\n]{1,80}?)\)'), r'(\1, \2)'),
    # Quoted paragraph em-dash — usually a dramatic pause → period
    (re.compile(r'\.\.\. — '), r'... '),
    # "X — nhưng/tuy nhiên/trong khi Y" → "X nhưng Y"
    (re.compile(r' — (nhưng|tuy nhiên|trong khi) '), r' \1 '),
    # "X — vì/do/bởi vì Y" → "X vì Y"
    (re.compile(r' — (vì|do|bởi vì|bởi) '), r' \1 '),
    # "X — với/và/hoặc Y" → "X với Y"
    (re.compile(r' — (với|và|hoặc|hay) '), r' \1 '),
    # "X — cần/nên Y" → "X, cần Y"
    (re.compile(r' — (cần|nên|phải|không cần) '), r', \1 '),
    # "X — là/chính là Y" appositive → "X, là Y"
    (re.compile(r' — (là|chính là|tức là|nghĩa là|đó là) '), r', \1 '),
    # "X — KHÔNG Y" emphasis caps → "X. KHÔNG Y"
    (re.compile(r' — (KHÔNG|TUYỆT ĐỐI|DANGER|WARNING|CHÚ Ý|CAUTION)'), r'. \1'),
    # "X — dẫn đến/kết quả Y"
    (re.compile(r' — (dẫn đến|kết quả|nên|vì vậy) '), r', \1 '),
    # "X — ở đây/ở chỗ Y"
    (re.compile(r' — (ở đây|ở chỗ|tại đây|tại chỗ) '), r' \1 '),
    # "X — theo Y" → "X theo Y"
    (re.compile(r' — (theo|qua|bằng|như) '), r' \1 '),
    # "X — `code`" → "X, `code`"
    (re.compile(r' — (`[^`]+`)'), r', \1'),
    # "X — *italic*" → "X, *italic*"
    (re.compile(r' — (\*\*?[^*]+\*\*?)'), r', \1'),
    # "X — [link]" → "X, [link]"
    (re.compile(r' — (\[)'), r', \1'),
    # "X — "quoted"" → "X. "quoted""
    (re.compile(r' — (")'), r'. \1'),
    # "X — 'số/năm/số khớp' (eg dates, figures)"
    (re.compile(r' — (\d)'), r', \1'),
    # Default: " — " with lowercase Vietnamese → ", x"
    (re.compile(r' — ([a-zà-ỹA-ZÀ-Ỹ])'), r', \1'),
    # Trailing em-dash at end of line → remove or colon
    (re.compile(r' —$'), r''),
    # Cleanup: "  " → " "
    (re.compile(r'  +'), r' '),
    # Cleanup: ". . " → ". "
    (re.compile(r'\. \. '), r'. '),
    # Cleanup: ", , " → ", "
    (re.compile(r', , '), r', '),
]

def clean_line(line):
    """Apply patterns to a single line of prose (outside code block)."""
    for pat, repl in PATTERNS:
        line = pat.sub(repl, line)
    return line

def process_file(p):
    content = p.read_text(encoding='utf-8')
    lines = content.split('\n')
    out = []
    in_code_block = False
    code_fence_pattern = re.compile(r'^```')
    for line in lines:
        if code_fence_pattern.match(line):
            in_code_block = not in_code_block
            out.append(line)
            continue
        if in_code_block:
            out.append(line)
            continue
        out.append(clean_line(line))
    new_content = '\n'.join(out)
    return content, new_content

def main():
    root = Path("C:/Users/voleh/Documents/network-onboard")
    files = sorted(glob.glob(str(root / "sdn-onboard/*.md")))
    total_before = 0
    total_after = 0
    changed = 0
    for f in files:
        p = Path(f)
        before_text, after_text = process_file(p)
        before_em = before_text.count('—')
        after_em = after_text.count('—')
        if before_text != after_text:
            p.write_text(after_text, encoding='utf-8')
            changed += 1
        rel = p.relative_to(root)
        if before_em != after_em:
            print(f"{before_em:4d} -> {after_em:4d}  {rel}")
        total_before += before_em
        total_after += after_em
    print()
    print(f"Total em-dash: {total_before} -> {total_after} (reduced {total_before-total_after})")
    print(f"Files changed: {changed}/{len(files)}")

if __name__ == '__main__':
    main()
