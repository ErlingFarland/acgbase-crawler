import re

from lib.data.indices import CVInfo
from lib.path import cv_root, indices_root
from lib.utils.json_utils import JSONReader


def get_anime():
    animes = set()
    for title in ["日本の女性声優", "日本の男性声優"]:
        src = cv_root/f'{title}.txt'
        with open(src) as f:
            for cv in JSONReader(f, CVInfo):
                for char in cv.characters:
                    name = char.anime
                    name = re.sub('#.+$', '', name)
                    if '{{' in name or '}}' in name:
                        continue
                    animes.add(name)
    return animes


def main():
    animes = get_anime()
    dst = indices_root / 'アニメ.txt'
    with open(dst, 'w') as f:
        for a in animes:
            f.write(a+"\n")

if __name__ == '__main__':
    main()
