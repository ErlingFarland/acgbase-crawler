from typing import List, Optional, Dict, Iterable
import wikitextparser as wtp
import zhconv
from wikitextparser import remove_markup


def read_template(text: str, template_name: str, keys: List[str]) -> Optional[Dict[str, Optional[str]]]:
    doc = wtp.parse(text)
    target_template = None
    for temp in doc.templates:
        if temp.name.strip() == template_name:
            target_template = temp
            break
    if target_template is None:
        return None
    result = {k: None for k in keys}
    for arg in target_template.arguments:
        key = arg.name.strip()
        if key in result:
            result[key] = clean_text(arg.value.strip())
    return result

def find_all_templates(text: str, template_name: str, keys: List[str]) -> Iterable[Dict[str, Optional[str]]]:
    doc = wtp.parse(text)
    for temp in doc.templates:
        if temp.name.strip() == template_name:
            result = {k: None for k in keys}
            for arg in temp.arguments:
                key = arg.name.strip()
                if key in result:
                    result[key] = clean_text(arg.value.strip())
            yield result


def clean_text(text):
    if not text:
        return text
    doc = wtp.parse(text)
    for link in doc.wikilinks:
        if not link.title.startswith('File:') and not link.title.startswith("ファイル:") :
            link.text = link.title
    for ref in doc.get_tags('ref'):
        if ref.contents:
            ref.contents = ''
    return doc.plain_text()


def to_zhs(text):
    return zhconv.convert(text, 'zh-cn')
