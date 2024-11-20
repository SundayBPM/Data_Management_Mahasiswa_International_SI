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
    tanggal_keluar = db.Column(db.Date, nullable=False)
    gpa = db.Column(db.String, nullable=False)
    esyp = db.Column(db.String, nullable=False)    

class ExchangeOutbound(db.Model):
    __tablename__ = 'exchange_outbound'
    nim = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim'), primary_key=True)
    student_folder = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    intake_year = db.Column(db.Date, nullable=True)
    intake = db.Column(db.Date, nullable=True)
    from_date = db.Column(db.Date, nullable=True)
    until = db.Column(db.Date, nullable=True)
    sem_at_telu = db.Column(db.String, nullable=True)
    sem_at_exch = db.Column(db.String, nullable=True)
    gpa = db.Column(db.String, nullable=True)
    update_gpa = db.Column(db.Date, nullable=True)
    transcript_telu = db.Column(db.String, nullable=True)
    transcript_exch = db.Column(db.String, nullable=True)
    folder = db.Column(db.String, nullable=True)
    jenis_exchange = db.Column(db.String, nullable=True)
    student_detail = db.Column(db.String, nullable=True)

class Bpp(db.Model):
    __tablename__ = 'bpp'
    nim = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim'), primary_key=True)
    discount = db.Column(db.Integer, nullable=True)
    period = db.Column(db.Date, nullable=True)
    notes = db.Column(db.String, nullable=True)