import os.path
import copy
import numpy as np
import random

def leerDiccionario():
    # leer archivo txt con las definiciones
    try:
        ruta = os.path.abspath("diccionario.txt")
        with open(ruta, "r", encoding="utf-8") as f:
            contents = f.readlines()
            diccionario=[]
            for row in contents:
                fila=[]
                palabra=""
                definicion=""
                #separar palabras y su definicion
                for pos, letra in enumerate(row):
                    if letra==":":
                        c=pos
                for pos, letra in enumerate(row):
                    if pos < c:
                        letra=letra.capitalize()
                        if letra=="Á":
                            letra="A"
                        elif letra=="É":
                            letra="E"
                        elif letra=="Í":
                            letra="I"
                        elif letra=="Ó":
                            letra="O"
                        elif letra=="Ú":
                            letra="U"
                        palabra+=letra
                    else:
                        definicion+=letra
                #eliminar ": " y \n de la definicion leida
                definicion=definicion[2:]
                definicion=definicion[:-1]
                fila.append(palabra) #primer columna: palabra
                fila.append(definicion) #segunda columna: defincion
                fila.append(len(palabra)) #tercer columna: longitud de palabra
                fila.append(0) #cuarta columna: poisicion en tablero; 
                            #0=no esta, 1=horizontal, 2=vertical
                #las siguientes columnas indican en donde fue insertada la palabra, mientras no ocurra, sera -1
                fila.append(-1) #inicio en renglon
                fila.append(-1) #termino en renglon
                fila.append(-1) #inicio en columna
                fila.append(-1) #termino en columna
                diccionario.append(fila)
        #ordenar el diccionario aleatoriamente
        diccionarioord=[]
        a=0
        while a<len(diccionario):
            b=random.choice(diccionario)
            if b not in diccionarioord:
                diccionarioord.append(b)
                a+=1
            else:
                pass
    except FileNotFoundError:
        return ruta
    return diccionarioord

def crearMatriz(n):
    # crear matriz vacia de tamaño entre 10 y 15 
    size = n 
    print("Generando árbol tamaño: ",size,"x",size,"...")
    #time.sleep(1)
    matriz = np.empty((size, size),str)
    matriz[matriz==""] = " "
    return matriz 

def buscarInterseccion(crucigrama, buscarpalabra, intersecciones):
    coincidencias=[]
    posicion=[]
    for letrap in buscarpalabra:
        row=0
        for fila in crucigrama:
            col=0
            for letraf in fila:
                entrada=[]
                #validar que esa interseccion no este ocupada
                if letraf==letrap and [row,col] not in intersecciones:
                    entrada.append(row)
                    entrada.append(col)
                    coincidencias.append(entrada)
                    posicion.append(buscarpalabra.index(letrap))
                col+=1
            row+=1
    return posicion, coincidencias #posicion de letra en la palabra y posicion del tablero (fila,col)

def calcularCuadrosVacios(crucigrama):
    count=0
    for row in range(len(crucigrama)):
        for col in range(len(crucigrama)):
            if crucigrama[row][col]==' ':
                count+=1
    return count/(len(crucigrama)*len(crucigrama))*100

def comparar(verifpos,diccionario,crucigrama,pos,row,col,i,fila,intersecciones,listapalabras,nodo):
    m,j=0,0
    comparar=[]
    palabra=[]
    for letra in (diccionario[i][0]):
        if verifpos==1:
            x1,x2=m-pos,0
        elif verifpos==2:
            x1,x2=0,m-pos
        #agregar casillas donde intersecta a un vector para compararlo con la palabra real
        if crucigrama[row+x1][col+x2] == letra:
            comparar.append(letra)
        elif crucigrama[row+x1][col+x2] == ' ':        
            comparar.append(' ')
        palabra.append(crucigrama[row+x1][col+x2])                           
        m+=1       
    if palabra == comparar:
        #si son iguales se agregara al tablero
        for letra in (diccionario[i][0]):  
            if verifpos==1:   
                y1,y2= j-pos,0 
            elif verifpos==2:
                y1,y2=0,j-pos       
            crucigrama[row+y1][col+y2]=letra
            j+=1                      
        fila.append(row)
        fila.append(col)
        intersecciones.append(fila)
        listapalabras.append(diccionario[i][0])
        cuadrosvacios=calcularCuadrosVacios(crucigrama)
        if verifpos==1:
            z1,z2,z3,z4,z5=2,row-pos,col,row -pos+ len(diccionario[i][0]),col
            diccionario[i][3] = z1                          #orientacion de la
            diccionario[i][4] = z2                          #inicio renglon
            diccionario[i][6] = z3                          #inicio columna
            diccionario[i][5] = z4                          #fin renglon
            diccionario[i][7] = z5    
        elif verifpos==2:
            z1,z2,z3,z4,z5=1,row,col-pos,row,col-pos+len(diccionario[i][0])
            diccionario[i][3] = z1                          #orientacion de la
            diccionario[i][4] = z2                          #inicio renglon
            diccionario[i][6] = z3                          #inicio columna
            diccionario[i][5] = z4                          #fin renglon
            diccionario[i][7] = z5    
        nodo.append(cuadrosvacios)
        nodo.append(len(listapalabras))
        nodo.append(copy.deepcopy(crucigrama))
        nodo.append(diccionario)
    else:
        nodo=[]    
    return diccionario,crucigrama,intersecciones,listapalabras,nodo      

def dfs(criterio,visit, arbol, nodo):
    if nodo not in visit:
        visit.append(nodo)
        criterio.append(nodo)
        for rama in arbol:
            for hijo in rama:
                for nodo in hijo:
                    dfs(criterio,visit, arbol, nodo)

def evaluar(arbol):
    #medida de performance: minimizar % de cuadros vacios (>=20%) y max cant de palabras
    x=[[[-rama[0]+rama[1]] for rama in hijo]for hijo in arbol]
    y=[[[rama[0]] for rama in hijo]for hijo in arbol]
    criterio1=[]
    criterio2=[]
    visit=[]
    aux2,aux1,a,b=[],[],0,0
    mayores=[]
    max=-100
    #buscar los nodos que cumplan con los criterios mencionados
    dfs(criterio1,visit, x, max)
    visit=[]
    dfs(criterio2,visit,y,100)
     
    for hijo in arbol:
        for rama in hijo:
            if rama[0]==criterio2[a]:
                aux2.append(criterio2[a])
                a+=1
            else:
                aux2.append(-1)
            if -rama[0]+rama[1]==criterio1[b]:
                aux1.append(criterio1[b])
                b+=1
            else:
                aux1.append(-100)
    criterio1=aux1
    criterio2=aux2
    #evaluar lista creada con los nodos encontrados
    for i in range(len(criterio2)):
        if criterio2[i]>=20 and criterio2[i]<30:
            mayores.append(criterio2.index(criterio2[i]))
    for i in mayores:
        if criterio1[i]>max:
            max=criterio1[i]
    for hijo in arbol:
        for rama in hijo:
            if -rama[0]+rama[1]==max: #sumar la cantidad de palabras y restar el porcentaje; el maximo es la mejor solucion
                return rama

def crearCrucigrama(): 
    n=10
    arbol=[]
    #se crearan crucigramas de tamaños 10 a 15 (5 hijos) cada uno con sus hijos que surgan de las iteraciones
    while n<=15:
        hijo=[]
        diccionario = leerDiccionario()
        if type(diccionario)==str:
            print("Archivo no encontrado en",diccionario)
            cerrar = input("\nPresione enter para salir.")
            print ("Saliendo...")
            quit()
        crucigrama = crearMatriz(n) 
        intersecciones=[]
        listapalabras=[]
        verifpos=0
        it=0
        for i in range(len(diccionario)):
            nodo=[]
            #verificar si la palabra cabe en el tablero del crucigrama
            if diccionario[i][2] <= len(crucigrama):
                #llenar primer palabra en la esquina superior izquierda
                if it==0: 
                    j=0
                    #llenar atributos del nodo raiz (crucigrama vacio)
                    cuadrosvacios=calcularCuadrosVacios(crucigrama)
                    nodo.append(cuadrosvacios)
                    nodo.append(len(listapalabras))
                    nodo.append(copy.deepcopy(crucigrama))
                    nodo.append(diccionario)
                    hijo.append(copy.deepcopy(nodo))
                    #llenar atributos de los primeros 5 hijos  
                    nodo=[]
                    for letra in diccionario[i][0]:
                        crucigrama[j][it] = letra
                        j+=1
                    cuadrosvacios=calcularCuadrosVacios(crucigrama)
                    listapalabras.append(diccionario[i][0])
                    diccionario[i][3] = 2                           #vertical
                    diccionario[i][4] = 0                           #inicio renglon
                    diccionario[i][6] = 0                           #inicio columna
                    diccionario[i][5] = 0 + len(diccionario[i][0])  #fin renglon
                    diccionario[i][7] = 0                           #fin columna
                    nodo.append(cuadrosvacios)
                    nodo.append(len(listapalabras))
                    nodo.append(copy.deepcopy(crucigrama))
                    nodo.append(diccionario)
                #llenar siguientes palabras
                if it>0:
                    #obtenemos interseccion y posicion de donde intersecta
                    posicion,coincidencias=buscarInterseccion(crucigrama,diccionario[i][0], intersecciones)
                    for c in range(len(coincidencias)):
                        pos=posicion[c]
                        row=coincidencias[c][0]
                        col=coincidencias[c][1]
                        for p in range(len(diccionario)):
                            #buscar con que palabra intersecta
                            if diccionario[p][3]!=0 and diccionario[p][4]<= row and diccionario[p][5] >= row and diccionario[p][6]<=col and diccionario[p][7]>=col :
                                verifpos=diccionario[p][3] #1 = la palabra con la que intersecta es horizontal, 2 si es vertical
                        fila=[]
                        #si donde intersecta es horizontal y si la palabra a insertar cabe desde arriba o no se sale  del tablero
                        if verifpos==1 and pos<=row and row+len(diccionario[i][0])-pos<=len(crucigrama) and diccionario[i][0] not in listapalabras:
                            diccionario,crucigrama,intersecciones,listapalabras,nodo=comparar(verifpos,diccionario,crucigrama,pos,row,col,i,fila,intersecciones,listapalabras,nodo)
                        #si donde intersecta es vertical y si la palabra a insertar cabe desde la izquierda o no se sale  del tablero
                        elif verifpos==2 and pos<=col and col+len(diccionario[i][0])-pos<=len(crucigrama) and diccionario[i][0] not in listapalabras:
                            #llenar horizontal
                            diccionario,crucigrama,intersecciones,listapalabras,nodo=comparar(verifpos,diccionario,crucigrama,pos,row,col,i,fila,intersecciones,listapalabras,nodo)
                        else:
                            pass
                it+=1
                if nodo!=[]:
                    hijo.append(copy.deepcopy(nodo))
            else:
                pass
        if hijo!=[]:
            arbol.append(copy.deepcopy(hijo))
        n+=1 
    
    cuadrosvacios,cantidaddepalabras,crucigrama,diccionario=evaluar(arbol)
    imprimirCrucigrama(diccionario,crucigrama,cuadrosvacios)
                    
def imprimirCrucigrama(diccionario,crucigrama,cuadrosvacios):
    print("\n\n\n\t  *****  C R U C I G R A M A  D E  B I O L O G Í A  Y  F Í S I C A  *****\n")
    nuevamatriz=[]   
    #asignar un numero para poder relacionar la defincion con la casilla correspondiente
    verticales=[]
    horizontales=[]
    numeracionh=[]
    numeracionv=[]
    for i in range(len(crucigrama)*2):
        for j in range(len(crucigrama)*2):
            for k in range(len(diccionario)):
                sub=[]
                if diccionario[k][4]*2 == i  and diccionario[k][6]*2 == j:
                    if diccionario[k][3]==1:
                        sub.append(diccionario[k][4]*2)
                        sub.append(diccionario[k][6]*2)
                        horizontales.append(diccionario[k][0])
                        numeracionh.append(sub)
                    else:
                        sub.append(diccionario[k][4]*2)
                        sub.append(diccionario[k][6]*2)
                        verticales.append(diccionario[k][0])
                        numeracionv.append(sub)
    for i in range(len(crucigrama)*2+1):
        fila=[]
        for j in range(len(crucigrama)*2+1):
            if i%2==0:
                if j%2!=0:
                    if [i,j-1] in numeracionv:
                        for k in range(len(diccionario)):
                            if diccionario[k][4]==i//2 and diccionario[k][6]==j//2:
                                if diccionario[k][0] not in verticales:
                                    continue
                                else:
                                    break
                        if len(str(verticales.index(diccionario[k][0])+1))>1:
                            fila.append(' '+str(verticales.index(diccionario[k][0])+1))
                        else:
                            fila.append(' '+str(verticales.index(diccionario[k][0])+1)+' ')
                    else:
                        fila.append('___')
                else:
                    if j!=len(crucigrama)*2:
                        fila.append('|__')   
                    else:
                        fila.append('|')
                               
            else:
                if j%2==0:
                    if [i-1,j] in numeracionh:
                        for k in range(len(diccionario)):
                            if diccionario[k][4]==i//2 and diccionario[k][6]==j//2:
                                if diccionario[k][0] not in horizontales:
                                    continue
                                else:
                                    break
                        if len(str(horizontales.index(diccionario[k][0])+1))>1:
                            fila.append('|'+str(horizontales.index(diccionario[k][0])+1))#
                        else:
                            fila.append('|'+str(horizontales.index(diccionario[k][0])+1)+' ')#" "+str()
                    else:
                        fila.append('|  ')
                else:
                    fila.append(" "+crucigrama[i//2][j//2]+" ")
        nuevamatriz.append(fila)

    imp = ""
    for fila in range(len(nuevamatriz)):
        for col in range(len(nuevamatriz)):
            imp += str(nuevamatriz[fila][col])
            #imp += " "
        imp += "\n"
    print(imp)
    print("\nCuadros vacíos: ", format(cuadrosvacios, "0.2f"),"%")
    print("\nHorizontales.")
    for i in range(len(horizontales)):
        for k in range(len(diccionario)):
            if diccionario[k][0]==horizontales[i]:
                break
        print('\t'+str(i+1)+". ",diccionario[k][1])
    print("Verticales.")
    for i in range(len(verticales)):
        for k in range(len(diccionario)):
            if diccionario[k][0]==verticales[i]:
                break
        print('\t'+str(i+1)+". ",diccionario[k][1])
    cerrar = input("\nPresione enter para salir.")
    print ("Saliendo...")

crearCrucigrama()




