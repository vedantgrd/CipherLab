# 🔐 CipherLab:

A polished, production-quality cryptography educational application with a **React frontend** and **Python (Flask) backend**. Demonstrates five classical ciphers with full encryption, decryption, step-by-step visualization, and a modern dark UI.

---

## Quick Start

```bash
# 1. Install the only dependency
pip install flask

# 2. Run — opens browser automatically
python start.py

# Or run Flask directly
cd backend
python app.py
# Then open http://localhost:5000
```

---

## Features

### Five Cipher Algorithms
| Cipher | Type | Key |
|---|---|---|
| **Caesar** | Monoalphabetic Substitution | Integer shift (±) |
| **Playfair** | Digraph Substitution | Keyword → live 5×5 matrix |
| **Vigenère** | Polyalphabetic Substitution | Repeating keyword |
| **Hill** | Matrix Cipher | 2×2 or 3×3 invertible matrix mod 26 |
| **Transposition** | Columnar Permutation | Keyword (column rank ordering) |

### UI Features
- Dark cybersecurity-inspired theme
- Sidebar navigation with breadcrumb
- Dashboard with clickable cipher cards and stats
- Per-cipher pages with Encrypt/Decrypt segmented toggle
- Live Playfair 5×5 key matrix (updates as you type)
- Hill matrix editor with real-time det/gcd validity indicator
- Step-by-step visualization (toggle per cipher)
- Copy, Swap, Clear on every cipher page
- Inline error banners — no crashes from bad input
- Vigenère alignment table visualization
- Transposition grid visualization
- About page with team info and architecture

---

## Running Tests

```bash
cd backend
python -m unittest tests.test_all -v
# 85 tests, all pass
```

---

## Project Structure

```
crypto_app/
├── start.py                    ← One-command launcher (opens browser)
├── requirements.txt            ← Only: flask
│
├── backend/
│   ├── app.py                  ← Flask server: API routes + static serving
│   │
│   ├── ciphers/
│   │   ├── caesar.py           ← encrypt / decrypt / steps
│   │   ├── playfair.py         ← encrypt / decrypt / build_matrix / steps
│   │   ├── vigenere.py         ← encrypt / decrypt / steps
│   │   ├── hill.py             ← encrypt / decrypt / validate / steps
│   │   └── transposition.py   ← encrypt / decrypt / col_order / steps
│   │
│   ├── static/
│   │   └── index.html          ← Complete React SPA (no build step needed)
│   │
│   └── tests/
│       └── test_all.py         ← 85 unit tests
│
└── README.md
```

---

## Architecture

```
Browser (React SPA)
       ↕  HTTP POST JSON
Flask Backend (app.py)
       ↕  Python calls
Cipher Modules (ciphers/)
```

- **No build step** — React loaded via CDN, JSX compiled by Babel in-browser
- **Single dependency** — only `flask`
- **GUI and cipher logic fully separated** — cipher modules contain zero web/UI code
- **All processing is local** — no internet required after initial load of CDN scripts

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/caesar` | Caesar encrypt/decrypt |
| POST | `/api/playfair` | Playfair encrypt/decrypt |
| POST | `/api/playfair/matrix` | Generate key matrix for display |
| POST | `/api/vigenere` | Vigenère encrypt/decrypt |
| POST | `/api/hill` | Hill encrypt/decrypt |
| POST | `/api/hill/validate` | Validate matrix invertibility |
| POST | `/api/transposition` | Transposition encrypt/decrypt |

All endpoints accept `{"text": "...", "mode": "encrypt"|"decrypt", "showSteps": bool, ...key params}` and return `{"result": "...", "steps": {...}}`.

---

## Sample I/O

| Cipher | Input | Key | Output |
|---|---|---|---|
| Caesar | `HELLO` | `3` | `KHOOR` |
| Vigenère | `ATTACKATDAWN` | `LEMON` | `LXFOPVEFRNHR` |
| Hill | `HE` | `[[3,3],[2,5]]` | `HI` |
| Playfair | `HELLO` | `MONARCHY` | digraph pairs |
| Transposition | `WEAREDISCOVEREDFLEEATONCE` | `ZEBRAS` | column-permuted |

---

## Team

| Name | Admission Number | Roll No. |
| :---: | :---: | :---: |
| Yash Krishna Patil | 2024PE0356 | 510 |
| Rushikesh Vichare | 2025PE0323 | 504 |
| Vedant Garud | 2025PE0316 | 502 |
| Aryan Govekar | 2024PE0362 | 506 |
| Akshat Vijesh | 2024PE0144 | 514 |


---

> **Educational Use Only.** Classical ciphers are for learning and demonstration only. Do not use for real-world security.
