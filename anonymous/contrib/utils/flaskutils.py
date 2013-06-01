""":mod:`meetytools.utils.flask` --- Utils for :mod:`flask`.  
=========================================================

Provides useful utils for :mod:`flask`.  
"""
from flask import Flask, abort

def add_url_rules(app, blueprint, fn=(lambda *args, **kwargs:abort(404)),
    **kwargs):
    duck = Flask('')
    defaults = set(duck.url_map.iter_rules())
    duck.register_blueprint(blueprint, **kwargs)
    for rule in duck.url_map.iter_rules():
        if rule in defaults:
            continue
        app.url_map.add(rule.empty())
        app.view_functions[rule.endpoint] = fn
