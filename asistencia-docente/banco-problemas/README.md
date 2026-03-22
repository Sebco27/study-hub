# Banco de problemas

Compilación de problemas de jueces en línea de diferentes categorías:

- Eficiencia (Esmeraldas)
- Backtracking (Blancos)
- Divide and Conquer (Dorados)
- Dynamic Programming (Platas)
- Voraces (Violetas)

Incluye problemas de:

- [UVa](https://onlinejudge.org/)
- [Kattis](https://open.kattis.com/)
- [Codeforces](https://codeforces.com/)

# Scripts de Python

El [banco de problemas original](old-banco.pdf) fue recopilado por el profesor [Eddy Ramírez](https://www.linkedin.com/in/eddy-ramirez-86951130).
Dada la necesidad de pasarlo a formato **LaTeX**, desarrollé los scripts `parser.py`, `genURL.py` y `genLaTeX.py` para automatizar el proceso.

El flujo general es:

1. Extraer los problemas desde el PDF del banco original
2. Generar las URL de cada problema
3. Construir el documento LaTeX

> [!TIP]
> El `Makefile` se encarga de todo el proceso. Para saber cómo usarlo revisa la sección **Extras** al final del README.

## parser.py

Extrae la información de los problemas desde el PDF original.

- Usa `pdfminer` para leer el contenido del archivo.
- Identifica los problemas siguiendo el formato:

  ```
  <número>. <juez> <código>
  ```

- Organiza los problemas por categoría según la cantidad de problemas de cada categoría.
- Genera una estructura de listas de Python.

**Uso:**

```bash
python3 parser.py old-banco.pdf > salidaParser.txt
```

**Salida:**

```python
[
  [[num, juez, problema], [num, juez, problema], ...], # Esmeraldas
  [[num, juez, problema], [num, juez, problema], ...], # Blancos
  ...
]
```

## genURL.py

Genera las URL en formato LaTeX para cada problema usando los datos extraídos por el parser (en el caso de UVa, se utiliza la API de uHunt para obtener la URL).

- Convierte cada problema en un `\href{}{}` listo para usar en LaTeX.

**Uso:**

```bash
python3 genURL.py salidaParser.txt > salidaURL.txt
```

**Salida:**
```bash
\href{https://open.kattis.com/problems/twostones}{Kattis twostones}
\href{https://onlinejudge.org/index.php?option=com_onlinejudge&Itemid=8&page=show_problem&problem=1692}{UVa 10751}
\href{https://codeforces.com/problemset/problem/2125/C}{Codeforces 2125C}
...
```

## genLaTeX.py

Construye el documento LaTeX (`.tex`).

- Necesita:
  - Lista de problemas (`salidaParser.txt`)
  - Las URL (`salidaURL.txt`)

**Uso:**

```bash
python3 genLaTeX.py salidaParser.txt < salidaURL.txt > main.tex
```

**Salida:**

El `.tex` generado no se compila automáticamente. Queda a disposición para ser compilado las veces que se quiera o modificar en caso de que sea necesario.

> [!NOTE]
> El PDF [banco-problemas](banco-problemas.pdf) fue modificado manualmente (y compilado en [Overleaf](https://www.overleaf.com/)) para añadir color a los encabezados y corregir enlaces que se generaron mal por errores en los nombres del banco original.

## Extras

### header.tex

Archivo de configuración LaTeX que:

- Incluye los paquetes a utilizar
- Define el formato del documento
- Incluye el título y autores del documento

Se importa automáticamente en el `main.tex` generado por el `genLaTeX.py`.

### Makefile

Automatiza las ejecuciones de los scripts:

- Parsear el PDF original
- Generar las URL
- Generar el `.tex`
- Limpiar los archivos auxiliares

**Uso:**

```bash
make
```

**Comandos:**

```bash
clean: main.tex
	rm -f salidaParser.txt salidaURL.txt

main.tex: salidaParser.txt salidaURL.txt
	python3 genLaTeX.py salidaParser.txt < salidaURL.txt > main.tex

salidaURL.txt: salidaParser.txt
	python3 genURL.py salidaParser.txt > salidaURL.txt

salidaParser.txt: old-banco.pdf
	python3 parser.py old-banco.pdf > salidaParser.txt
```
