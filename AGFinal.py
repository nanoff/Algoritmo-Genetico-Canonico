"""""
funcion a maximizar: 
   0.5-(dividendo/divisor) 
      donde:
            dividendo=pow(sin(sqrt(pow(x,2)+pow(y,2))),2)-0.5
            divisor=pow(1+0.001*(pow(x,2)+pow(y,2)),2)

probabilidad de crossover = 0.65 (65%)
probabilidad de mutacion = 0.08 (0.8%) Se ha tomado esta probabilidad debido a que con probabilidad 0.008 (0.8%)
                                       y la poblacion 100 no iba a a haber mutacion
Poblacion = 100
Generaciones = 100
Experimentos = 20
metodo de seleccion = ruleta
metodo de crossover = 1/2/Cruce uniforme
"""""

import random
import sys
from math import sin,sqrt
import matplotlib.pyplot as plt

"""""
    INGRESO DE VARIABLES
"""""

TAM_POBLA=100 #Tamaño de la Poblacion
TAM_GEN=100 #Cantidad de Generaciones a realizar
CANT_EXP=20 #Cantidad de Experimentos a realizar
PRO_CRU=0.65 #Probabilidad de Cruce
PROB_MUT=0.08 #Probabilidad de Mutacion
TIP_CRU=2 #Tipo de Cruce a usar: 1=unpunto, 2=dospuntos, 3= cruce uniforme

"""""
    Declaramos los arreglos para la grafica
"""""

v_best = []
v_off = []
v_on = []
p_prom = []
   
random.seed()


"""
    Definimos la funcion de CRUCE de acuerdo a Tipo de Cruce 1/2/Uniforme  
"""
def cruce(indice_padre1,indice_padre2,tipo_cruce):
   if(tipo_cruce==1):
      punto_a=random.randint(0,61)
      for i in range(punto_a+1,62):
         temporal=cromosoma[indice_padre1][i]
         cromosoma[indice_padre1][i]=cromosoma[indice_padre2][i]
         cromosoma[indice_padre2][i]=temporal

   if(tipo_cruce==2):
      punto_a=random.randint(0,61)
      punto_b=random.randint(0,61)
      if punto_a>punto_b:
         temporal=punto_a
         punto_a=punto_b
         punto_b=temporal
      for i in range (punto_a+1,punto_b+1):
         temporal=cromosoma[indice_padre1][i]
         cromosoma[indice_padre1][i]=cromosoma[indice_padre2][i]
         cromosoma[indice_padre2][i]=temporal

   if(tipo_cruce==3):
      for i in range(0,62):
         probabilidad=random.random()
         if probabilidad<0.5:
            temporal=cromosoma[indice_padre1][i]
            cromosoma[indice_padre1][i]=cromosoma[indice_padre2][i]
            cromosoma[indice_padre2][i]=temporal

"""""
    Funcion a Maximizar
"""""
def optimizar(x,y):
   dividendo=pow(sin(sqrt(pow(x,2)+pow(y,2))),2)-0.5;
   divisor=pow(1+0.001*(pow(x,2)+pow(y,2)),2);
   return 0.5-(dividendo/divisor);

"""""
    Funciones de lectura de variables que estan en cada cromosoma
"""""
   
def leer_x1(secuencia):
   suma=0
   for i in range(0,31):
      suma+=pow(2,i)*secuencia[i];
   x=-100+(suma*200/float(pow(2,31)-1))
   return x

def leer_x2(secuencia):
   suma=0
   for i in range(31,62):
      suma+=pow(2,i-31)*secuencia[i];
   x=-100+(suma*200/float(pow(2,31)-1))
   return x

"""""
    Inicializacion en 0, de vector de mejores y promedio
""""" 

for i in range(0,TAM_GEN):
   v_best.append(0)
      
for i in range(0,TAM_GEN):
   p_prom.append(0)
   
for exp in range(0,CANT_EXP):
   t=0
   cromosoma = []
   aptitud = []

# Inicializa Poblacion

   for i in range(0,TAM_POBLA):
      for j in range(0,62):
         cromosoma.append([]);
         cromosoma[i].append(random.randint(0,1))

#Decodificacion y evaluacion del cromosoma
   for i in range(0,TAM_POBLA):   
      aptitud.append(optimizar(leer_x1(cromosoma[i]),leer_x2(cromosoma[i])))

   while(t<TAM_GEN):
      
      for i in range(0,TAM_POBLA):
         p_prom[t]+=aptitud[i]
      p_prom[t]/=TAM_GEN

      t=t+1 # Cambio de Generacion

# Se inicializa la Mutacion

      nuevos_cromosoma = []
      for i in range(0,TAM_POBLA): 
         aleatorio=random.randint(0,TAM_POBLA-1)
         nuevos_cromosoma.append(cromosoma[aleatorio]);

# Elitismo

      mejor=[] 
      for i in cromosoma[aptitud.index(max(aptitud))]:
         mejor.append(i)
      indice_mejor=aptitud.index(max(aptitud)) 
      v_best[t-1]+=max(aptitud)

      cromosoma=[]
      for i in range(0,TAM_POBLA):
         cromosoma.append(nuevos_cromosoma[i])
         
      cantidad=-1
      
      seleccionados=[]

# Se establece los que van a cruzarse

      for i in range(0,TAM_POBLA):
         aleatorio=random.random()
         if aleatorio<PRO_CRU:
            seleccionados.append(i)
            cantidad = cantidad + 1
      if(cantidad%2):
         cantidad = cantidad - 1
      for i in range (0,int(cantidad/2)):
         cruce(seleccionados[i],seleccionados[i+1+int(cantidad/2)],TIP_CRU)

# Proceso de MUTACION

      for i in range(0,TAM_POBLA):
         aleatorio=random.random()
         if aleatorio<PROB_MUT:
            punto=random.randint(0,61)
            if cromosoma[i][punto]==0:
               cromosoma[i][punto]=1
            else:
               cromosoma[i][punto]=0
      
      del cromosoma[TAM_POBLA-1]

      cromosoma.append(mejor)
      
      aptitud=[]
      for i in range(0,TAM_POBLA):   
         aptitud.append(optimizar(leer_x1(cromosoma[i]),leer_x2(cromosoma[i])))
      
for i in range(0,TAM_GEN):
   v_best[i]/=CANT_EXP

suma=0
for i in range(0,TAM_GEN):
   suma+=v_best[i]
   v_off.append(suma/(i+1))


suma=0
for i in range(0,TAM_GEN):
   suma+=p_prom[i]
   v_on.append(suma/(i+1))


lista_datos=[]
for i in range(0,TAM_GEN):
   tupla=(v_best[i],v_on[i],v_off[i])
   lista_datos.append(tupla)
   print (str(i)+"---"+str(v_best[i])+"---"+str(v_on[i])+"---"+str(v_off[i]))


# Se grafica el resultado 
 
plt.plot(lista_datos)
plt.ylabel("Verde: Best\nAzul: online\nRojo: offline")
plt.xlabel("Tiempo")
plt.show()
