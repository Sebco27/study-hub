#!/usr/bin/env bash

# =====================================================================
# Script para evaluar laboratorios
# =====================================================================

# Variables Globales

TIME_LIMIT="5s" # Cambia con cada lab

# Definir rutas
F="Files" # Carpeta con los entregables (zip) y binarios por estudiante
I="Inputs" # Entradas (.txt) para ejecutable
E="Expecteds" # Salidas esperadas por cada ejecutable
O="Outputs" # Salidas producidas por cada estudiante

# Definir colores
R='\033[1;31m' # Códigos ANSI de color Rojo
G='\033[1;32m' # Códigos ANSI de color Verde
B='\033[1;36m' # Códigos ANSI de color Azul
Y='\033[1;33m' # Códigos ANSI de color Amarillo
NC='\033[0m' # Sin color

echo -e "${B}===== Iniciando prueba de ejecución =====${NC}"

echo -e "${Y}Descomprimiendo todos los archivos...${NC}"

for file in $F/*.zip; do # Bucle: itera sobre cada .zip en $F
  [ -e "$file" ] || continue # Si no hay zips salta la iteración
  dir="${file%.zip}" # `dir` = nombre de carpeta destino
  echo -e "${G}  ->${NC} Descomprimiendo $file"
  mkdir -p "$dir" # Crea el directorio de descompresión (-p evita error si ya existe)
  unzip -oq "$file" -d "$dir" # Descompresión de entregables
done

echo -e "${G}Todos los archivos se descomprimieron${NC}"

echo -e "${Y}Compilando todos los .cpp...${NC}"

for dir in $F/*; do # Compilar y crear .txt
  [ -d "$dir" ] || continue # Solo procesa entradas que sean directorios
  fileName=$(basename "$dir")
  studentName=($(echo "$fileName" | grep -o '[A-Z][a-z]*')) # Separa el nombre y los apellidos
  echo -e "${G}  -> ${NC}Compilando los .cpp de ${studentName[2]} ${studentName[0]}"
  make -s -C $dir
  echo "${studentName[2]} ${studentName[0]} ${studentName[1]}" > "$dir/$fileName.txt"
done

echo -e "${G}Todos los .cpp se compilaron${NC}"

echo -e "${Y}Realizando test individuales...${NC}"

rm -rf "$O"/* # Limpiamos la carpeta de Outputs

for dir in $F/*; do # Ejecutar los ejecutables
  [ -d "$dir" ] || continue
  studentName=$(basename "$dir") # Extrae nombre del estudiante a partir de la ruta del directorio actual
  reportFile="$dir/$studentName.txt" # Archivo de reporte por estudiante
  echo "Resultados de pruebas:" >> "$reportFile"
  
  for exe in $dir/L*; do # Itera sobre ejecutables en el directorio de cada estudiante
    [ -x "$exe" ] || continue # Solo corre binarios marcados como ejecutables
    exeName=$(basename "$exe") # Nombre lógico del ejercicio que se usa para localizar Inputs/Expecteds
    echo "$exeName:" >> "$reportFile"
    buenas=0
    malas=0
    total=0
	
    for inputFile in $I/$exeName/*.txt; do # Itera sobre todos los casos de prueba
      [ -e "$inputFile" ] || continue
      fileName=$(basename "$inputFile" .txt)
      expectedFile="$E/$exeName/$fileName.txt"
      mkdir -p "$O/$studentName/$exeName" # Crea el directorio para guardar los resultados de ejecución
      outputFile="$O/$studentName/$exeName/$fileName.txt" # Crea el archivo para guardar los resultados de ejecución
      timeout -k 2s "$TIME_LIMIT" ./"$exe" < "$inputFile" > /dev/null 2>&1 # Ejecuta y mata si excede el tiempo límite
      ec=$? # Captura el exit status del último comando
# Valores de interés: 124 = timeout; 137 = terminó por SIGKILL (128+9).
      if [ "$ec" -eq 124 ] || [ "$ec" -eq 137 ]; then
        echo -e "${R}  ⏱ Timeout a los $TIME_LIMIT ${NC}"
        echo "$fileName: ⏱ Timeout ($TIME_LIMIT)" >> "$reportFile"
		((malas++))
      else
		    runtime=$( { time ./"$exe" < "$inputFile" > "$outputFile"; } 2>&1 ) # Se vuelve a ejecutar el binario sin timeout para medir tiempos
		    if diff -qZ "$outputFile" "$expectedFile"; then # Compara en modo silencioso (`-q`) la salida producida contra la esperada
		      echo "$outputFile"
		      echo -e "${G}  ✔ OK ✔${NC}"
		      echo -n "$fileName: OK" >> "$reportFile"
		      ((buenas++))
		    else
		      echo -e "${R}  X Diferencias encontradas X${NC}"
		      echo -n "$fileName: X Diferencias encontradas X" >> "$reportFile"
		    ((malas++))
		    fi
		    echo "$runtime" >> "$reportFile" # Agrega el runtime al reporte.
      fi
	  ((total++))
    done
	echo -e "----------\nBuenas: $buenas\nMalas: $malas\nTotal: $total\n----------" >> "$reportFile"
  done
done

echo -e "${G}Todos los test individuales terminaron${NC}"

echo -e "${B}===== Prueba de ejecución finalizada =====${NC}"
