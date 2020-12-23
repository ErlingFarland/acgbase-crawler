from functools import lru_cache

import mwclient


@lru_cache(1)
def wikipedia_ja() -> mwclient.Site:
    site = mwclient.Site('ja.wikipedia.org')
    return site

@lru_cache(1)
def wikipedia_zh() -> mwclient.Site:
    site = mwclient.Site('zh.wikipedia.org')
    return site

@lru_cache(1)
def moegirl() -> mwclient.Site:
    site = mwclient.Site('zh.moegirl.org.cn', path='/')
    return site
