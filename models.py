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
    status = db.Column(db.String, nullable=False)
    student_folder = db.Column(db.String, nullable=False)
    esyp = db.Column(db.String, nullable=False)    

class ExchangeOutbound(db.Model):
    __tablename__ = 'exchange_outbound'
    nim = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim'), primary_key=True)
    student_folder = db.Column(db.Integer, nullable=False)
    intake = db.Column(db.Date, nullable=False)
    from_date = db.Column(db.Date, nullable=False)
    until = db.Column(db.Date, nullable=False)
    student_detail = db.Column(db.String, nullable=False)
    jenis_exchange = db.Column(db.String, nullable=False)

class Bpp(db.Model):
    __tablename__ = 'bpp'
    nim = db.Column(db.Integer, db.ForeignKey('mahasiswa.nim'), primary_key=True)
    discount = db.Column(db.Integer, nullable=False)
    period = db.Column(db.Date, nullable=False)
    notes = db.Column(db.String, nullable=False)