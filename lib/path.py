from pathlib import Path

root_path = Path(__file__).parent.parent
indices_root = root_path / 'data' / 'indices'
lang_root = root_path / 'data' / 'lang'
cv_root = root_path / 'data' / 'cv'
anime_root = root_path / 'data' / 'anime'
char_root = root_path / 'data' / 'character'
results_root = root_path / 'data' / 'results'

indices_root.mkdir(parents=True, exist_ok=True)
lang_root.mkdir(parents=True, exist_ok=True)
cv_root.mkdir(parents=True, exist_ok=True)
anime_root.mkdir(parents=True, exist_ok=True)
results_root.mkdir(parents=True, exist_ok=True)
