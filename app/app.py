from flask import Flask
import routes

app = Flask(__name__)
app.config.from_object('config.Config')

app.register_blueprint(routes.bp)

if __name__ == '__main__':
    app.run(debug=True)
