#!/usr/bin/env python3
"""Write seed_ledger.json for agent 4. read_in_full is recorded per source as read."""
import json, os, hashlib
OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S = os.path.join(OUT, "sources")
def sha(f):
    return hashlib.sha256(open(os.path.join(S, f), "rb").read()).hexdigest()
NOTE_STRIP = "read from sources/<id>.txt with lines consisting only of numbers/table cells stripped; prose, captions and section text read in order, numeric table cells not read line by line"
seeds = []
def seed(id, file, full, contrib, facts, note=""):
    seeds.append({"id": id, "file": file, "sha256": sha(file), "read_in_full": full,
                  "reading_note": note, "contribution": contrib, "facts": facts})

seed("CabreraVives2024_ATAT_arXiv2405.03078", "arxiv_2405.03078.pdf", True,
     "ATAT tool card: paper side of every disagreement; trained-on field of the inventory",
     [{"assertion": "ELAsTiCC dataset: 1,845,146 light curves in ugrizY; ATAT trained on first-campaign training set", "locator": "Sec 2.1 para 1"},
      {"assertion": "64 metadata attributes incl. best heliocentric redshift, MW extinction, host photo-z quantiles", "locator": "Sec 2.1 para 2"},
      {"assertion": "x_{j,b} = (mu, sigma) projected by W_TM (E_TM x 2)", "locator": "Sec 2.2.1, footnote 9"},
      {"assertion": "Adam lr 2e-4, batch 256, dropout 0.2, T_max 1500, H 64, eval every 20k iterations, patience 3", "locator": "Sec 2.2.5"},
      {"assertion": "MTA t* in {8,128,2048}", "locator": "Sec 2.2.4"},
      {"assertion": "BHRF baseline: 350 trees, entropy, max depth 100, 15000/9000/3900 per class per tree, 100 features", "locator": "Sec 2.4"},
      {"assertion": "ELAsTiCC may not be representative of the real LSST alert stream", "locator": "Sec 4 para 3"},
      {"assertion": "code to be public once accepted", "locator": "Sec 1 last para"}],
     "read in full including table cells (sources txt, 4237 lines)")
seed("Boone2021_ParSNIP_arXiv2109.13999", "arxiv_2109.13999.pdf", True,
     "ParSNIP tool card; generator/scorer role evidence; ZTF/Rubin coverage caveats",
     [{"assertion": "redshifts of all transients assumed known", "locator": "Sec 2 para 4"},
      {"assertion": "PS1 dataset 2,885 light curves with host-galaxy redshifts, 557 typed", "locator": "Sec 2 para 1"},
      {"assertion": "background from observations >=250 d from max; normalise by max flux with S/N>=5; error floor 0.01", "locator": "Sec 2.1"},
      {"assertion": "Jeffreys prior on amplitude, importance sampling with one sample", "locator": "Sec 3.7"},
      {"assertion": "decoder predicts photometry for any instrument/bandpass without modification", "locator": "Sec 6.8 para 1"},
      {"assertion": "photo-z could be used as prior; encoder insensitive to 0.05 redshift noise", "locator": "Sec 6.3"},
      {"assertion": "SN Ia AUC 0.977 vs Avocado 0.962 on PLAsTiCC with true redshifts", "locator": "Sec 5.3"},
      {"assertion": "no instrument-specific elements other than bandpass definitions", "locator": "Sec 5.3 last para"}],
     NOTE_STRIP)
seed("Kenworthy2021_SALT3_arXiv2104.07795", "arxiv_2104.07795.pdf", True,
     "SALT3 tool card paper side",
     [{"assertion": "F = x0[M0 + x1 M1] exp(c CL(lambda))", "locator": "Sec 2, Eq. 1"},
      {"assertion": "model uncertainty at filter central wavelength; flagged as systematic", "locator": "Sec 2.2 Eq. 3; Sec 6 para 'Further development work'"},
      {"assertion": "chi2 uses Sigma_Total = diag + Sigma_Model", "locator": "Sec 2.5 Eqs. 10-11"},
      {"assertion": "K21 wavelength range 2000-11000 A; fourth-order colour law to 8000 A", "locator": "Abstract body; Sec 5 para 1"},
      {"assertion": "K21 compilation surveys: Calan-Tololo, CfA1-4, SDSS, SNLS, misc low-z, Foundation, PS1-MDS, DES", "locator": "Table 4"},
      {"assertion": "training restricted to Branch-normal SNe Ia incl. 1991T-like", "locator": "Sec 4.4"}],
     NOTE_STRIP)
seed("SanchezSaez2021_ALeRCE_LC_arXiv2008.03311", "arxiv_2008.03311.pdf", True,
     "ALeRCE BHRF tool card paper side; ZTF coverage evidence",
     [{"assertion": ">=6 detections in g or >=6 in r", "locator": "Abstract; Sec 2.2.1; Sec 6.1"},
      {"assertion": "152 features: 142 ZTF + 10 extra (coords, AllWISE colours, sgscore1, median rb)", "locator": "Sec 3"},
      {"assertion": "BRF 500 trees, max depth none, sqrt features, stochastic 20%", "locator": "Sec 4.1.1 last para"},
      {"assertion": "bottom level macro P/R/F1 0.57/0.76/0.59", "locator": "Sec 6.1"},
      {"assertion": "Version 1.0; lc_classifier v1.0.1 archived on Zenodo", "locator": "Sec 6.1 last para; Sec 6.2"},
      {"assertion": "distance information absent; SN Ibc over-predicted", "locator": "Sec 5.3.2"}],
     NOTE_STRIP)
seed("Zhang_Helfer2024_Maven_arXiv2408.16829", "arxiv_2408.16829.pdf", True,
     "Maven inventory row: training data (BTS), inputs, ZTF-only bands",
     [{"assertion": "pre-trained on 0.5M SNANA ZTF-like simulations; fine-tuned on 4,702 ZTF BTS SNe", "locator": "Abstract body; Sec 2.1; Sec 2.2"},
      {"assertion": "light-curve encoder uses magnitudes with 0/1 band embedding for r/g", "locator": "Sec 3.2; Fig 3"},
      {"assertion": "Maven does not dramatically outperform supervised baselines", "locator": "Sec 6 item 3"}],
     NOTE_STRIP)
seed("Rehemtulla2023_BTSbot_arXiv2307.07618", "arxiv_2307.07618.pdf", True,
     "BTSbot inventory row: labels are BTS scanning decisions; ZTF-alert inputs",
     [{"assertion": "positive class = bright SNe classified by BTS; negatives = sources rejected by BTS; 14,348 sources", "locator": "Sec 2.1"},
      {"assertion": "inputs: science/reference/difference cutouts + extracted features incl. distpsnr1, sgscore1, ndethist", "locator": "Sec 2; Fig 1"},
      {"assertion": "integrated into Fritz, posts scores to all new ZTF alerts", "locator": "Sec 4"}],
     NOTE_STRIP + " (ICML workshop version v2)")
seed("Shah2025_ORACLE_arXiv2501.01496", "arxiv_2501.01496.pdf", True,
     "ORACLE inventory row: ELAsTiCC2 training, static host/redshift features, ORACLE-lite",
     [{"assertion": "23 time-independent features incl. REDSHIFT_HELIO, HOSTGAL_PHOTOZ/SPECZ, HOSTGAL_MAG_*", "locator": "Table 1; Sec 3"},
      {"assertion": "ORACLE-lite uses only time-dependent features", "locator": "Sec 5; Sec 7"},
      {"assertion": "trained on simulated ELAsTiCC; fine-tuning and validation with real LSST data still needed", "locator": "future-work section, paragraphs beginning 'Longer-term developments of ORACLE' and 'Ultimately, simulated data sets such as ELAsTiCC'"},
      {"assertion": "open-source and open-weight on GitHub", "locator": "Sec 10 para 'ORACLE models are both open-source and open-weight'"}],
     NOTE_STRIP)
seed("Fraga2024_Fink_arXiv2404.08798", "arxiv_2404.08798.pdf", True,
     "Fink CATS/SNN/RF inventory rows; ELAsTiCC-only training; CATS metadata branch",
     [{"assertion": "classifiers trained and tested on ELAsTiCC v1 streamed alerts", "locator": "Sec 2"},
      {"assertion": "CATS concatenates mwebv, hostgal_zphot, z_final and errors before dense layers", "locator": "Sec 5.1 para 'Our inputs were'"},
      {"assertion": "SNN adds redshift and MW extinction as features", "locator": "Sec 5.2"},
      {"assertion": "transition from ZTF to LSST requires significant adaptation", "locator": "Abstract body; Sec 3; Sec 9"}],
     NOTE_STRIP)
seed("Muthukrishna2019_RAPID_arXiv1904.00014", "arxiv_1904.00014.pdf", False,
     "RAPID trained-on field only (Sec 2.1 read); blocks I3 card for RAPID",
     [{"assertion": "training set simulated with SNANA + PLAsTiCC models + ZTF MSIP observing-conditions library; g and r bands", "locator": "Sec 2.1, 2.1.1, 2.1.2"},
      {"assertion": "work relies on knowing redshift of each transient (z<0.5)", "locator": "Sec 2.3"}],
     "Introduction and Sec 2 (lines 290-545 of the stripped text) read; rest not read")
for id, f, why in [
    ("Kessler2009_SNANA_arXiv0908.4280", "arxiv_0908.4280.pdf", "SNANA row rests on code only; blocks I3 card for SNANA"),
    ("Moller2019_SuperNNova_arXiv1901.06384", "arxiv_1901.06384.pdf", "SNN row rests on code and Fink paper; blocks I3 card"),
    ("Smith2020_ATLAS_Sherlock_arXiv2003.09052", "arxiv_2003.09052.pdf", "Sherlock row rests on code only"),
    ("Hosseinzadeh2020_Superphot_arXiv2008.04912", "arxiv_2008.04912.pdf", "Superphot row rests on code only"),
    ("Gagliano2021_GHOST_arXiv2008.09630", "arxiv_2008.09630.pdf", "GHOST row rests on code only"),
    ("Qu2021_SCONE_arXiv2106.04370", "arxiv_2106.04370.pdf", "SCONE row rests on README/code only"),
    ("DonosoOliva2023_Astromer_arXiv2205.01677", "arxiv_2205.01677.pdf", "Astromer rows rest on README/code only"),
    ("Parker2024_AstroCLIP_arXiv2310.03024", "arxiv_2310.03024.pdf", "AstroCLIP row rests on README/HF API only"),
    ("deSoto2024_SuperphotPlus_arXiv2403.07975", "arxiv_2403.07975.pdf", "Superphot+ row rests on README/code only"),
    ("Jones2024_Blast_arXiv2410.17322", "arxiv_2410.17322.pdf", "Blast row rests on code only"),
    ("Rizhko2024_AstroM3_arXiv2411.08842", "arxiv_2411.08842.pdf", "AstroM3 row: weights-availability sentence located by grep (line ~601 'will be made available upon acceptance'); not decision-bearing beyond 'no weights found in repo'"),
    ("MMU2024_MultimodalUniverse_arXiv2412.02527", "arxiv_2412.02527.pdf", "MMU excluded as non-channel from repo contents"),
    ("DonosoOliva2025_Astromer2_arXiv2502.02717", "arxiv_2502.02717.pdf", "Astromer2 row rests on README only"),
    ("AppleCiDEr_I_2025_arXiv2507.16088", "arxiv_2507.16088.pdf", "AppleCiDEr row rests on repo only"),
    ("Rubin_web_how-rubin-works_alerts", "rubin_explore_how-rubin-works_alerts.html", "fetched, not read"),
    ("Rubin_web_press-releases", "rubin_news_press-releases.html", "index page fetched, not read; no release article followed"),
]:
    seed(id, f, False, "zero decision-bearing facts from this source; " + why, [], "not read in full")
seed("Rubin_web_alerts-and-brokers_2026-07-03", "rubin_for-scientists_data-products_alerts-and-brokers.html", True,
     "broker list; Lasair runs Sherlock; no survey start or first-alert dates on this page",
     [{"assertion": "page last updated 03 Jul 2026 15:27 MST", "locator": "txt, header 'Date last updated'"},
      {"assertion": "seven full-stream brokers: ALeRCE, AMPEL, ANTARES, Babamul, Fink, Lasair, Pitt-Google", "locator": "txt, 'Full-stream brokers' paragraph"},
      {"assertion": "Lasair filters use the Sherlock intelligent crossmatch", "locator": "txt, Lasair paragraph"}],
     "page text extracted to .txt and read in full")

L = {"agent": "agent4_tools_instrument", "date": "2026-09-16", "seeds": seeds,
     "unverified_brief_claims": [
        {"claim": "Rubin alerts began streaming to brokers in February 2026", "status": "UNDEMONSTRATED from agent-4 sources (the alerts-and-brokers page carries no date); agent3 cites RTN-011 line 2468 for 2026-02-24"},
        {"claim": "ten-year LSST formally started 2026-06-30", "status": "UNDEMONSTRATED from agent-4 sources"}],
     "completeness": "9 of 26 sources read in full (8 papers + 1 Rubin page); 1 partially (RAPID Sec 2); 16 fetched and not read. Their inventory rows rest on code/README/HF metadata and carry that in tool_inventory_slot.json. Search for conditional light-curve generators beyond ParSNIP/SALT3/SNANA/Superphot+ used one arXiv API query (diffusion AND light curves AND supernova AND generat) that returned zero entries; that negative is a query result, not a completeness claim."}
json.dump(L, open(os.path.join(OUT, "seed_ledger.json"), "w"), indent=1)
print(len(seeds), sum(s["read_in_full"] for s in seeds))
