# Amendment ledger (after compositions_FROZEN.md sha256 b2f72948…427c)

calibration only, contamination FAIL on this cohort
PRE-I1: graph edge R1→I1 unmet, escalated

## A-1: ParSNIP `input_redshift` (recorded before any ParSNIP fold trained; no label read)
- **Rule changed:** FROZEN §7 said `predict_redshift=True, input_redshift=False`.
- **Cause, observed in code:** with `input_redshift=False`, kboone/parsnip@dcea62f `parsnip.py::_get_data` line 630 raises `UnboundLocalError: extra_input_data`. The variable is only assigned inside `if self.settings['input_redshift']`. Found by a label-free smoke test on 400 fetched light curves in the scratchpad.
- **New rule:** `predict_redshift=True`, `input_redshift=True` (the code default). Every object gets meta `hostgal_photoz=0.0` and `hostgal_photoz_err=1e3`, identical for all objects. The two extra encoder input channels are therefore constants and carry no redshift information. `hostgal_specz=NaN`, so the specz term of the loss is masked out.
- **Not done:** the ParSNIP source was not patched. Repairing the tool would change the tool being measured.
- **Effect on other declarations:** none.

## A-2: ParSNIP learning rate (recorded before any fold's model was kept; no label read)
- **Rule changed:** FROZEN §7 said "all other settings default" (`learning_rate=1e-3`).
- **Cause, observed and label-free:** the first launch of fold 0 at the frozen settings logged `Loss: nan` within epoch 0, and it was stopped. An instrumented step loop (scratchpad `nan_train_debug.py`, fold-0 training set, seed 0) found two failures:
  1. **With augmentation (code default):** non-finite loss at step 2. Augmentation (`augment_light_curves`, drop_frac up to 0.5) removed the only point of a single-detection first-alert light curve (unit 1757, E1). The empty light curve gives `nll = 0.5·0·(0 − model_flux·amplitude)²` with the product overflowing float32, so 0·inf = NaN. The code comment "can very rarely end up with no light curve points. Handle that gracefully" does not hold on this input.
  2. **Repair 1, `augment=False`:** still non-finite at step 30. `amplitude_logvar` reached −inf and the spectral penalty was 0/0, with decoder spectra reaching about 1e16.
- **Repair 2, `learning_rate=1e-4`:** 0 non-finite losses in 1,075 steps, both with and without augmentation.
- **New rule:** `learning_rate=1e-4`, augmentation at its code default (on), everything else as FROZEN §7 plus A-1.
- **Ladder note:** this is the second distinct repair (loop.md rung 3). Had it shown the same symptom, the diagnosis would have been reclassified as "ParSNIP is numerically non-viable on decision-time ZTF photometry at the pinned commit" and C5 recorded dead, with no third repair.
- **Validity note:** the change was chosen on training-loss finiteness only. No label, metric or held-out prediction was seen. The residual risk of non-finite batches during 60 epochs is measured and logged per fold as the finite fraction of held-out predictions.
- **Not done:** the ParSNIP source was not patched.

## A-3: all-NaN columns at GBDT fit (recorded before any composition fit completed; no metric computed)
- **Rule changed:** FROZEN §7 said "NaN is passed natively".
- **Cause, observed:** sklearn 1.9.1 `HistGradientBoostingClassifier.fit` raises `ValueError: window shape cannot be larger than input array shape` in `_find_binning_thresholds` when a column has no non-NaN value. That holds for the C3 fit columns, which are NaN for every unit at E1 and for all but 2 units at E3. The error came on the first fit call; no model was saved and no prediction was written.
- **New rule:** inside each fold, columns with no finite value among the training rows are dropped before `fit`, and the same columns are dropped at predict. The dropped list is saved with each model pickle.
- **Why this changes no information:** a tree cannot split on a column that is constant-missing in training, so it could not use the column anyway.
- **Unchanged:** channel alive fractions and the dead-channel count are computed from the features, not from the fitted columns, so they are unaffected.
