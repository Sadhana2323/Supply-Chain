import os
import re
import sys

app_dir = r"c:/Supply chain/Supply-Chain"
sys.path.insert(0, app_dir)

from utils.translations import translations

en_keys = set(translations["en"].keys())
ta_keys = set(translations["ta"].keys())

found_keys = set()
for root, _, files in os.walk(app_dir):
    for file in files:
        if file.endswith('.py'):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                content = f.read()
                # find all occurrences of _("something") or _('something')
                # this simple regex assumes no escaped quotes inside the string itself
                matches_double = re.findall(r'_\("([^"]+)"\)', content)
                matches_single = re.findall(r"_\('([^']+)'\)", content)
                for m in matches_double + matches_single:
                    found_keys.add(m)

missing_en = found_keys - en_keys
missing_ta = found_keys - ta_keys

print("Missing in EN:", sorted(list(missing_en)))
print("Missing in TA:", sorted(list(missing_ta)))
