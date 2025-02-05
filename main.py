from flask import Flask, request, jsonify, g, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import logging


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

class Utente(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipo_utente= db.Column(db.String(50), nullable=False)

    def __init__(self, nome, cognome, email, telefono, password, tipo_utente):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.telefono = telefono
        self.password = password
        self.tipo_utente = tipo_utente

    def __repr__(self):
        return f"Utente('{self.nome}', '{self.cognome}', '{self.email}', '{self.telefono}', '{self.password}', '{self.tipo_utente_utente_utente}')";

def connect_db():
    return sqlite3.connect('database.db');

def get_db():
    if not hasattr(g, '_database'):
        g.sqlite_db = connect_db();  
    return g.sqlite_db;



@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close();

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route("/Home")
def home(): 
    return render_template("home.html")

@app.route("/Registrazione")
def registrati():
    return render_template("registrazione.html")


@app.route('/Utenti')
def Utenti():
    db = get_db();
    cursor = db.cursor();
    cursor.execute('SELECT id, nome, cognome FROM Users');
    rows = cursor.fetchall();
    output = ""
    for row in rows:
        output += f"<p>L'id dell'utente è {row[0]}. Il nome è {row[1]}. Il cognome è {row[2]}</p>"
    return output

@app.route('/registrazione', methods=['POST'])
def registrazione():
    dati = request.form
    nome = dati['nome']
    cognome = dati['cognome']
    email = dati['email']
    telefono = dati['telefono']
    password = dati['password']
    tipo_utente = dati['tipo_utente']

    # Crea un nuovo utente
    if Utente.query.filter_by(email=email).first():
        flash('La mail è già stata usata per un account', 'error')
        return redirect(url_for('registrati'))
    
    utente = Utente(nome=nome, cognome=cognome, email=email, telefono=telefono, password=password, tipo_utente=tipo_utente)
    db.session.add(utente)
    db.session.commit()

    flash('Utente registrato con successo', 'success')
    return redirect(url_for('login'))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        logging.debug("Form data: %s", request.form)
        dati = request.form
        email = dati.get('email')
        password = dati.get('password')
        
        if not email or not password:
            return "Email or password not provided", 400
        
        utente = Utente.query.filter_by(email=email, password=password).first()
        if utente:
            return render_template("benvenuto.html", utente=utente)
        else:
            return "Credenziali errate", 401
    else:
        return render_template("login.html")
    
if __name__ == '__main__':
    app.run(debug=True, port = 5001)