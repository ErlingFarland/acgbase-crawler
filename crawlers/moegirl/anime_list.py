import json

from lib.data.convert import class_to_json
from lib.data.indices import PageIndex
from lib.path import indices_root
from lib.sites import wikipedia_ja, moegirl


def crawl(category):
    target_fp = indices_root / f'{category}.txt'
    site = moegirl()
    with open(target_fp, 'w') as f:
        for p in site.categories[category]:
            title = p.name
            if not title.startswith("Category:"):
                continue
            f.write(f"{title[len('Category:'):]}\n")

def main():
    crawl('日本作品')
    crawl('中国作品')
    crawl('美国作品')
    crawl('日本游戏作品')
    crawl('韩国游戏作品')
    crawl('中国游戏作品')

if __name__ == '__main__':
    main()
