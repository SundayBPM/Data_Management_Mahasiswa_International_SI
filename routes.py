from flask import flash, render_template, request, redirect, url_for, session, make_response
from models import User, Mahasiswa, ExchangeOutbound, Bpp

def register_routes(app, db):

    @app.after_request
    def add_cache_headers(response):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    @app.route('/', methods=['GET'])
    def home_page():
        return render_template('login.html')
    
    @app.route('/login', methods=['POST'])
    def login():
        username = request.form['username']
        print("ini usernamenya: ",username)
        password = request.form['password']
        print("ini passwornya: ",password)
        
        user = get_user(username)
        print('hasil dari function get_user: ', user)
        if user and user.password == password:
            print('true')
            session['username'] = username
            session['role'] = user.role
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', message="Invalid username or password <br> please try again")

    
    def get_user(username):
        user = db.session.query(User).filter(User.username == username).first()
        return user
    
    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        username = session.get('username')
        role = session.get('role')
        if role == "mahasiswa":
            return render_template('home.html')
        elif role == "dosen":
            return "ini dosen"