"""Manual test runner (works without pytest).

Usage:
    python tests/run_manual.py
"""
import sys
import importlib
from pathlib import Path

# Add parent dir to path so we can import scripts/ and tests/
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT))

test_modules = [
    'tests.test_filters',
    'tests.test_region_classifier',
    'tests.test_clusters',
    'tests.test_bilingual',
    'tests.test_html_builder',
    'tests.test_deploy',
]

total_pass = 0
total_fail = 0
failures = []

for mod_name in test_modules:
    print(f'\n=== {mod_name} ===')
    mod = importlib.import_module(mod_name)
    test_funcs = sorted([name for name in dir(mod) if name.startswith('test_')])
    for tf in test_funcs:
        try:
            getattr(mod, tf)()
            print(f'  ✓ {tf}')
            total_pass += 1
        except Exception as e:
            print(f'  ❌ {tf}: {e}')
            total_fail += 1
            failures.append(f'{mod_name}.{tf}: {e}')

print(f'\n=== Summary ===')
print(f'Total: {total_pass + total_fail}')
print(f'Passed: {total_pass}')
print(f'Failed: {total_fail}')

if failures:
    print('\nFailures:')
    for f in failures:
        print(f'  - {f}')
    sys.exit(1)
else:
    print('\n🎉 All tests passed!')
    sys.exit(0)