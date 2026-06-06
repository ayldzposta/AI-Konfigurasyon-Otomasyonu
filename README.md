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





Gelişmiş Özelleştirme Örnekleri1. Farklı bir GitHub reposundan veya kural dosyasından kurulum yapmak:Bashpython3 installer.py --repo-url "[https://github.com/kullanici/ozel-kurallar/archive/refs/heads/main.zip](https://github.com/kullanici/ozel-kurallar/archive/refs/heads/main.zip)" --skill-file "RULES.md" --extract-root "ozel-kurallar-main"
2. Kullanıcı onay ekranını atlayarak (Sessiz Mod) kurulum yapmak (CI/CD / Otomasyon için):Bashpython3 installer.py -y
3. Global kuralları tamamen atlayıp sadece mevcut proje dizinine kurmak:Bashpython3 installer.py --no-global
📊 Komut Satırı ParametreleriParametreVarsayılan DeğerAçıklama--dirMevcut çalışma diziniKurulumun yapılacağı yerel proje/çalışma dizini.-y, --yesFalseGlobal kuralların kurulumu için onay istemez, doğrudan onaylar.--no-globalFalseGlobal kuralların (~/.cursorrules vb.) kurulumunu tamamen devre dışı bırakır.--repo-urlPrompt-Master Ana Deposuİndirilecek ZIP arşivinin URL adresi.--skill-fileSKILL.mdZIP arşivi içerisinde aranacak ana kural/beceri dosyasının adı.--extract-rootprompt-master-mainZIP içindeki ana kök klasör kalıbı (GitHub zip mimarisi).--claude-dir~/.claude/skills/prompt-masterClaude Code için hedef skills dizini.--cursor-skills-dir~/.cursor/skills-cursor/...Cursor için özel skills dizini.--gemini-skills-dir~/.gemini/skills-antigravity/...Gemini / Antigravity için hedef skills dizini.--extra-global-rule(Liste)Ekstra kopyalanmasını istediğiniz global kural dosyası yolları (Birden fazla kez kullanılabilir).🎯 Kurulum Sonrası Yapay Zekayı Nasıl Kullanırım?Kurulum başarıyla tamamlandıktan sonra, yapay zekalarınız (örneğin Claude Code veya Cursor) arka planda bu kuralları otomatik olarak okur. Onlarla konuşurken doğrudan şu tarz komutlar verebilirsiniz:Claude Code İçinde (Prompt Üretmek İçin):“Write me a prompt for Cursor to refactor my auth module”“I need a prompt for Claude Code to build a REST API — ask me what you need to know”Cursor, Windsurf, Gemini vb. Editörlerde:Herhangi bir şey yapmanıza gerek yok! Global kurallar sayesinde açtığınız tüm projelerde yapay zeka artık bir Prompt Engineer gibi davranacak ve temiz, standartlara uygun kodlar üretecektir.📄 LisansBu proje MIT Lisansı ile lisanslanmıştır. Daha fazla bilgi için LICENSE dosyasına göz atabilirsiniz.
