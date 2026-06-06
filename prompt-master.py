#!/usr/bin/env python3
"""
Prompt-Master Universal Installer (Jenerik Sürüm)
Linux, macOS, Windows uyumlu. Komut satırı parametreleri ile özelleştirilebilir.
Güvenlik: ZIP Slip koruması, platform bağımsız dizinler, güvenli geçici dizin yönetimi.

Yeni eklenen parametrelerin açıklamaları:

Parametre	Varsayılan	Açıklama
--repo-url	https://github.com/.../main.zip	Farklı bir depodan veya release ZIP’i indirmek için
--skill-file	SKILL.md	ZIP içinde aranacak beceri dosyasının adı (ör. RULES.md)
--extract-root	prompt-master-main	ZIP’in içindeki ana klasör adı (GitHub repo-main kalıbı)
--claude-dir	~/.claude/skills/prompt-master	Claude için skills dizinini değiştirmek
--cursor-skills-dir	~/.cursor/skills-cursor/prompt-master	Cursor skills dizini
--gemini-skills-dir	~/.gemini/skills-antigravity/prompt-master	Antigravity/Gemini skills dizini
--extra-global-rule	(liste)	İlave global kural dosyası (birden çok kez --extra-global-rule /path/file şeklinde kullanılır)
Bu sayede betik herhangi bir benzer GitHub deposu veya farklı bir SKILL.md dosyası içeren herhangi bir ZIP arşiviyle kullanılabilecek kadar jenerik hale geldi. Aynı zamanda platform bağımsızlığı ve güvenlik önlemleri korunmaktadır.
"""

import os
import sys
import argparse
import logging
import shutil
import tempfile
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

# ------------------------------------------------------------
# Varsayılan yapılandırma
# ------------------------------------------------------------
DEFAULT_REPO_URL = "https://github.com/nidhinjs/prompt-master/archive/refs/heads/main.zip"
DEFAULT_SKILL_FILE = "SKILL.md"
DEFAULT_EXTRACT_ROOT = "prompt-master-main"   # GitHub arşivlerinde repo-main kalıbı
DEFAULT_CLAUDE_DIR = Path.home() / ".claude" / "skills" / "prompt-master"
DEFAULT_CURSOR_SKILLS_DIR = Path.home() / ".cursor" / "skills-cursor" / "prompt-master"
DEFAULT_GEMINI_SKILLS_DIR = Path.home() / ".gemini" / "skills-antigravity" / "prompt-master"

# Platforma göre Cursor settings.json yolu
def get_cursor_settings_path():
    if sys.platform == "win32":
        return Path(os.environ.get("APPDATA", "")) / "Cursor" / "User" / "settings.json"
    else:
        return Path.home() / ".config" / "Cursor" / "User" / "settings.json"

# ------------------------------------------------------------
# Loglama
# ------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S"
)
log = logging.getLogger(__name__)

# ------------------------------------------------------------
# Güvenli ZIP çıkartma (Zip Slip koruması)
# ------------------------------------------------------------
def _is_safe_path(base_dir: Path, member_path: str) -> bool:
    target = (base_dir / member_path).resolve()
    return target.is_relative_to(base_dir.resolve())

def _safe_extract(zip_ref: zipfile.ZipFile, extract_path: Path):
    for member in zip_ref.infolist():
        if member.is_dir():
            continue
        if not _is_safe_path(extract_path, member.filename):
            log.warning("Güvensiz ZIP yolu atlandı: %s", member.filename)
            continue
        zip_ref.extract(member, extract_path)

# ------------------------------------------------------------
# Adım fonksiyonları
# ------------------------------------------------------------
def download_zip(url: str, dest: Path) -> bool:
    log.info("ZIP indiriliyor: %s -> %s", url, dest)
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req) as response, open(dest, "wb") as out:
            shutil.copyfileobj(response, out)
        log.info("✅ ZIP indirildi.")
        return True
    except Exception as e:
        log.error("❌ İndirme hatası: %s", e)
        return False

def extract_zip(zip_path: Path, extract_to: Path, skill_filename: str, extract_root: str) -> Path:
    """
    ZIP'i çıkar, istenen SKILL dosyasını bul.
    extract_root: ZIP içindeki ana klasör adı (GitHub için repo-main gibi).
    """
    log.info("ZIP çıkartılıyor: %s -> %s", zip_path, extract_to)
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            _safe_extract(zf, extract_to)
    except Exception as e:
        log.error("❌ Çıkartma hatası: %s", e)
        return None

    # Önce beklenen ana dizin altında ara
    root_dir = extract_to / extract_root
    skill_md = root_dir / skill_filename
    if not skill_md.exists():
        # Alternatif: extract_to altında recursive ara
        for path in extract_to.rglob(skill_filename):
            skill_md = path
            break
    if skill_md and skill_md.exists():
        log.info("✅ %s bulundu: %s", skill_filename, skill_md)
        return skill_md
    log.warning("⚠️ %s ZIP içinde bulunamadı.", skill_filename)
    return None

def install_claude(skill_md: Path, claude_dir: Path) -> bool:
    """Claude Code için skills dizinine sadece ilgili beceri dosyasını güvenle kopyalar."""
    try:
        claude_dir.mkdir(parents=True, exist_ok=True)
        # copytree yerine doğrudan dosyayı hedef klasöre kopyalıyoruz (Geçici dizin bağımlılığını çözer)
        shutil.copy2(skill_md, claude_dir / skill_md.name)
        log.info("✅ Claude Code kurulumu tamamlandı: %s", claude_dir)
        return True
    except Exception as e:
        log.error("❌ Claude Code kurulum hatası: %s", e)
        return False

def install_local_rules(base_dir: Path, skill_md: Path) -> bool:
    """Proje dizinine .cursorrules ve .antigravityrules kopyala."""
    rules = {
        base_dir / ".cursorrules": skill_md,
        base_dir / ".antigravityrules": skill_md,
    }
    success = True
    for target, src in rules.items():
        try:
            shutil.copy2(src, target)
            log.info("✅ Yerel kural oluşturuldu: %s", target)
        except Exception as e:
            log.error("❌ Yerel kural hatası (%s): %s", target, e)
            success = False
    return success

def install_global_rules(skill_md: Path,
                         cursor_skills_dir: Path,
                         gemini_skills_dir: Path,
                         global_rules_list: list) -> bool:
    """Home dizininde global yapay zeka kurallarını oluştur."""
    # Varsayılan global hedefler
    targets = [
        Path.home() / ".cursorrules",
        Path.home() / ".antigravityrules",
        Path.home() / ".cline_rules",
        Path.home() / ".windsurfrules",
        Path.home() / ".cursor" / "rules" / "prompt-master.mdc",
        cursor_skills_dir / skill_md.name,
        gemini_skills_dir / skill_md.name,
    ] + global_rules_list  # kullanıcıdan gelen ek dosyalar

    success = True
    for target in targets:
        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(skill_md, target)
            log.info("✅ Global kural: %s", target)
        except Exception as e:
            log.error("❌ Global kural hatası (%s): %s", target, e)
            success = False

    # Cursor settings.json güncellemesi
    settings_path = get_cursor_settings_path()
    if settings_path.parent.exists():
        try:
            import json
            settings = {}
            if settings_path.exists():
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
            global_prompt = (
                "You must strictly follow the Prompt-Master rules defined in the global "
                "~/.cursorrules file. Act as a Prompt Engineer when requested."
            )
            current = settings.get("cursor.general.rulesForAi", "")
            if "Prompt-Master" not in current:
                settings["cursor.general.rulesForAi"] = (current + "\n\n" + global_prompt).strip()
                with open(settings_path, "w", encoding="utf-8") as f:
                    json.dump(settings, f, indent=4)
                log.info("✅ Cursor settings.json güncellendi.")
        except Exception as e:
            log.warning("Cursor settings.json güncellenemedi: %s", e)
    return success

# ------------------------------------------------------------
# Ana iş akışı
# ------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Prompt-Master evrensel kurulum aracı (jenerik)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--dir", default=str(Path.cwd()),
                        help="Proje (çalışma) dizini")
    parser.add_argument("--yes", "-y", action="store_true",
                        help="Global kural kurulumunu sormadan onayla")
    parser.add_argument("--no-global", action="store_true",
                        help="Global kuralları tamamen atla")

    # Jenerik parametreler
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL,
                        help="İndirilecek ZIP arşivinin URL'si")
    parser.add_argument("--skill-file", default=DEFAULT_SKILL_FILE,
                        help="ZIP içinde aranacak beceri (skills) dosyasının adı")
    parser.add_argument("--extract-root", default=DEFAULT_EXTRACT_ROOT,
                        help="ZIP içindeki ana klasör adı (GitHub: repo-main)")
    parser.add_argument("--claude-dir", default=str(DEFAULT_CLAUDE_DIR),
                        help="Claude Code skills dizini")
    parser.add_argument("--cursor-skills-dir", default=str(DEFAULT_CURSOR_SKILLS_DIR),
                        help="Cursor skills dizini")
    parser.add_argument("--gemini-skills-dir", default=str(DEFAULT_GEMINI_SKILLS_DIR),
                        help="Antigravity/Gemini skills dizini")
    parser.add_argument("--extra-global-rule", action="append", default=[],
                        help="Ekstra global kural dosyası (birden fazla kez kullanılabilir)")

    args = parser.parse_args()

    base_dir = Path(args.dir).resolve()
    home_dir = Path.home()

    log.info("🚀 Prompt-Master Kurulumu")
    log.info("Çalışma dizini: %s", base_dir)
    log.info("Kullanıcı dizini: %s", home_dir)

    # OS düzeyinde güvenli geçici dizin yönetimi (tempfile)
    with tempfile.TemporaryDirectory() as tmpdir:
        temp_path = Path(tmpdir)
        zip_target = temp_path / "prompt-master.zip"
        extract_dir = temp_path / "prompt-master-temp"

        # 1. İndir
        if not download_zip(args.repo_url, zip_target):
            sys.exit(1)

        # 2. Çıkart ve SKILL dosyasını bul
        skill_md = extract_zip(zip_target, extract_dir, args.skill_file, args.extract_root)
        if not skill_md:
            log.error("%s dosyası elde edilemedi; kurulum iptal edildi.", args.skill_file)
            sys.exit(1)

        # 3. Claude Code kurulumu
        install_claude(skill_md, Path(args.claude_dir))

        # 4. Yerel proje kuralları
        install_local_rules(base_dir, skill_md)

        # 5. Global kurallar
        if not args.no_global:
            # CI/CD veya boru hattı (pipeline) kilitlenmelerini önlemek için TTY kontrolü
            is_interactive = sys.stdin.isatty()
            user_approval = False
            
            if args.yes:
                user_approval = True
            elif is_interactive:
                try:
                    user_approval = input(
                        "Prompt-Master genel olarak tüm AI'larda çalışsın mı? [Y/N]: "
                    ).strip().upper() == "Y"
                except (KeyboardInterrupt, EOFError):
                    log.info("\nGirdi algılanamadı, global kurulum atlanıyor.")
            
            if user_approval:
                extra_paths = [Path(p) for p in args.extra_global_rule]
                install_global_rules(
                    skill_md,
                    Path(args.cursor_skills_dir),
                    Path(args.gemini_skills_dir),
                    extra_paths
                )
            else:
                log.info("Global kurulum atlandı.")
        else:
            log.info("Global kurulum devre dışı bırakıldı (--no-global).")
            
        # 'with' bloğundan çıkıldığı an tempfile otomatik olarak diskten tamamen silinir.
        log.info("Geçici dosyalar güvenli bir şekilde temizlendi.")

    # 6. Kullanım bilgisi
    print("\n" + "="*55)
    print("🎯 NASIL KULLANILIR?")
    print("="*55)
    print("1. CLAUDE İÇİNDE (Prompt Üretmek İçin):")
    print("   - Write me a prompt for Cursor to refactor my auth module")
    print("   - I need a prompt for Claude Code to build a REST API — ask me what you need to know")
    print("\n2. CURSOR, ANTIGRAVITY, WINDSURF VB. (Doğrudan Kullanım):")
    print("   - Global kurallar sayesinde tüm projelerde otomatik olarak devrede olacaktır.")
    print("="*55 + "\n")

if __name__ == "__main__":
    main()
