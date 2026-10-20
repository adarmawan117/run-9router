/**
 * auto-mitm.js
 * Otomatisasi startup 9Router, bypass password, dan aktivasi MITM Proxy untuk Antigravity.
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { exec } = require('child_process');

const ROUTER_PORT = 20128;
const ROUTER_HOST = '127.0.0.1';
const DATA_DIR = process.env.DATA_DIR || path.join(process.env.APPDATA || '', '9router');

function getCliToken() {
  try {
    const machineIdFile = path.join(DATA_DIR, 'machine-id');
    const cliSecretFile = path.join(DATA_DIR, 'auth', 'cli-secret');
    if (!fs.existsSync(machineIdFile) || !fs.existsSync(cliSecretFile)) {
      return '';
    }
    const raw = fs.readFileSync(machineIdFile, 'utf8').trim();
    const secret = fs.readFileSync(cliSecretFile, 'utf8').trim();
    if (!raw || !secret) return '';
    return crypto.createHash('sha256').update(raw + '9r-cli-auth' + secret).digest('hex').substring(0, 16);
  } catch (e) {
    return '';
  }
}

function request(method, reqPath, body = null) {
  return new Promise((resolve, reject) => {
    const token = getCliToken();
    const req = http.request({
      hostname: ROUTER_HOST,
      port: ROUTER_PORT,
      path: reqPath,
      method: method,
      headers: {
        'Content-Type': 'application/json',
        'x-9r-cli-token': token
      },
      timeout: 10000
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = data ? JSON.parse(data) : {};
          resolve({ status: res.statusCode, data: parsed });
        } catch (err) {
          resolve({ status: res.statusCode, raw: data });
        }
      });
    });

    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`Timeout menghubungi ${reqPath}`));
    });

    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

function sleep(ms) {
  return new Promise(res => setTimeout(res, ms));
}

async function isRouterReady() {
  try {
    const res = await request('GET', '/api/version');
    return res.status === 200;
  } catch (e) {
    return false;
  }
}

async function launch9Router() {
  return new Promise((resolve) => {
    exec('powershell -WindowStyle Hidden -Command "Start-Process 9router.cmd -ArgumentList \'--tray\' -WindowStyle Hidden"', {
      windowsHide: true
    }, (error) => {
      resolve(!error);
    });
  });
}

async function main() {
  console.log('====================================================');
  console.log('        9ROUTER & ANTIGRAVITY AUTO-STARTER          ');
  console.log('====================================================');

  // 1. Memeriksa apakah 9Router sudah berjalan
  process.stdout.write('[1/4] Memeriksa status 9Router... ');
  let ready = await isRouterReady();

  if (!ready) {
    console.log('\n      -> 9Router belum aktif. Menjalankan di latar belakang (--tray)...');
    await launch9Router();

    const maxWaitMs = 30000;
    const start = Date.now();
    let connected = false;

    while (Date.now() - start < maxWaitMs) {
      await sleep(1000);
      process.stdout.write('.');
      if (await isRouterReady()) {
        connected = true;
        break;
      }
    }

    if (!connected) {
      console.log('\n[GAGAL] 9Router tidak merespon dalam 30 detik.');
      process.exit(1);
    }
    console.log('\n      -> 9Router web server aktif!');
  } else {
    console.log('AKTIF (Port 20128)');
  }

  // 2. Bypass Password (requireLogin: false)
  process.stdout.write('[2/4] Mengatur bypass password (requireLogin: false)... ');
  try {
    await request('PATCH', '/api/settings', { requireLogin: false });
    console.log('SUKSES');
    console.log('      -> Login dashboard dinonaktifkan (bebas buka web tanpa password).');
  } catch (err) {
    console.log('LEWATI (' + err.message + ')');
  }

  // 3. Memeriksa & Menghidupkan MITM Proxy + DNS Antigravity
  process.stdout.write('[3/4] Menyiapkan MITM Proxy untuk Antigravity... ');
  try {
    let mitmStatus = await request('GET', '/api/cli-tools/antigravity-mitm');
    let data = mitmStatus.data || {};

    if (!data.running) {
      console.log('\n      -> Memulai MITM Server (Port 443)...');
      let apiKey = 'sk_9router';
      try {
        const keysRes = await request('GET', '/api/keys');
        if (keysRes.data?.keys?.length > 0) {
          apiKey = keysRes.data.keys[0].key;
        }
      } catch (e) {}

      await request('POST', '/api/cli-tools/antigravity-mitm', {
        apiKey: apiKey,
        forceKillPort443: true
      });
    } else {
      console.log('SERVER SEDANG BERJALAN');
    }

    // Pastikan sertifikat root CA terpercaya
    if (data.certTrusted === false) {
      console.log('      -> Memasang sertifikat Root CA...');
      await request('PATCH', '/api/cli-tools/antigravity-mitm', {
        tool: 'antigravity',
        action: 'trust-cert'
      });
    }

    // Pastikan DNS redirection untuk Antigravity aktif
    if (!data.dnsStatus?.antigravity) {
      console.log('      -> Mengaktifkan DNS redirection untuk Antigravity...');
      await request('PATCH', '/api/cli-tools/antigravity-mitm', {
        tool: 'antigravity',
        action: 'enable'
      });
    }
  } catch (err) {
    console.log('\n[PERINGATAN] Gagal inisialisasi MITM: ' + err.message);
  }

  // 4. Verifikasi status akhir MITM
  process.stdout.write('[4/4] Memverifikasi status akhir MITM Proxy... ');
  const verifyStart = Date.now();
  let mitmReady = false;
  let lastData = null;

  while (Date.now() - verifyStart < 15000) {
    try {
      const res = await request('GET', '/api/cli-tools/antigravity-mitm');
      lastData = res.data || {};
      if (lastData.running && lastData.dnsStatus?.antigravity) {
        mitmReady = true;
        break;
      }
    } catch (e) {}
    await sleep(800);
    process.stdout.write('.');
  }

  if (mitmReady) {
    console.log(' SIAP!');
    console.log(`      -> Status: MITM Server Running (PID: ${lastData.pid})`);
    console.log('      -> Antigravity DNS: AKTIF (cloudcode-pa redirected ke 127.0.0.1)');
    console.log('====================================================');
    console.log('[SUKSES] Antigravity & 9Router siap digunakan!');
    console.log('Jendela ini akan menutup otomatis dalam 3 detik...');
    console.log('====================================================');
    await sleep(3000);
    process.exit(0);
  } else {
    console.log('\n[PERINGATAN] MITM belum terkonfirmasi aktif sepenuhnya.');
    console.log('Detail status saat ini:', JSON.stringify(lastData, null, 2));
    console.log('Tekan Ctrl+C untuk menutup atau periksa dashboard 9Router.');
    await sleep(5000);
    process.exit(1);
  }
}

main().catch((err) => {
  console.error('\n[FATAL ERROR]', err);
  process.exit(1);
});
