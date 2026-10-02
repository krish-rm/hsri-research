import urllib.request
import re

meth_req = urllib.request.Request(
    'https://krish-rm.github.io/hsri-research/methodology/',
    headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache',
             'User-Agent': 'HSRI-Audit/5.0'}
)
meth_html = urllib.request.urlopen(meth_req).read().decode('utf-8')

results = {
    'exp_pipeline_section_present': 'Behavioral Experiment Pipeline' in meth_html,
    'exp01_label_present': 'SYNTHETIC PILOT COMPLETE: IRB PACKAGE READY' in meth_html,
    'exp02_label_present': 'SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB SUBMISSION' in meth_html,
    'exp03_label_present': ('SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB PACKAGING' in meth_html or 'STIMULI GENERATED: CONSTRAINT CHECKS PASSED' in meth_html),
    'proceed_to_irb_absent': 'PROCEED TO IRB' not in meth_html,
    'pilot_in_progress_absent': 'PILOT IN PROGRESS' not in meth_html,
    'irb_warning_present': 'All experiments are under IRB gate' in meth_html or 'IRB gate' in meth_html,
}

for k, v in results.items():
    print(f'{k}: {v}')

assert results['exp_pipeline_section_present'], 'PIPELINE SECTION MISSING'
assert results['exp01_label_present'], 'EXP-01 LABEL MISSING: SYNTHETIC PILOT COMPLETE: IRB PACKAGE READY'
assert results['exp02_label_present'], 'EXP-02 LABEL MISSING: SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB SUBMISSION'
assert results['exp03_label_present'], 'EXP-03 LABEL MISSING: SYNTHETIC PILOT COMPLETE: STIMULI CLEARED FOR IRB PACKAGING'
assert results['proceed_to_irb_absent'], 'PROCEED TO IRB STILL PRESENT'
assert results['pilot_in_progress_absent'], 'PILOT IN PROGRESS STILL PRESENT'
assert results['irb_warning_present'], 'IRB WARNING MISSING'
print('ALL SUPPLEMENTARY CHECKS PASSED')
