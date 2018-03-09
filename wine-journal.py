import os
from flask import Flask, render_template, request, redirect, url_for, \
    flash, jsonify
from flask_assets import Environment, Bundle

app = Flask(__name__)
assets = Environment(app)
app.config['ASSETS_DEBUG'] = True

css = Bundle('scss/styles.scss',
            filters='pyscss', output='css/styles.css')
assets.register('css_all', css)
assets.init_app(app)


@app.route('/')
def hello_world():
    return render_template('base.html')


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
