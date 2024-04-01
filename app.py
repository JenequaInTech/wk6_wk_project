from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://honwduhi:feQgGMR_bcdQDzrF6fSOSrUy5yOkaufk@raja.db.elephantsql.com/honwduhi'
db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


 #confingure my marshmellow app &intializze it with my flask
      
      from flask_marshmallow import Marshmallow

ma = Marshmallow(app)
