#!/usr/bin/env python3
"""Flag corpus objects whose ZTF or IAU name appears in the full text of a seed (D2 refusal 14 input)."""
import re, json, pandas as pd
from pathlib import Path
H = Path(__file__).resolve().parent.parent
d = pd.read_csv(H/'out/corpus_rows.csv', dtype=str, keep_default_na=False)
res = {}
for f in ['sources/1910.12973.raw.txt', 'sources/2009.01242.raw.txt', 'sources/rubin_news_first_alerts.txt']:
    t = open(H/f).read()
    z = set(re.findall(r'ZTF\d{2}[a-z]{7}', t))
    iau = set(re.findall(r'(?:SN|AT)\s?(20\d\d[a-z]{2,4})\b', t)) | set(re.findall(r'\b(20(?:18|19|20)[a-z]{2,3}) \(', t))
    hits = d[d.ZTFID.isin(z) | d.IAUID.str.replace(r'^(SN|AT)', '', regex=True).isin(iau)]
    res[f] = hits[['ZTFID', 'IAUID', 'type']].to_dict('records')
json.dump(res, open(H/'out/answer_in_seed_text.json', 'w'), indent=1)
