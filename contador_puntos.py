import sys

if len(sys.argv) != 2:
    print("Para usar el script: python3 contarpuntos.py archivo.pcd")
    sys.exit(1)

archivo= sys.argv[1]

num_puntos= 0
num_total= 0

with open(archivo,"r") as f:
    flag_cabecera=False
    for linea in f:

        linea=linea.strip()
        if not linea:
            continue
        if linea.startswith("DATA"):
            flag_cabecera= True
            continue
        if flag_cabecera:
            x, y, z, intensidad= linea.split()
            num_total += 1

            #if float(x) < 7.2 and float(x) > 3.5: #sunapee 232.pcd kayak 2
            #if float(x) < 10 and float(x) > 7.5: #sunapee 232.pcd kayak 1
            #if float(x) < 17 and float(x) > 12: #sunapee 232.pcd kayak 3

            #if float(y) < 4.5 and float(y) > 1.5 and float(x)<10 and float(x)>0 : #sunapee 28.pcd kayak 2
            #if float(y) >5 and float(y) < 10 and float(x)<10 and float(x)>0 : #sunapee 28.pcd kayak 1
            #if float(y) < 4.5 and float(y) > -1 and float(x)<15 and float(x)>10 : #sunapee 28.pcd kayak 3

            #if float(y) < -6.5 and float(y) > -12 and float(x)<48 and float(x)>45 : #mascoma 457.pcd barco 1
            #if float(y) < 12.5 and float(y) > 6.5 and float(x)<33.5 and float(x)>30 : #mascoma 457.pcd barco 2
            #if float(y) < -5.9 and float(y) > -12 and float(x)<-2 and float(x)>-5 : #mascoma 457.pcd barco 3
            #if float(y) < -34 and float(y) > -36 and float(x)<4.2 and float(x)>-0.5 : #mascoma 457.pcd barco 4
            #if float(y) < -21 and float(y) > -26 and float(x)<-5.2 and float(x)>-7.3 : #mascoma 457.pcd barco 5

            #if float(y) < -2 and float(y) > -5.2 and float(x)<-7 and float(x)>-9.5 : #mascoma 206.pcd barca con personas
            #if float(y) < 12 and float(y) > 5 and float(x)<7.5 and float(x)>4.5 : #mascoma 206.pcd barco 1
            #if float(y) < 19.5 and float(y) > 14 and float(x)<-13 #and float(x)>-15 : #mascoma 206.pcd barco 2
            if float(y) < 27.2 and float(y) > 24.5 and float(x)<4.5 and float(x)>-1: #mascoma 206.pcd barco 3
            
                num_puntos += 1
print(f"Archivo: {archivo}")
print(f"Total de puntos: {num_total}")
print(f"Puntos dentro del margen: {num_puntos}")
print(f"Puntos fuera del margen: {num_total - num_puntos}")


