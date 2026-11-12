import http from 'k6/http';
import { check, sleep } from 'k6';
import { SharedArray } from 'k6/data';
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.2/index.js';

// Cargar y parametrizar datos desde CSV de forma nativa
const usersData = new SharedArray('Credenciales Usuarios', function () {
  const fileContent = open('../data/users.csv');
  const lines = fileContent.trim().split('\n');
  const records = [];
  
  // Omitir cabecera (i = 1)
  for (let i = 1; i < lines.length; i++) {
    const line = lines[i].trim();
    if (line) {
      const [username, password] = line.split(',');
      records.push({
        username: username.trim(),
        password: password.trim(),
      });
    }
  }
  return records;
});

// Configuración de la prueba de carga
export const options = {
  scenarios: {
    login_load_test: {
      executor: 'constant-arrival-rate',
      rate: 22, // 22 TPS (garantiza superar el requisito mínimo de 20 TPS)
      timeUnit: '1s',
      duration: '30s', // Duración de la prueba
      preAllocatedVUs: 25,
      maxVUs: 60,
    },
  },
  thresholds: {
    // 1. Tiempo de respuesta permitido: máximo 1.5 segundos
    http_req_duration: ['max<1500', 'p(95)<1500'],
    // 2. Tasa de error aceptable: menor al 3% del total de peticiones
    http_req_failed: ['rate<0.03'],
    // 3. Tasa de checks exitosos >= 97%
    checks: ['rate>0.97'],
    // 4. Rendimiento mínimo requerido: >= 20 TPS
    http_reqs: ['rate>=20'],
  },
};

export default function () {
  // Selección de usuario del pool CSV
  const randomIndex = Math.floor(Math.random() * usersData.length);
  const user = usersData[randomIndex];

  const url = 'https://fakestoreapi.com/auth/login';
  const payload = JSON.stringify({
    username: user.username,
    password: user.password,
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
      'User-Agent': 'K6-LoadTest-Performance-QA/1.0',
    },
    timeout: '60s',
  };

  const response = http.post(url, payload, params);

  // Validaciones (Checks)
  check(response, {
    'Status code es 200 o 201': (r) => r.status === 200 || r.status === 201,
    'Token de autenticacion recibido': (r) => {
      try {
        const body = r.json();
        return body && body.token && body.token.length > 0;
      } catch (e) {
        return false;
      }
    },
    'Tiempo de respuesta < 1500ms': (r) => r.timings.duration < 1500,
  });
}

// Generación de reportes
export function handleSummary(data) {
  return {
    '../reports/summary.txt': textSummary(data, { indent: ' ', enableColors: false }),
    '../reports/summary.json': JSON.stringify(data, null, 2),
    stdout: textSummary(data, { indent: ' ', enableColors: true }),
  };
}
