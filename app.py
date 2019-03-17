import connexion
from flask_cors import CORS, cross_origin
from flask import redirect

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yml')
app.app.config['ENV'] = 'development'
CORS(app.app)

host = '0.0.0.0'
port = 5000


@app.route('/')
def index():
    return redirect("http://"+host+":"+str(port)+"/api/ui")


if __name__ == '__main__':
    app.run(host=host, port=port, debug=True)
