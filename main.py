from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
import logging
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)

class Utente(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    cognome = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    telefono = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    tipo_utente = db.Column(db.String(50), nullable=False)

    def __init__(self, nome, cognome, email, telefono, password, tipo_utente):
        self.nome = nome
        self.cognome = cognome
        self.email = email
        self.telefono = telefono
        self.password = password
        self.tipo_utente = tipo_utente

    def __repr__(self):
        return f"Utente('{self.nome}', '{self.cognome}', '{self.email}', '{self.telefono}', '{self.password}', '{self.tipo_utente}')"

class Evento(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(20))
    luogo = db.Column(db.String(50))
    descrizione = db.Column(db.String(255))
    data_inizio = db.Column(db.String(100))
    data_fine = db.Column(db.String(100))

    def __init__(self, nome, luogo, descrizione, data_inizio, data_fine):
        self.nome = nome    
        self.luogo = luogo
        self.descrizione = descrizione
        self.data_inizio = data_inizio
        self.data_fine = data_fine

class Partecipazione(db.Model):
    __tablename__ = 'partecipazione'
    id_utente = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    id_evento = db.Column(db.Integer, db.ForeignKey('evento.id'), primary_key=True)
    user = db.relationship('Utente', backref='partecipazioni')
    evento = db.relationship('Evento', backref='partecipazioni')

def connect_db():
    return sqlite3.connect('database.db')

def get_db():
    if not hasattr(g, '_database'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/')
def hello_world():
    return render_template('login.html')

@app.route("/Home")
def home(): 
    return render_template("home.html")

@app.route("/Registrazione")
def registrati():
    return render_template("registrazione.html")

@app.route("/organizzatore_index")
def organizzatore_index():
    user_id = session.get('user_id')
    logging.debug("User ID from session: %s", user_id) 
    if not user_id:
        return redirect(url_for('login'))
    
    utente = Utente.query.get(user_id)
    if not utente:
        return redirect(url_for('login'))
    
    return render_template('organizzatore_index.html', utente=utente)

@app.route("/user_index")
def user_index():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    
    utente = Utente.query.get(user_id)
    if not utente:
        return redirect(url_for('login'))
    
    eventi = Evento.query.all()  
    logging.debug("Eventi dal database: %s", eventi)  


    eventi_con_testo_bottone = []
    for evento in eventi:
        partecipazione = Partecipazione.query.filter_by(id_utente=user_id, id_evento=evento.id).first()
        if partecipazione:
            testo_bottone = "Già partecipando"
            
        else:
            testo_bottone = "Partecipa"
        eventi_con_testo_bottone.append((evento, testo_bottone))
    
    return render_template('user_index.html', utente=utente, eventi_con_testo_bottone=eventi_con_testo_bottone)

@app.route('/Utenti')
def Utenti():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, nome, cognome FROM Users')
    rows = cursor.fetchall()
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
            logging.debug("User role: %s", utente.tipo_utente)  
            session['user_id'] = utente.id 
            if utente.tipo_utente == "organizzatore_eventi":
                return redirect(url_for('organizzatore_index'))
            elif utente.tipo_utente == "utente_base":
                return redirect(url_for('user_index'))
            else:
                return "Unknown role", 403
        else:
            return "Credenziali errate", 401
    else:
        return render_template("login.html")

@app.route("/crea_evento", methods=["POST"])
def crea_evento():
    nome_evento = request.form.get('nome_evento')
    luogo_evento = request.form.get('luogo_evento')
    descrizione = request.form.get('descrizione')
    data_inizio = request.form.get('data_inizio')
    data_fine = request.form.get('data_fine')

    if not nome_evento or not luogo_evento or not descrizione or not data_inizio or not data_fine:
        flash("Tutti i campi sono obbligatori", "error")
        return redirect(url_for('organizzatore_index'))

    nuovo_evento = Evento(nome=nome_evento, luogo=luogo_evento, descrizione=descrizione, data_inizio=data_inizio, data_fine=data_fine)
    db.session.add(nuovo_evento)
    db.session.commit()

    flash("Evento creato con successo!", "success")
    return redirect(url_for('organizzatore_index'))

@app.route("/partecipa/<int:evento_id>", methods=["POST"])
def partecipa(evento_id):
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    partecipazione = Partecipazione.query.filter_by(id_utente=user_id, id_evento=evento_id).first()
    if partecipazione:
        flash("Hai già partecipato a questo evento!", "error")
        return redirect(url_for('user_index'))

    nuova_partecipazione = Partecipazione(id_utente=user_id, id_evento=evento_id)
    db.session.add(nuova_partecipazione)
    db.session.commit()

    flash("Partecipazione registrata con successo!", "success")
    return redirect(url_for('user_index'))

if __name__ == '__main__':
    app.run(debug=True, port=5004)