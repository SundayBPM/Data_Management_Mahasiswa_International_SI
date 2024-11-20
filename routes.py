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
        username = session.get('username')
        if username is None:
            return render_template('login.html')
        return redirect(url_for('dashboard'))
    
    @app.route('/login', methods=['POST'])
    def login():
        username = request.form['username']
        password = request.form['password']

        user = get_user(username)
        if user and user.password == password:
            session['username'] = username
            session['role'] = user.role
            session['id'] = user.id
            return redirect(url_for('dashboard'))
        
        return render_template('login.html', message="Invalid username or password <br> please try again")

    # Handle Log out    
    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home_page'))  # Redirect to login page

    def get_user(username):
        user = db.session.query(User).filter(User.username == username).first()
        return user
    
    @app.route('/dashboard', methods=['GET'])
    def dashboard():
        username = session.get('username')
        if username is None:
            return render_template('login.html')
        
        role = session.get('role')
        if role == "mahasiswa":
            return render_template('home_mahasiswa.html')
        elif role == "dosen":
            return render_template('home_dosen.html')
    
    @app.route('/IISMA', methods=['GET', 'POST'])
    def iisma():
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))

        user_id = session.get('id')
        if request.method == 'GET':
            student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
            iisma_inf = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.nim == user_id).first()
            # print(iisma_inf.nim)
            # return render_template('test.html', student_inf=student_inf, iisma_inf=iisma_inf)
            return render_template('iisma.html', student_inf=student_inf, iisma_inf=iisma_inf)
        elif request.method == 'POST':
            return "Formulir dikirim dengan metode POST"
    
    @app.route('/IISMA-admin', methods=['GET', 'POST'])
    def iisma_admin():
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        
        if request.method == 'GET':
            # stud_iisma = db.session.query(ExchangeOutbound).all()
            stud_iisma = db.session.query(ExchangeOutbound, Mahasiswa).join(Mahasiswa, ExchangeOutbound.nim == Mahasiswa.nim).all()

            return render_template('iisma_admin.html', stud_iisma=stud_iisma)
        elif request.method == 'POST':
            return "Formulir dikirim dengan metode post"
