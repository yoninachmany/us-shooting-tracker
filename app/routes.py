from flask import render_template
from app import app
from app.models import Store


@app.route('/')
@app.route('/index')
def index():
    stores = Store.query.all()
    return render_template('index.html', stores=stores)
