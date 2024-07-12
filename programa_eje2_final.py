from os import system     #Declaramos que trabajamos en windows 
import csv                      #Declaramos que trabajmamos con excel
def obtener_fichero_calificaciones():    #función para obtener los datos de la planilla excel
    lista = []
    lista_curso = []
    with open(r"C:\Users\svele\OneDrive\Documentos\Fundamentos_Programación\Ev3B\notas_alumnos.csv", "r", newline="") as archivo:
        lector_csv = csv.reader(archivo, delimiter=";") #Excel separa (por defecto)los archivos con ";" por eso es el delimitador de cada dato
        pos = 0
        for linea in lector_csv:
            if pos != 0:
               curso = linea[0].replace(' ','') # Este replace quita los espacios 
               rut    = linea[1].replace(' ','')
               nombre = linea[2].strip()           # Strip vendría siendo otra forma de usar el replace
               nota1 = float(linea[3].replace(',','.')) # Python no utiliza "," para los decimales, por eos los cambiamos por un "."
               nota2 = float(linea[4].replace(',','.'))
               nota3 = float(linea[5].replace(',','.'))
               lista.append({                     #Dentro de la lista que creamos agregamos cada dato correspondiente
                   'curso':curso,
                   'rut':rut,
                   'nombre': nombre,
                   'nota1': nota1,
                   'nota2': nota2,
                   'nota3': nota3,
                   'promedio': round((nota1+nota2+nota3)/3,1), #Esto no está dentro del archivo original, se agrega el promedio para facilitar la realización del código
                })
               if not (curso in lista_curso):
                   lista_curso.append(curso)   
            else:
                pos = 1    
    return lista, lista_curso





def menu_principal():     # Función para crear el menú
    opciones = {
        '1': ('Consultar la  notas y promedio  de  un alumno dado su Rut', visulizar_notas_rut),
        '2': ('Visualizar  alumnos  con  Promedio menor  a  4.0', visualizar_alumnos_4),
        '3': ('Visualizar  alumnos  con  Promedio menor  a  4.0 de un  curso', visualizar_alumnos_4_curso),
        '4': ('Generar archivo alumnos con sus notas y  promedios de un curso', generar_alumnos_curso),
        '5': ('Generar archivo alumnos con los mayores promedios (5 alumnos) por  curso', generar_alumnos_top_curso),
        '6': ('Salir de Programa', salir),
    }

    generar_menu(opciones, '6')

def generar_menu(opciones, opcion_salida):
    opcion = None
    while opcion != opcion_salida:
        system("cls")
        mostrar_menu(opciones)
        opcion = leer_opcion(opciones)
        ejecutar_opcion(opcion, opciones)
        print() # se imprime una línea en blanco para clarificar la salida por pantalla

def mostrar_menu(opciones):
    print('Seleccione una opción:')
    for clave in sorted(opciones):
        print(f' {clave}) {opciones[clave][0]}')

def leer_opcion(opciones):
    while (a := input('Opción: ')) not in opciones:
        print('Opción incorrecta, vuelva a intentarlo.')
    return a

def ejecutar_opcion(opcion, opciones):
    opciones[opcion][1]()


def visulizar_notas_rut():    # Primera función 
    lista,lista_curso = obtener_fichero_calificaciones() # Se llama la función para obtener los datos
    rut_ingreso = input("Ingrese el RUT de alumno ") # Se solicita un dato para poder comparar, puesto que esto se solicita
    for alumnos in lista: # recorre los datos 
        if rut_ingreso ==  alumnos['rut']: # Si ingreso es igual a lo quue se encunetra en la  parte de rut que definimos en el primera función ejecuta:
            print(f"Alumno {alumnos['nombre']} : nota1  {alumnos['nota1']} nota2  {alumnos['nota2']} nota3  {alumnos['nota3']} Promedio {alumnos['promedio']}")
            input() #Esto viene siendo un arreglo(?)

def visualizar_alumnos_4(): # Segunda función 
    lista,lista_curso = obtener_fichero_calificaciones() # Se llama la función para obtener los datos 
    for alumnos in lista: # se recorre la lista 
        if alumnos['promedio'] < 4: # si la iteración es menor a 4 se imprime 
            print(f"Curso {alumnos['curso']} Alumno {alumnos['nombre']} : Promedio {alumnos['promedio']}") # Nota tener cuidado con las comillas dobles y simples
    input()
    

def visualizar_alumnos_4_curso(): # Tercera función 
    lista,lista_curso = obtener_fichero_calificaciones() # Se llama la función para obtener los datos
    valido = False # Creamos una variable y la declaramos como Falsa 
    while not valido: # Mientras valido sea True se agrega: 
        curso_ingreso = input("Ingrese curso a Visualizar ") # Se solicita un dato para poder comparar con los datos del archivo  
        if curso_ingreso in lista_curso: # Si el dato solicitado está en nuestro archivo valido es True 
            valido = True
        else:
            print("Curso no Valido")

    for alumnos in lista: # Se recorre la lista de datos 
        if alumnos['promedio'] < 4 and alumnos['curso'] == curso_ingreso: # Si promedio es menor a 4 y curso es igual a dato ingresado:
            print(f"Curso {alumnos['curso']} Alumno {alumnos['nombre']} : Promedio {alumnos['promedio']}") # Se imprime 
    input()



def generar_alumnos_curso():     # Cuarta Función  
    lista,lista_curso = obtener_fichero_calificaciones() # Se llama a la función para obtener los datos 
    valido = False # Se inicia una variable en falso
    while not valido: # Mientras sea True ejecuta
        curso_ingreso = input("Ingrese curso a Visualizar ") # Pide un dato para comparar 
        if curso_ingreso in lista_curso: # Si está en la lista entonces ejecuta
            valido = True
        else:
            print("Curso no Valido")
    with open(r'salida.csv','w', newline='') as archivo_csv:
        escritor_csv =csv.writer(archivo_csv, delimiter=";")
        escritor_csv.writerow(['Curso','Nombre','Nota1','Nota2','Nota3','Promedio'])
        for alumnos in lista:
            lista_imp = []
            if alumnos['curso'] == curso_ingreso:
               lista_imp.append(alumnos['curso'])
               lista_imp.append(alumnos['nombre'])
               lista_imp.append(alumnos['nota1'])
               lista_imp.append(alumnos['nota2'])
               lista_imp.append(alumnos['nota3'])            
               lista_imp.append(alumnos['promedio'])
               escritor_csv.writerow(lista_imp)


def generar_alumnos_top_curso():
    lista,lista_curso = obtener_fichero_calificaciones()
    with open(r'salida2.csv','w', newline='') as archivo_csv:
        escritor_csv =csv.writer(archivo_csv, delimiter=";")
        escritor_csv.writerow(['Curso','Nombre','Nota1','Nota2','Nota3','Promedio'])
        for curso_ingreso in lista_curso:
            lista_imp2 = []
            for alumnos in lista:
                if alumnos['curso'] == curso_ingreso:
                   lista_imp = []
                   lista_imp.append(alumnos['curso'])
                   lista_imp.append(alumnos['nombre'])
                   lista_imp.append(alumnos['nota1'])
                   lista_imp.append(alumnos['nota2'])
                   lista_imp.append(alumnos['nota3'])            
                   lista_imp.append(alumnos['promedio'])
                   lista_imp2.append(lista_imp) 
            for i in range(5):
                   escritor_csv.writerow(lista_imp2[i])    


def salir():
    print('Saliendo')


menu_principal()
