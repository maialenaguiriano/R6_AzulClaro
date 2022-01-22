#!/usr/bin/env python
# coding: utf-8

# ### Librerias

# In[1]:


import pandas as pd  
import os
import numpy as np
import datetime as dt # para gestión de fechas
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import matplotlib
plt.style.use('ggplot')
from matplotlib.pyplot import figure
from datetime import datetime
import locale
from scipy import stats
import re
import os


# In[2]:


os.getcwd()


# ### Importar módulos creados por nosotros

# In[3]:


import funciones as fn #funciones es el nombre del script dnd hemos creado las funciones


# ### Carga de datos

# In[4]:


path_dataset = '..\\datosOriginales\\' # ruta donde se encuentran los datos
path_dataset1 = '..\\datosTransformados\\' # ruta donde se van a guardar los datos limpios
file = 'EDERJAKIN_LA_Datos_2021.xlsm'
fichero = pd.ExcelFile(path_dataset + file)
nombres_hojas = fichero.sheet_names


# In[5]:


# leer todas las hojas
todo  = pd.read_excel(os.path.join(path_dataset,file), sheet_name = nombres_hojas)

# separar
for i in todo.keys():
    globals()['%s' % i.replace(" ", "_").lower()] = todo[i]


# # Limpieza 

# ## DATA CLEANING

# ### ELIMINACION DE VARIABLES Y FILAS QUE NO DAN INFORMACION

# In[6]:


#Usuarios
fn.eliminar_columnas(usuarios, 'last_access') #mas tarde imputaremos esta columna junto al primer acceso que estan en df accesos_1ero_ultimo


# In[7]:


#Conocimientos
fn.eliminar_columnas(conocimientos, ['color', 'description', 'referencia']) #quitamos color y description ya que no aportan info y tienen pocos valores 


# In[8]:


#Cursos
fn.eliminar_columnas(cursos, ['summary', 'sortorder']) #quitamos summary ya que con la informacion de course_name es suficiente, y sortorder porque no aporta info necesaria


# In[9]:


#Itinerarios
fn.eliminar_columnas(itinearios, ['remarks']) #esta vacia y no aporta informacion


# In[10]:


#Accesos
accesos.groupby('description').size() #quitamos los accesos que fueron ERROR, ya que no son errores validos
erroneas = accesos[accesos['description'] == 'Login SRM ERROR 1']
indice_erroneas = list(erroneas.index)
accesos = accesos.drop(indice_erroneas, axis = 0)


# ### CORRECCION DEL TIPO DE LAS VARIABLES

# In[11]:


#usuarios:
usuarios.info()


# In[12]:


fn.corregir_tipo(df = usuarios, columnas = ['user_id','language', 'planta_name','mdl_user_id'], tipo = 'category') #las pasamos a tipo category
fn.corregir_tipo(df = usuarios, columnas = ['active_flag',  'role_admin','role_manager','role_student','role_tutor'], tipo = 'bool') #a tipo bool
fn.corregir_tipo(df = usuarios, columnas = ['useranonimo_name'], tipo = 'string')

#quitamos columnas Unnamed:
fn.eliminar_unnamed(usuarios)
usuarios.info() #correcto


# In[13]:


#tutores_perfil
tutores_perfil.info()


# In[14]:


fn.corregir_tipo(df= tutores_perfil, columnas= ['user_id','perfil_id'], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= tutores_perfil, columnas= ['perfil_name'], tipo= 'string')
fn.eliminar_unnamed(tutores_perfil) #eliminamos columnas unnamed
tutores_perfil.info() #correcto


# In[15]:


#Conocimientos
conocimientos.info()


# In[16]:


fn.corregir_tipo(df= conocimientos, columnas= [ 'conocimiento_id','categoria_conocimiento_id','created_by'], tipo= 'category') #las pasamos a category
fn.corregir_tipo(df= conocimientos, columnas= [ 'conocimiento_name','categoria_conocimiento_name'], tipo= 'string')
fn.eliminar_unnamed(conocimientos) #quitamos columnas 'unnamed'

conocimientos.info() #correcto


# In[17]:


#Cursos
cursos.info()


# In[18]:


fn.corregir_tipo(df= cursos, columnas= ['category', 'course_id'], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= cursos, columnas= ['course_name', 'course_shortname'], tipo= 'string') #a string
fn.eliminar_unnamed(cursos) #eliminamos columnas unnamed
cursos.rename(columns={'category':'course_category_id'}, inplace = True) #le ponemos un nombre mas apropiado
cursos.info()


# In[19]:


#Programas
programas.info()


# In[20]:


fn.corregir_tipo(df= programas, columnas= ['program_id', 'program_category_id' ], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= programas, columnas= ['program_name'], tipo= 'string')
fn.eliminar_unnamed(programas) #eliminamos columnas unnamed
programas.info() #correcto


# In[21]:


#Cursos en programas
cursos_en_programas.info()


# In[22]:


fn.corregir_tipo(df= cursos_en_programas, columnas= ['program_course_online_id','course_moodle_id','conocimiento_id', 'program_id', 'num_periodo' ], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= cursos_en_programas, columnas= ['conocimiento_name','program_name','course_moodle_id.1'], tipo= 'string')
fn.eliminar_unnamed(cursos_en_programas) #eliminamos columnas unnamed

#cambiamos el mobre de course_moodle_id.1 a course_moodle_name
cursos_en_programas.rename(columns={'course_moodle_id.1': 'course_moodle_name'}, inplace=True)
cursos_en_programas.info() #correcto


# In[23]:


#Itinerarios
itinearios.info()


# In[24]:


#En primer lugar, cambiar nombre a tabla.

itinerarios = itinearios
del itinearios #la eliminamos para que no intervenga

fn.corregir_tipo(df= itinerarios, columnas= ['active_flag'], tipo= 'bool') #las pasamos a tipo bool
fn.corregir_tipo(df= itinerarios, columnas= ['user_id','tutor_academico_id', 'tutor_empresa_id','category_id', 'program_id' ], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= itinerarios, columnas= ['category_name', 'program_name'], tipo= 'string') #las pasamos a tipo string

itinerarios['enroll_end'] = pd.to_datetime(itinerarios['enroll_end'], utc= True) #las pasamos a tipo date
itinerarios['date_enroll'] = pd.to_datetime(itinerarios['date_enroll'], utc= True)

fn.eliminar_unnamed(itinerarios) #eliminamos columnas unnamed
itinerarios.rename(columns={'category_id':'itinerary_category_id', 'category_name':'itinerary_category_name'}, inplace = True) #le ponemos un nombre mas apropiado
itinerarios.info() #correcto


# In[25]:


#Notas_cursos
notas_cursos.info()


# In[26]:


fn.corregir_tipo(df= notas_cursos, columnas= ['active_flag'], tipo= 'bool') #las pasamos a tipo bool
fn.corregir_tipo(df= notas_cursos, columnas= ['enroll_grade_id', 'course_id', 'enroll_id', 'user_id' ], tipo= 'category')
fn.corregir_tipo(df= notas_cursos, columnas= ['course_name'], tipo= 'string')

fn.eliminar_unnamed(notas_cursos) #eliminamos columnas unnamed
notas_cursos.info() #correcto


# In[27]:


#Roles
roles.info()


# In[28]:


fn.corregir_tipo(df= roles, columnas= ['role_id'], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= roles, columnas= ['role_name'], tipo= 'string')
fn.eliminar_unnamed(roles) #eliminamos columnas unnamed
roles.info() #correcto


# In[29]:


#Plantas
plantas.info()


# In[30]:


fn.corregir_tipo(df= plantas, columnas= ['planta_id'], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= plantas, columnas= ['planta_name'], tipo= 'string')
fn.eliminar_unnamed(plantas) #eliminamos columnas unnamed
plantas.info()


# In[31]:


#Accesos
accesos.info()


# In[32]:


fn.corregir_tipo(df= accesos, columnas= ['mdl_user_id', 'user_id'], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= accesos, columnas= ['description'], tipo= 'string')
fn.eliminar_unnamed(accesos) #eliminamos columnas unnamed
accesos['timestamp'] = pd.to_datetime(accesos['timestamp'], utc= True)
accesos.info() #correcto


# In[33]:


#Acceso_1ero_ultimo
acceso_1ero_ultimo.info()


# In[36]:


acceso_1ero_ultimo.head(1)


# In[37]:


#Acceso_1ero_ultimo
fn.eliminar_dias(df= acceso_1ero_ultimo , columna= '1er acceso') #convertimos las fechas de texto a numerico, primero eliminando el dia de la semana
fn.eliminar_dias(df= acceso_1ero_ultimo , columna= 'ultimo acceso')

locale.setlocale(locale.LC_ALL, 'esp_esp') #cambiamos el idioma
fn.fecha_texto(acceso_1ero_ultimo, '1er acceso')
fn.fecha_texto(acceso_1ero_ultimo, 'ultimo acceso')

fn.corregir_tipo(df= acceso_1ero_ultimo, columnas= ['mdl_user_id'], tipo= 'category') #las pasamos a tipo category
acceso_1ero_ultimo['1er acceso'] = pd.to_datetime(acceso_1ero_ultimo['1er acceso'], utc= True) #a tipo datetime
acceso_1ero_ultimo['ultimo acceso'] = pd.to_datetime(acceso_1ero_ultimo['ultimo acceso'], utc= True)
fn.eliminar_unnamed(accesos) #eliminamos columnas unnamed
acceso_1ero_ultimo.info()


# In[38]:


#Actividades
actividades.info()


# In[39]:


fn.corregir_tipo(df= actividades, columnas= ['mdl_user_id', 'course_id', 'category'], tipo= 'category') #las pasamos a tipo category
fn.corregir_tipo(df= actividades, columnas= ['course_name', 'actividad_name'], tipo= 'string')
actividades['time'] = pd.to_datetime(actividades['time'], utc= True) #a tipo datetime

fn.eliminar_unnamed(actividades) #eliminamos columnas unnamed
actividades.rename(columns = {'category': 'course_category_id'}, inplace= True) #le ponemos el mismo nombre que en las otras tablas ya que es la misma variable
actividades.info()


# # Estadisticos

# In[40]:


#Usuarios
usuarios.shape #dimensiones (420, 12)
usuarios.columns
usuarios.describe() #son todas variables discretas
usuarios['language'].value_counts().to_frame()
usuarios['planta_name'].value_counts().to_frame() 
usuarios.loc[usuarios['planta_name'] == 'MT Aretxabal', 'planta_name'] = 'MT Aretxabaleta' #renombramos MT Aretxabal a MT Aretxabaleta


# In[41]:


#Tutores_perfil
tutores_perfil.shape #dimensiones (188, 3)
tutores_perfil.columns
tutores_perfil.describe() #son todas variables discretas
tutores_perfil['perfil_name'].value_counts().to_frame()


# In[42]:


#Conocimientos
conocimientos.shape #dimensiones (155, 5)
conocimientos.columns
conocimientos.describe()
conocimientos['created_by'].value_counts().to_frame()
conocimientos['categoria_conocimiento_name'].value_counts().to_frame()


# In[43]:


#Cursos
cursos.shape #dimensiones (139, 5)
cursos.columns
cursos.describe(include=['object', 'category'])
cursos['hours'].describe()
cursos['course_category_id'].value_counts().to_frame()


# In[44]:


#Programas
programas.shape #dimensiones (110, 3)
programas.columns
programas.describe()
programas['program_category_id'].value_counts().to_frame()


# In[45]:


#Cursos en programas
cursos_en_programas.shape #dimensiones (253, 8)
cursos_en_programas.columns
cursos_en_programas.describe(include=['category', 'object'])
cursos_en_programas['course_moodle_name'].value_counts().to_frame()
cursos_en_programas['conocimiento_name'].value_counts().to_frame()
cursos_en_programas['num_periodo'].value_counts().to_frame()
cursos_en_programas['program_name'].value_counts().to_frame()


# In[46]:


#Itinerarios
itinerarios.shape #dimensiones (467, 10)
itinerarios.columns
itinerarios.describe(include=['category', 'object', 'bool'])
itinerarios.describe(include=['datetime64[ns, UTC]'])

#hacemos una nueva variable para saber la duracion del programa
itinerarios['duracion'] = itinerarios['enroll_end'] - itinerarios['date_enroll']
itinerarios.describe(include=['timedelta64[ns]']) #tenemos duraciones por debajo de cero, quiere decir que el date_enroll de algunos programas ocurre despues que el enroll_end, es imposible
itinerarios[itinerarios['duracion'] < '0 days'] #intercambiamos los valores las dos columnas en esas dos filas

fecha = itinerarios.loc[96, 'date_enroll']
itinerarios.loc[96, 'date_enroll'] = itinerarios.loc[96, 'enroll_end']
itinerarios.loc[96, 'enroll_end'] = fecha

fecha = itinerarios.loc[317, 'date_enroll']
itinerarios.loc[317, 'date_enroll'] = itinerarios.loc[317, 'enroll_end']
itinerarios.loc[317, 'enroll_end'] = fecha


# In[47]:


itinerarios['duracion'] = itinerarios['enroll_end'] - itinerarios['date_enroll'] #volvemos a calcular la variable duracion
itinerarios[itinerarios['duracion'] < '0 days'] #correcto


# In[48]:


#Notas_cursos
notas_cursos.shape #dimensiones (3898, 8)
notas_cursos.columns
notas_cursos.describe(include=['category', 'object', 'bool']) #variables discretas
notas_cursos['course_name'].value_counts().to_frame()

notas_cursos.describe(include= 'float64') #variables continuas


# In[49]:


#Roles
roles.shape #dimensiones (4, 2)
roles.columns
roles['role_name'].describe() 


# In[50]:


#Plantas
plantas.shape #dimensiones (18, 2)
plantas.columns
plantas.describe() #variables discretas
plantas['planta_id'].value_counts().to_frame()
plantas['planta_name'].value_counts().to_frame() #eliminamos MT Aretxabal, ya que esta mal escrito y antes en usuarios hemos convertido MT Aretxabal en MT Aretxabaleta

plantas = plantas.loc[:16, :]


# In[51]:


#Accesos
accesos.shape #dimensiones (8816, 4)
accesos.columns
accesos.describe() #variables discretas
accesos['description'].value_counts().to_frame()
accesos['mdl_user_id'].value_counts().to_frame()
accesos['user_id'].value_counts().to_frame()


# In[52]:


#Acceso_1ero_ultimo
acceso_1ero_ultimo.shape #dimensiones (372, 3)
acceso_1ero_ultimo.columns
acceso_1ero_ultimo.describe() #variables discretas
h =acceso_1ero_ultimo['1er acceso'] < acceso_1ero_ultimo['ultimo acceso']
h.value_counts().to_frame() #en todos los casos el primer acceso ocurre antes del ultimo acceso, es correcto
acceso_1ero_ultimo['mdl_user_id'].value_counts().to_frame()


# In[53]:


#Actividades
actividades.shape #dimensiones (3464, 7)
actividades.columns
actividades.describe(include = ['object', 'category','bool', 'datetime64[ns, UTC]'] ) #variables discretas
actividades.describe(include = ['float64']) #tenemos maximos por encima de 10


# In[54]:


actividades.info()


# ### DUPLICADOS

# In[55]:


#Quitamos filas duplicadas
fn.eliminar_duplicados(usuarios)
fn.eliminar_duplicados(tutores_perfil)
fn.eliminar_duplicados(conocimientos)
fn.eliminar_duplicados(cursos)
fn.eliminar_duplicados(programas)
fn.eliminar_duplicados(cursos_en_programas)
fn.eliminar_duplicados(itinerarios) # se han eliminado 26 filas duplicadas 
fn.eliminar_duplicados(notas_cursos)
fn.eliminar_duplicados(roles)
fn.eliminar_duplicados(accesos) # se han eliminado 26 filas duplicadas 
fn.eliminar_duplicados(acceso_1ero_ultimo)
fn.eliminar_duplicados(actividades) # se han eliminado 89 filas duplicadas


# In[56]:


#Identificamos las columnas duplicadas
fn.columnas_duplicadas(usuarios) #ninguna


# In[57]:


fn.columnas_duplicadas(tutores_perfil) #ninguna


# In[58]:


fn.columnas_duplicadas(conocimientos) #ninguna


# In[59]:


fn.columnas_duplicadas(cursos) #ninguna


# In[60]:


fn.columnas_duplicadas(programas) #ninguna


# In[61]:


fn.columnas_duplicadas(cursos_en_programas) #ninguna


# In[62]:


fn.columnas_duplicadas(itinerarios) #ninguna


# In[63]:


fn.columnas_duplicadas(notas_cursos) #ninguna


# In[64]:


fn.columnas_duplicadas(roles) #ninguna


# In[65]:


fn.columnas_duplicadas(accesos) #ninguna


# In[66]:


fn.columnas_duplicadas(acceso_1ero_ultimo) #ninguna


# In[67]:


fn.columnas_duplicadas(actividades) #ninguna
#Ningun data frame tiene columnas duplicadas


# ### MISSING VALUES

# In[69]:


#Usuarios
fn.identificar_missings(usuarios)
sns.heatmap(usuarios.isnull(), cbar=False) #visualizamos los missings


# In[70]:


#Observamos que la columna last_acces está completamente vacia. Procedemos a imputarla desde acceso_1ero_ultimo (ultimo acceso)
#Imputamos tambien 1er acceso
#Esto lo haremos tras tratar "acceso_1ero_ultimo"


#Asimismo, la columna de mdl_user_id, tiene 15 instancias con NaN. 
#Las eliminamos ya que esos usuarios no aparecen en ninguna tabla mas, no participan en los programas
usuarios.dropna(subset=["mdl_user_id"], inplace = True)


# In[71]:


sns.heatmap(usuarios.isnull(), cbar=False) #visualizamos los missings


# In[72]:


#Tutores_perfil
fn.identificar_missings(tutores_perfil)
sns.heatmap(tutores_perfil.isnull(), cbar=False) #visualizamos los missings


# In[73]:


tutores_perfil = tutores_perfil.dropna() #quitamos las filas con NaN en perfil_name. el perfil_id de esas filas es 0, por lo que definitivamente no aportan valor


# In[74]:


sns.heatmap(tutores_perfil.isnull(), cbar=False) #visualizamos los missings


# In[75]:


#Conocimientos
fn.identificar_missings(conocimientos)
sns.heatmap(conocimientos.isnull(), cbar=False) #visualizamos los missings


# In[76]:


#La variable categoria_conocimiento_name tiene 22 missings. Esto se debe a que la categoria_conocimiento_id es 0. 
#Es decir, no existe ni tiene datos. Por lo tanto, vamos a quitar las filas que son missings o lo q es lo mismo, Filas
# que tienen el valor de 0 en la variable categoria_conocimiento_id.

indexNames = conocimientos[ conocimientos['categoria_conocimiento_id'] == 0 ].index
conocimientos.drop(indexNames , inplace=True)


# In[77]:


sns.heatmap(conocimientos.isnull(), cbar=False) #visualizamos los missings


# In[78]:


#Cursos
fn.identificar_missings(cursos) #no contiene valores vacios
sns.heatmap(cursos.isnull(), cbar=False) #visualizamos los missings


# In[79]:


#Programas
fn.identificar_missings(programas)

sns.heatmap(programas.isnull(), cbar=False) #visualizamos los missings


# In[80]:


#identificamos la fila con NaN
programas['vacio'] = programas['program_category_id'].isnull()
programas[programas['vacio'] == True] #vemos que el program_name es pepe, por lo que no es valido

programas.drop(['vacio'], axis = 1, inplace= True)

programas.dropna(subset=["program_category_id"], inplace = True) #lo eliminamos

#puede que haya mas program_name inventados:
programas['program_name'].unique() #se observan nombres que resultan extraños e inventados.

#los quitamos
#cursos_en_programas tiene program_name y program_id correctos (la mayoria), por lo que los imputamos desde ahi
#ademas, asi eliminamos programas que no aparecen en la tabla cursos en programas, ya que que no aparezcan significa que no pertenecen a ningun curso de modle. No nos interesan
cursos_en_programas['program_id'].unique().shape #71 programas no inventados (suponemos)
programas['program_id'].unique().shape #109-71 = 38 programas inventados

programas_correctos= []
programas_correctos = pd.DataFrame(cursos_en_programas['program_id'].unique())
programas_correctos.columns = ['program_id'] 
programas_correctos

programas = programas_correctos.merge(programas, on="program_id", how = "left")

programas['program_name'].unique() #seguimos teniendo nombres inventados; los identificamos:
programas[programas['program_name'].str.contains('prueba|Sergio')] 

#son las filas 24 - 38, las quitamos
programas = programas.drop(range(24,39,1), axis = 0 ).reset_index(drop= True)


# In[81]:


#Nos hemos dado cuenta de que hay program_names con un DNI al final o con la propia palabra DNI
#Eliminamos ese trozo de texto
fn.eliminar_dni(programas, 'program_name')


# In[82]:


sns.heatmap(programas.isnull(), cbar=False) #visualizamos los missings


# In[83]:


#Cursos en programas
fn.identificar_missings(cursos_en_programas) #no hay missings

sns.heatmap(cursos_en_programas.isnull(), cbar=False) #visualizamos los missings


# In[84]:


#El program name tiene los mismos nombres inventados q en el caso anterior. Los eliminamos
cursos_en_programas[cursos_en_programas['program_name'].str.contains('prueba|Sergio')] 

cursos_en_programas = cursos_en_programas.drop(range(128,156,1), axis = 0 ).reset_index(drop = True)


# In[85]:


#eliminamos el DNI que hay al final de algunos program_names
fn.eliminar_dni(cursos_en_programas, 'program_name')


# In[86]:


cursos_en_programas[cursos_en_programas['program_name'].str.contains('prueba|Sergio')] #correcto


# In[87]:


#Itinerarios
fn.identificar_missings(itinerarios)

sns.heatmap(itinerarios.isnull(), cbar=False) #visualizamos los missings


# In[88]:


#identificamos la fila con NaN en date_enroll
itinerarios1 = pd.DataFrame()
itinerarios1['vacio'] = itinerarios['date_enroll'].isnull()
itinerarios1
itinerarios1[itinerarios1['vacio'] == True] 
itinerarios.iloc[52, :]

#La eliminamos ya que todo itinerario debe tener fecha de comienzo, y no se puede imputar
itinerarios.drop([52],axis=0, inplace = True)
itinerarios.reset_index(drop = True)

#con los missings de la variable enroll_end no hacemos nada, ya que la fecha final del itinerario no tiene porque estar siempre determinada

sns.heatmap(itinerarios.isnull(), cbar=False) #visualizamos los missings


# In[89]:


#Notas_cursos
fn.identificar_missings(notas_cursos)
sns.heatmap(notas_cursos.isnull(), cbar=False) #visualizamos los missings


# In[90]:


#Las dos variables con instancias que contienen missings son grade y online_progress. 

#En el caso de estas dos variables, es importante preguntarse porque tienen valores missings. La respuesta que se cree correcta
#es de que se tratan de variables que no tienen que tener un valor de obligatoriamente. Es decir, quizas algunos aprendices todavia 
# no han realizado el grado o el curso por lo que no tienen ninguna nota asociada. Lo mismo ocurre con el online_progress,
#puesto que mide el porcentaje de progreso del curso y quizas algunos aprendices no hayan dado comienzo al curso.

#Por estos motivos, se ha decidido que los valores ausentes que se encuentran en blanco se sustituyen por un 0 (sin iniciar.)
notas_cursos['grade'].fillna(0, inplace=True)#convertir NaN en 0
notas_cursos['online_progress'].fillna(0, inplace=True)#convertir NaN en 0

sns.heatmap(notas_cursos.isnull(), cbar=False) #visualizamos los missings


# In[91]:


#Roles
fn.identificar_missings(roles) #ningun valor ausente
sns.heatmap(roles.isnull(), cbar=False) #visualizamos los missings


# In[92]:


#Plantas
fn.identificar_missings(plantas) #ningun valor ausente
sns.heatmap(plantas.isnull(), cbar=False) #visualizamos los missings


# In[93]:


#Accesos
fn.identificar_missings(accesos) #ningun valor ausente
sns.heatmap(accesos.isnull(), cbar=False) #visualizamos los missings


# In[94]:


#Acceso_1ero_ultimo
fn.identificar_missings(acceso_1ero_ultimo)
sns.heatmap(acceso_1ero_ultimo.isnull(), cbar=False) #visualizamos los missings


# In[95]:


#Los NaN de 1er acceso y ultimo acceso son de las mismas filas, por lo que podemos quitarlas
acceso_1ero_ultimo.dropna(subset=["1er acceso"], inplace = True)

#Imputamos las dos variables de "acceso_1ero_ultimo" en "usuarios"
usuarios = usuarios.merge(acceso_1ero_ultimo, on="mdl_user_id", how = "left")
usuarios

sns.heatmap(acceso_1ero_ultimo.isnull(), cbar=False) #visualizamos los missings
#Eliminamos este dataframe
del acceso_1ero_ultimo


# In[96]:


#Actividades
fn.identificar_missings(actividades)
sns.heatmap(actividades.isnull(), cbar=False) #visualizamos los missings


# In[97]:


#Eliminamos las filas con NaN en actividad_name, ya que no contienen informacion tampoco de grade y time
actividades.dropna(subset=["actividad_name"], inplace = True) 

#Los valores de las notas no se pueden imputar debido a que se tratan de usuarios que no han comenzado
#con el curso, por lo que todavia no tienen ninguna nota.

#En cuanto a la ultima variable, la columna time consta de un numero elevado de missings (1331). En este caso, como es logico, 
#ocurre lo mismo. Aquellos usuarios que no hayan comenzado con la actividad, no tienen la fecha ni la nota correspondiente. 
#Por ello, no se cree oportuno eliminar todas las intancias y los mantendremos como NaN. (En caso de necesidad, posteriormente
#se eliminaran estos missings)

sns.heatmap(actividades.isnull(), cbar=False) #visualizamos los missings


# ### OUTLIERS

# In[98]:


#Usuarios
#En esta tabla, no se puede realizar la tecnica para identificar outlier puesto que no se cuenta con ninguna variable cuantitva.


# In[99]:


#Tutores_perfil
#En esta tabla, no se puede realizar la tecnica para identificar outlier puesto que no se cuenta con ninguna variable cuantitva.


# In[100]:


#Conocimientos
#En esta tabla, no se puede realizar la tecnica para identificar outlier puesto que no se cuenta con ninguna variable cuantitva.


# In[101]:


#Cursos
#En esta tabla, existe una variable cuantitativa (hours). Por lo que se puede analizar si existe algun outlier.
sns.boxplot(x=cursos['hours'])#se observan los valores en boxplot.


# In[102]:


#Utilizaremos la función Z-score definida en la biblioteca scipy para detectar los valores atípicos.
z = np.abs(stats.zscore(cursos['hours']))
print(z)

threshold = 3 #definir un umbral para identificar un valor atípico.
print(np.where(z > 3)) # existen dos filas que se identifican como outliers

#Las dos filas (25 y 50) identificadas como outliers, se observan y se ve que quizas se trata de un error debido a que tienen un
#cero de más.
cursos['hours'][25]#se observa el valor correspondiente
cursos['hours'][50]#se observa el valor correspondiente

cursos['hours'].replace({800: 80,600: 60}, inplace = True)#se quita un cero

z = np.abs(stats.zscore(cursos['hours']))
print(z)

sns.boxplot(x=cursos['hours'])#se observan los valores en boxplot.


# In[103]:


#Programas
#En esta tabla, no se puede realizar la tecnica para identificar outlier puesto que no se cuenta con ninguna variable cuantitva.


# In[104]:


#Cursos en programas
#En esta tabla, existe una variable cuantitativa (num_periodos). No tiene outliers ya que, como hemos observado en los estadisticos, los valores que toma son 0, 1, 2, o 3


# In[105]:


#Itinerarios
#No hay variables cuantitativas


# In[106]:


#Notas_cursos
notas_cursos.describe() #como hemos visto antes, los valores de grade superan el 10

sns.boxplot(x=notas_cursos['grade'])#se observan los valores en boxplot.
z = np.abs(stats.zscore(notas_cursos['grade']))

threshold = 3 #definir un umbral para identificar un valor atípico.
print(np.where(z > 3)) # existen 27 filas con umbral mayor que 3

#notas mayores que 10, se dividen por 10 y se obtiene la nota real
notas_cursos.loc[notas_cursos['grade'] > 10, 'grade'] = notas_cursos['grade']/10 #transformacion de la nota
notas_cursos['grade'].max()#se observa que el valor maximo es 10.


# In[107]:


sns.boxplot(x=notas_cursos['grade'])#se observan los valores sin outliers en boxplot.


# In[108]:


#Roles
#No hay variables cuantitativas


# In[109]:


#Plantas
#No hay variables cuantitativas


# In[110]:


#Accesos
#No hay variables cuantitativas


# In[111]:


#Acceso_1ero_ultimo
#No hay variables cuantitativas


# In[112]:


#Actividades
#tiene una variable cualitativa: grade
actividades.describe() #notas por encima de 10

sns.boxplot(x=actividades['grade'])#se observan los valores en boxplot.
z = np.abs(stats.zscore(actividades['grade']))
threshold = 3 #definir un umbral para identificar un valor atípico.
print(np.where(z > 3)) #se observa que contamos con algunos outliers

#notas mayores que 10, se dividen por 10 y se obtiene la nota real
actividades.loc[actividades['grade'] > 10, 'grade'] = actividades['grade']/10
actividades['grade'].max()#se observa que el valor maximo es 10.


# In[113]:


sns.boxplot(x=actividades['grade'])#se observan los valores sin outliers en boxplot.


# In[114]:


#Una vez los datos limpios, los descargamos como csv a la carpeta datosTransformados


# In[115]:


# Eliminar los .csv existentes (antiguos) en la carpeta de datos transformados y descargar la última version
fn.eliminar_csv(path_dataset1)

fn.convertir_csv(usuarios, filename='usuarios.csv',path_dataset = path_dataset1 ) #descargar
fn.convertir_csv(tutores_perfil, 'tutores_perfil.csv',path_dataset = path_dataset1)
fn.convertir_csv(conocimientos, 'conocimientos.csv',path_dataset = path_dataset1)
fn.convertir_csv(cursos, 'cursos.csv',path_dataset = path_dataset1)
fn.convertir_csv(programas, 'programas.csv',path_dataset = path_dataset1)
fn.convertir_csv(cursos_en_programas, 'cursos_en_programas.csv',path_dataset = path_dataset1)
fn.convertir_csv(itinerarios, 'itinerarios.csv',path_dataset = path_dataset1)
fn.convertir_csv(notas_cursos, 'notas_cursos.csv',path_dataset = path_dataset1)
fn.convertir_csv(roles, 'roles.csv',path_dataset = path_dataset1)
fn.convertir_csv(plantas, 'plantas.csv',path_dataset = path_dataset1)
fn.convertir_csv(accesos, 'accesos.csv',path_dataset = path_dataset1)
fn.convertir_csv(actividades, 'actividades.csv',path_dataset = path_dataset1)



# %%
