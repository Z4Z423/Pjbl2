import csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def carregar_base(caminho=ROOT/"dados"/"base.csv"):
    with open(caminho,encoding="utf-8-sig",newline="") as f: return list(csv.DictReader(f))
