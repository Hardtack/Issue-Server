from anonymous.app import create_app

if __name__ == '__main__':
    app = create_app({
        'DEBUG':True,
        'SECRET_KEY':'secret',
    })
    app.run(host='0.0.0.0', port=8080)
