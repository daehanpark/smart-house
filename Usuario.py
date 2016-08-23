class Usuario:
    def __init__(self,id_usuario="1",nombre="default"):
        self.__id=id_usuario
        self.__nombre=nombre
    
    def get_nombre(self):
        return self.__nombre
    
    def get_id_usuario(self):
        return self.__id
    
    def set_nombre(self,nombre):
        self.__nombre=nombre
    
    def set_id_usuario(self,id_usuario):
        self.__id=id_usuario