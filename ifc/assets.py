# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.css',
    'css/style.css',
    filters='cssmin',
    output='public/css/common.css'
)

js = Bundle(
    'libs/underscore/underscore.js',
    'libs/backbone/backbone.js',
    'libs/jQuery/dist/jquery.js',
    'libs/bootstrap/dist/js/bootstrap.js',
    'js/plugins.js',
    filters='jsmin',
    output='public/js/common.js'
)

guest_list_js = Bundle(
    'js/guest_list.coffee',
    filters=['coffeescript', 'jsmin'],
    output='public/js/compiled/guest_list.js'
)



assets = Environment()

assets.register('js_all', js)
assets.register('guest_list_js', guest_list_js)
assets.register('css_all', css)
