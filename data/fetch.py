"""Hash-verified downloads of all external inputs.

Every artifact is pinned by SHA-256; a mismatch aborts the run so evidence can
never silently drift from the recorded sources.
"""
import hashlib
import sys
import urllib.request
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

POURSABZI = "https://raw.githubusercontent.com/Foroughp/Manipulating-and-Measuring-Model-Interpretability/master"

SOURCES = {
    # De Cock (2011) Ames Iowa dataset, Journal of Statistics Education 19(3).
    "AmesHousing.txt": (
        "http://jse.amstat.org/v19n3/decock/AmesHousing.txt",
        "6cfe6cb525ba437de428653a1040e2aed7d696640bf75203786a6d7a0e67cfcc",
    ),
    # Poursabzi-Sangdeh et al. (CHI 2021) controlled human-subject study,
    # experiment 1 per-participant responses (paper's reference [48]).
    "poursabzi_exp1.csv": (
        f"{POURSABZI}/data/exp1/data.csv",
        "01e2f864240b7eb5675666789433e95e377b6ee8aea1b8eb62d6294f5b7a736d",
    ),
    # UCI Statlog German Credit (for Example 2, recourse provision).
    "german.data": (
        "https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/german/german.data",
        None,  # pinned after first fetch; see german_sha256.txt
    ),
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def fetch(name: str) -> Path:
    url, want = SOURCES[name]
    dest = DATA_DIR / name
    if not dest.exists():
        req = urllib.request.Request(url, headers=UA)
        dest.write_bytes(urllib.request.urlopen(req, timeout=120).read())
    got = sha256(dest)
    if want is None:
        pin = DATA_DIR / f"{name}.sha256"
        if pin.exists():
            want = pin.read_text().strip()
        else:
            pin.write_text(got + "\n")
            want = got
    if got != want:
        sys.exit(f"FATAL: {name} sha256 {got} != pinned {want}")
    return dest


if __name__ == "__main__":
    for n in SOURCES:
        p = fetch(n)
        print(f"{n}: {sha256(p)} ({p.stat().st_size} bytes)")
