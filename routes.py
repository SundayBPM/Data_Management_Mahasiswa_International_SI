from flask import flash, render_template, request, redirect, url_for, session, make_response

def register_routes(app, db):
    @app.route('/', methods=['GET'])
    def home_page():
        return "Hello World"