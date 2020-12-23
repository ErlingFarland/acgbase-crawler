import json
import re

from lib.data.convert import class_to_json, json_to_class
from lib.data.indices import PageIndex, PageIndexWithTag
from lib.path import indices_root
from lib.sites import wikipedia_ja, moegirl


def crawl(ftype):
    index_fp = indices_root / f'{ftype}_index.txt'
    target_fp = indices_root / f'{ftype}.txt'
    site = moegirl()
    categories = open(index_fp).read().split()
    with open(target_fp, 'w') as f:
        for cate in categories:
            for p in site.categories[cate]:
                title = p.name
                if title.startswith("Category:"):
                    continue
                print(ftype, cate, title)
                item = PageIndexWithTag(title=title, tag=cate, source=site.host)
                json.dump(class_to_json(item), f)
                f.write("\n")

def main():
    crawl('按肤色分类')
    crawl('按瞳色分类')
    crawl('按发色分类')
    crawl('按发型分类')

if __name__ == '__main__':
    main()
