import json

from lib.data.convert import json_to_class, class_to_json
from lib.data.result.character.simple import RCharacter
from lib.path import results_root


def load_character(page_name) -> RCharacter:
    fp = results_root / f"{page_name}.json"
    if fp.exists():
        with open(fp) as f:
            data = json.load(f)
        return json_to_class(data, RCharacter)
    else:
        return RCharacter(page_name=page_name)


def save_character(page_name, data: RCharacter):
    fp = results_root / f"{page_name}.json"
    data = class_to_json(data)
    with open(fp, 'w') as f:
        json.dump(data, f)
