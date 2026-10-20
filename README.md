# 9Router & Antigravity Auto-Starter

Otomatisasi one-click untuk menjalankan **9Router**, melakukan bypass login password dashboard, mengaktifkan **MITM Proxy** (Port 443), serta memastikan DNS redirection untuk **Google Antigravity** aktif tanpa perlu membuka browser secara manual.

---

## 🚀 Latar Belakang Masalah & Solusi

### Masalah Sebelumnya
1. Pengguna harus menjalankan shortcut 9Router dan menyetujui prompt Administrator (UAC).
2. CMD langsung tertutup sebelum layanan MITM siap.
3. Pengguna terpaksa membuka browser ke `http://localhost:20128/dashboard/mitm`.
4. Harus mengetik password login dashboard secara manual.
5. Harus menunggu indikator MITM Proxy dan DNS Antigravity menyala hijau (*Running*). Jika membuka Antigravity sebelum MITM menyala, terjadi kendala *auth error*.

### Solusi Otomatisasi
* **Tanpa Buka Browser**: Semua komunikasi dilakukan via API internal lokal 9Router.
* **Bypass Password**: Menggunakan token internal CLI (`x-9r-cli-token`) serta mengatur `requireLogin: false` sehingga dashboard bebas diakses kapan saja tanpa prompt login.
* **Aktivasi MITM Otomatis**: Menjalankan MITM Server di port 443 dengan API Key aktif dan flag `forceKillPort443: true` untuk membebaskan port jika sebelumnya tertahan.
* **Verifikasi DNS & Sertifikat**: Mengaktifkan redirection `cloudcode-pa.googleapis.com -> 127.0.0.1` dan memverifikasi sertifikat Root CA.
* **Auto-Close CMD**: CMD menampilkan progres langkah demi langkah (1/4 hingga 4/4), memverifikasi kesehatan server, lalu otomatis menutup sendiri dalam 3 detik setelah siap.

---

## 📁 Struktur File

| File | Deskripsi |
| :--- | :--- |
| [`9Router.cmd`](9Router.cmd) | Batch script launcher utama dengan auto-elevation Administrator dan pendeteksi Node.js (FlyEnv / System PATH). |
| [`auto-mitm.js`](auto-mitm.js) | Engine otomatisasi Node.js murni (tanpa dependensi eksternal) untuk autentikasi CLI, bypass password, start MITM, dan verifikasi health check. |
| [`9Router.lnk`](9Router.lnk) | Shortcut Windows praktis siap pakai di Desktop atau Taskbar. |
| [`icon.ico`](icon.ico) / [`icon.png`](icon.png) | Aset ikon representatif untuk shortcut. |
| [`.gitignore`](.gitignore) | Mengabaikan file sistem sementara dan log runtime. |

---

## ⚙️ Tahapan Kerja Otomatisasi

```text
[Double-Click 9Router.cmd]
          │
          ▼
[Auto-Elevate Administrator (UAC)]
          │
          ▼
[1/4] Cek 9Router Web Server (Port 20128)
          ├── Jika belum aktif ──► Start 9router.cmd --tray (Hidden)
          └── Jika sudah aktif ──► Lanjut
          │
          ▼
[2/4] Bypass Password Dashboard
          └── Kirim PATCH /api/settings { requireLogin: false }
          │
          ▼
[3/4] Inisialisasi MITM Proxy
          ├── Ambil API Key akun aktif
          ├── Start MITM Proxy (Port 443, forceKillPort443)
          └── Aktifkan DNS Antigravity (cloudcode-pa -> 127.0.0.1)
          │
          ▼
[4/4] Verifikasi Status Akhir
          └── Polling status MITM & DNS sampai siap
          │
          ▼
[SUKSES] CMD otomatis tertutup dalam 3 detik. Antigravity siap digunakan!
```

---

## 📋 Prasyarat

1. **Sistem Operasi**: Windows 10 / 11 dengan hak Administrator.
2. **Node.js**: Terinstal secara global atau terintegrasi di `FlyEnv` (`C:\Program Files\FlyEnv-Data\env\node\node.exe`).
3. **9Router CLI**: Terinstal secara global (`npm i -g 9router`).

---

## 💻 Cara Penggunaan

1. Double-klik [`9Router.cmd`](9Router.cmd) atau shortcut [`9Router.lnk`](9Router.lnk).
2. Klik **Yes** pada dialog User Account Control (UAC) Windows.
3. Perhatikan status progres di jendela terminal (sekitar 2–4 detik).
4. Setelah muncul notifikasi `[SUKSES]`, jendela akan menutup sendiri.
5. Anda bisa langsung menggunakan **Google Antigravity** tanpa kendala autentikasi!

---

## 👨‍💻 Pengembang

Dikembangkan dengan ❤️ oleh [ADR Programming](https://www.instagram.com/adr_programming/)
