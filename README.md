# 🚀 AI Konfigürasyon Otomasyonu (Prompt-Master Universal Installer)

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org)
[![Platform Compatibility](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-green.svg)]()
[![License](https://img.shields.io/badge/license-MIT-purple.svg)]()

Bu araç; **Cursor, Claude Code, Gemini (Antigravity), Windsurf, Cline** gibi popüler yapay zeka kod asistanlarını tek bir komutla en optimize "Prompt Engineering" (Sistem Komutları) kurallarıyla donatan **evrensel ve jenerik bir kurulum betiğidir**.

İnternetten veya yerel bir kaynaktan aldığı "Süper Güç/Beceri" (`SKILL.md`) dosyalarını, bilgisayarındaki tüm yapay zeka editörlerine ve küresel (global) sistem dizinlerine otomatik olarak entegre eder.

---

## ✨ Özellikler

* **🌐 Evrensel ve Jenerik Mimari:** Sadece belirli bir repo ile sınırlı kalmaz; `--repo-url` parametresi ile dilediğiniz herhangi bir GitHub reposundan veya harici ZIP arşivinden kural setlerini çekebilir.
* **🛡️ Zip Slip Koruması:** Arşiv açma işlemleri sırasında dizin dışına taşma (path traversal) açıklarına karşı güvenlik kontrolü içerir.
* **⚙️ Otomasyon ve CI/CD Dostu:** Non-interactive (TTY olmayan) ortamlarda boru hattının (pipeline) kilitlenmesini önlemek için akıllı terminal kontrollerine sahiptir.
* **🧼 Güvenli Geçici Dizin:** İşletim sisteminin `tempfile` mekanizmasını kullanarak indirme ve çıkarma işlemlerini iz bırakmadan, tamamen arka planda temizler.
* **🎛️ Otomatik Konfigürasyon:** Cursor editörünün `settings.json` dosyasına küresel kuralları otomatik olarak enjekte eder.

---

## 🛠️ Kurulum ve Kullanım

Betik herhangi bir harici kütüphaneye (third-party dependency) ihtiyaç duymaz. Sadece standart Python 3 kütüphanelerini kullanır.

### Hızlı Başlangıç (Varsayılan Ayarlarla)

Betikli doğrudan çalıştırmak, varsayılan Prompt-Master kurallarını indirir ve hem yerel projenize hem de global AI dizinlerinize kurar:

```bash
python3 installer.py
