import json

from lib.data.convert import class_to_json
from lib.data.indices import PageIndex
from lib.path import indices_root
from lib.sites import wikipedia_ja


def crawl(category):
    target_fp = indices_root / f'{category}.txt'
    site = wikipedia_ja()
    with open(target_fp, 'w') as f:
        for p in site.categories[category]:
            title = p.name
            if title.startswith("Category:"):
                continue
            print(category, title)
            item = PageIndex(title=title, source=site.host)
            json.dump(class_to_json(item), f)
            f.write("\n")

def main():
    # crawl('日本の声優')
    # crawl('日本の男性声優')
    # crawl('日本の女性声優')
    # crawl('バーチャルYouTuber')
    # crawl('にじさんじ')
    # crawl('Upd8')
    # crawl('ENTUM')
    # crawl('ホロライブプロダクション')
    crawl('ホロライブ')

if __name__ == '__main__':
    main()
