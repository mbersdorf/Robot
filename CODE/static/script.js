// Stellt die WebSocket-Verbindung her
var socket = io();


// Wird ausgeführt, sobald die Webseite geladen ist
document.addEventListener('DOMContentLoaded', () => {

  // Richtungssteuerung: Bewegung
  setupControlButton('btn_forward',  'forward',  controlMovement);
  setupControlButton('btn_backward', 'backward', controlMovement);
  setupControlButton('btn_turn_right', 'turn_right', controlMovement);
  setupControlButton('btn_turn_left', 'turn_left', controlMovement);

  // Linearbewegung (z. B. Ein-/Ausfahren)
  setupControlButton('btn_out', 'out', controlLin);
  setupControlButton('btn_in',  'in',  controlLin);

  // Slider für Geschwindigkeit
  const speedSlider = document.getElementById('speedSlider');
  const speedValue = document.getElementById('speedValue');

  // Aktualisiert Anzeige + sendet Speed an Server
  speedSlider.addEventListener('input', () => {
    speedValue.textContent = `${speedSlider.value}%`;
    sendSpeed(speedSlider.value);
  });
});



/**
 * Bindet Maus- und Touch-Events an einen Button
 * @param {string} buttonId - ID des Buttons
 * @param {string} direction - Richtung für die Steuerung
 * @param {function} controlFn - Funktion, die ausgeführt wird (z.B. controlMovement)
 */
function setupControlButton(buttonId, direction, controlFn) {

  const btn = document.getElementById(buttonId);
  console.log("Button gefunden:", btn?.id);

  if (!btn) {
    console.error("Button nicht gefunden:", buttonId);
    return;
  }

  // Mausevents
  btn.addEventListener('mousedown', () => controlFn(direction, 'on'));
  btn.addEventListener('mouseup', () => controlFn(direction, 'off'));
  btn.addEventListener('mouseleave', () => controlFn(direction, 'off'));

  // Touch-Events (für Smartphones/Tablets)
  btn.addEventListener('touchstart', (e) => {
    e.preventDefault();
    controlFn(direction, 'on');
  });

  btn.addEventListener('touchend', (e) => {
    e.preventDefault();
    controlFn(direction, 'off');
  });
}


/**
 * Sendet Bewegungssteuerung an den Server
 * @param {string} direction - Bewegungsrichtung
 * @param {string} action - Aktion ('on' oder 'off')
 */
function controlMovement(direction, action) {
  socket.emit('movement_control', { direction: direction.toString(), action: action });
}

/**
 * Sendet neue Geschwindigkeit an den Server
 * @param {number} value - Geschwindigkeit (0-100)
 */
function sendSpeed(value) {
  socket.emit('set_speed', { speed: value });
}


/**
 * Steuerung der Walze
 * @param {string} action - Aktion ('on' oder 'off')
 */
function controlWalze(action) {
    socket.emit('walze_control', {
        action: action
    });
}

/**
 * Steuerung der Wasserpumpe
 * @param {string} action - Aktion ('on' oder 'off')
 */
function controlWasser(action) {
    socket.emit('wasser_control', {
        action: action
    });
}

/**
 * Steuerung des Motors
 * @param {string} action - Aktion ('on' oder 'off')
 */
function controlMotor(action) {
    socket.emit('motor_control', {
        action: action
    });
}

/**
 * Linearbewegung (z.B. Ein-/Ausfahren)
 * @param {string} direction - Richtung ('in' oder 'out')
 * @param {string} action - Aktion ('on' oder 'off')
 */
function controlLin(direction, action) {
    socket.emit('Lin_control', {
        direction: direction.toString(),
        action: action
    });
}


// Empfang der Temperaturwerte
let popupShown = false;

socket.on('temperature_update', function(data) {
    const temp = data.value;

    document.getElementById('temp').textContent =
        temp.toFixed(2) + " °C";

    if (temp > 30 && !popupShown) {
        document.getElementById('popup').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
        popupShown = true;

        if (navigator.vibrate) {
            navigator.vibrate([200, 100, 300]);
        }
    }

    // Reset, wenn Temperatur wieder ok ist
    if (temp <= 28) {
        popupShown = false;
    }
});


// Bewegungstatus empfangen
socket.on('movement_status', data => {
    document.getElementById('status').innerText = data.status;
});

// Ventilstatus empfangen
socket.on('valve_status', data => {
    document.getElementById('valvestatus').innerText = data.valvestatus;
});

// Bürstenstatus empfangen
socket.on('brush_status', data => {
    document.getElementById('brushstatus').innerText = data.brushstatus;
});

// Linearstatus empfangen
socket.on('lin_status', data => {
    document.getElementById('linstatus').innerText = data.linstatus;
});



//  source.addEventListener('warning', function(e) {
//   document.getElementById('popup').style.display = 'block';
//   document.getElementById('overlay').style.display = 'block';
//   navigator.vibrate([200, 100, 300]);
//  }, false);


function closePopup() {
    const popup = document.getElementById('popup');
    const overlay = document.getElementById('overlay');

    if (popup) popup.style.display = 'none';
    if (overlay) overlay.style.display = 'none';
}

