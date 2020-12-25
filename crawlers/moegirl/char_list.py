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
            if title.startswith("Category:"):
                continue
            print(category, title)
            f.write(title+"\n")

def main():
    crawl('人物')

if __name__ == '__main__':
    main()
