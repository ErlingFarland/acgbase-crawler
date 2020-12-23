from typing import Optional, List
import re

from lib.data.indices import GenderInfo, CVCharacter, CVInfo, PageIndex
from lib.path import indices_root, cv_root
from lib.sites import moegirl
from lib.utils.json_utils import JSONReader, JSONWriter
from lib.utils.wiki import read_template, clean_text
from zhconv import convert as convert_zh


def get_gender(name, text) -> Optional[GenderInfo]:
    res = re.search(fr"'''{name}'''是.+?(男性|女性).+?。", convert_zh(text, 'zh-CN'), re.I)
    if res is None:
        return None
    g = res.group(1)
    if g == '男性':
        return GenderInfo.Male
    else:
        return GenderInfo.Female


def get_birth_year(text) -> Optional[int]:
    temp = read_template(text, '声优信息', ['生日', '年龄'])
    if temp is not None:
        if temp['生日'] is not None:
            res = re.search(r'(\d{4})年\d+月\d+日', temp['生日'])
            if res is not None:
                return int(res.group(1))
        elif temp['年龄'] is not None:
            temp2 = read_template(temp['年龄'], 'Age', ['1'])
            if temp2 and temp2['1']:
                return int(temp2['1'])



def get_characters(text, source) -> List[CVCharacter]:
    pairs = re.findall(r'\n\s*(?:\*\s*)+(.+?)\s*————+\s*《\s*(.+?)\s*》', text)
    return [
        CVCharacter(
            name=convert_zh(ch, 'zh-CN'),
            anime=convert_zh(clean_text(src), 'zh-CN'),
            source=source
        )
        for char_l, src in pairs
        for ch in clean_text(char_l).split('、')
    ]


def get_page(title) -> CVInfo:
    title = convert_zh(title, 'zh-CN')
    site = moegirl()
    page = site.pages[title]
    text = page.text()
    gender = get_gender(title, text)
    birth_year = get_birth_year(text)
    characters = get_characters(text, site.host)
    return CVInfo(name=title, gender=gender, birth_year=birth_year, characters=characters, source=site.host)


def main():
    with open(indices_root / '声优.txt') as f, open(cv_root / '声优.txt', 'w') as target:
        writer = JSONWriter(target)
        for it in JSONReader(f, PageIndex):
            info = get_page(it.title)
            print(info)
            writer.write(info)


if __name__ == '__main__':
    main()
