import urllib.request
import re

req = urllib.request.Request(
    'https://krish-rm.github.io/hsri-research/',
    headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache',
             'User-Agent': 'HSRI-Audit/5.0'}
)
html = urllib.request.urlopen(req).read().decode('utf-8')

results = {
    'version_badge': re.findall(r'Preview Benchmark v[\d.]+', html),
    'pagination': re.findall(r'Showing \d+ of \d+ countries', html),
    'footer_methodology': re.findall(r'href="(/[^"]*methodology[^"]*)"', html)[:2],
    'coverage_link': '/hsri-research/coverage/' in html,
}

for k, v in results.items():
    print(f'{k}: {v}')

assert any(v in str(results['version_badge']) for v in ['v0.2', 'v0.3']), 'VERSION WRONG'
assert '39' in str(results['pagination']), 'PAGINATION WRONG'
assert any('/hsri-research/' in str(l) for l in results['footer_methodology']), 'FOOTER WRONG'
assert results['coverage_link'], 'COVERAGE LINK MISSING'
print('ALL INDEPENDENT CHECKS PASSED')
