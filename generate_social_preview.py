import os
import base64
import subprocess
from PIL import Image

base_dir = os.path.dirname(os.path.abspath(__file__))
icon_path = os.path.join(base_dir, "icon.png")

with open(icon_path, "rb") as f:
    icon_b64 = base64.b64encode(f.read()).decode("utf-8")

# Prepare HTML template (1280 x 640 standard Open Graph ratio)
html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
  }}

  body {{
    width: 1280px;
    height: 640px;
    overflow: hidden;
    background-color: #07090e;
    background-image: 
      radial-gradient(circle at 82% 38%, rgba(255, 79, 56, 0.18) 0%, transparent 55%),
      radial-gradient(circle at 18% 25%, rgba(16, 185, 129, 0.10) 0%, transparent 48%),
      radial-gradient(rgba(255, 255, 255, 0.07) 1.2px, transparent 1.2px);
    background-size: 100% 100%, 100% 100%, 30px 30px;
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    color: #ffffff;
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 60px;
  }}

  /* LEFT HERO SECTION */
  .left-hero {{
    width: 540px;
    display: flex;
    flex-direction: column;
    z-index: 2;
  }}

  .top-tag-row {{
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
  }}

  .logo-icon {{
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    filter: drop-shadow(0 0 16px rgba(255, 79, 56, 0.8));
  }}

  .logo-icon img {{
    width: 100%;
    height: 100%;
    object-fit: contain;
  }}

  .category-pill {{
    display: inline-flex;
    align-items: center;
    padding: 6px 16px;
    border-radius: 9999px;
    border: 1px solid rgba(255, 79, 56, 0.45);
    background: rgba(255, 79, 56, 0.12);
    color: #ff7663;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
  }}

  .main-title {{
    font-size: 46px;
    font-weight: 800;
    letter-spacing: -1.2px;
    line-height: 1.15;
    color: #ffffff;
    margin-bottom: 16px;
  }}

  .main-title .highlight {{
    color: #FF4F38;
    text-shadow: 0 0 34px rgba(255, 79, 56, 0.55);
  }}

  .main-title .highlight-blue {{
    color: #38BDF8;
    text-shadow: 0 0 34px rgba(56, 189, 248, 0.45);
  }}

  .subtitle {{
    font-size: 17.5px;
    font-weight: 400;
    color: #94a3b8;
    line-height: 1.48;
    margin-bottom: 24px;
  }}

  .badge-row {{
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 20px;
  }}

  .feature-pill {{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 7px 13px;
    border-radius: 8px;
    font-size: 12.5px;
    font-weight: 600;
    background: #0d121d;
    border: 1px solid #1e293b;
  }}

  .pill-instant {{
    color: #fcd34d;
    border-color: rgba(245, 158, 11, 0.35);
    background: rgba(245, 158, 11, 0.08);
  }}

  .pill-bypass {{
    color: #6ee7b7;
    border-color: rgba(16, 185, 129, 0.35);
    background: rgba(16, 185, 129, 0.08);
  }}

  .pill-mitm {{
    color: #ff8e80;
    border-color: rgba(255, 79, 56, 0.35);
    background: rgba(255, 79, 56, 0.08);
  }}

  .dot {{
    width: 7px;
    height: 7px;
    border-radius: 50%;
  }}

  .dot-orange {{ background-color: #f59e0b; box-shadow: 0 0 8px #f59e0b; }}
  .dot-green {{ background-color: #10b981; box-shadow: 0 0 8px #10b981; }}
  .dot-coral {{ background-color: #FF4F38; box-shadow: 0 0 8px #FF4F38; }}

  .support-text {{
    font-size: 13.5px;
    color: #64748b;
    font-weight: 500;
    letter-spacing: 0.2px;
    margin-bottom: 22px;
  }}

  .divider {{
    width: 500px;
    height: 1px;
    background: linear-gradient(90deg, rgba(255, 255, 255, 0.22) 0%, rgba(255, 255, 255, 0.03) 100%);
    margin-bottom: 18px;
  }}

  .footer-text {{
    font-size: 14.5px;
    color: #94a3b8;
    font-weight: 400;
  }}

  .footer-text strong {{
    color: #f1f5f9;
    font-weight: 600;
  }}

  /* RIGHT CARD: AUTHENTIC WINDOWS CMD WINDOW */
  .right-preview {{
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 2;
  }}

  .cmd-window {{
    position: relative;
    width: 560px;
    border-radius: 12px;
    background: #090c13;
    border: 1.6px solid rgba(255, 79, 56, 0.6);
    box-shadow: 
      0 0 36px rgba(255, 79, 56, 0.24),
      0 20px 50px rgba(0, 0, 0, 0.88),
      inset 0 0 16px rgba(255, 79, 56, 0.03);
    overflow: hidden;
  }}

  .cmd-titlebar {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background: #181d28;
    border-bottom: 1px solid #242c3d;
  }}

  .cmd-title-left {{
    display: flex;
    align-items: center;
    gap: 8px;
  }}

  .cmd-icon-badge {{
    width: 17px;
    height: 17px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: #000;
    color: #ffffff;
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    font-weight: 700;
    border-radius: 3px;
    border: 1px solid #475569;
  }}

  .cmd-title-text {{
    font-size: 12px;
    font-weight: 600;
    color: #cbd5e1;
    font-family: 'Segoe UI', system-ui, sans-serif;
  }}

  .cmd-controls {{
    display: flex;
    align-items: center;
    gap: 14px;
    color: #64748b;
    font-size: 12px;
    font-family: 'Segoe UI', system-ui, sans-serif;
  }}

  .cmd-body {{
    padding: 16px 18px;
    background: #090c13;
    font-family: 'JetBrains Mono', 'Cascadia Code', Consolas, monospace;
    font-size: 10.6px;
    line-height: 1.56;
    color: #cbd5e1;
    white-space: nowrap;
  }}

  .cli-prompt {{
    color: #94a3b8;
    margin-bottom: 8px;
  }}
  .cli-cmd {{
    color: #f8fafc;
    font-weight: 700;
  }}

  .cli-separator {{
    color: #334155;
    letter-spacing: -0.5px;
  }}

  .cli-header {{
    color: #f1f5f9;
    font-weight: 700;
  }}

  .cli-step {{
    color: #38bdf8;
    font-weight: 700;
  }}

  .cli-status-green {{
    color: #34d399;
    font-weight: 700;
  }}

  .cli-subtext {{
    color: #64748b;
  }}

  .cli-subtext-white {{
    color: #cbd5e1;
  }}

  .cli-success-title {{
    color: #fcd34d;
    font-weight: 700;
  }}

  .cli-closing {{
    color: #94a3b8;
  }}

  .cli-cursor {{
    display: inline-block;
    width: 7px;
    height: 13px;
    background: #34d399;
    margin-left: 4px;
    vertical-align: middle;
    box-shadow: 0 0 8px #34d399;
  }}
</style>
</head>
<body>

  <!-- LEFT HERO SECTION -->
  <div class="left-hero">
    <div class="top-tag-row">
      <div class="logo-icon">
        <img src="data:image/png;base64,{icon_b64}" alt="9Router Icon" />
      </div>
      <div class="category-pill">Windows Automation Tool</div>
    </div>

    <h1 class="main-title">
      9Router &amp; <span class="highlight-blue">Antigravity</span><br>
      <span class="highlight">Auto-Starter</span>
    </h1>
    
    <p class="subtitle">
      One-Click Background Launcher, Auto Password Bypass<br>
      &amp; MITM Proxy Enabler for Google Antigravity
    </p>

    <div class="badge-row">
      <div class="feature-pill pill-instant">
        <span class="dot dot-orange"></span>
        1-Click Auto Run
      </div>
      <div class="feature-pill pill-bypass">
        <span class="dot dot-green"></span>
        Zero-Password Bypass
      </div>
      <div class="feature-pill pill-mitm">
        <span class="dot dot-coral"></span>
        MITM Proxy Ready
      </div>
    </div>

    <div class="support-text">
      Supports: Windows 10/11 &bull; 9Router CLI &bull; Port 443 &bull; DNS Redirection
    </div>

    <div class="divider"></div>

    <div class="footer-text">
      Dikembangkan dengan ❤️ oleh <strong>ADR Programming</strong>
    </div>
  </div>

  <!-- RIGHT COLUMN: 100% SAMA PERSIS DENGAN OUTPUT CMD ASLI -->
  <div class="right-preview">
    <div class="cmd-window">
      <div class="cmd-titlebar">
        <div class="cmd-title-left">
          <span class="cmd-icon-badge">&gt;_</span>
          <span class="cmd-title-text">Administrator: 9Router &amp; Antigravity Auto-Starter</span>
        </div>
        <div class="cmd-controls">
          <span>&minus;</span>
          <span>&#9633;</span>
          <span>&#10005;</span>
        </div>
      </div>
      
      <div class="cmd-body">
        <div class="cli-prompt">C:\\MyPrograms\\run-9router&gt; <span class="cli-cmd">9Router.cmd</span></div>
        
        <div class="cli-separator">====================================================</div>
        <div class="cli-header">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;9ROUTER &amp; ANTIGRAVITY AUTO-STARTER&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</div>
        <div class="cli-separator">====================================================</div>

        <div><span class="cli-step">[1/4]</span> Memeriksa status 9Router... <span class="cli-status-green">AKTIF (Port 20128)</span></div>
        
        <div><span class="cli-step">[2/4]</span> Mengatur bypass password (requireLogin: false)... <span class="cli-status-green">SUKSES</span></div>
        <div class="cli-subtext">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&gt; Login dashboard dinonaktifkan (bebas buka web tanpa password).</div>

        <div><span class="cli-step">[3/4]</span> Menyiapkan MITM Proxy untuk Antigravity... <span class="cli-status-green">SERVER SEDANG BERJALAN</span></div>

        <div><span class="cli-step">[4/4]</span> Memverifikasi status akhir MITM Proxy... <span class="cli-status-green">SIAP!</span></div>
        <div class="cli-subtext">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&gt; Status: <span class="cli-subtext-white">MITM Server Running (PID: 15324)</span></div>
        <div class="cli-subtext">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;-&gt; Antigravity DNS: <span class="cli-status-green">AKTIF (cloudcode-pa redirected ke 127.0.0.1)</span></div>

        <div class="cli-separator">====================================================</div>
        <div class="cli-success-title">[SUKSES] Antigravity &amp; 9Router siap digunakan!</div>
        <div class="cli-closing">Jendela ini akan menutup otomatis dalam 3 detik...<span class="cli-cursor"></span></div>
        <div class="cli-separator">====================================================</div>
      </div>
    </div>
  </div>

</body>
</html>
"""

temp_html = os.path.join(base_dir, "preview_temp.html")
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

output_png = os.path.join(base_dir, "social-preview.png")
temp_png = os.path.join(os.environ.get("USERPROFILE", "C:\\"), "temp_social_preview.png")

edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
cmd = [
    edge_path,
    "--headless",
    "--no-sandbox",
    "--disable-gpu",
    "--force-device-scale-factor=1",
    "--hide-scrollbars",
    "--window-size=1280,640",
    f"--screenshot={temp_png}",
    f"file:///{temp_html.replace(os.sep, '/')}"
]

print("Rendering 100% identical CMD output via Edge headless...")
subprocess.run(cmd, check=True)

if os.path.exists(temp_png):
    im = Image.open(temp_png)
    if im.size != (1280, 640):
        im = im.crop((0, 0, 1280, 640))
    im.save(output_png)
    os.remove(temp_png)
    print(f"Social preview successfully created at: {output_png} (Size: {im.size})")

if os.path.exists(temp_html):
    os.remove(temp_html)
