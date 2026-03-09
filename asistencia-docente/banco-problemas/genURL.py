import sys
import requests
import ast

UVaAPI = "https://uhunt.onlinejudge.org/api/p"

def descargarProblemasUVa():
    r = requests.get(UVaAPI, timeout=30)
    r.raise_for_status()
    data = r.json()
    mapa = {}
    for problema in data:
        pid = problema[0] # ID interno
        num = problema[1] # número UVa
        mapa[num] = pid
    return mapa

PROBLEMAS_UVA = descargarProblemasUVa()

def UVaURL(uvaNum):
    pid = PROBLEMAS_UVA.get(int(uvaNum))
    if pid is None:
        return ""
    return "\\href{" + f"https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem={pid}"+ "}"
    
def KattisURL(nombre):
    return "\\href{" + f"https://open.kattis.com/problems/{nombre}"+ "}"
    
def CodeforcesURL(codigo):
    pos = [i for i, c in enumerate(codigo) if c.isalpha()][0]
    contest = codigo[:pos]
    problema = codigo[pos:]
    return "\\href{" + f"https://codeforces.com/problemset/problem/{contest}/{problema}"+ "}"

JUECES = {
    "Kattis": KattisURL,
    "UVa": UVaURL,
    "Codeforces": CodeforcesURL
}

txtProblemas = sys.argv[1]

with open(txtProblemas) as f:
    PROBLEMAS = ast.literal_eval(f.read())

for banco in PROBLEMAS:
    for num, juez, problema in banco:
        print(JUECES[juez](problema))
