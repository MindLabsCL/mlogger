### mlogger - Libreria de logs para Mindlabs v0.0.1

#### Dependencias
> pip3 install wheel 

#### Instalación
> git clone https://github.com/MindLabsCL/mlogger  
> cd mlogger  
> python3 setup.py bdist_wheel  
> pip3 install dist/{build}.whl  

#### Uso 
> from mlogger import Logger  
> Logger.get_instance().configure(uuid="Identificador unico", component="Nombre de la solucion", user="Nombre del usuario que ejecuta el codigo")

#### Revisión de los logs
> Los logs quedan almacenados en la ruta /home/{user}/log/{uuid}. 
La idea de utilizar el nombre de usuario es para tener permisos de escritura sobre ese directorio.
