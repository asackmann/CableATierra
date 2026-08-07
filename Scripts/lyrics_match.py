#!/usr/bin/env python3
"""
lyrics_match.py — Identificación de canciones por transcripción

Transcribe un archivo MP3 y lo compara contra lyrics_db.json
usando similitud de texto (TF-IDF coseno + Jaccard).

Uso como módulo:
  from lyrics_match import match_by_lyrics
  result = match_by_lyrics("/path/to/Parte_XX.mp3")

Uso desde línea de comandos:
  python3 lyrics_match.py /path/to/Parte_XX.mp3
"""

import os, sys, json, re
import numpy as np
from collections import Counter

SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPTS_DIR, "config.json")
DB_PATH     = os.path.join(SCRIPTS_DIR, "lyrics_db.json")
FFMPEG      = None  # se carga de config

# Stopwords comunes (español + inglés) — no aportan discriminación
STOPWORDS = {
    "el","la","los","las","un","una","unos","unas","de","del","al","a","en",
    "y","e","o","u","que","no","si","me","te","se","lo","le","les","nos",
    "por","para","con","sin","sobre","pero","mas","más","ya","era","fue",
    "the","a","an","and","or","but","in","on","at","to","for","of","is",
    "it","i","you","he","she","we","they","my","your","his","her","our",
    "this","that","with","not","be","have","do","so","as","if","can","will",
    "oh","yeah","hey","ah","na","la","da","ooh","eh","mmm",
}


# ── Utilidades de texto ──────────────────────────────────────────────────────

def normalize(name):
    name = name.lower().strip()
    for a, b in [("á","a"),("é","e"),("í","i"),("ó","o"),("ú","u"),("ü","u"),("ñ","n")]:
        name = name.replace(a, b)
    return name


def tokenize(text):
    tokens = re.findall(r'\b[a-záéíóúüñ]+\b', text.lower())
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def build_vocab(all_texts):
    vocab = {}
    for text in all_texts:
        for token in tokenize(text):
            if token not in vocab:
                vocab[token] = len(vocab)
    return vocab


def tfidf_vector(tokens, vocab, idf):
    vec = np.zeros(len(vocab))
    counts = Counter(tokens)
    total = max(sum(counts.values()), 1)
    for token, count in counts.items():
        if token in vocab:
            tf = count / total
            vec[vocab[token]] = tf * idf.get(token, 1.0)
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def cosine_sim(a, b):
    return float(np.dot(a, b))  # ya están normalizados


def jaccard_sim(tokens_a, tokens_b):
    set_a, set_b = set(tokens_a), set(tokens_b)
    if not set_a and not set_b:
        return 0.0
    return len(set_a & set_b) / len(set_a | set_b)


# ── DB helpers ───────────────────────────────────────────────────────────────

def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH) as f:
        return json.load(f)


def build_index(db):
    """
    Pre-computa vectores TF-IDF para cada canción.
    Combina todos los transcripts de una canción en un solo texto.
    """
    # Texto combinado por canción
    song_texts = {}
    for key, entry in db.items():
        transcripts = entry.get("transcripts", [])
        combined = " ".join(transcripts)
        if combined.strip():
            song_texts[key] = combined

    if not song_texts:
        return None, None, None, None

    # Vocab global
    all_text_list = list(song_texts.values())
    vocab = build_vocab(all_text_list)

    # IDF
    N = len(all_text_list)
    idf = {}
    for token in vocab:
        df = sum(1 for t in all_text_list if token in tokenize(t))
        idf[token] = np.log((N + 1) / (df + 1)) + 1  # smoothed

    # Vectores por canción
    song_vectors = {}
    song_tokens  = {}
    for key, text in song_texts.items():
        tokens = tokenize(text)
        song_vectors[key] = tfidf_vector(tokens, vocab, idf)
        song_tokens[key]  = tokens

    return song_texts, vocab, idf, song_vectors, song_tokens


# ── Transcripción ────────────────────────────────────────────────────────────

def transcribe_file(path, model_name="medium", secs=90):
    """Transcribe los primeros `secs` segundos del archivo."""
    import subprocess, tempfile

    global FFMPEG
    if FFMPEG is None:
        with open(CONFIG_PATH) as f:
            cfg = json.load(f)
        FFMPEG = cfg.get("ffmpeg", "/opt/homebrew/bin/ffmpeg")
        secs   = cfg.get("transcribe_secs", secs)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        tmp_path = tmp.name

    try:
        cmd = [FFMPEG, "-y", "-i", path, "-t", str(secs),
               "-ar", "16000", "-ac", "1", "-f", "wav", tmp_path]
        subprocess.run(cmd, capture_output=True, check=True)

        from faster_whisper import WhisperModel
        model = WhisperModel(model_name, device="cpu", compute_type="int8")
        segments, _ = model.transcribe(
            tmp_path, beam_size=5,
            vad_filter=True,
            vad_parameters={"min_silence_duration_ms": 500},
        )
        return " ".join(seg.text.strip() for seg in segments).strip()
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


# ── Match principal ──────────────────────────────────────────────────────────

def match_by_lyrics(path, model_name=None, verbose=False):
    """
    Transcribe `path` y retorna el match más probable en lyrics_db.json.

    Retorna dict:
      {
        "transcript": "...",
        "match": "Nombre canción",
        "score": 0.85,
        "confidence": "OK" | "MEDIA" | "BAJA" | "SIN_VOZ",
        "top3": [("song", score), ...]
      }
    """
    with open(CONFIG_PATH) as f:
        cfg = json.load(f)
    if model_name is None:
        model_name = cfg.get("whisper_model", "medium")

    db = load_db()
    if not db:
        return {"error": "lyrics_db.json vacía o no existe"}

    result = build_index(db)
    if result[0] is None:
        return {"error": "DB sin transcripciones aún"}

    song_texts, vocab, idf, song_vectors, song_tokens = result

    # Transcribir el archivo nuevo
    if verbose:
        print(f"Transcribiendo {os.path.basename(path)}...")
    transcript = transcribe_file(path, model_name=model_name,
                                  secs=cfg.get("transcribe_secs", 90))

    if not transcript or len(transcript.split()) < 5:
        return {
            "transcript": transcript,
            "match": None,
            "score": 0.0,
            "confidence": "SIN_VOZ",
            "top3": [],
        }

    if verbose:
        print(f"Transcript: {transcript[:120]}...")

    query_tokens = tokenize(transcript)
    query_vec    = tfidf_vector(query_tokens, vocab, idf)

    # Calcular similitudes
    scores = {}
    for key, vec in song_vectors.items():
        cos  = cosine_sim(query_vec, vec)
        jac  = jaccard_sim(query_tokens, song_tokens[key])
        scores[key] = 0.7 * cos + 0.3 * jac  # weighted combo

    top = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_key, best_score = top[0]
    second_score = top[1][1] if len(top) > 1 else 0.0
    gap = best_score - second_score

    # Thresholds de confianza
    if best_score >= 0.25 and gap >= 0.10:
        confidence = "OK"
    elif best_score >= 0.10 and gap >= 0.04:
        confidence = "MEDIA"
    else:
        confidence = "BAJA"

    top3 = [(db[k]["name"], round(s, 4)) for k, s in top[:3]]

    return {
        "transcript": transcript,
        "match": db[best_key]["name"],
        "score": round(best_score, 4),
        "gap": round(gap, 4),
        "confidence": confidence,
        "top3": top3,
    }


# ── CLI ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 lyrics_match.py <archivo.mp3> [--model medium]")
        sys.exit(1)

    path = sys.argv[1]
    model_arg = None
    if "--model" in sys.argv:
        model_arg = sys.argv[sys.argv.index("--model") + 1]

    result = match_by_lyrics(path, model_name=model_arg, verbose=True)

    print(f"\n{'─'*50}")
    print(f"Archivo:     {os.path.basename(path)}")
    print(f"Transcript:  {result.get('transcript','')[:100]}...")
    print(f"Match:       {result.get('match')} (score={result.get('score')}, gap={result.get('gap')})")
    print(f"Confianza:   {result.get('confidence')}")
    print(f"Top 3:       {result.get('top3')}")
