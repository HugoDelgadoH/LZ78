"""Información General del Programa:
Autor: Hugo Delgado de las Heras
Versión: 16/11/2020
Descripción: Algoritmo de compresión LZ78 con codificador de longitud variable
"""

#importaciones globales
from bitarray import bitarray

#Variables globales: tamaño inicial de lectura y tamaño máximo
INITBIT=2
MAXBIT=12

#Compresión

"""leerFichero()
Abre el fichero en la ruta dada y lo copia en una variable de tipo String
@return Variable que contiene la información del documento de texto leido
"""
def leerFichero():
    ruta=input("Defina la ruta del archivo que desea comprimir: ")
    
    f=open(ruta,encoding='utf-8')
    Documento=f.read()
    f.close()
    
    return (Documento)

"""escribirFichero(Doc)
Escribe en la ruta dada, un fichero binario con el contenido de la compresión
@param Doc variable de tipo bitarray con el contenido de la compresión
"""
def escribirFichero(Doc):
    ruta=input("Determine la ruta o el nombre del archivo binario donde guardar la compresión: ")
    
    f=open(ruta,'wb')
    f.write(Doc)
    f.close()

"""rellenaBitarray(b,tam)
Añade 0s hasta ser de tamaño exp(para los numeros) u 8 para las letras(byte) 
@param b bitarray introducido para añadirle 0s
@param tam tamaño de bits que debe cumplir el bitarray para ser valido (variable exp en main)
@return bitarray completo
"""
def rellenaBitarray(b,tam):
    while(len(b)<tam):
        b.insert(0,0)
    return(b)

"""addNumero(exp, total, pn)
Añade una posición(entero) del diccionario al bitarray
@param exp 
"""
def addNumero(exp, total, pn):
    b=bitarray()
    
    cad=format(pn,'b') #formatea la posicion a binario en un string  
    b.extend(cad)
    b=rellenaBitarray(b, exp)
    total.extend(b)

"""addLetra(total, Documento, n)
Añade una letra al bitarray, esta ocupará un byte
@param total bitarray que contiene la codificación en bits
@param Documento variable en la que se ha volcado el interior del archivo que se quiere comprimir
@param n posición de lectura de la variable
"""
def addLetra(total, Documento, n):
    b=bitarray()
    
    cad=format(ord(Documento[n]),'b') #formatea la letra a binario en un string    
    b.extend(cad)
    b=rellenaBitarray(b, 8)
    total.extend(b)

"""addHeader(total)
Define la cabecera en la que se especifica el numero inicial con el que se empiezan a leer bits y el máximo de bits que usa el programa
En este caso no haría falta porque ya están declarados como variables globales pero puede ser que no se supiesen e hiciesen falta
@param total bitarray que contendrá la codificación
"""
def addHeader(total):
    addNumero(8, total, INITBIT)
    addNumero(8, total, MAXBIT)

"""compresion()
Método principal donde se hace uso de otros métodos para comprimir un archivo
"""
def compresion():
    Documento=leerFichero()

    Diccionario=dict()
    Tam=len(Documento)
    i=1 #posición de diccinario nueva entrada
    n=0 #posición de lectura
    exp=INITBIT

    total=bitarray()
    addHeader(total)

    while(n<Tam): #Pasa por todos los caracteres del documento
        a=Documento[n]

        if(a in Diccionario):
            while(a in Diccionario):
                pn=Diccionario[a] #pn es la posicion del nodo
                n=n+1 
                if(n<Tam):
                    a=a+Documento[n] #añade valores a a para comparar con ya existentes
                else:
                    n-=1
                    break
            
            Diccionario[a]=i #asigna posicion en el diccionario
         
            addNumero(exp, total, pn)
            addLetra(total, Documento, n)
        
            i=i+1
            
            if((i)==(2**exp)-1): #suma un bit a la escritura de los numeros si la posición en el diccionario lo requiere
                exp+=1
                
            if(exp==MAXBIT+1): #Borra el diccionario al pasar de 12 bits y crea uno nuevo
                Diccionario=dict()
            
        else:
            Diccionario[a]=i
            
            addNumero(exp, total, 0)
            addLetra(total, Documento, n)
        
            i=i+1
            if((i)==(2**exp)-1):
                exp+=1
            
            if(exp==MAXBIT+1):
                Diccionario=dict()
                
        n=n+1 #Avanza posición en la lectura
         
    escribirFichero(total)
    print("\nCompresión realizada con éxito")
 
#Decompresion

"""importFromFich()
Importa la compresión en bits a una variable tipo bitarray
"""
def importFromFich():
    CadenaBits=bitarray() 
    
    ruta=input("Introduzca la ruta del fichero de texto para descomprimir: ")
    
    with open(ruta,'rb') as F:
        CadenaBits.fromfile(F)
        
    return CadenaBits

"""guardaDescomp(Documento)
Exporta a un archivo de texto el documento descomprimido
@param Documento variable tipo String que contiene el texto descomprimido
"""
def guardaDescomp(Documento):
    ruta=input("Introduzca la ruta o el nombre del fichero para guardar en directorio actual: ")
    
    f=open(ruta,'w')
    f.write(Documento)
    f.close()

"""decompresion()
Usa los otros métodos y otras acciones para descomprimir el texto
"""
def decompresion():
    exp=INITBIT
    Descompreso=''
    a=1
    i=1 #Cuenta apariciones de numeros. Si es potencia de 2, añade un bit más a la lectura
    DecodeDict=dict()
    pos=16
    CadenaBits=bitarray() 

    CadenaBits=importFromFich()
    while(pos<len(CadenaBits)):
        c=0
        cadenaParcial=''
        
        while(c<exp and pos<len(CadenaBits)): #saca los numeros
            cadenaParcial+=str(int(CadenaBits[pos]))#string con bits
            c+=1
            pos+=1
        
        numero=int(cadenaParcial,2)
        i+=1
        c=0
        cadenaParcial=''

        if(i==(2**exp)-1): #añade un bit más a la lectura
            exp+=1
        
        while(c<8 and pos<len(CadenaBits)): #saca los simbolos
            cadenaParcial+=str(int(CadenaBits[pos]))
            c+=1
            pos+=1
        
        if(pos<len(CadenaBits)): #Comprobación por si el último número no tenía letra asociada 
            letra=chr(int(cadenaParcial,2))
        
            if(numero==0): 
                DecodeDict[a]=letra
            else:
                DecodeDict[a]=DecodeDict[numero]+letra
        
            Descompreso+=DecodeDict[a]
            a+=1
            
        if(exp==MAXBIT+1):
            DecodeDict=dict()

    guardaDescomp(Descompreso)
    print("\nDecompresión realizada con éxito")
        
"""main()
Núcleo principal del programa que da la opción de comprimir o descomprimir un archivo
"""
def main():
    opcion=-1
    
    while(opcion!=0):
        print("\n\t\tMENÚ PRINCIPAL")
        opcion=int(input("Qué es lo que desea hacer: Comprimir=1, Descomprimir=2, Salir=0: "))
        
        if(opcion==1):
            compresion()
        elif(opcion==2):
            decompresion()
        elif(opcion==0):
            print("\nAplicación terminada...")
        else:
            print("ERROR: Símbolo no válido, redirección a menú principal...")
            

#Ejecución
main()
