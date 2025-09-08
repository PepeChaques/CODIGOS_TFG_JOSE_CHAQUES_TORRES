import sys 

if len(sys.argv) != 3:
    print("Para usar el script: python3 pcd_to_dat.py archivo_entrada.pcd archivo_salida.dat")
    sys.exit(1)

archivo_entrada= sys.argv[1]
archivo_salida= sys.argv[2]

with open(archivo_entrada,"r") as f_in, open(archivo_salida,"w") as f_out:
    flag_cabecera= True
    for linea in f_in:
        linea= linea.strip()
        if not linea:
            continue

        if flag_cabecera:
            # La cabecera termina en "DATA ascii"
            if linea.startswith( "DATA" ):
                flag_cabecera= False
            continue

        x , y , z , intensidad = linea.split()
        if x=="0" and y=="0" and z=="0":
            continue

        f_out.write(f"{x},{y},{z}\n")