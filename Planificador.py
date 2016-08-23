import networkx as nx
from Dispositivo import Dispositivo.tipos

class Planificador:
    def __init__(self):
        self.__plan= None
        
    def get_plan(self):
        return self.__plan
    
    #Config = Es una lista donde cada elemento es una tupla que proviene de la
    #vista v_preferencia_usuarios
    def planificar(self,inicial,final,config):
    #dispo_power = [True for i in range(len(inicial))]
        for i in range[0,5]:
            if inicial[i] and not final[i]:
                
            elif not inicial[i] and final[i]:
            
            elif inicial[i] and final[i]:
                 
        self.__plan = []
        estados = []
        
        
        #Agregar los nodos al grafo
        #self.__plan.add_nodes_from(estados)
        
        #Crear arco (Uno por uno)
        #self.__plan.add_edge(state,node_to_connect)
        #Imprimir el grafo para ver como queda
        #nx.draw(self.__plan)
        
    
    
    