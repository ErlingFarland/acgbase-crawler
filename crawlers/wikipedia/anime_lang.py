import re
from itertools import product
from typing import Optional, Iterable

from lib.data.indices import PairedAnimeInfo, PageLang
from lib.path import anime_root, lang_root
from lib.utils.json_utils import JSONReader, JSONWriter
from lib.utils.wiki import to_zhs

src_lang = 'ja'
dst_lang = 'zh'
source = 'ja.wikipedia.org'


def pair_anime_lang(info: PairedAnimeInfo) -> Optional[PageLang]:
    if info.ja_info is None or info.zh_info is None:
        return None
    ja_title = info.ja_info.page_title or info.ja_info.name
    zh_title = info.zh_info.page_title or info.zh_info.name
    if not ja_title or not zh_title:
        return None
    zh_title = to_zhs(zh_title)
    return PageLang(
        src_lang=src_lang, dst_lang=dst_lang,
        src_name=ja_title, dst_name=zh_title,
        source=source
    )


def pair_character_names(info: PairedAnimeInfo) -> Iterable[PageLang]:
    if not info.ja_characters or not info.zh_characters:
        return
    def replace(pattern, text):
        res = re.search(pattern, text)
        if res:
            return res.group(1)
        else:
            return text
    stop_words = {'Anchor'}
    print(info.ja_characters)
    for ja, zh in product(info.ja_characters, info.zh_characters):
        ja_name = ja.name
        ja_name = replace(r"^(?:Anchor\|)?([^|]+?)\|(?:.+?)$", ja_name)
        ja_name = ja_name.replace(" ", "")

        zh_name = to_zhs(zh.name).replace(' ', '')

        ja_names = set(ja.other_names) | {ja_name}
        ja_names = {n for nm in ja_names for n in re.split(r"[|、]", nm) if n not in stop_words}
        zh_names = set(zh.other_names)
        if ja_names & zh_names:
            yield PageLang(
                src_lang=src_lang, dst_lang=dst_lang, source=source,
                src_name=ja_name, dst_name=zh_name
            )


def main():
    anime_fp = anime_root / 'アニメ.txt'
    lang_anime_fp = lang_root / 'アニメ_anime.txt'
    lang_char_fp = lang_root / 'アニメ_characters.txt'
    with open(anime_fp) as src_f, open(lang_anime_fp, 'w') as anime_f, open(lang_char_fp, 'w') as char_f:
        src = JSONReader(src_f, PairedAnimeInfo)
        # anime_dst = JSONWriter(anime_f)
        # char_dst = JSONWriter(char_f)
        for anime in src:
            info = pair_anime_lang(anime)
            if not info or 'ソードアート・オンライン' not in info.src_name:
                continue
            if info:
                print('A:', info.src_name, info.dst_name)
                # anime_dst.write(info)
            for character in pair_character_names(anime):
                print('\tC:', character.src_name, character.dst_name)
                # char_dst.write(character)
            break


if __name__ == '__main__':
    main()
