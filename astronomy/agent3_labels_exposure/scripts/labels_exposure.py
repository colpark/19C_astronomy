#!/usr/bin/env python3
"""Agent 3: label-source shares, exposure key, contamination axis (pre-clustering) for the ZTF BTS file.

Every count written by this script is recomputable from:
  ../data/raw/ztf_bts_all_2026-09-16.csv                (sha256 checked)
  sources/bts_all_extracols_2026-09-16.csv               (same explorer query + savedate, discdate, discID, sample codes)
  sources/wayback_bts_explorer_<timestamp>.html          (Internet Archive captures of the explorer default page)
Outputs: derived_counts.json (all numbers), used by build_records.py.

Run:  <venv>/bin/python scripts/labels_exposure.py
"""
import hashlib, html, json, re, sys
from pathlib import Path
import pandas as pd
from astropy.time import Time

HERE = Path(__file__).resolve().parent.parent
RAW = HERE.parent / "data/raw/ztf_bts_all_2026-09-16.csv"
RAW_SHA = "61415979b75f96bcf2532439109b35f923c5fa1aadfacc5d6013235187ebe570"
EXTRA = HERE / "sources/bts_all_extracols_2026-09-16.csv"
CAPTURES = {  # Internet Archive capture timestamp -> file
    "2024-12-08T23:13:31": HERE / "sources/wayback_bts_explorer_20241208231331.html",
    "2025-08-10T06:50:56": HERE / "sources/wayback_bts_explorer_20250810065056.html",
    "2026-07-25T03:35:57": HERE / "sources/wayback_bts_explorer_20260725033557.html",
}

# ---- subject cutoffs, read from primary pages saved in sources/ (month granularity kept as published) ----
# first_day / last_day bracket the published month or day. "status" UNDEMONSTRATED when no cutoff is published.
SUBJECTS = [
    dict(subject="Claude Fable 5.1", published="Jun 2026", first_day="2026-06-01", last_day="2026-06-30",
         kind="reliable knowledge cutoff", locator="sources/anthropic_models_overview.txt line 49",
         status="DERIVED", note="Transparency Hub (sources/anthropic_transparency.txt) has no Fable 5.1 entry; lists Claude Fable 5 at January 2026 (line 104). Disagreement listed, not reconciled."),
    dict(subject="Claude Opus 5", published="May 2026", first_day="2026-05-01", last_day="2026-05-31",
         kind="reliable knowledge cutoff", locator="sources/anthropic_models_overview.txt line 49; sources/anthropic_transparency.txt line 34",
         status="DERIVED", note="two Anthropic pages agree"),
    dict(subject="Claude Sonnet 5", published="Jan 2026", first_day="2026-01-01", last_day="2026-01-31",
         kind="reliable knowledge cutoff", locator="sources/anthropic_models_overview.txt line 49; sources/anthropic_transparency.txt line 69",
         status="DERIVED", note="two Anthropic pages agree"),
    dict(subject="Claude Haiku 4.5", published="Feb 2025", first_day="2025-02-01", last_day="2025-02-28",
         kind="reliable knowledge cutoff", locator="sources/anthropic_models_overview.txt line 49; sources/anthropic_transparency.txt line 348",
         status="DERIVED", note="two Anthropic pages agree"),
    dict(subject="GPT-6 Astra", published="Apr 30, 2026", first_day="2026-04-30", last_day="2026-04-30",
         kind="knowledge cutoff", locator="sources/openai_models.txt lines 660-673", status="DERIVED", note=""),
    dict(subject="GPT-5.6 Sol", published="Feb 16, 2026", first_day="2026-02-16", last_day="2026-02-16",
         kind="knowledge cutoff", locator="sources/openai_models.txt lines 678-693", status="DERIVED", note=""),
    dict(subject="GPT-5.6 Terra", published="Feb 16, 2026", first_day="2026-02-16", last_day="2026-02-16",
         kind="knowledge cutoff", locator="sources/openai_models.txt lines 698-711", status="DERIVED", note=""),
    dict(subject="GPT-5.6 Luna", published="Feb 16, 2026", first_day="2026-02-16", last_day="2026-02-16",
         kind="knowledge cutoff", locator="sources/openai_models.txt lines 716-729", status="DERIVED", note=""),
    dict(subject="Gemini 3.8 Flash", published="March 2026", first_day="2026-03-01", last_day="2026-03-31",
         kind="knowledge cutoff", locator="sources/deepmind_modelcard_gemini-3-8-flash.txt line 243",
         status="DERIVED", note="card adds that some domains are limited to January 2025"),
    dict(subject="Gemini 3.1 Pro (preview)", published=None, first_day=None, last_day=None,
         kind="none published on the pages read", locator="sources/google_gemini-3.1-pro-preview.txt lines 244-245 (only 'Latest update February 2026'); sources/deepmind_modelcard_gemini-3-1-pro.txt (defers to Gemini 3 Pro card, not fetched)",
         status="UNDEMONSTRATED", note="no cutoff read from a primary page"),
]

TRANSIENT_SPEC = {  # spectroscopic-basis classes per Perley+2020 Fig.3 caption ("always spectroscopic for SNe/transients")
    "SN Ia", "SN Ia-91bg", "SN Ia-CSM", "SN Ia-SC", "SN Ia-pec", "SN Iax", "SN II", "SN II-pec", "SN IIb", "SN IIn",
    "SN Ib", "SN Ib-pec", "SN Ib/c", "SN Ibn", "SN Ic", "SN Ic-BL", "SN Ic-pec", "SN Icn", "SN Ca-rich-Ca", "Ca-rich",
    "TDE", "TDE-H-He", "TDE-He", "TDE-featureless", "nova", "ILRT", "LBV", "LRN", "Other", "other"}
SPEC_PLUS_PHOT = {  # spectroscopic class whose definition uses photometry (Fremling+2020 3.3.2, 3.3.1, 3.3.4; Perley+2020 App. E)
    "SLSN-I": "luminosity threshold Mg < -20 (Fremling+2020 sec 3.3.4)",
    "SLSN-II": "luminosity threshold Mg < -20 (Fremling+2020 sec 3.3.4)",
    "SN IIP": "IIP/IIL are photometrically defined subtypes (Fremling+2020 sec 3.3.2; Perley+2020 App. E)",
    "SN Ia-91T": "91T label requires strong spectroscopic or photometric evidence (Fremling+2020 sec 3.3.1)",
}
VARIABLE_MAYBE_PHOT = {"AGN", "CV"}      # Perley+2020 sec 2.4: photometric-only classification permitted
TENTATIVE = {"AGN?", "CV?"}              # '?' suffix: basis not documented in any source read
SNIASCORE_DEPLOY = "2021-04-15"          # Fremling+2021 (arXiv:2104.12980) sec 7

PERLEY_TABLE3 = {  # arXiv:2009.01242 Table 3, non-TNS classifications ('-' = retained TNS class)
    "ZTF18aamfrvy": "-", "ZTF18aazgfkq": "-", "ZTF18abcfcoo": "other", "ZTF18actuhrs": "SN Ia-CSM", "ZTF19aadnwvc": "SN Ia",
    "ZTF19aagqkrq": "ILRT", "ZTF19aaniqrr": "other", "ZTF19aaplpaa": "-", "ZTF19aatubsj": "none", "ZTF19aatevrp": "-",
    "ZTF19aavxfib": "none", "ZTF19acdsqir": "-", "ZTF19acnfsij": "nova", "ZTF19acoaiub": "ILRT", "ZTF19adakuos": "nova",
    "ZTF20aaertpj": "SN Ib", "ZTF20aaeuxqk": "-", "ZTF20aakdppm": "nova", "ZTF20aatwonv": "-", "ZTF20abijfqq": "-",
    "ZTF20abfhyil": "none"}


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def parse_capture(path):
    """Return {ZTFID: type string} from an explorer table capture."""
    t = Path(path).read_text(encoding="utf-8", errors="replace")
    out = {}
    for row in re.findall(r"<tr>\s*(<td>.*?)</tr>", t, flags=re.S):
        cells = [html.unescape(re.sub(r"<[^>]+>", "", c)).replace("\xa0", " ").strip()
                 for c in re.findall(r"<td[^>]*>(.*?)</td>", row, flags=re.S)]
        if len(cells) >= 15 and re.fullmatch(r"ZTF\d\d[a-z]{7}", cells[0]):
            out[cells[0]] = cells[11]
    return out


def main():
    res = {}
    got = sha256(RAW)
    if got != RAW_SHA:
        sys.exit(f"raw sha256 mismatch {got}")
    raw = pd.read_csv(RAW, dtype=str, keep_default_na=False)
    ext = pd.read_csv(EXTRA, dtype=str, keep_default_na=False)
    res["raw_sha256"] = got
    res["extra_sha256"] = sha256(EXTRA)
    res["rows_raw"] = int(len(raw))
    res["unique_ztfid"] = int(raw.ZTFID.nunique())
    iau = raw[raw.IAUID != "-"].IAUID.value_counts()
    res["iauid_missing"] = int((raw.IAUID == "-").sum())
    res["iauid_shared_by_2plus_ztfid"] = int((iau > 1).sum())
    res["ztfid_rows_in_shared_iauid"] = int(iau[iau > 1].sum())
    df = raw.merge(ext[["ZTFID", "discID", "savedate", "discdate", "IAUID", "type", "peakt"]], on="ZTFID", suffixes=("", "_x"))
    res["extra_join_rows"] = int(len(df))
    res["extra_vs_raw_mismatch"] = {c: int((df[c] != df[c + "_x"]).sum()) for c in ["IAUID", "type", "peakt"]}

    # ---- peakt zero point ----
    pk = pd.to_numeric(df.peakt, errors="coerce")
    df["peak_date_jd2458000"] = Time(pk.fillna(0).values + 2458000.0, format="jd").to_datetime()
    df["peak_date_mjd2018"] = pd.to_datetime("2018-01-01") + pd.to_timedelta(pk.fillna(0), unit="D")
    df["disc"] = pd.to_datetime(df.discdate.str[:10], errors="coerce")
    df["saved"] = pd.to_datetime(df.savedate, errors="coerce")
    df["iau_year"] = pd.to_numeric(df.IAUID.str.extract(r"(\d{4})")[0], errors="coerce")
    ok = pk.notna() & df.iau_year.notna() & df.disc.notna()
    zp = {}
    for name, col in [("JD-2458000 (explorer_info.txt line 79; Fremling+2020 Table 1 note d)", "peak_date_jd2458000"),
                      ("days since 2018-01-01 (panel brief guess)", "peak_date_mjd2018")]:
        d = pd.to_datetime(df.loc[ok, col])
        lag = (d - df.loc[ok, "disc"]).dt.days
        zp[name] = dict(n=int(ok.sum()),
                        peak_year_equals_iau_year_or_next=round(float(d.dt.year.sub(df.loc[ok, "iau_year"]).isin([0, 1]).mean()), 4),
                        median_peak_minus_discdate_days=float(lag.median()),
                        share_peak_within_minus30_plus200_days_of_discdate=round(float(lag.between(-30, 200).mean()), 4))
    res["peakt_zero_point_test"] = zp
    # known-object check against dates stated in arXiv:2104.12980 sec 6 ("taken around maximum light on <date>")
    known = {"ZTF18aaxmhvk": ("SN2018cne", "2018-06-14"), "ZTF20aatxryt": ("SN2020eyj", "2020-04-02")}
    kc = {}
    for z, (name, d) in known.items():
        row = df[df.ZTFID == z]
        if row.empty:
            kc[z] = dict(iau=name, paper_max_light=d, in_file=False)
            continue
        v = float(row.peakt.iloc[0])
        kc[z] = dict(iau=name, paper_max_light=d, in_file=True, peakt=v,
                     date_if_jd_minus_2458000=str(Time(v + 2458000.0, format="jd").to_datetime().date()),
                     date_if_days_since_2018_01_01=str((pd.Timestamp("2018-01-01") + pd.Timedelta(days=v)).date()),
                     file_type=row.type.iloc[0], paper_official_type="SN Ic (arXiv:2104.12980 sec 6, Fremling & Sharma 2018 TNS report 2018-886)" if z == "ZTF18aaxmhvk" else "SN Ia")
    res["peakt_known_objects"] = kc
    res["peakt_non_numeric"] = int(pk.isna().sum())

    # ---- label basis taxonomy ----
    def basis(t):
        if t == "-": return "unlabeled"
        if t in SPEC_PLUS_PHOT: return "spectroscopic_with_photometric_criterion"
        if t in TRANSIENT_SPEC: return "spectroscopic_transient_class"
        if t in VARIABLE_MAYBE_PHOT: return "variable_spectroscopic_or_photometric_unresolved"
        if t in TENTATIVE: return "tentative_variable_basis_undocumented"
        return "unmapped"
    df["basis"] = df.type.map(basis)
    res["label_basis_counts"] = df.basis.value_counts().to_dict()
    res["type_counts"] = df.type.value_counts().to_dict()
    lab = df[df.type != "-"]
    res["labeled_objects"] = int(len(lab))
    res["unlabeled_objects"] = int((df.type == "-").sum())

    # SNIascore: annotation produced by a model. Reporter identity is not in the file.
    ia = df[df.type == "SN Ia"]
    peak = pd.to_datetime(ia.peak_date_jd2458000)
    dep = pd.Timestamp(SNIASCORE_DEPLOY)
    res["sniascore"] = dict(
        plain_SN_Ia=int(len(ia)),
        plain_SN_Ia_peak_on_or_after_deploy_minus_30d=int((peak >= dep - pd.Timedelta(days=30)).sum()),
        plain_SN_Ia_peak_before_deploy_minus_30d=int((peak < dep - pd.Timedelta(days=30)).sum()),
        note="SNIascore phase range -20..+30 d (arXiv:2104.12980 sec 2) and deployment 2021-04-15 (sec 7). Objects peaking >=30 d before deployment cannot have had a SNIascore spectrum inside that range; the complement is the population in which SNIascore origin is possible. Actual reporter per object needs TNS classification reports.")

    # reporter group (BTS vs other TNS groups vs SNIascore bot): not in file
    res["reporter_group_resolvable_in_file"] = 0
    res["reporter_group_unresolved_labeled_objects"] = int(len(lab))

    # IAU prefix vs label (identifier leakage)
    df["prefix"] = df.IAUID.str.extract(r"^([A-Z]+)")[0].fillna("none")
    sn_types = {t for t in TRANSIENT_SPEC | set(SPEC_PLUS_PHOT) if t.startswith("SN") or t.startswith("SLSN")}
    res["iau_prefix"] = dict(
        crosstab={p: g.type.value_counts().to_dict() for p, g in df.groupby("prefix")},
        SN_prefix_total=int((df.prefix == "SN").sum()),
        SN_prefix_with_SN_or_SLSN_type=int(((df.prefix == "SN") & df.type.isin(sn_types)).sum()),
        SN_prefix_unlabeled_in_BTS=int(((df.prefix == "SN") & (df.type == "-")).sum()),
        AT_prefix_with_SN_or_SLSN_type=int(((df.prefix == "AT") & df.type.isin(sn_types)).sum()),
        TDE_prefix_total=int((df.prefix == "TDE").sum()))

    # Perley Table 3 overrides present in file
    t3 = df[df.ZTFID.isin(PERLEY_TABLE3)]
    res["perley_table3"] = dict(listed=len(PERLEY_TABLE3), present=int(len(t3)), absent=sorted(set(PERLEY_TABLE3) - set(t3.ZTFID)),
                                rows={r.ZTFID: dict(file_type=r.type, table3=PERLEY_TABLE3[r.ZTFID]) for r in t3.itertuples()})

    # ---- exposure key ----
    demo = [s for s in SUBJECTS if s["status"] == "DERIVED"]
    earliest = min(pd.Timestamp(s["first_day"]) for s in demo)
    latest = max(pd.Timestamp(s["last_day"]) for s in demo)
    demo_no_haiku = [s for s in demo if s["subject"] != "Claude Haiku 4.5"]
    earliest_nh = min(pd.Timestamp(s["first_day"]) for s in demo_no_haiku)
    res["subjects"] = SUBJECTS
    res["cutoff_bounds"] = dict(earliest_first_day=str(earliest.date()), latest_last_day=str(latest.date()),
                                earliest_first_day_excluding_haiku45=str(earliest_nh.date()),
                                subjects_undemonstrated=[s["subject"] for s in SUBJECTS if s["status"] != "DERIVED"])

    caps = {k: parse_capture(v) for k, v in CAPTURES.items()}
    res["captures"] = {k: dict(file=str(CAPTURES[k].relative_to(HERE)), sha256=sha256(CAPTURES[k]), rows_parsed=len(v),
                               rows_with_type=sum(1 for t in v.values() if t != "-")) for k, v in caps.items()}

    def split(capture_key, cutoff_first_day, cutoff_last_day):
        cap = caps[capture_key]
        capt = pd.Timestamp(capture_key)
        assert capt < cutoff_first_day
        lab = df[df.type != "-"].copy()
        lab["cap_type"] = lab.ZTFID.map(cap)
        before = lab.cap_type.notna() & (lab.cap_type == lab.type)
        after = lab.disc > cutoff_last_day
        changed = lab.cap_type.notna() & (lab.cap_type != "-") & (lab.cap_type != lab.type)
        cap_unlabeled = lab.cap_type.notna() & (lab.cap_type == "-")
        assert not (before & after).any()
        unresolved = ~(before | after)
        # label public date lower bound is the TNS discovery date; show the discovery-year spread of unresolved
        return dict(
            capture=capture_key, cutoff_window=[str(cutoff_first_day.date()), str(cutoff_last_day.date())],
            labeled_objects=int(len(lab)),
            label_public_before_every_cutoff=int(before.sum()),
            label_public_after_every_cutoff=int(after.sum()),
            unresolved=int(unresolved.sum()),
            unresolved_breakdown=dict(
                absent_from_capture=int((unresolved & lab.cap_type.isna()).sum()),
                unlabeled_in_capture=int((unresolved & cap_unlabeled).sum()),
                label_changed_since_capture=int((unresolved & changed).sum()),
                absent_and_discovered_after_capture=int((unresolved & lab.cap_type.isna() & (lab.disc > capt)).sum()),
                absent_and_discovered_before_capture=int((unresolved & lab.cap_type.isna() & (lab.disc <= capt)).sum())),
            unresolved_by_discovery_year=lab[unresolved].disc.dt.year.value_counts().sort_index().astype(int).to_dict(),
            after_by_type=lab[after].type.value_counts().to_dict(),
            discovered_after_latest_cutoff_all_objects=int((df.disc > cutoff_last_day).sum()),
            discovered_before_earliest_cutoff_labeled=int((lab.disc < cutoff_first_day).sum()),
            discovered_inside_cutoff_window_labeled=int(((lab.disc >= cutoff_first_day) & (lab.disc <= cutoff_last_day)).sum()),
        )
    res["exposure_split_all_demonstrated_subjects"] = split("2024-12-08T23:13:31", earliest, latest)
    res["exposure_split_excluding_haiku45"] = split("2025-08-10T06:50:56", earliest_nh, latest)
    res["all_units_predate_all_subjects"] = bool((df[df.type != "-"].disc <= latest).all())
    res["discovery_after_2026_06_29_all"] = int((df.disc >= pd.Timestamp("2026-06-29")).sum())
    res["discovery_on_or_after_2026_07_01_labeled"] = int(((df.disc >= pd.Timestamp("2026-07-01")) & (df.type != "-")).sum())
    res["discovery_on_or_after_2026_07_01_all"] = int((df.disc >= pd.Timestamp("2026-07-01")).sum())
    res["discdate_range"] = [str(df.disc.min().date()), str(df.disc.max().date())]
    res["savedate_range"] = [str(df.saved.min().date()), str(df.saved.max().date())]
    res["objects_discovered_after_max_savedate"] = int((df.disc > df.saved.max()).sum())
    res["sniascore_first_auto_object_in_file"] = df[df.IAUID == "SN2021ijb"][["ZTFID", "type", "discID"]].to_dict("records")
    out = HERE / "derived_counts.json"
    out.write_text(json.dumps(res, indent=1, default=str))
    print(json.dumps({k: res[k] for k in ["rows_raw", "unique_ztfid", "iauid_shared_by_2plus_ztfid", "label_basis_counts",
                                          "sniascore", "peakt_zero_point_test", "cutoff_bounds", "captures",
                                          "exposure_split_all_demonstrated_subjects", "exposure_split_excluding_haiku45",
                                          "all_units_predate_all_subjects", "discovery_on_or_after_2026_07_01_labeled", "peakt_known_objects", "objects_discovered_after_max_savedate",
                                          "discovery_on_or_after_2026_07_01_all", "perley_table3", "extra_vs_raw_mismatch"]},
                     indent=1, default=str))
    print({k: v for k, v in res["iau_prefix"].items() if k != "crosstab"})


if __name__ == "__main__":
    main()
