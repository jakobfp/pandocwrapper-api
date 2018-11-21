import connexion

app = connexion.FlaskApp(__name__, specification_dir='./')
app.add_api('swagger.yml')
app.app.config['ENV'] = 'development'


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
