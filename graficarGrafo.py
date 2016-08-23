#!/usr/bin/env python

# -*- coding: utf-8 -*-

#Se importa la libreria networkx como nx
import networkx as nx

#Se importa la libreria pyplot de matplotlib como plt
import matplotlib.pyplot as plt

#numero de dispositivos
num_devices = 5

#numero de arcos generados
arc = 0

#Se crea un grafo vacio
G = nx.Graph()

#Se crea la lista vacia
states = []

for i in range(0,2**num_devices):
	state = bin(i)[2:].zfill(num_devices)
	print state
	states.append(state)

#Se agregan los nodos al grafo desde la lista de estados
G.add_nodes_from(states)

for i in range(0,2**num_devices):
	state = bin(i)[2:].zfill(num_devices)

	for j in range(0,num_devices):	
		if(state[j] == '0'):
			z = i + (2**(num_devices -1 - j))
			node_to_connect = bin(z) [2:].zfill(num_devices)
			#Se genera el arco
			G.add_edge(state,node_to_connect)
			print (state + " --> " + node_to_connect)
			arc = arc + 1

#Se dibuja el grafo
nx.draw(G)
#Se muestra en pantalla
plt.show()
#Se salva en un archivo png.
plt.savefig("networkx1.png")

#print "Ruta mas corta entre 0000 y 1111: ",nx.algorithms.shortest_path(G,'00000','11111')

print "La cantidad de arcos generados es de: " 
print arc