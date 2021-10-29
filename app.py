from flask import Flask, render_template, redirect, sessions, url_for, session
from flask.scaffold import F
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref, selectin_polymorphic
from flask_bcrypt import Bcrypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import InputRequired
from flask_bootstrap import Bootstrap
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "#$sdfsdfsd234g"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/db.klinik'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
bootstrap = Bootstrap(app)

class Login(FlaskForm):
    username = StringField('', validators=[InputRequired()], render_kw={'autofocus' :True, 'placeholder' : 'Username'})
    password = PasswordField('', validators=[InputRequired()], render_kw={'autofocus' :True, 'placeholder' : 'Password'})
    level = SelectField('', validators=[InputRequired()], choices=[('Admin', 'Admin'), ('Dokter', 'Dokter'), 
                                                                    ('Administrasi', 'Administrasi')])

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.Text)
    level = db.Column(db.String(100))
    usernya = db.relationship('Pasien', backref=db.backref('user', lazy=True))

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
    supliernya = db.relationship('Obat', backref=db.backref('suplier', lazy=True))

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
    db.relationship('pasien', backref=db.backref('pendaftaran', lazy=True))

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
    return redirect(url_for('login'))

def login_dulu(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'login' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
        return_wrap

@app.route('/login')
def login():
    form = Login()
    if form.validate_on_submit():
        user = User.query.filter_by(user=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data) and user.level == form.level.data:
                session['login'] = True
                session['id'] = user.id
                session['level'] = user.level
                return redirect(url_for('dashboard'))
        pesan = "Username atau Password anda salah"
        return render_template("login.html", pesan=pesan, form=form)
    return render_template('login.html', form=form)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)
 