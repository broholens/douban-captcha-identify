from flask import Flask, request
from flask_restful import Api, Resource
from baidu_identify import recognize_url


app = Flask(__name__)

api = Api(app) 

class Captcha(Resource):
    def post(self):
        captcha_url = request.form.get('img_url')
        word = recognize_url(captcha_url)
        return word 

api.add_resource(Captcha, '/')

if __name__ == '__main__':
    app.run('0.0.0.0', 5001)
