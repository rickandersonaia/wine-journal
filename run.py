from winejournal.app import create_app

import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'


app = create_app()

if __name__ == '__main__':
    app.debug = app.config['DEBUG']
    app.run(host='0.0.0.0', port=5000)

