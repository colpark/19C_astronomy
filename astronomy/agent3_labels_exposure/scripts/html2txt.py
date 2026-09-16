#!/usr/bin/env python3
"""Convert a saved HTML file to plain text for full reading (strips script/style, keeps line structure)."""
import html, re, sys
src, dst = sys.argv[1], sys.argv[2]
t = open(src, encoding="utf-8", errors="replace").read()
t = re.sub(r"<(script|style|svg|noscript)[^>]*>.*?</\1>", "", t, flags=re.S | re.I)
t = re.sub(r"<br\s*/?>|</(p|div|li|tr|h[1-6]|table|section|pre)>", "\n", t, flags=re.I)
t = re.sub(r"<[^>]+>", " ", t)
t = html.unescape(t)
t = re.sub(r"[ \t\r]+", " ", t)
t = re.sub(r"\n\s*\n+", "\n", t)
open(dst, "w").write(t.strip() + "\n")
