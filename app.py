from routes import app
from routes import bp
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host="localhost", port=5000)
