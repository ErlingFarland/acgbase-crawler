import os
import re
import time
import traceback
from itertools import chain
from typing import Tuple, Optional, List, Dict, Iterable

import mwclient.page

from lib.data.indices import CharacterJAName, AnimeInfo, CharacterZHName, PairedAnimeInfo
from lib.path import indices_root, anime_root
from lib.sites import wikipedia_ja, wikipedia_zh
from lib.utils.json_utils import JSONWriter
from lib.utils.wiki import read_template, clean_text, find_all_templates, to_zhs
import wikitextparser as wtp
from lxml import etree


def merge_from_template(text, temp_name, mapping: Dict[str, List[str]]) -> Dict[str, List[str]]:
    result = {k: [] for k in mapping.keys()}
    all_keys = list(chain(*mapping.values()))
    res = read_template(text, temp_name, all_keys)
    if res is not None:
        for k, keys in mapping.items():
            for kk in keys:
                if res[kk]:
                    result[k].extend(res[kk].split("\n"))
    return result


def get_ja_anime(title) -> Tuple[AnimeInfo, List[CharacterJAName], Optional[str]]:
    site = wikipedia_ja()
    page = site.pages[title]
    while page.redirect:
        page = page.resolve_redirect()
    text = page.text()
    zh_link = dict(page.langlinks()).get('zh')
    temp_manga = merge_from_template(text, 'Infobox animanga/Manga',
                                     dict(author=['作者'], design=['作画'], production=[], music=[]))
    temp_anime = merge_from_template(text, 'Infobox animanga/TVAnime',
                                     dict(author=['原作', '監督', 'シリーズ構成', '脚本'], music=['音楽'], design=['キャラクターデザイン'],
                                          production=['アニメーション制作']))
    info = AnimeInfo(
        page_title=page.page_title,
        name=title,
        country='日本',
        **{
            k: temp_manga[k] + temp_anime[k]
            for k in ['author', 'design', 'music', 'production']
        }
    )
    characters = list(parse_ja_characters(text, _safe_html(site, title), {title}, 1))
    return info, characters, zh_link


def parse_ja_characters(text, full_source, visited, depth) -> Iterable[CharacterJAName]:
    pairs = re.findall(r";\s*(.+?(?:（.+）.*?)?)\n:\s*(?:声|\[\[\s*声優\s*\|\s*声\s*\]\])\s*-\s*(.+?)\n", text)
    for ch, cv_list in pairs:
        other_names = re.search(r"（([^\n]+)）", ch)
        ch = re.sub(r"\{|\}|Visible anchor\s*\||（.+?）", "", ch)
        ch = clean_text(ch).strip()
        if other_names:
            other_names = other_names.group(1).split('、')
        else:
            other_names = []
        cv = clean_text(cv_list)
        yield CharacterJAName(name=ch, cv=cv, other_names=other_names)
    if full_source is None or depth == 0: return
    links = _parse_links_from_html(full_source)
    site = wikipedia_ja()
    for link in links:
        if 'の登場人物' in link and link not in visited and ":" not in link:
            visited.add(link)
            p = site.pages[link]
            while p.redirect:
                print("Redirect", p.page_title)
                p = p.resolve_redirect()
            dt = p.text()
            yield from parse_ja_characters(dt, _safe_html(site, link), visited, depth-1)


def get_zh_anime(title) -> Tuple[AnimeInfo, List[CharacterZHName]]:
    site = wikipedia_zh()
    page = site.pages[title]
    while page.redirect:
        page = page.resolve_redirect()
    text = page.text()
    temp_manga = merge_from_template(to_zhs(text), 'Infobox animanga/Manga',
                                     dict(author=['作者'], design=['作画'], production=[], music=[]))
    temp_anime = merge_from_template(to_zhs(text), 'Infobox animanga/TVAnime',
                                     dict(author=['原作', '导演', '系列构成', '脚本'], music=['音乐'], design=['人物设定', '人物原案'],
                                          production=['动画制作']))
    info = AnimeInfo(
        page_title=page.page_title,
        name=to_zhs(title),
        country='日本',
        **{
            k: list(map(to_zhs, temp_manga[k] + temp_anime[k]))
            for k in ['author', 'design', 'music', 'production']
        }
    )
    characters = list(parse_zh_characters(text, _safe_html(site, title), {title}, 1))
    return info, characters

def parse_zh_characters(text, full_source, visited, depth) -> Iterable[CharacterZHName]:
    pairs = []
    def _resolve_cv(a4, a5):
        if a4 is not None:
            ret = re.search(r"(?:配音員|配音员)：(.+)", a4)
            if ret is not None:
                return ret.group(1)
        if a5 is not None:
            ret = re.search(r"(?:聲優|声优)——日：([^／]+)", a5)
            if ret is not None:
                return ret.group(1)
    rm_visible_anchor = r"\{|\}|Visible anchor\s*\||\(.+?\)"
    for d in find_all_templates(text, 'nihongo', ['1', '2', '3', '4', '5']):
        cv = _resolve_cv(d.get('4'), d.get('5'))
        if d['1'] and d['2']:
            zh_name = re.sub(r"（.+?）", "", d['1']).strip()
            ja_name = re.sub(r"（.+?）", "", d['2']).strip()
            en_name = re.sub(r"（.+?）", "", d['3'] or '').strip()
            zh_name = re.sub(rm_visible_anchor, "", zh_name).strip()
            other_names = [ja_name, en_name]
            other_names = [re.sub(rm_visible_anchor, "", f).strip() for f in other_names if f]
            pairs.append((zh_name, [f for f in other_names if f], cv))
    for n, cv in re.findall(r"\n;(.+?)（聲優：(.+?)\n", text):
        n = re.sub(rm_visible_anchor, "", n).strip()
        n = clean_text(n)
        cv = re.sub(rm_visible_anchor, "", cv).strip()
        cv = clean_text(cv)
        n = to_zhs(n)
        pairs.append((n, [], cv))
    for d in find_all_templates(text, 'Infobox animanga character', ['name', 'japanese', 'english', 'kana', 'romaji', 'voiced by']):
        name = to_zhs(clean_text(d['name']))
        other_names = [clean_text(d[k]) for k in ['japanese', 'english', 'kana', 'romaji'] if d[k]]
        cv = d['voiced by'] or ''
        cv = to_zhs(clean_text(cv))
        cv = '、'.join(cv.split())
        pairs.append((name, other_names, cv))
    for zh_name, other_names, cv_list in pairs:
        if cv_list:
            for cv in clean_text(cv_list).split('、'):
                cv = re.sub(r"（.+?）", "", cv).strip()
                yield CharacterZHName(name=to_zhs(zh_name), cv=to_zhs(cv), other_names=other_names)
        else:
            yield CharacterZHName(name=to_zhs(zh_name), cv=None, other_names=other_names)
    if full_source is None or depth == 0: return
    links = _parse_links_from_html(full_source)
    site = wikipedia_zh()
    for link in links:
        if '角色列表' in to_zhs(link) and link not in visited and ":" not in link:
            visited.add(link)
            p = site.pages[link]
            while p.redirect:
                p = p.resolve_redirect()
            dt = p.text()
            yield from parse_zh_characters(dt, _safe_html(site, link), visited, depth-1)
            break

def crawl(title):
    ja_info, ja_char, zh_link = get_ja_anime(title)
    if zh_link is None:
        zh_info = zh_char = None
    else:
        zh_info, zh_char = get_zh_anime(zh_link)
    info = PairedAnimeInfo(
        ja_characters=ja_char,
        ja_info=ja_info,
        zh_characters=zh_char,
        zh_info=zh_info
    )
    return info


def _safe_crawl(title):
    import requests.exceptions
    while True:
        try:
            ret = crawl(title)
        except requests.exceptions.RequestException:
            traceback.print_exc()
            time.sleep(10)
        else:
            return ret

def _safe_html(site: mwclient.Site, title):
    try:
        result = site.parse(page=title)
    except mwclient.errors.APIError:
        return None
    else:
        r = result.get('text')
        if r is None: return None
        r = r.get('*')
        return r


def _parse_links_from_html(html) -> List[str]:
    return re.findall(r'<a href=".+?" title="(.+?)">', html)

def test():
    info = _safe_crawl('遊☆戯☆王 (アニメ第1作)')
    # info = get_zh_anime('遊戲王 (動畫)')
    print(info)

def main():
    index_file = indices_root / 'アニメ.txt'
    visited_file = indices_root / 'アニメ_visited.txt'
    dst_file = anime_root / 'アニメ.txt'
    visited = set()
    if os.path.exists(visited_file):
        with open(visited_file) as f:
            for line in f.readlines():
                visited.add(line.strip())
    with open(index_file) as src_f, open(visited_file, 'a') as visited_f, open(dst_file, 'a') as dst_f:
        writer = JSONWriter(dst_f)
        for line in src_f.readlines():
            if re.match(r"^:|^[a-zA-Z]{,5}:", line):
                continue
            title = re.sub(r'^Redirect |の登場人物$', '', line)
            title = title.strip()
            title = clean_text(title)
            if title in visited or not title:
                continue
            print(title)
            info = _safe_crawl(title)
            writer.write(info)
            visited_f.write(title+"\n")


if __name__ == '__main__':
    main()
