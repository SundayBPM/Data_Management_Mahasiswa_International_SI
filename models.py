from sqlalchemy import Column, Integer, String, Date, ForeignKey, create_engine, Text
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, nullable=False)

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    nim = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    nama = db.Column(db.String, nullable=False)
    wali = db.Column(db.String, nullable=False)
    angkatan = db.Column(db.Integer, nullable=False)
    kode_angkatan = db.Column(db.String, nullable=False)
    tanggal_masuk = db.Column(db.Date, nullable=False)
    tanggal_keluar = db.Column(db.Date, nullable=True)
    gpa = db.Column(db.String, nullable=False)

class ExchangeOutbound(db.Model):
    __tablename__ = 'exchange_outbound'
    id_ = db.Column(db.String, primary_key=True)
    nim = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim', name='fk_exchange_outbound_nim'))
    status = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    univ = db.Column(db.String, nullable=True)
    intake_year = db.Column(db.String, nullable=True)
    intake = db.Column(db.Date, nullable=True)
    from_date = db.Column(db.Date, nullable=True)
    until = db.Column(db.Date, nullable=True)
    letter_of_Acc = db.Column(db.String, nullable=True)
    sem_at_telu = db.Column(db.String, nullable=True)
    sem_at_exch = db.Column(db.String, nullable=True)
    gpa = db.Column(db.String, nullable=True)
    update_gpa = db.Column(db.Date, nullable=True)
    transcript_telu = db.Column(db.String, nullable=True)
    transcript_exch = db.Column(db.String, nullable=True)
    jenis_exchange = db.Column(db.String, nullable=True)
    student_detail = db.Column(db.String, nullable=True)
    others_docs = db.Column(db.String, nullable=True)
    
    def to_dict(self):
        return {
            "nim":self.nim,
            "status":self.status,
            "location":self.location,
            "intake_year":self.intake_year,
            "intake":self.intake,
            "from_date":self.from_date,
            "until":self.until,
            "jenis_exchange":self.jenis_exchange
        }

class Bpp(db.Model):
    __tablename__ = 'bpp'
    nim = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim'))
    id_program = db.Column(db.String, nullable=True, primary_key=True)
    discount = db.Column(db.Integer, nullable=True)
    period = db.Column(db.String, nullable=True)
    notes = db.Column(db.String, nullable=True)