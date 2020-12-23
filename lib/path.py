from pathlib import Path

root_path = Path(__file__).parent.parent
indices_root = root_path / 'data' / 'indices'
lang_root = root_path / 'data' / 'lang'
cv_root = root_path / 'data' / 'cv'

indices_root.mkdir(parents=True, exist_ok=True)
lang_root.mkdir(parents=True, exist_ok=True)
cv_root.mkdir(parents=True, exist_ok=True)
