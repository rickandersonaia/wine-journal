from winejournal.app import create_app

app = create_app()

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=5000)

