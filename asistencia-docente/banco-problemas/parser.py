import sys
import re
from pdfminer.high_level import extract_text

BANCO_PROBLEMAS = [
    ["ESMERALDAS", 89],
    ["BLANCOS", 78],
    ["DORADOS", 56],
    ["PLATA", 89],
    ["VIOLETA", 90]
]

pdf = sys.argv[1]

texto = extract_text(pdf)

regex = re.compile(r'(\d+)\.\s*(UVa|Kattis|Codeforces)\s+([A-Za-z0-9]+)')

banco = 0
problemas = [[] for _ in range(len(BANCO_PROBLEMAS))]
limite = BANCO_PROBLEMAS[banco][1]
agregados = 0

for num, juez, problema in regex.findall(texto):
    problemas[banco].append([int(num), juez, problema])
    agregados += 1
    if agregados >= limite:
        banco += 1
        agregados = 0
        if banco < len(BANCO_PROBLEMAS):
            limite = BANCO_PROBLEMAS[banco][1]

for banco in problemas:
    banco.sort()

print(problemas)
