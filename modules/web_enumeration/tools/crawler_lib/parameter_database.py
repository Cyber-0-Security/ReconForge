"""
ReconForge Parameter Intelligence Database

Includes the top25-parameter wordlists
(https://github.com/lutfumertceylan/top25-parameter) merged in
alongside the original entries.
"""

PARAMETER_DATABASE = {
    "action": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "arg": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "begindate": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "board": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "callback": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "cat": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "category": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "categoryid": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "checkout_url": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "class": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "cmd": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "code": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "command": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "conf": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "content": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "continue": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'SSRF'],
    },
    "data": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "date": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'SQL Injection'],
    },
    "dest": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'SSRF'],
    },
    "destination": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "detail": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "dir": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'SQL Injection', 'SSRF'],
    },
    "do": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "doc": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "document": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "domain": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "download": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "email": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "enddate": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "exe": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "exec": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "execute": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "feature": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "feed": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "file": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'SQL Injection'],
    },
    "folder": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "form": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "func": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "function": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "go": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "host": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "html": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "id": {
        "severity": "HIGH",
        "categories": ['Reflected XSS', 'SQL Injection'],
    },
    "image": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "image_url": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "inc": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "include": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "item": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "join": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "jump": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "key": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "keyword": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "keywords": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "lang": {
        "severity": "HIGH",
        "categories": ['Reflected XSS', 'SQL Injection'],
    },
    "layout": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "list_type": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "load": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "locate": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "login": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "main": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "menu": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "mod": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "module": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "month": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "name": {
        "severity": "HIGH",
        "categories": ['Reflected XSS', 'SQL Injection'],
    },
    "nav": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "news": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "next": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'SSRF'],
    },
    "option": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "out": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "p": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "page": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'Reflected XSS', 'SQL Injection', 'SSRF'],
    },
    "path": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'SSRF'],
    },
    "payload": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "ping": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "port": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "prefix": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "print": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "process": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "q": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "query": {
        "severity": "HIGH",
        "categories": ['Reflected XSS', 'Remote Code Execution'],
    },
    "read": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "redir": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "redirect": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'SSRF'],
    },
    "redirect_uri": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "redirect_url": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "ref": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "reference": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "reg": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "region": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "req": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "return": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'SSRF'],
    },
    "return_path": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "return_to": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "returnto": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "run": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "rurl": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "s": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "search": {
        "severity": "HIGH",
        "categories": ['Reflected XSS', 'SQL Injection'],
    },
    "show": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion'],
    },
    "site": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'SSRF'],
    },
    "step": {
        "severity": "HIGH",
        "categories": ['Remote Code Execution'],
    },
    "target": {
        "severity": "HIGH",
        "categories": ['Open Redirect'],
    },
    "terms": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
    "thread": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "title": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "to": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'SSRF'],
    },
    "topic": {
        "severity": "HIGH",
        "categories": ['SQL Injection'],
    },
    "type": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'Reflected XSS', 'SQL Injection'],
    },
    "uri": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "url": {
        "severity": "HIGH",
        "categories": ['Open Redirect', 'Reflected XSS', 'SQL Injection', 'SSRF'],
    },
    "val": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "validate": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "view": {
        "severity": "HIGH",
        "categories": ['Local File Inclusion', 'Open Redirect', 'Reflected XSS', 'SQL Injection', 'SSRF'],
    },
    "window": {
        "severity": "HIGH",
        "categories": ['SSRF'],
    },
    "year": {
        "severity": "MEDIUM",
        "categories": ['Reflected XSS'],
    },
}
