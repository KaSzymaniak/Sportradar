import json
import re
import os

# Odczytnie Json
home_dir = os.path.expanduser("~")
ocr_path = home_dir + "\\Downloads\\DATA. JSON file.json"

with open(ocr_path, encoding='utf-8') as f:
    ocr_data = json.load(f)

# Zebranie tekstu
all_text = ""
for page in ocr_data['pages']:
    for item in page['content']:
        all_text = all_text + item.get('text', '')

# Usunięcie błędów
all_text = re.sub(r',\s*}', '}', all_text)
all_text = re.sub(r',\s*]', ']', all_text)

# Wyodrębnienie czystego JSONa
clean_json = json.loads(all_text[all_text.find('{'):])

# Zapisanie czystego JSONa do pliku
project_dir = os.path.dirname(os.path.abspath(__file__))
clean_path = os.path.join(project_dir, "data.json")

with open(clean_path, 'w', encoding='utf-8') as f:
    json.dump(clean_json, f, indent=2)
