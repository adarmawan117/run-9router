@echo off
title 9Router ^& Antigravity Auto-Starter
cd /d "%~dp0"

:: 1. Meminta izin Administrator secara otomatis (dibutuhkan untuk Port 443 & DNS hosts)
net session >nul 2>&1
if %errorLevel% neq 0 (
    powershell -Command "Start-Process cmd -ArgumentList '/c \"%~f0\"' -Verb RunAs"
    exit /b
)

:: 2. Mencari lokasi executable Node.js
where node >nul 2>&1
if %errorLevel% equ 0 (
    set "NODE_EXE=node"
) else (
    if exist "C:\Program Files\FlyEnv-Data\env\node\node.exe" (
        set "NODE_EXE=C:\Program Files\FlyEnv-Data\env\node\node.exe"
    ) else (
        echo [ERROR] Node.js tidak ditemukan di sistem!
        pause
        exit /b 1
    )
)

:: 3. Jalankan script otomatisasi (Bypass password, start 9Router & MITM proxy)
"%NODE_EXE%" "%~dp0auto-mitm.js"
if %errorLevel% neq 0 (
    echo.
    echo [GAGAL] Terjadi kendala saat menyalakan 9Router / MITM.
    pause
    exit /b 1
)

:: 4. Jendela CMD akan menutup otomatis setelah proses sukses
exit /b 0
