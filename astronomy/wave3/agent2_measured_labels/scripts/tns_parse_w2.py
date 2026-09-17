"""Parser for archived TNS object pages (old and new layouts). Bug fix of fetch-time parser: new layout uses details/summary."""
import re, html


def cells(row):
    return {m.group(1): html.unescape(re.sub(r"<[^>]+>", " ", m.group(2))).replace("\xa0", " ").strip()
            for m in re.finditer(r'<td class="cell-([a-z_]+)"[^>]*>(.*?)</td>', row, flags=re.S)}


SEC_RE = re.compile(r'<span class="fieldset-legend">([^<]*)</span>|<summary[^>]*>([^<]*)</summary>')


def fieldset(t, legend):
    """Section body for old (fieldset/legend, pre-2025) and new (details/summary) TNS layouts."""
    secs = [(m.start(), (m.group(1) or m.group(2)).strip()) for m in SEC_RE.finditer(t)]
    for k, (pos, name) in enumerate(secs):
        if name == legend:
            end = secs[k + 1][0] if k + 1 < len(secs) else len(t)
            return t[pos:end]
    return None


def parse(t, name):
    title = re.search(r"<title>(.*?)</title>", t, flags=re.S)
    title = html.unescape(title.group(1)).strip() if title else ""
    valid = bool(re.search(r"\b" + re.escape(name) + r"\b", title)) and "Transient Name Server" in title
    cls = fieldset(t, "Classification Reports")
    spec = fieldset(t, "Spectra")
    reports = []
    if cls:
        for row in re.findall(r"<tr[^>]*>(.*?)</tr>", cls, flags=re.S):
            c = cells(row)
            if "time_received" in c:
                reports.append(dict(id=c.get("id"), time=c.get("time_received"), sender=c.get("user_name"),
                                    classifier=c.get("classifier_name"), group=c.get("source_group_name"),
                                    classification=c.get("type"), remarks=c.get("remarks")))
    spectra = []
    if spec:
        for row in re.findall(r'<tr class="spectrum-row[^"]*"[^>]*>(.*?)</tr>', spec, flags=re.S):
            c = cells(row)
            spectra.append(dict(obsdate=c.get("obsdate"), tel_inst=c.get("tel_inst"), observer=c.get("observer"),
                                group=c.get("source_group_name")))
    top_type = re.search(r'field-type">\s*<span class="name">Type</span>\s*<div class="value">(.*?)</div>', t, flags=re.S)
    return dict(title=title, valid=valid, has_class_fieldset=cls is not None, reports=reports, spectra=spectra,
                page_type=html.unescape(re.sub(r"<[^>]+>", "", top_type.group(1))).strip() if top_type else None)


