from flask import Flask, jsonify
from flask_restful import Resource, Api, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("Practica APIs Python")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root:1234@localhost:3306/api'
db = SQLAlchemy(app)
api = Api(app)

class ModeloLoteria(db.Model):
    __tablename__ = 'loteria'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(50))
    nombreLoteria = db.Column(db.String(50))
    numeros = db.Column(db.String(10))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'Historial: id={self.id}, fecha={self.fecha}, nombreLoteria={self.nombreLoteria}, numeros={self.numeros}'

class ListarLoteria(Resource):
    def get(self):
        # items = ModeloLoteria.query.filter(ModeloLoteria.id == 1).first()
        items = ModeloLoteria.query.all()
        if items:
            result = [item.as_dict() for item in items]
            # return jsonify(item.as_dict())
            return jsonify(result)
        else:
            return {"message": "No se encontró el elemento"}, 404

    # def post(self):
    #     try:
    #         datos = request.get_json()
    #         item = HistorialModel(**datos)
    #         db.session.add(item)
    #         db.session.commit()
    #         return jsonify(item.as_dict()), 201
    #     except Exception as e:
    #         return {"error": str(e)}, 400
        
class ListarLoteriaPorNombre(Resource):
    def get(self, nombreLoteria=None):
        # items = ModeloLoteria.query.filter(ModeloLoteria.id == 1).first()
        items = ModeloLoteria.query.filter(ModeloLoteria.nombreLoteria==nombreLoteria)
        if items:
            result = [item.as_dict() for item in items]
            # return jsonify(item.as_dict())
            return jsonify(result)
        else:
            return {"message": "No se encontró el elemento"}, 404

with app.app_context():
    db.create_all()

    # Agrega algunos datos de ejemplo
    # loteria1 = ModeloLoteria(fecha='2023-01-01', nombreLoteria='Loteria1', numeros='1,2,3,4,5')
    # loteria2 = ModeloLoteria(fecha='2023-01-02', nombreLoteria='Loteria2', numeros='6,7,8,9,10')
    # db.session.add(loteria1)
    # db.session.add(loteria2)
    # db.session.commit()

        # Agrega 20 loterías de Bolivia como datos de ejemplo
    loterias_bolivia = [
        {'fecha': '2023-01-01', 'nombreLoteria': 'Loteria1', 'numeros': '1,2,5,5,9'},
        {'fecha': '2023-01-01', 'nombreLoteria': 'Loteria2', 'numeros': '6,2,9,3,1'},
        {'fecha': '2023-01-01', 'nombreLoteria': 'Loteria3', 'numeros': '7,3,7,2,3'},
        {'fecha': '2023-01-02', 'nombreLoteria': 'Loteria1', 'numeros': '6,5,3,7,4'},
        {'fecha': '2023-01-02', 'nombreLoteria': 'Loteria2', 'numeros': '8,7,1,9,9'},
        {'fecha': '2023-01-02', 'nombreLoteria': 'Loteria3', 'numeros': '6,2,2,4,0'},
        {'fecha': '2023-01-03', 'nombreLoteria': 'Loteria1', 'numeros': '9,8,5,8,6'},
        {'fecha': '2023-01-03', 'nombreLoteria': 'Loteria2', 'numeros': '0,9,8,2,0'},
        {'fecha': '2023-01-03', 'nombreLoteria': 'Loteria3', 'numeros': '5,0,7,9,2'},
        #
    ]

    for loteria_data in loterias_bolivia:
        nueva_loteria = ModeloLoteria(**loteria_data)
        db.session.add(nueva_loteria)
        db.session.commit()

api.add_resource(ListarLoteria, '/')
api.add_resource(ListarLoteriaPorNombre, '/nombre/<string:nombreLoteria>')

if __name__ == "__main__":
    app.run(debug=True)
