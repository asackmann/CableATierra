import sys
sys.path.insert(0, "/Users/agustinsackmann/Repos/Personal/CableATierra/Scripts")
from fingerprint import fingerprint
target = "/Users/agustinsackmann/Library/CloudStorage/Dropbox/04. Multimedia/Ableton/2026. Projects/CableATierra Project/20260807. Ensayo - Partes"
out = "/Users/agustinsackmann/Repos/Personal/CableATierra/Scripts/fp_20260807.json"
fingerprint(target, None, out)
