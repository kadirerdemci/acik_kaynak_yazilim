from flask import Flask, request, render_template
from flask_restful import Api, Resource
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
api = Api(app)

class Users(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        data = data.to_dict('records')
        return {'data': data}, 200

    def post(self):
        json = request.get_json()
        req_data = pd.DataFrame({
            'name': [json['name']],
            'age': [json['age']],
            'city': [json['city']]
        })
        data = pd.read_csv('users.csv')
        data = pd.concat([data, req_data], ignore_index=True)
        data.to_csv('users.csv', index=False)
        return {'message': 'Record successfully added.'}, 200

    def delete(self):
        name = request.args.get('name')
        data = pd.read_csv('users.csv')

        if name in data['name'].values:
            data = data[data['name'] != name]
            data.to_csv('users.csv', index=False)
            return {'message': 'Record successfully deleted.'}, 200
        else:
            return {'message': 'Record not found.'}, 404

class Cities(Resource):
    def get(self):
        data = pd.read_csv('users.csv')
        cities = data['city'].to_dict()
        return {'cities': cities}, 200

class Name(Resource):
    def get(self, name):
        data = pd.read_csv('users.csv')
        user_data = data[data['name'] == name].to_dict('records')
        if user_data:
            return {'data': user_data[0]}, 200
        else:
            return {'message': 'No entry found with this name!'}, 404

class Statistics(Resource):
    def get(self):
        data = pd.read_csv('users.csv')

        # Ortalama yaş
        average_age = data['age'].mean()

        # En sık bulunan şehir
        most_common_city = data['city'].mode().iloc[0]

        return {'average_age': average_age, 'most_common_city': most_common_city}, 200

class Visualization(Resource):
    def get(self):
        data = pd.read_csv('users.csv')

        # Yaş dağılımı grafiği
        plt.hist(data['age'], bins=20, color='blue', edgecolor='black')
        plt.xlabel('Age')
        plt.ylabel('Count')
        plt.title('Age Distribution')
        plt.grid(True)

        # Grafiği base64 formatına çevirip gönderme
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        graph_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return {'graph': graph_url}, 200

# Add URL endpoints
api.add_resource(Users, '/users')
api.add_resource(Cities, '/cities')
api.add_resource(Name, '/users/<string:name>')
api.add_resource(Statistics, '/statistics')
api.add_resource(Visualization, '/visualization')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
