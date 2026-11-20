from pathlib import Path
p = Path("index.html")
s = p.read_text(encoding="utf-8")
old = 'id="sync-note"'
new = 'id="sync-note" style="display:none!important"'
if old not in s:
    raise SystemExit("No se encontró el aviso de sincronización; no se modificó la aplicación")
if new not in s:
    s = s.replace(old, new, 1)
    p.write_text(s, encoding="utf-8")
    print("Aviso técnico oculto sin alterar la sincronización")
else:
    print("Aviso técnico ya oculto")
