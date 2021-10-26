from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import selectin_polymorphic
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config['SECRET_KEY'] = "#$sdfsdfsd234g"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/db.klinik'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.Text)
    level = db.Column(db.String(100))

    def __init__(self, username, password, level):
        self.username = username
        if password !='':
            self.password = bcrypt.generate_password_hash(password).decode('UTF-8')
        self.level = level

class Dokter(db.Model):
    __tablename__ = 'dokter'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150))
    jadwal = db.Column(db.Text)
    
    def __init__(self, nama, jadwal):
        self.nama = nama
        self.jadwal = jadwal

class Suplier(db.Model):
    __tablename__ = 'suplier'
    id = db.Column(db.Integer, primary_key=True)
    perusahaan = db.Column(db.String(200))
    kontak = db.Column(db.String(100))
    alamat = db.Column(db.Text)

    def __init__(self, perusahaan, kontak, alamat):
        self.perusahaan = perusahaan
        self.kontak = kontak
        self.alamat = alamat

class Obat(db.Model):
    __tablename__ = 'obat'
    id = db.Column(db.Integer, primary_key=True)
    namaObat = db.Column(db.String(150))
    jenisObat = db.Column(db.String(150))
    harga_beli = db.Column(db.Integer)
    harga_jual = db.Column(db.Integer)
    suplier_id = db.Column(db.Integer, db.ForeignKey('suplier.id'))

    def __init__(self, namaObat, jenisObat, harga_beli, harga_jual, suplier_id):
        self.namaObat = namaObat
        self.jenisObat = jenisObat
        self.harga_beli = harga_beli
        self.harga_jual = harga_jual
        self.suplier_id = suplier_id

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150))
    tl = db.Column(db.String(150))
    tgl_lahir = db.Column(db.String(150))
    jk = db.Column(db.String(150))
    profesi = db.Column(db.String(100))
    alamat = db.Column(db.Text)
    keterangan = db.Column(db.String(100))

    def __init__(self, nama, tl, tlg_lahir, jk, profesi, alamat, keterangan):
        self.nama = nama
        self.tl = tl
        self.tgl_lahir = tlg_lahir
        self.jk = jk
        self.profesi = profesi 
        self.alamat = alamat
        self.keterangan = keterangan

class Pasien(db.Model):
    __tablename__ = 'pasien'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(150))
    keluhan = db.Column(db.Text)
    diagnosa = db.Column(db.String(150))
    resep = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pendaftaran_id = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'))
    alamat = db.Column(db.Text)

    def __init__(self, nama, keluhan, diagnosa, resep, user_id, pendaftaran_id, alamat):
        self.nama = nama
        self.keluhan = keluhan
        self.diagnosa = diagnosa
        self.resep = resep
        self.user_id = user_id
        self.pendaftaran_id = pendaftaran_id
        self.alamat = alamat

db.create_all()

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
