from flask import flash, render_template, request, redirect, url_for, session, make_response, current_app, send_from_directory
from werkzeug.utils import secure_filename
from models import User, Mahasiswa, ExchangeOutbound, Bpp
from collections import Counter
from flask import jsonify
from datetime import datetime
from sqlalchemy import func
import os

def register_routes(app, db):

    # dir_upload = current_app.config['UPLOAD_DIRECTORY']

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
            all_exch = db.session.query(ExchangeOutbound).filter(ExchangeOutbound.jenis_exchange == 'student_exchange').count()


            return render_template('home_dosen.html', all_exch=all_exch, all_iisma=all_iisma)

    @app.route('/ExchangeIISMA', methods=['GET'])
    def ExchangeIISMA():
        """
        End point untuk mengirim data peserta student exchange dan iisma 
        """
        # Query untuk mengambil data dari database
        query = db.session.query(ExchangeOutbound.nim, ExchangeOutbound.intake_year, ExchangeOutbound.jenis_exchange).all()

        # Ekstrak data intake_year dan jenis_exchange
        intake_years = [i[1] for i in query]
        jenis_exch = [i[2] for i in query]

        # Buat dictionary untuk menghitung jenis pertukaran per tahun
        jenis_per_year = {}
        for year in set(intake_years):
            # Hitung jumlah per jenis untuk setiap tahun
            jenis_per_year[year] = dict(Counter([status for i, status in enumerate(jenis_exch) if intake_years[i] == year]))

        # Tentukan dataset_jenis (jenis exchange yang diinginkan)
        dataset_jenis = ["IISMA", "student_exchange"]
        
        # Mengambil labels (tahun)
        labels = sorted([key for key in jenis_per_year.keys() if key is not None])  # Filter None sebelum sorting

        # Membuat dataset untuk JSON output
        datasets = []
        for jenis in dataset_jenis:
            data = []  # Daftar untuk menyimpan jumlah per tahun
            for year in labels:
                # Ambil jumlah untuk jenis tertentu di tahun tersebut, default 0 jika tidak ada
                year_data = jenis_per_year.get(year, {})
                data.append(year_data.get(jenis, 0))  # Jika jenis tidak ditemukan, beri 0
            datasets.append({
                'label': jenis,
                'data': data
            })

        # Hasil akhir dalam format JSON
        result = {
            "datasets": datasets,
            "labels": labels
        }

        # Cetak hasil untuk debugging (bisa dihapus jika tidak diperlukan)
        print(result)

        return result
    
    @app.route('/status-count', methods=['GET'])
    def status_count():
        """
        Routes ini berisi busines logic untuk menghitung jumlah dan mengelompokkan status mahasiswa
        """
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

    @app.route('/most-preferred-country-count', methods=['GET'])
    def most_preferred_country():
        """
        Routes ini berisi busines logic untuk menghitung jumlah dan mengelompokkan negara paling banyak di pilih oleh peserta
        """
        results = (
            db.session.query(
                func.count(ExchangeOutbound.nim).label('count'), 
                ExchangeOutbound.location
            )
            .filter(ExchangeOutbound.intake_year == "2024")
            .group_by(ExchangeOutbound.location)
            .all()
        )
        labels = [label[1] for label in results]
        data = [data[0] for data in results]

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
            iisma_inf = db.session.query(ExchangeOutbound).filter(
                ExchangeOutbound.nim == user_id,
                ExchangeOutbound.jenis_exchange == 'IISMA').first()
            return render_template('iisma.html', student_inf=student_inf, iisma_inf=iisma_inf)
        
        elif request.method == 'POST':
            # Check apakah user sudah pernah mendaftar iisma atau belum
            # exch_info = ExchangeOutbound.query.filter_by(nim=user_id).first()
            exch_info = db.session.query(ExchangeOutbound).filter(
                ExchangeOutbound.nim == user_id,
                ExchangeOutbound.jenis_exchange == 'IISMA').first()
            if exch_info is None:
                # Ambil nilai dari form, None jika tidak diisi
                intake_value = request.form.get('intake', '').strip()  # Ambil nilai atau kosong
                from_date_value = request.form.get('from', '').strip()
                until_value = request.form.get('until', '').strip()
                update_gpa_value = request.form.get('latest_update_iisma', '').strip()

                # Parsing hanya jika nilai tidak kosong
                intake_year_value = datetime.strptime(intake_value, '%Y-%m-%d').year if intake_value else None
                intake_value = datetime.strptime(intake_value, '%Y-%m-%d').date() if intake_value else None
                from_date_value = datetime.strptime(from_date_value, '%Y-%m-%d').date() if from_date_value else None
                until_value = datetime.strptime(until_value, '%Y-%m-%d').date() if until_value else None
                update_gpa_value = datetime.strptime(update_gpa_value, '%Y-%m-%d').date() if update_gpa_value else None

                new_exch_info = ExchangeOutbound(
                    id_= str(user_id)+"_iisma",
                    jenis_exchange = 'IISMA',
                    nim=user_id,
                    location = request.form['location'],
                    univ = request.form['univ'],
                    status=request.form['status'],
                    intake_year=intake_year_value,
                    intake=intake_value,
                    from_date=from_date_value,
                    until=until_value,
                    sem_at_telu=request.form['semester'],
                    sem_at_exch=request.form['semester_at_iisma'],
                    gpa=request.form['gpa_at_iisma'],
                    update_gpa=update_gpa_value
                )

                db.session.add(new_exch_info)
                db.session.commit()
            else:
                print("USER SUDAH PERNAH TERDAFTAR DI IISMA")
                exch_info.status = request.form['status']
                exch_info.location = request.form['location']
                exch_info.univ = request.form['univ']
                intake = datetime.strptime(request.form['intake'], '%Y-%m-%d').date()
                exch_info.intake = intake
                exch_info.intake_year = intake.year
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
                
                # Menggunakan fungsi untuk menambah file transcript dari user lalu menghapus file lama
                file_transcript = request.files['transcript']
                print(file_transcript.filename)
                if file_transcript:
                    exch_info.transcript_telu = handle_file_upload(
                        file_transcript, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{file_transcript.filename}'
                    )

                # Menggunakan fungsi untuk menambah file transcript_at_iisma dari user lalu menghapus file lama
                file_transcript_iisma = request.files['transcript_at_iisma']
                print(file_transcript_iisma.filename)
                if file_transcript_iisma:
                    exch_info.transcript_exch = handle_file_upload(
                        file_transcript_iisma, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{file_transcript_iisma.filename}'
                    )

                # Menggunakan fungsi untuk menambah file letter_of_Acc dari user lalu menghapus file lama
                letter_of_Acc = request.files['letter_of_Acc']
                if letter_of_Acc:
                    exch_info.letter_of_Acc = handle_file_upload(
                        letter_of_Acc, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{letter_of_Acc.filename}'
                    )

                # Menggunakan fungsi untuk menambah file others_docs dari user lalu menghapus file lama
                others_docs = request.files['others_docs']
                if others_docs:
                    exch_info.others_docs = handle_file_upload(
                        others_docs, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{others_docs.filename}'
                    )

                db.session.commit()
            
            return redirect(url_for('iisma'))
    
    def handle_file_upload(file, old_file_path, save_path):
        if file:
            if os.path.exists(old_file_path):
                os.remove(old_file_path)
            file.save(save_path)
            return file.filename
        return None
    
    @app.route('/IISMA-admin', methods=['GET'])
    def iisma_admin():
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        
        # stud_iisma = db.session.query(ExchangeOutbound).all()
        stud_iisma = db.session.query(ExchangeOutbound, Mahasiswa).join(
            Mahasiswa, ExchangeOutbound.nim == Mahasiswa.nim).filter(
                ExchangeOutbound.jenis_exchange == "IISMA"
            ).all()
        return render_template('iisma_admin.html', stud_iisma=stud_iisma)

    @app.route('/IISMA-admin/<user_id>', methods=['GET'])
    def iisma_view(user_id):
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        bpp_inf = db.session.query(Bpp).filter(Bpp.id_program == str(user_id)+"_iisma").first()
        student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
        iisma_inf = db.session.query(ExchangeOutbound).filter(
            ExchangeOutbound.nim == user_id,
            ExchangeOutbound.jenis_exchange == 'IISMA'
            ).first()
        return render_template('iisma.html', student_inf=student_inf, iisma_inf=iisma_inf, bpp_inf=bpp_inf)

    @app.route('/IISMA-admin/<user_id>/update', methods=['POST'])
    def iisma_update(user_id):
        bpp_inf = db.session.query(Bpp).filter(Bpp.id_program == str(user_id)+"_iisma").first()
        if bpp_inf:
            bpp_inf.discount=request.form['discount']
            bpp_inf.period=request.form['period_discount']
            bpp_inf.notes=request.form['notes']
        else:
            new_bpp = Bpp(
                nim=user_id,
                id_program=str(user_id)+"_iisma",
                discount=request.form['discount'],
                period=request.form['period_discount'],
                notes=request.form['notes']
            )
            db.session.add(new_bpp)
        
        # Ambil nilai dari form, None jika tidak diisi
        intake_value = request.form.get('intake', '').strip()  # Ambil nilai atau kosong
        from_date_value = request.form.get('from', '').strip()
        until_value = request.form.get('until', '').strip()
        update_gpa_value = request.form.get('latest_update_iisma', '').strip()

        # Parsing hanya jika nilai tidak kosong
        intake_year_value = datetime.strptime(intake_value, '%Y-%m-%d').year if intake_value else None
        intake_value = datetime.strptime(intake_value, '%Y-%m-%d').date() if intake_value else None
        from_date_value = datetime.strptime(from_date_value, '%Y-%m-%d').date() if from_date_value else None
        until_value = datetime.strptime(until_value, '%Y-%m-%d').date() if until_value else None
        update_gpa_value = datetime.strptime(update_gpa_value, '%Y-%m-%d').date() if update_gpa_value else None

        exch_info = db.session.query(ExchangeOutbound).filter(
                ExchangeOutbound.nim == user_id,
                ExchangeOutbound.jenis_exchange == 'IISMA').first()
        
        exch_info.status = request.form['status']
        exch_info.location = request.form['location']
        exch_info.univ = request.form['univ']
        exch_info.intake_year = intake_year_value
        exch_info.intake = intake_value
        exch_info.from_date = from_date_value
        exch_info.until = until_value
        exch_info.sem_at_telu = request.form['semester']
        # exch_info.semester_telu = request.form['sem_at_telu']
        # exch_info.gpa = request.form['gpa']
        exch_info.sem_at_exch = request.form['semester_at_iisma']
        exch_info.gpa = request.form['gpa_at_iisma']
        exch_info.update_gpa = update_gpa_value
        
        # Menggunakan fungsi untuk menambah file transcript dari user lalu menghapus file lama
        file_transcript = request.files['transcript']
        print(file_transcript.filename)
        if file_transcript:
            exch_info.transcript_telu = handle_file_upload(
                file_transcript, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{file_transcript.filename}'
            )

        # Menggunakan fungsi untuk menambah file transcript_at_iisma dari user lalu menghapus file lama
        file_transcript_iisma = request.files['transcript_at_iisma']
        print(file_transcript_iisma.filename)
        if file_transcript_iisma:
            exch_info.transcript_exch = handle_file_upload(
                file_transcript_iisma, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{file_transcript_iisma.filename}'
            )

        # Menggunakan fungsi untuk menambah file letter_of_Acc dari user lalu menghapus file lama
        letter_of_Acc = request.files['letter_of_Acc']
        if letter_of_Acc:
            exch_info.letter_of_Acc = handle_file_upload(
                letter_of_Acc, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{letter_of_Acc.filename}'
            )

        # Menggunakan fungsi untuk menambah file others_docs dari user lalu menghapus file lama
        others_docs = request.files['others_docs']
        if others_docs:
            exch_info.others_docs = handle_file_upload(
                others_docs, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{others_docs.filename}'
            )

        db.session.commit()
        return redirect(url_for('iisma_view', user_id=user_id))
    
    @app.route('/student-exchange', methods=['GET', 'POST'])
    def exchange():
        """
        Routes untuk masuk ke halaman form program exchange
        """
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))

        user_id = session.get('id')
        if request.method == 'GET':
            student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
            iisma_inf = db.session.query(ExchangeOutbound).filter(
                ExchangeOutbound.nim == user_id,
                ExchangeOutbound.jenis_exchange == 'student_exchange').first()
            print(iisma_inf)
            return render_template('exchange.html', student_inf=student_inf, iisma_inf=iisma_inf)
        
        elif request.method == 'POST':
            # Check apakah user sudah pernah mendaftar iisma atau belum
            exch_info = db.session.query(ExchangeOutbound).filter(
                ExchangeOutbound.nim == user_id,
                ExchangeOutbound.jenis_exchange == 'student_exchange').first()
            if exch_info is None:

                # Ambil nilai dari form, None jika tidak diisi
                intake_value = request.form.get('intake', '').strip()  # Ambil nilai atau kosong
                print(intake_value)
                from_date_value = request.form.get('from', '').strip()
                until_value = request.form.get('until', '').strip()
                update_gpa_value = request.form.get('latest_update_iisma', '').strip()

                # Parsing hanya jika nilai tidak kosong
                intake_year_value = datetime.strptime(intake_value, '%Y-%m-%d').year if intake_value else None
                print(intake_year_value)
                intake_value = datetime.strptime(intake_value, '%Y-%m-%d').date() if intake_value else None
                from_date_value = datetime.strptime(from_date_value, '%Y-%m-%d').date() if from_date_value else None
                until_value = datetime.strptime(until_value, '%Y-%m-%d').date() if until_value else None
                update_gpa_value = datetime.strptime(update_gpa_value, '%Y-%m-%d').date() if update_gpa_value else None

                new_exch_info = ExchangeOutbound(
                    id_= str(user_id)+"_student_exchange",
                    jenis_exchange = 'student_exchange',
                    nim=user_id,
                    location = request.form['location'],
                    univ = request.form['univ'],
                    status=request.form['status'],
                    intake_year=intake_year_value,
                    intake=intake_value,
                    from_date=from_date_value,
                    until=until_value,
                    sem_at_telu=request.form['semester'],
                    sem_at_exch=request.form['semester_at_iisma'],
                    gpa=request.form['gpa_at_iisma'],
                    update_gpa=update_gpa_value
                )

                db.session.add(new_exch_info)
                db.session.commit()
            else:
                print("USER SUDAH PERNAH TERDAFTAR DI EXCHANGE")
                exch_info.status = request.form['status']
                exch_info.location = request.form['location']
                exch_info.univ = request.form['univ']
                intake = datetime.strptime(request.form['intake'], '%Y-%m-%d').date()
                exch_info.intake = intake
                exch_info.intake_year = intake.year
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
                
                # Menggunakan fungsi untuk menambah file transcript dari user lalu menghapus file lama
                file_transcript = request.files['transcript']
                print(file_transcript.filename)
                if file_transcript:
                    exch_info.transcript_telu = handle_file_upload(
                        file_transcript, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{file_transcript.filename}'
                    )

                # Menggunakan fungsi untuk menambah file transcript_at_iisma dari user lalu menghapus file lama
                file_transcript_iisma = request.files['transcript_at_iisma']
                print(file_transcript_iisma.filename)
                if file_transcript_iisma:
                    exch_info.transcript_exch = handle_file_upload(
                        file_transcript_iisma, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{file_transcript_iisma.filename}'
                    )

                # Menggunakan fungsi untuk menambah file letter_of_Acc dari user lalu menghapus file lama
                letter_of_Acc = request.files['letter_of_Acc']
                if letter_of_Acc:
                    exch_info.letter_of_Acc = handle_file_upload(
                        letter_of_Acc, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{letter_of_Acc.filename}'
                    )

                # Menggunakan fungsi untuk menambah file others_docs dari user lalu menghapus file lama
                others_docs = request.files['others_docs']
                if others_docs:
                    exch_info.others_docs = handle_file_upload(
                        others_docs, 
                        f'static/uploads/{exch_info.transcript_telu}', 
                        f'static/uploads/{others_docs.filename}'
                    )

                db.session.commit()
            
            return redirect(url_for('exchange'))

    @app.route('/student-exchange-admin', methods=['GET'])
    def exchange_admin():
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        
        # stud_iisma = db.session.query(ExchangeOutbound).all()
        stud_exchange = db.session.query(ExchangeOutbound, Mahasiswa).join(
            Mahasiswa, ExchangeOutbound.nim == Mahasiswa.nim).filter(
                ExchangeOutbound.jenis_exchange == "student_exchange"
            ).all()
        return render_template('exchange_admin.html', stud_exchange=stud_exchange)

    @app.route('/student-exchange-admin/<int:user_id>', methods=['GET'])
    def exchange_view(user_id):
        username = session.get('username')
        if username is None:
            return redirect(url_for('home_page'))
        bpp_inf = db.session.query(Bpp).filter(Bpp.id_program == str(user_id)+"_student_exchange").first()
        student_inf = db.session.query(Mahasiswa).filter(Mahasiswa.nim == user_id).first()
        iisma_inf = db.session.query(ExchangeOutbound).filter(
            ExchangeOutbound.nim == user_id,
            ExchangeOutbound.jenis_exchange == 'student_exchange'
            ).first()
        return render_template('exchange.html', student_inf=student_inf, iisma_inf=iisma_inf, bpp_inf=bpp_inf)

    @app.route('/student-exchange-admin/<int:user_id>/update', methods=['POST'])
    def exchange_update(user_id):
        bpp_inf = db.session.query(Bpp).filter(Bpp.id_program == str(user_id)+"_student_exchange").first()
        if bpp_inf:
            print("sudah pernah diisi --> POST")
            bpp_inf.discount=request.form['discount']
            bpp_inf.period=request.form['period_discount']
            bpp_inf.notes=request.form['notes']
        else:
            print("Belum pernah diisi --> POST")
            new_bpp = Bpp(
                nim=user_id,
                id_program=str(user_id)+"_student_exchange",
                discount=request.form['discount'],
                period=request.form['period_discount'],
                notes=request.form['notes']
            )
            db.session.add(new_bpp)
        
        # Ambil nilai dari form, None jika tidak diisi
        intake_value = request.form.get('intake', '').strip()  # Ambil nilai atau kosong
        from_date_value = request.form.get('from', '').strip()
        until_value = request.form.get('until', '').strip()
        update_gpa_value = request.form.get('latest_update_iisma', '').strip()

        # Parsing hanya jika nilai tidak kosong
        intake_year_value = datetime.strptime(intake_value, '%Y-%m-%d').year if intake_value else None
        intake_value = datetime.strptime(intake_value, '%Y-%m-%d').date() if intake_value else None
        from_date_value = datetime.strptime(from_date_value, '%Y-%m-%d').date() if from_date_value else None
        until_value = datetime.strptime(until_value, '%Y-%m-%d').date() if until_value else None
        update_gpa_value = datetime.strptime(update_gpa_value, '%Y-%m-%d').date() if update_gpa_value else None
        
        exch_info = db.session.query(ExchangeOutbound).filter(
                ExchangeOutbound.nim == user_id,
                ExchangeOutbound.jenis_exchange == 'student_exchange').first()
        
        exch_info.status = request.form['status']
        exch_info.location = request.form['location']
        exch_info.univ = request.form['univ']
        exch_info.intake_year = intake_year_value
        exch_info.intake = intake_value
        exch_info.from_date = from_date_value
        exch_info.until = until_value
        exch_info.sem_at_telu = request.form['semester']
        # exch_info.semester_telu = request.form['sem_at_telu']
        # exch_info.gpa = request.form['gpa']
        exch_info.sem_at_exch = request.form['semester_at_iisma']
        exch_info.gpa = request.form['gpa_at_iisma']
        exch_info.update_gpa = update_gpa_value
        
        # Menggunakan fungsi untuk menambah file transcript dari user lalu menghapus file lama
        file_transcript = request.files['transcript']
        print(file_transcript.filename)
        if file_transcript:
            exch_info.transcript_telu = handle_file_upload(
                file_transcript, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{file_transcript.filename}'
            )

        # Menggunakan fungsi untuk menambah file transcript_at_iisma dari user lalu menghapus file lama
        file_transcript_iisma = request.files['transcript_at_iisma']
        print(file_transcript_iisma.filename)
        if file_transcript_iisma:
            exch_info.transcript_exch = handle_file_upload(
                file_transcript_iisma, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{file_transcript_iisma.filename}'
            )

        # Menggunakan fungsi untuk menambah file letter_of_Acc dari user lalu menghapus file lama
        letter_of_Acc = request.files['letter_of_Acc']
        if letter_of_Acc:
            exch_info.letter_of_Acc = handle_file_upload(
                letter_of_Acc, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{letter_of_Acc.filename}'
            )

        # Menggunakan fungsi untuk menambah file others_docs dari user lalu menghapus file lama
        others_docs = request.files['others_docs']
        if others_docs:
            exch_info.others_docs = handle_file_upload(
                others_docs, 
                f'static/uploads/{exch_info.transcript_telu}', 
                f'static/uploads/{others_docs.filename}'
            )
        db.session.commit()
        return redirect(url_for('exchange_view', user_id=user_id))
    
    @app.route('/download/<filename>')
    def download_file(filename):
        dir_upload = current_app.config['UPLOAD_DIRECTORY']
        return send_from_directory(dir_upload, filename)