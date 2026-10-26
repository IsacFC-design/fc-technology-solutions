import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
t = open("template.html").read()
if "[hidden] { display: none !important; }" not in t:
    t = t.replace("* { box-sizing: border-box; }", "* { box-sizing: border-box; }\n[hidden] { display: none !important; }", 1)
    open("template.html","w").write(t)
out = t.replace("{{LOGO}}", open("logo.b64").read()).replace("{{PHOTO}}", open("photo.b64").read())
for k, src in {"BARNARDHOME":"barnardHome","BARNARDSUNAT":"barnardSunat","INVENTORY":"inventory","OMNI":"omni","LINGUA":"lingua","SWEET":"sweet"}.items():
    out = out.replace("{{S_%s}}" % k, open("shot_%s.b64" % src).read())
import json
lg = json.load(open("logos.json"))
out = out.replace("{{LOGOS_JSON}}", json.dumps({k: "data:image/png;base64," + v for k, v in lg.items()}, ensure_ascii=False))
assert "{{" not in out
open("portafolio-vista-previa.html","w").write(out)
print("built", len(out)//1024, "KB")
