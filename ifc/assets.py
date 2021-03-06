# -*- coding: utf-8 -*-
"""Application assets."""
from flask_assets import Bundle, Environment

css = Bundle(
    'libs/bootstrap/dist/css/bootstrap.min.css',
    'libs/animate.css/animate.min.css',
    'css/style.css',
    filters='cssmin',
    output='public/css/compiled/common.css'
)

js = Bundle(
    'libs/underscore/underscore-min.js',
    'libs/backbone/backbone-min.js',
    'libs/jQuery/dist/jquery.min.js',
    'libs/bootstrap/dist/js/bootstrap.min.js',
    'libs/noty/js/noty/packaged/jquery.noty.packaged.js',
    'libs/d3/d3.min.js',
    'libs/chart.js/dist/Chart.min.js',
    'js/version_update.js',
    'js/drift_identify.js',
    filters='jsmin',
    output='public/js/compiled/common.js'
)

guest_list_js = Bundle(
    'js/party/guest_list.js',
    'js/party/guest_list_view.js',
    'js/party/add_guest_view.js',
    'js/party/guest.js',
    'js/party/guest_view.js',
    'js/party/guest_collection.js',
    output='public/js/compiled/guest_list.js'
)

guest_list_css = Bundle(
    'css/party.css',
    output='public/css/compiled/party.css'
)

report_coffee = Bundle(
    'coffee/reports/main.coffee',
    'coffee/reports/newcharts.coffee',
    output='public/js/compiled/reports.js',
    filters=['coffeescript', 'jsmin']
)

report_css = Bundle(
    'css/report.css',
    output='public/css/compiled/report.css'
)


assets = Environment()

assets.register('js_all', js)
assets.register('guest_list_js', guest_list_js)
assets.register('css_all', css)
assets.register('guest_list_css', guest_list_css)
assets.register('report_coffee', report_coffee)
assets.register('report_css', report_css)
