from src import omnibus



if __name__ == '__main__':
    omnibus.secret_key = 'maria'
    omnibus.config['SESSION_TYPE'] = 'filesystem'
    omnibus.run(debug = True)