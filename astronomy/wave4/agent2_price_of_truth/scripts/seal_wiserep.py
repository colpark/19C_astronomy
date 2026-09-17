import json, hashlib, numpy as np, pathlib
D=pathlib.Path(__file__).resolve().parent.parent
assert hashlib.sha256((D/'calendar_model_FROZEN.md').read_bytes()).hexdigest()=="a681d81a8c0e25fa6885096e9ad01bd114fbfa768f67c8a683182b23629227e6"
E=json.load(open(D.parents[1]/'wave3/agent2_measured_labels/sealed/enumeration_E_SEALED.json'))
typed=['2026rwk','2026srp','2026stj','2026stu','2026tim','2026trp','2026tzm','2026uii','2026uvw','2026uwo','2026uxs','2026uyc','2026vpl']
rng=np.random.default_rng(20260918)
untyped=[x['name'] for x in E['tierA'] if not x.get('typed_T9') and x['name'] not in typed]
samp=[untyped[i] for i in rng.permutation(len(untyped))[:20]]
tb=[x['name'] for x in E['tierB']]
ctrl=[tb[i] for i in rng.permutation(len(tb))[:10]]
look=dict(calendar_model_sha256="a681d81a8c0e25fa6885096e9ad01bd114fbfa768f67c8a683182b23629227e6", typed_cohort=typed, untyped_cohort_sample=samp, positive_controls_noncohort=ctrl, rule="calendar_model_FROZEN.md sec 7")
pred=dict(calendar_model_sha256="a681d81a8c0e25fa6885096e9ad01bd114fbfa768f67c8a683182b23629227e6", written="before any WISeREP content read",
  predictions={"wiserep_live_reachable":{"p":0.2,"point":"HTTP 403 (as wave 3)"},
               "wayback_captures_exist_for_typed_cohort_object_pages":{"point":2,"range":[0,13]},
               "if_reachable_typed_cohort_with_public_spectrum":{"point":8,"range":[0,13]},
               "if_reachable_positive_controls_with_spectrum":{"point":8,"range":[3,10]},
               "if_reachable_uploader_shows_classifier_human_vs_bot":{"point":"no (group only)"},
               "IRSA_U_annual_mean":{"point":0.7,"range":[0.5,0.85]},
               "months_to_N485_at_c8_p0.93_s0.93":{"point":3,"range":[2,6]}})
for n,o in [('wiserep_lookup_SEALED.json',look),('wiserep_predictions_SEALED.json',pred)]:
    p=D/'sealed'/n; p.write_text(json.dumps(o,indent=1)); h=hashlib.sha256(p.read_bytes()).hexdigest(); (D/'sealed'/n.replace('.json','.sha256')).write_text(f"{h}  {n}\n"); print(n,h)
