import json
import re
from typing import Optional, Tuple, List

import mwclient

from lib.data.convert import json_to_class, class_to_json
from lib.data.indices import PageIndex, PageLang, CVInfo, CVCharacter, GenderInfo
from lib.path import indices_root, lang_root, cv_root
from lib.sites import wikipedia_ja
import wikitextparser as wtp

def _cvinfo(doc: wtp.WikiText):
    cv_table = None
    for temp in doc.templates:
        if temp.name.strip() == '声優':
            cv_table = temp
            break
    if cv_table is None:
        return None, None
    gender, birth_year = None, None
    for arg in cv_table.arguments:
        if arg.name.strip() == '性別':
            gender = arg.value
            gender = re.sub(r'<!--.+?-->', '', gender)
            gender = re.sub(r'\[|\]|\s', '', gender)
        elif arg.name.strip() == '生年':
            birth_year = arg.value.strip()
            birth_year = re.sub(r'<!--.+?-->', '', birth_year)
            if birth_year:
                birth_year = int(arg.value.strip())
            else:
                birth_year = None
    if gender == '男性':
        gender = GenderInfo.Male
    elif gender == '女性':
        gender = GenderInfo.Female
    elif gender:
        gender = GenderInfo.Other
    else:
        gender = GenderInfo.Unknown
    return gender, birth_year




def get_page_info(title: str) -> Optional[Tuple[CVInfo, List[PageLang]]]:
    site = wikipedia_ja()
    page = site.pages[title]
    if not page.exists:
        return None
    langs = [PageLang(
        src_lang='ja',
        src_name=title,
        dst_lang=ln,
        dst_name=t,
        source=site.host
    ) for ln, t in page.langlinks()]
    def _on_title(t):
        t = re.sub(r"<ref>.+?<\/ref>", "", t)
        t = re.sub(r'<!--.+?-->', '', t)
        r = re.search(r"\s*\*\s*(?:\[\[(.+?)\|.+?\]\]|\[\[(.+?)\]\]|([^[]+))\s*（(.+)）", t)
        if r is None: return
        a, b, c, n = r.groups()
        return a or b or c, [re.sub(r"\[|\]|\s|\'\'\'", "", x) for x in n.split('、') if not re.match(r"(19|20)\d{2}年", x)]
    text = page.text()
    doc = wtp.parse(text)
    gender, birth_year = _cvinfo(doc)
    l = [
        _on_title(it)
        for tp in doc.templates
        if tp.name.startswith('dl2')
        for arg in tp.arguments
        if arg.positional
        for it in re.findall(r'\n(\*.*)$', arg.value)
    ]
    l = [x for x in l if x is not None]
    chars = [
        CVCharacter(
            name=nm,
            anime=anime,
            source=site.host
        )
        for anime, name_list in l
        for nm in name_list
    ]
    cv = CVInfo(
            name=title,
            source=site.host,
            gender=gender,
            birth_year=birth_year,
            characters=chars
        )
    return cv, langs


def get_lang(title):
    src_fp = indices_root / f'{title}.txt'
    dst_fp = lang_root / f'{title}.txt'
    cv_fp = cv_root / f'{title}.txt'
    if cv_fp.exists():
        with open(cv_fp) as f:
            visited = set([
                json_to_class(json.loads(line), CVInfo).name
                for line in f.readlines()
            ])
    else:
        visited = set()
    with open(src_fp) as src, open(dst_fp, 'a') as dst, open(cv_fp, 'a') as cv_f:
        for line in src.readlines():
            idx = json_to_class(json.loads(line), PageIndex)
            if idx.title in visited:
                continue
            ret = get_page_info(idx.title)
            if ret is None: continue
            cv, langs = ret
            print(title, idx.title)
            json.dump(class_to_json(cv), cv_f, ensure_ascii=False)
            cv_f.write("\n")
            for ln in langs:
                json.dump(class_to_json(ln), dst, ensure_ascii=False)
                dst.write("\n")

def main():
    get_lang('日本の男性声優')
    get_lang('日本の女性声優')
    get_lang('バーチャルYouTuber')
    get_lang('にじさんじ')
    get_lang('Upd8')
    get_lang('ENTUM')
    get_lang('ホロライブプロダクション')
    get_lang('ホロライブ')


if __name__ == '__main__':
    # print(get_page_info('五十嵐優樹'))
    main()
