"""
split_ensayo.py — CableATierra pipeline
Divide un MP3 largo en partes basándose en detección de silencios con ffmpeg.
Uso: python3 split_ensayo.py <input.mp3> <output_dir> [album_name]
"""
import subprocess, re, os, datetime, sys, json

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FFPROBE = "/opt/homebrew/bin/ffprobe"

def get_duration(input_file):
    r = subprocess.run(
        [FFPROBE, "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", input_file],
        capture_output=True, text=True
    )
    return float(r.stdout.strip())

def detect_silences(input_file, threshold="-35dB", min_dur=8):
    cmd = [FFMPEG, "-i", input_file,
           "-af", f"silencedetect=noise={threshold}:d={min_dur}",
           "-f", "null", "-"]
    r = subprocess.run(cmd, capture_output=True, text=True)
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    ends   = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return list(zip(starts, ends))

def group_into_zones(silences, gap_seconds=45):
    if not silences:
        return []
    zones = []
    zs, ze = silences[0]
    for ss, se in silences[1:]:
        if ss - ze < gap_seconds:
            ze = se
        else:
            zones.append((zs, ze))
            zs, ze = ss, se
    zones.append((zs, ze))
    return zones

def extract_sections(zones, total_duration, min_dur=60):
    sections = []
    cursor = 0.0
    for zs, ze in zones:
        if zs - cursor >= min_dur:
            sections.append((cursor, zs))
        cursor = ze
    if total_duration - cursor >= min_dur:
        sections.append((cursor, total_duration))
    return sections

def export_section(input_file, start, end, output_path, title, artist, album, year):
    cmd = [
        FFMPEG, "-y",
        "-ss", str(start), "-t", str(end - start),
        "-i", input_file,
        "-c:a", "copy",
        "-id3v2_version", "3",
        "-metadata", f"title={title}",
        "-metadata", f"artist={artist}",
        "-metadata", f"album={album}",
        "-metadata", f"date={year}",
        output_path
    ]
    r = subprocess.run(cmd, capture_output=True)
    return r.returncode == 0

def write_m3u(playlist_path, sections, filenames):
    lines = ["#EXTM3U", ""]
    for (start, end), fname in zip(sections, filenames):
        dur = int(end - start)
        title = os.path.basename(fname).replace(".mp3", "").replace("_", " ")
        s = str(datetime.timedelta(seconds=int(start)))
        e = str(datetime.timedelta(seconds=int(end)))
        lines += [f"#EXTINF:{dur},{title}  [{s} → {e}]",
                  os.path.basename(fname), ""]
    with open(playlist_path, "w") as f:
        f.write("\n".join(lines))

def split(input_file, output_dir, artist="CableATierra", album=None, year="2026",
          threshold="-35dB", min_dur=8, gap=45, min_section=60):
    os.makedirs(output_dir, exist_ok=True)
    if album is None:
        album = os.path.basename(input_file).replace(".mp3", "")

    print(f"Duración total...")
    total = get_duration(input_file)
    print(f"  {total/60:.1f} min")

    print("Detectando silencios...")
    silences = detect_silences(input_file, threshold, min_dur)
    print(f"  {len(silences)} silencios")

    zones = group_into_zones(silences, gap)
    print(f"  {len(zones)} zonas de transición")

    sections = extract_sections(zones, total, min_section)
    print(f"  {len(sections)} secciones")

    filenames = []
    for i, (start, end) in enumerate(sections, 1):
        title = f"Parte {i:02d}"
        fname = f"Parte_{i:02d}.mp3"
        out = os.path.join(output_dir, fname)
        ok = export_section(input_file, start, end, out, title, artist, album, year)
        status = "✓" if ok else "✗"
        print(f"  {status} {fname}  ({(end-start)/60:.1f} min)")
        if ok:
            filenames.append(out)

    playlist = os.path.join(output_dir, f"{artist}_Ensayo.m3u")
    write_m3u(playlist, sections, filenames)
    print(f"Playlist: {playlist}")
    return filenames, sections

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 split_ensayo.py <input.mp3> <output_dir> [album]")
        sys.exit(1)
    inp = sys.argv[1]
    out = sys.argv[2]
    alb = sys.argv[3] if len(sys.argv) > 3 else None
    split(inp, out, album=alb)
