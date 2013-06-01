import code
import anonymous.models as m
from flask import g
from anonymous.app import create_app

def shell():
    app = create_app({})
    session = m.Session()
    env = {
        'app':app,
        'models':m,
        'm':m,
        'session':session,
        'g':g,
    }
    ctx = app.test_request_context()
    try:
        ctx.push()
        code.interact(local=env)
    finally:
        ctx.pop()

def main():
    shell()

if __name__ == '__main__':
    main()
