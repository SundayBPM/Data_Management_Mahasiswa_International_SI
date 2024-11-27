from flask import flash, render_template, request, redirect, url_for, session, make_response
from models import User, Mahasiswa, ExchangeOutbound, Bpp
from collections import Counter
from datetime import datetime
from sqlalchemy import func

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
            all_iisma = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.jenis_exchange == 'IISMA').count()
            all_exch = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.jenis_exchange == 'student exchange').count()


            return render_template('home_dosen.html', all_exch=all_exch, all_iisma=all_iisma)

    @app.route('/ExchangeIISMA', methods=['GET'])
    def ExchangeIISMA():
        query = db.session.query(ExchangeOutbound.nim, ExchangeOutbound.intake_year, ExchangeOutbound.jenis_exchange).all()
        intake_years = [i[1] for i in query]
        jenis_exch = [i[2] for i in query]
        
        jenis_per_year = {}
        for year in set(intake_years):
            jenis_per_year[year] = dict(Counter([status for i, status in enumerate(jenis_exch) if intake_years[i] == year]))
        labels = list(jenis_per_year.keys())
        dataset_jenis = ["IISMA","student exchange"]

        datasets = []
        for jenis in dataset_jenis:
            data = [jenis_per_year.get(year, {}).get(jenis,0) for year in labels]
            datasets.append({
                'label': jenis,
                'data': data
            })
        
        result = {
            "labels":labels,
            "datasets":datasets
        }
        return result
    
    @app.route('/status-count', methods=['GET'])
    def status_count():
        result = db.session.query(
            func.count(ExchangeOutbound.status).label('status_count'),
            ExchangeOutbound.status,
            ExchangeOutbound.intake_year
            ).filter(ExchangeOutbound.intake_year=='2024').group_by(ExchangeOutbound.status).all()
        
        labels = [label[1] for label in result]
        data = [data[0] for data in result]

        dataset = {
            'labels': labels,
            'datasets': [{
                'data': data
            }]
        }
        return dataset

    @app.route('/testing', methods=['GET', 'POST'])
    def testing():
        result = db.session.query(
            func.count(ExchangeOutbound.status).label('status_count'),
            ExchangeOutbound.status,
            ExchangeOutbound.intake_year
            ).filter(ExchangeOutbound.intake_year=='2024').group_by(ExchangeOutbound.status).all()
        labels = [label[1] for label in result]
        data = [data[0] for data in result]
        print(data)
        print(result)
        return "None"
    
    @app.route('/IISMA', methods=['GET', 'POST'])
    def iisma():
        """
        Routes untuk masuk ke halaman form IISMA
        """
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))

        user_id = session.get('id')
        if request.method == 'GET':
            student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
            iisma_inf = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.nim == user_id).first()
            return render_template('iisma.html', student_inf=student_inf, iisma_inf=iisma_inf)
        
        elif request.method == 'POST':
            # mahasiswa = Mahasiswa.query.filter_by(nim = user_id).first()
            exch_info = ExchangeOutbound.query.filter_by(nim = user_id).first()
            exch_info.status = request.form['status']
            exch_info.intake_year = datetime.strptime(request.form['intake_year'], '%Y-%m-%d').date()
            exch_info.intake = datetime.strptime(request.form['intake'], '%Y-%m-%d').date()
            from_date = request.form['from']
            exch_info.from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            until = request.form['until']
            exch_info.until = datetime.strptime(until, '%Y-%m-%d').date()
            exch_info.sem_at_telu = request.form['semester']
            # exch_info.semester_telu = request.form['sem_at_telu']
            # exch_info.gpa = request.form['gpa']
            exch_info.sem_at_exch = request.form['semester_at_iisma']
            exch_info.gpa = request.form['gpa_at_iisma']
            update_gpa = request.form['latest_update_iisma']
            exch_info.update_gpa = datetime.strptime(update_gpa, '%Y-%m-%d').date()
            db.session.commit()
            
            return redirect(url_for('iisma'))
    
    @app.route('/IISMA-admin', methods=['GET'])
    def iisma_admin():
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        
        # stud_iisma = db.session.query(ExchangeOutbound).all()
        stud_iisma = db.session.query(ExchangeOutbound, Mahasiswa).join(Mahasiswa, ExchangeOutbound.nim == Mahasiswa.nim).all()
        return render_template('iisma_admin.html', stud_iisma=stud_iisma)

    @app.route('/IISMA-admin/<int:user_id>', methods=['GET'])
    def iisma_view(user_id):
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        bpp_inf = db.session.query(Bpp).filter(Bpp.nim == user_id).first()
        student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
        iisma_inf = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.nim == user_id).first()
        return render_template('iisma.html', student_inf=student_inf, iisma_inf=iisma_inf, bpp_inf=bpp_inf)

    @app.route('/IISMA-admin/<int:user_id>/update', methods=['POST'])
    def iisma_update(user_id):
        exch_info = ExchangeOutbound.query.filter_by(nim = user_id).first()
        exch_info.status = request.form['status']
        exch_info.intake_year = datetime.strptime(request.form['intake_year'], '%Y-%m-%d').date()
        exch_info.intake = datetime.strptime(request.form['intake'], '%Y-%m-%d').date()
        from_date = request.form['from']
        exch_info.from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
        until = request.form['until']
        exch_info.until = datetime.strptime(until, '%Y-%m-%d').date()
        exch_info.sem_at_telu = request.form['semester']
        exch_info.sem_at_exch = request.form['semester_at_iisma']
        exch_info.gpa = request.form['gpa_at_iisma']
        update_gpa = request.form['latest_update_iisma']
        exch_info.update_gpa = datetime.strptime(update_gpa, '%Y-%m-%d').date()
        db.session.commit()
        return redirect(url_for('iisma_view', user_id=user_id))
    
    @app.route('/student-exchange', methods=['GET', 'POST'])
    def exchange():
        """
        Routes untuk masuk ke halaman form IISMA
        """
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))

        user_id = session.get('id')
        if request.method == 'GET':
            student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
            iisma_inf = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.nim == user_id).first()
            return render_template('iisma.html', student_inf=student_inf, iisma_inf=iisma_inf)
        
        elif request.method == 'POST':
            # mahasiswa = Mahasiswa.query.filter_by(nim = user_id).first()
            exch_info = ExchangeOutbound.query.filter_by(nim = user_id).first()
            exch_info.status = request.form['status']
            exch_info.intake_year = datetime.strptime(request.form['intake_year'], '%Y-%m-%d').date()
            exch_info.intake = datetime.strptime(request.form['intake'], '%Y-%m-%d').date()
            from_date = request.form['from']
            exch_info.from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
            until = request.form['until']
            exch_info.until = datetime.strptime(until, '%Y-%m-%d').date()
            exch_info.sem_at_telu = request.form['semester']
            # exch_info.semester_telu = request.form['sem_at_telu']
            # exch_info.gpa = request.form['gpa']
            exch_info.sem_at_exch = request.form['semester_at_iisma']
            exch_info.gpa = request.form['gpa_at_iisma']
            update_gpa = request.form['latest_update_iisma']
            exch_info.update_gpa = datetime.strptime(update_gpa, '%Y-%m-%d').date()
            db.session.commit()
            
            return redirect(url_for('iisma'))    
