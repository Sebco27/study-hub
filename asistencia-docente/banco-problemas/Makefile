clean: main.tex
	rm -f salidaParser.txt salidaURL.txt

main.tex: salidaParser.txt salidaURL.txt
	python3 genLaTeX.py salidaParser.txt < salidaURL.txt > main.tex

salidaURL.txt: salidaParser.txt
	python3 genURL.py salidaParser.txt > salidaURL.txt

salidaParser.txt: old-banco.pdf
	python3 parser.py old-banco.pdf > salidaParser.txt
