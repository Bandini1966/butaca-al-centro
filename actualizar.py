#!/usr/bin/env python3
"""Actualiza el archivo público de publicaciones de Blogger."""
import json
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from html.parser import HTMLParser
import re

class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.chunks=[]
        self.skip=0
    def handle_starttag(self, tag, attrs):
        if tag in ("style","script"): self.skip+=1
    def handle_endtag(self, tag):
        if tag in ("style","script"): self.skip=max(0,self.skip-1)
    def handle_data(self, data):
        if not self.skip: self.chunks.append(data)

def plain(s):
    p=Text()
    p.feed(s or "")
    return re.sub(r"\s+"," "," ".join(p.chunks)).strip()

def fetch(start):
    params=urllib.parse.urlencode({"alt":"json","max-results":100,"start-index":start})
    req=urllib.request.Request("https://butacaalcentro.blogspot.com/feeds/posts/default?"+params,headers={"User-Agent":"Mozilla/5.0"})
    with urllib.request.urlopen(req,timeout=30) as res:
        return json.load(res).get("feed",{}).get("entry",[])

posts=[]
for start in range(1,1002,100):
    entries=fetch(start)
    for e in entries:
        links=[x.get("href","") for x in e.get("link",[]) if x.get("rel")=="alternate"]
        url=next((x for x in links if x.startswith("https://butacaalcentro.blogspot.com/")),None)
        title=e.get("title",{}).get("$t","").strip()
        date=e.get("published",{}).get("$t","")[:10]
        if not (url and title and re.fullmatch(r"\d{4}-\d{2}-\d{2}",date)): continue
        summary=plain(e.get("content",e.get("summary",{})).get("$t",""))
        posts.append({"id":e.get("id",{}).get("$t",url),"t":title,"url":url,"date":date,"s":summary[:500],"r":None,"type":""})
    if len(entries)<100: break

posts.sort(key=lambda p:p["date"],reverse=True)
Path("novedades.json").write_text(json.dumps({"updated_at":datetime.now(timezone.utc).isoformat(),"posts":posts},ensure_ascii=False),encoding="utf-8")
print(f"Actualizadas {len(posts)} publicaciones")
