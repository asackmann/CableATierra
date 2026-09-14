"""pipeline.py — CableATierra pipeline principal

Revisa Samples/Imported por archivos nuevos y corre:
  split → fingerprint → lyrics match → metadata.

Uso:
  python3 pipeline.py                        # procesa archivos nuevos
  python3 pipeline.py --force <filename.mp3> # forzar un archivo
  python3 pipeline.py --lyrics-only <dir>    # solo lyrics match en carpeta ya spliteada
"""

import os, sys, json, re, datetime, subprocess, shutil

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPTS_DIR   = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH   = os.path.join(SCRIPTS_DIR, "config.json")
PROCESSED_LOG = os.path.join(SCRIPTS_DIR, "processed.json")
LYRICS_DB     = os.path.join(SCRIPTS_DIR, "lyrics_db.json")

with open(CONFIG_PATH) as f:
    CFG = json.load(f)

PROJECT    = CFG["project_root"]
INCOMING   = CFG["incoming_root"]
ARCHIVE    = os.path.join(INCOMING, CFG.get("incoming_processed_dir", "Procesados"))
REFERENCE  = os.path.join(PROJECT, CFG["reference_dir"])
ARTIST     = CFG["artist"]
YEAR       = CFG["year"]
FFPROBE   = CFG.get("ffprobe", "/opt/homebrew/bin/ffprobe")

PARTE_RE = re.compile(r'^Parte_\d+\.mp3$', re.IGNORECASE)
NAMED_RE = re.compile(r'^Parte_\d+\.\s+.+\.mp3$', re.IGNORECASE)


# ── Helpers ────────────────────────────────────────────────────────────────────

def log(msg):
    ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    print(f"[{ts}] {msg}")


def load_processed():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG) as f:
            return json.load(f)
    return {}


def save_processed(data):
    with open(PROCESSED_LOG, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def date_from_filename(fname):
    m = re.match(r"(\d{4})\.(\d{2})\.(\d{2})", fname)
    if m:
        return m.group(1) + m.group(2) + m.group(3)
    return None


def get_duration(path):
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", path],
        capture_output=True, text=True
    )
    try:
        return float(r.stdout.strip())
    except Exception:
        return None


def is_rehearsal(fname):
    if not fname.endswith(".mp3"):
        return False
    if not re.match(r"\d{4}\.\d{2}\.\d{2}", fname):
        return False
    dur = get_duration(os.path.join(INCOMING, fname))
    return dur is not None and dur > 1800


# ── Lyrics matching ────────────────────────────────────────────────────────────

def run_lyrics_match(out_dir, fp_results):
    """
    Corre lyrics_match.py sobre las partes que no tienen confianza OK.
    Retorna dict: {filename: lyrics_result}
    Omite partes que ya tienen nombre (ya procesadas).
    """
    if not os.path.exists(LYRICS_DB):
        log("  → lyrics_db.json no existe, saltando lyrics match")
        log("     (corré build_lyrics_db.py para construirla)")
        return {}

    # Solo intentar en partes sin confianza OK del fingerprinting
    targets = [r for r in fp_results if r.get("confidence") != "OK"]
    if not targets:
        log("  → Todas las partes tienen confianza OK, no se necesita lyrics match")
        return {}

    log(f"  → Lyrics matching en {len(targets)} partes (fingerprint MEDIA/BAJA)...")

    try:
        from lyrics_match import match_by_lyrics
    except ImportError:
        log("  → ERROR: no se puede importar lyrics_match.py")
        return {}

    lyrics_results = {}
    model_name = CFG.get("whisper_model", "medium")

    for r in targets:
        fname = r["file"]
        fpath = os.path.join(out_dir, fname)
        if not os.path.exists(fpath):
            continue

        log(f"     Transcribiendo {fname}...", )
        try:
            result = match_by_lyrics(fpath, model_name=model_name)
            lyrics_results[fname] = result
            conf = result.get("confidence", "BAJA")
            match = result.get("match", "—")
            score = result.get("score", 0)
            log(f"     → {match} ({conf}, score={score})")
        except Exception as e:
            log(f"     ERROR en {fname}: {e}")
            lyrics_results[fname] = {"confidence": "BAJA", "match": None}

    return lyrics_results


def merge_results(fp_results, lyrics_results):
    """
    Combina resultados de fingerprinting y lyrics.
    Estrategia:
      - Si fingerprint=OK → mantener (ya confiable)
      - Si fingerprint=MEDIA/BAJA y lyrics=OK → upgrade a lyrics result
      - Si ambos OK y mismo match → DOBLE_OK (máxima confianza)
      - Si ambos OK pero distinto match → CONFLICTO (manual)
    """
    for r in fp_results:
        fname = r["file"]
        if fname not in lyrics_results:
            continue

        lr = lyrics_results[fname]
        fp_conf  = r.get("confidence", "BAJA")
        ly_conf  = lr.get("confidence", "BAJA")
        fp_song  = r.get("song", "")
        ly_song  = lr.get("match", "")

        if fp_conf == "OK" and ly_conf == "OK":
            if fp_song.lower() == (ly_song or "").lower():
                r["confidence"]    = "DOBLE_OK"
                r["lyrics_match"]  = ly_song
                r["lyrics_conf"]   = ly_conf
            else:
                r["confidence"]    = "CONFLICTO"
                r["lyrics_match"]  = ly_song
                r["lyrics_conf"]   = ly_conf
        elif fp_conf != "OK" and ly_conf == "OK":
            # Lyrics rescata lo que fingerprint no pudo
            r["song"]          = ly_song
            r["confidence"]    = "LYRICS_OK"
            r["lyrics_match"]  = ly_song
            r["lyrics_conf"]   = ly_conf
            r["lyrics_score"]  = lr.get("score", 0)
        else:
            # Lyrics no mejora la situación
            r["lyrics_match"]  = ly_song
            r["lyrics_conf"]   = ly_conf
            r["lyrics_score"]  = lr.get("score", 0)

    return fp_results


# ── Reporte ────────────────────────────────────────────────────────────────────

CONF_ICON = {
    "DOBLE_OK":  "✅✅",
    "OK":        "✅",
    "LYRICS_OK": "🎤",
    "MEDIA":     "⚠️",
    "BAJA":      "❌",
    "CONFLICTO": "⚡",
    "SIN_VOZ":   "🔇",
}


def write_fp_report(out_dir, results, md_path):
    has_lyrics = any("lyrics_match" in r for r in results)

    if has_lyrics:
        header = "| Parte | FP Match | FP Conf | Lyrics Match | Lyrics Conf | Final |"
        sep    = "|-------|----------|---------|--------------|-------------|-------|"
    else:
        header = "| Parte | Match | Score | Gap | Confianza |"
        sep    = "|-------|-------|-------|-----|-----------|"

    lines = ["# Fingerprinting + Lyrics — análisis automático", "", header, sep]

    for r in results:
        icon = CONF_ICON.get(r["confidence"], "❓")
        if has_lyrics:
            ly_match = r.get("lyrics_match", "—") or "—"
            ly_conf  = r.get("lyrics_conf", "—")
            ly_icon  = CONF_ICON.get(ly_conf, "—")
            lines.append(
                f"| {r['file']} | {r['song']} | {CONF_ICON.get(r.get('fp_confidence', r['confidence']), '—')} "
                f"| {ly_match} | {ly_icon} {ly_conf} | {icon} {r['confidence']} |"
            )
        else:
            lines.append(
                f"| {r['file']} | {r['song']} | {r['score']} | {r['gap']} | {icon} {r['confidence']} |"
            )

    lines += ["", "Leyenda: ✅✅ DOBLE_OK · ✅ OK · 🎤 LYRICS_OK · ⚠️ MEDIA · ❌ BAJA · ⚡ CONFLICTO"]
    lines += ["", "Completar `mapping.csv` para las partes sin confianza OK/LYRICS_OK/DOBLE_OK."]

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def write_mapping_csv(out_dir, results):
    csv_path = os.path.join(out_dir, "mapping.csv")
    auto_confs = {"OK", "DOBLE_OK", "LYRICS_OK"}
    lines = [
        "# Completar columna 'cancion' y correr apply_metadata.py",
        "parte,cancion,confianza"
    ]
    for r in results:
        base = r["file"].replace(".mp3", "")
        song = r["song"] if r["confidence"] in auto_confs else ""
        lines.append(f"{base},{song},{r['confidence']}")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def auto_apply_ok(out_dir, results):
    from apply_metadata import apply_tag, rename_file, update_m3u
    album = os.path.basename(out_dir)
    auto_confs = {"OK", "DOBLE_OK", "LYRICS_OK"}
    ok_matches = [r for r in results if r["confidence"] in auto_confs]
    if not ok_matches:
        return
    log(f"  → Aplicando metadata a {len(ok_matches)} partes con confianza alta...")
    renamed = []
    for r in ok_matches:
        mp3 = os.path.join(out_dir, r["file"])
        if not os.path.exists(mp3):
            continue
        if apply_tag(mp3, r["song"], ARTIST, album, YEAR):
            _, new_fname = rename_file(mp3, r["song"])
            log(f"    ✓ {r['file']} → {new_fname}")
            num = r["file"].replace(".mp3", "").split("_")[1]
            renamed.append((num, r["song"]))
    update_m3u(out_dir, renamed)


# ── Procesamiento principal ────────────────────────────────────────────────────

def process_file(fname, force=False):
    from split_ensayo import split
    from fingerprint import fingerprint

    fpath    = os.path.join(INCOMING, fname)
    date_str = date_from_filename(fname) or "XXXXXXXX"
    out_dir  = os.path.join(PROJECT, f"{date_str}. Ensayo - Partes")
    album    = f"Ensayo {date_str}"

    log(f"Procesando: {fname}")

    # 1. Split
    log("  → Split por silencios...")
    filenames, sections = split(
        fpath, out_dir,
        artist=ARTIST, album=album, year=YEAR,
        threshold=CFG["silence_threshold_db"],
        min_dur=CFG["silence_min_duration"],
        gap=CFG["zone_gap_seconds"],
        min_section=CFG["min_section_duration"]
    )
    log(f"  → {len(filenames)} partes exportadas en {out_dir}")

    fp_json = os.path.join(out_dir, "fingerprinting_results.json")
    fp_md   = os.path.join(out_dir, "fingerprinting_results.md")
    results = []

    # 2. Fingerprint
    if os.path.isdir(REFERENCE):
        log("  → Fingerprinting (audio features)...")
        results = fingerprint(
            out_dir, REFERENCE, fp_json,
            gap_ok=CFG.get("fingerprint_gap_ok", 0.010),
            gap_media=CFG.get("fingerprint_gap_media", 0.002)
        )
        # Guardar confianza original de fingerprint para el reporte
        for r in results:
            r["fp_confidence"] = r["confidence"]

        # 3. Lyrics matching (segunda pasada, solo partes no-OK)
        log("  → Lyrics matching (transcripción)...")
        lyrics_results = run_lyrics_match(out_dir, results)
        if lyrics_results:
            merge_results(results, lyrics_results)

        # Reporte y mapping
        write_fp_report(out_dir, results, fp_md)
        write_mapping_csv(out_dir, results)
        log(f"  → Resultados en {fp_md}")

        # 4. Auto-aplicar metadata
        auto_apply_ok(out_dir, results)
    else:
        log(f"  → Sin referencia en {REFERENCE}, saltando fingerprint")

    # 5. Archivar el original: sacarlo de la carpeta de entrada para que
    #    quede claro qué está pendiente vs qué ya se procesó.
    os.makedirs(ARCHIVE, exist_ok=True)
    archived_path = os.path.join(ARCHIVE, fname)
    if os.path.exists(archived_path):
        base, ext = os.path.splitext(archived_path)
        i = 1
        while os.path.exists(archived_path):
            archived_path = f"{base} (dup{i}){ext}"
            i += 1
    shutil.move(fpath, archived_path)
    log(f"  → Original archivado en {archived_path}")

    log(f"Listo: {fname}")
    return out_dir, archived_path


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]

    # Modo: solo lyrics match en una carpeta ya spliteada
    if "--lyrics-only" in args:
        idx = args.index("--lyrics-only")
        target_dir = args[idx + 1]
        fp_json = os.path.join(target_dir, "fingerprinting_results.json")
        fp_md   = os.path.join(target_dir, "fingerprinting_results.md")
        if not os.path.exists(fp_json):
            log(f"No se encontró {fp_json}")
            return
        with open(fp_json) as f:
            results = json.load(f)
        for r in results:
            r["fp_confidence"] = r["confidence"]
        lyrics_results = run_lyrics_match(target_dir, results)
        if lyrics_results:
            merge_results(results, lyrics_results)
            write_fp_report(target_dir, results, fp_md)
            write_mapping_csv(target_dir, results)
            auto_apply_ok(target_dir, results)
        log("Lyrics-only completado.")
        return

    force_file = None
    if "--force" in args:
        idx = args.index("--force")
        force_file = args[idx + 1] if idx + 1 < len(args) else None

    processed = load_processed()

    if force_file:
        files_to_process = [force_file]
    else:
        all_files = [f for f in os.listdir(INCOMING) if is_rehearsal(f)]
        files_to_process = [f for f in all_files if f not in processed]

    if not files_to_process:
        log("Sin archivos nuevos para procesar.")
        return

    log(f"Archivos nuevos: {files_to_process}")
    for fname in files_to_process:
        try:
            out_dir, archived_path = process_file(fname)
            processed[fname] = {
                "date": datetime.datetime.now().isoformat(),
                "output_dir": out_dir,
                "archived_original": archived_path
            }
            save_processed(processed)
        except Exception as e:
            log(f"ERROR procesando {fname}: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    sys.path.insert(0, SCRIPTS_DIR)
    main()
