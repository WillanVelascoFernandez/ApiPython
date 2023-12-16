from flask import Flask, jsonify
from flask_restful import Resource, Api, request
from db_direct import read_historial

app =Flask("Practica APIs Python")

api= Api(app)

class HistorialModel:
    def __init__(self, id, fecha, nombreLoteria, numeros):
        self.id = id
        self.fecha = fecha
        self.nombreLoteria = nombreLoteria
        self.numeros = numeros 

    def __repr__(self):
       return f'Historial: id = {self.id}, fecha={self.fecha}, nombreLoteria={self.nombreLoteria}, numeros={self.numeros}'

class HistorialResource(Resource):
    def get(self):
        try:
            # producto = request.args['producto']
            # fecha = request.args['fecha']
            items = read_historial()
            resultado = [HistorialModel(*item).__dict__ for item in items]
            # resultado = []
            # for item in items:
            #     resultado.append(HistorialModel(item[0], item[1], item[2], item[3]).__dict__)
            return jsonify(resultado)
        except Exception as e:
            return {"error": str(e)}
    


    
api.add_resource(HistorialResource, "/")

if __name__ == "__main__":
    app.run(debug=True)