
const form = document.getElementById('form');
const submitButton = document.getElementById('submit');

function confrontaPassword() {
  const password = document.getElementById('password').value;
  const confermaPassword = document.getElementById('conferma_password').value;
  if (password !== confermaPassword) {
    alert('Le password non coincidono');
  }
}

form.addEventListener('submit', (e) => {
  const form = document.getElementById('form');
  const submitButton = document.getElementById('submit');
  
  function confrontaPassword() {
    const password = document.getElementById('password').value;
    const confermaPassword = document.getElementById('conferma_password').value;
    if (password !== confermaPassword) {
      alert('Le password non coincidono');
    }
  }
  
  form.addEventListener('submit', (e) => {
  
    e.preventDefault();
  
    const nome = document.getElementById('nome').value;
    const cognome = document.getElementById('cognome').value;
    const email = document.getElementById('email').value;
    const telefono = document.getElementById('telefono').value;
    const password = document.getElementById('password').value;
    const passwordVerifica = document.getElementById('password_verifica').value;
    const tipoUtente = document.getElementById('tipo_utente').value;
    
    const dati = {
      nome,
      cognome,
      email,
      telefono,
      password,
      tipoUtente,
    };
  
    // Invia i dati al server utilizzando la fetch API
    ffetch('/registrazione', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: 'nome=' + encodeURIComponent(nome) + '&cognome=' + encodeURIComponent(cognome) + '&email=' + encodeURIComponent(email) + '&telefono=' + encodeURIComponent(telefono) + '&password=' + encodeURIComponent(password) + '&tipo_utente=' + encodeURIComponent(tipo_utente)
    })
  });

  e.preventDefault();

  const nome = document.getElementById('nome').value;
  const cognome = document.getElementById('cognome').value;
  const email = document.getElementById('email').value;
  const telefono = document.getElementById('telefono').value;
  const password = document.getElementById('password').value;
  const passwordVerifica = document.getElementById('password_verifica').value;
  const tipoUtente = document.getElementById('tipo_utente').value;
  
  const dati = {
    nome,
    cognome,
    email,
    telefono,
    password,
    tipoUtente,
  };

  // Invia i dati al server utilizzando la fetch API
  ffetch('/registrazione', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'nome=' + encodeURIComponent(nome) + '&cognome=' + encodeURIComponent(cognome) + '&email=' + encodeURIComponent(email) + '&telefono=' + encodeURIComponent(telefono) + '&password=' + encodeURIComponent(password) + '&tipo_utente=' + encodeURIComponent(tipo_utente)
  })
});