from flask import Flask, jsonify
from flask_restful import Resource, Api, request
from flask_sqlalchemy import SQLAlchemy

app = Flask("LottoApi")
app.config['SQLALCHEMY_DATABASE_URI'] = 'mariadb://root:1234@localhost:3306/api'
db = SQLAlchemy(app)
api = Api(app)

class ModeloLoteria(db.Model):
    __tablename__ = 'lottoapi'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fecha = db.Column(db.String(50))
    proveedor = db.Column(db.String(50))
    nombreLoteria = db.Column(db.String(50))
    numeros = db.Column(db.String(10))

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return f'Historial: id={self.id}, fecha={self.fecha}, proveedor={self.proveedor},, nombreLoteria={self.nombreLoteria}, numeros={self.numeros}'

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
        
class ListarLoteriaPorProveedor(Resource):
    def get(self, proveedor=None):
        # items = ModeloLoteria.query.filter(ModeloLoteria.id == 1).first()
        items = ModeloLoteria.query.filter(ModeloLoteria.proveedor==proveedor)
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

        # Agrega loterías de Bolivia como datos de ejemplo
    loterias_bolivia = [
        {'fecha': '2023-01-01', 'proveedor': 'Banco', 'nombreLoteria': 'Macro Cuenta', 'numeros': '1,2,5,5,9'},
        {'fecha': '2023-01-01', 'proveedor': 'Loteria', 'nombreLoteria': 'Nacional', 'numeros': '6,2,9,3,1'},
        {'fecha': '2023-01-01', 'proveedor': 'Banco', 'nombreLoteria': 'Fabulosa', 'numeros': '7,3,7,2,3'},
        {'fecha': '2023-01-02', 'proveedor': 'Loteria', 'nombreLoteria': 'Navideña', 'numeros': '6,5,3,7,4'},
        {'fecha': '2023-01-02', 'proveedor': 'Banco', 'nombreLoteria': 'GanaDoble', 'numeros': '8,7,1,9,9'},
        {'fecha': '2023-01-02', 'proveedor': 'Loteria', 'nombreLoteria': 'Semanal', 'numeros': '6,2,2,4,0'},
        {'fecha': '2023-01-03', 'proveedor': 'Loteria', 'nombreLoteria': 'Diaria', 'numeros': '0,9,8,2,0'},
    ]

    for loteria_data in loterias_bolivia:
        nueva_loteria = ModeloLoteria(**loteria_data)
        db.session.add(nueva_loteria)
        db.session.commit()

api.add_resource(ListarLoteria, '/api')
api.add_resource(ListarLoteriaPorNombre, '/api/nombre/<string:nombreLoteria>')
api.add_resource(ListarLoteriaPorProveedor, '/api/proveedor/<string:proveedor>')

if __name__ == "__main__":
    app.run(host='172.25.112.1', port=5055,debug=True)
