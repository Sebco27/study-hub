import sys
import ast

BANCO_PROBLEMAS = [
    ["ESMERALDAS", 89],
    ["BLANCOS", 78],
    ["DORADOS", 56],
    ["PLATA", 89],
    ["VIOLETA", 90]
]

INICIO = r"""\input{header}
\begin{document}
\maketitle
\tableofcontents"""

FIN = r"\end{document}"

LABS = [
    r"Lab 1 - Esmeraldas (eficiencia)",
    r"Lab 2 - Blancos (Backtracking)",
    r"Lab 3 - Dorados (D\&C)",
    r"Lab 4 -  Plata (DP)",
    r"Lab 5 -  Violeta (voraces)"
]

txtProblemas = sys.argv[1]

with open(txtProblemas) as f:
    PROBLEMAS = ast.literal_eval(f.read())

print(INICIO)
for i in range(len(PROBLEMAS)):
    print(rf"""\section{{{LABS[i]}}}
        \begin{{enumerate}}""")
    for num, juez, problema in PROBLEMAS[i]:
        url = sys.stdin.readline().strip()
        print(rf"\item {url}{{{juez} {problema}}}")
    print(r"\end{enumerate}")
print(FIN)