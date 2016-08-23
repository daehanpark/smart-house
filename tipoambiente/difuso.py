import fuzzy.storage.fcl.Reader

class Difuso:
    
    def __init__(self):
        self.system = fuzzy.storage.fcl.Reader.Reader().load_from_file("tipoambiente/definicion.fcl")
        self.input = {
        "Temperatura" : 0.0,
        "Volumen" : 0.0,
        "Intensidad" : 0.0
        }
        
        self.output = {
        "Tipoambiente": 0.0
        }
    
    def setInput(self,temp,vol,intense):
        self.input["Temperatura"]=temp
        self.input["Volumen"]=vol
        self.input["Intensidad"]=intense
    
    def getOutput(self):
        self.system.calculate(self.input, self.output)
        tipo = self.output["Tipoambiente"]
        retval="No clasificado"
        if(tipo==1):
            retval= "Descanso"
        elif(tipo==2):
            retval= "Trabajo"
        elif(tipo==3):
            retval= "Estres"    
        
        return retval
    
    #ESTO ES UN COMENTARIO

if __name__ == '__main__':
    difuso = Difuso()
    difuso.setInput(18, 20, 20)
    print "TIPO DE AMBIENTE: ",difuso.getOutput()