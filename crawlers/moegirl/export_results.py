from functools import lru_cache

from lib.data.indices import PageIndex
from lib.path import indices_root
from lib.utils.json_utils import JSONReader


@lru_cache(1)
def animes():
    return set(
        line.strip()
        for nm in ['中国作品', '中国游戏作品', '日本作品', '日本游戏作品', '美国作品']
        for line in open(indices_root / f"{nm}.txt").readlines()
    )

@lru_cache(1)
def cv_set():
    return set(
        idx.title
        for idx in JSONReader(open(indices_root / "声优.txt"), PageIndex)
    )

def get_character():
    pass

def main():
    pass


if __name__ == '__main__':
    main()
