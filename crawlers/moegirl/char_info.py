import json
import time

from lib.data.convert import class_to_json
from lib.data.indices import PageIndex
from lib.path import indices_root, char_root
from lib.sites import wikipedia_ja, moegirl
import wikitextparser as wtp

from lib.utils.wiki import clean_text

tag_keys = {'本名', '别号', '代号', '种族', '专精', '出身地区', '活动范围', '所属团体', '生日', '血型', '星座', '年龄', '身高', '体重', '声优', '配音', 'CV', '多位声优', '萌点'}

def get_info(title):
    site = moegirl()
    page = site.pages[title]
    tags = {}
    doc = wtp.parse(page.text())
    for temp in doc.templates:
        for arg in temp.arguments:
            k = arg.name.strip()
            if k in tag_keys:
                tags[k] = arg.value.strip()
    categories = [c.name[9:] for c in page.categories()]
    info = {
        'page_title': title,
        'tags': tags,
        'categories': categories
    }
    return info


def crawl(category):
    source_fp = indices_root / f'{category}.txt'
    dest_fp = char_root / f'{category}.txt'
    visited = set()
    if dest_fp.exists():
        with open(dest_fp) as f:
            for line in f.readlines():
                d = json.loads(line)
                visited.add(d['page_title'])
    import traceback
    import requests.exceptions
    with open(source_fp) as sf, open(dest_fp, 'a') as fp:
        for line in sf.readlines():
            title = line.strip()
            if title in visited:
                continue
            print(title)
            while True:
                try:
                    info = get_info(title)
                except requests.exceptions.RequestException:
                    traceback.print_exc()
                    time.sleep(10)
                else:
                    break
            fp.write(json.dumps(info, ensure_ascii=False)+"\n")
            time.sleep(1)

def main():
    crawl('人物')
    # print(get_info('贝尔·克朗尼'))

if __name__ == '__main__':
    main()
