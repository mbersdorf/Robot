// Stellt die WebSocket-Verbindung her
var socket = io();


document.addEventListener('DOMContentLoaded', () => {
  setupHoldButton('btn1', 1);
  setupHoldButton('btn2', 2);
  setupHoldButton('btn3', 3);
  setupHoldButton('btn4', 4);

  setupLinButton('btn_out', 'out');
  setupLinButton('btn_in', 'in');

  // setupSwitch('toggleSwitch', 5); 

const speedSlider = document.getElementById('speedSlider');
const speedValue = document.getElementById('speedValue');

speedSlider.addEventListener('input', () => {
  speedValue.textContent = `${speedSlider.value}%`;
  sendSpeed(speedSlider.value);
});
});


function controlLED(led, action) {
  socket.emit('led_control', { led: led.toString(), action: action });
}

function sendSpeed(value) {
  socket.emit('set_speed', { speed: value });
}

function setupHoldButton(buttonId, ledNumber) {
  const btn = document.getElementById(buttonId);
    console.log("Button gefunden:", btn?.id); // Debug

  if (!btn) {
    console.error("Button nicht gefunden:", buttonId);
    return;
  }

  // Maussteuerung
  btn.addEventListener('mousedown', () => controlLED(ledNumber, 'on'));
  btn.addEventListener('mouseup', () => controlLED(ledNumber, 'off'));
  btn.addEventListener('mouseleave', () => controlLED(ledNumber, 'off'));

  // Touchsteuerung (Mobile)
  btn.addEventListener('touchstart', (e) => {
    e.preventDefault(); // verhindert Textkopieren oder Scrollen
    controlLED(ledNumber, 'on');
  });

  btn.addEventListener('touchend', (e) => {
    e.preventDefault();
    controlLED(ledNumber, 'off');
  });
}

function setupLinButton(buttonId, direction) {
  const btn = document.getElementById(buttonId);
    console.log("Button gefunden:", btn?.id); // Debug

  if (!btn) {
    console.error("Button nicht gefunden:", buttonId);
    return;
  }

  // Maussteuerung
  btn.addEventListener('mousedown', () => controlLin(direction, 'on'));
  btn.addEventListener('mouseup', () => controlLin(direction, 'off'));
  btn.addEventListener('mouseleave', () => controlLin(direction, 'off'));

  // Touchsteuerung (Mobile)
  btn.addEventListener('touchstart', (e) => {
    e.preventDefault(); // verhindert Textkopieren oder Scrollen
    controlLin(direction, 'on');
  });

  btn.addEventListener('touchend', (e) => {
    e.preventDefault();
    controlLin(direction,'off');
  });
}


function controlWalze(action) {
    socket.emit('walze_control', {
        action: action
    });
}

function controlWasser(action) {
    socket.emit('wasser_control', {
        action: action
    });
}

  function controlMotor(action) {
    socket.emit('motor_control', {
        action: action
    });
  }

  function controlLin(direction, action) {
    socket.emit('Lin_control', {
        direction: direction.toString(), action: action
    });
  }

// Temperaturanzeige empfangen & anzeigen
socket.on('temperature_update', function(data) {
    document.getElementById('temp').textContent = data.value.toFixed(2) + " °C";
    
    // var temp = data.value;
    // if (temp > 30) {
    //   alert("Warnung: Temperatur über 30°C!");
    // }
});

// Event empfangen
  socket.on('movement_status', data => {
      document.getElementById('status').innerText = data.status;
  });

  socket.on('valve_status', data => {
      document.getElementById('valvestatus').innerText = data.valvestatus;
  });
  
  socket.on('brush_status', data => {
      document.getElementById('brushstatus').innerText = data.brushstatus;
  });
  
  socket.on('lin_status', data => {
      document.getElementById('linstatus').innerText = data.linstatus;
  });




