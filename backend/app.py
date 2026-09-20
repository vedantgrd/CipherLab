"""
Classical Cryptography Suite — Flask Backend
Run: python app.py
Serves the React frontend at / and cipher API at /api/*
"""

import sys
import os
import math
import webbrowser
from threading import Timer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, send_from_directory

from ciphers import caesar, playfair, vigenere, hill, transposition


app = Flask(__name__, static_folder="static", static_url_path="")


# ── CORS headers ──────────────────────────────────────────────────────────────
@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    resp.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
    return resp


@app.route("/api/<path:p>", methods=["OPTIONS"])
def options(p):
    return "", 204


# ── Frontend ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


# ── Helpers ───────────────────────────────────────────────────────────────────
def err(msg, code=400):
    return jsonify({"error": msg}), code


def body():
    return request.get_json(force=True) or {}


# ── Caesar ────────────────────────────────────────────────────────────────────
@app.route("/api/caesar", methods=["POST"])
def api_caesar():
    d = body()
    text = d.get("text", "")
    mode = d.get("mode", "encrypt")
    show_steps = d.get("showSteps", False)

    try:
        shift = int(d.get("shift", 3))
    except (ValueError, TypeError):
        return err("Shift must be an integer.")

    if not text.strip():
        return err("Input text cannot be empty.")

    try:
        result = (
            caesar.encrypt(text, shift)
            if mode == "encrypt"
            else caesar.decrypt(text, shift)
        )

        resp = {"result": result}

        if show_steps:
            resp["steps"] = caesar.steps(text, shift, mode)

        return jsonify(resp)

    except Exception as e:
        return err(str(e))


# ── Playfair ──────────────────────────────────────────────────────────────────
@app.route("/api/playfair", methods=["POST"])
def api_playfair():
    d = body()
    text = d.get("text", "")
    keyword = "".join(
        c for c in d.get("keyword", "")
        if c.isalpha()
    )
    mode = d.get("mode", "encrypt")
    show_steps = d.get("showSteps", False)

    if not text.strip():
        return err("Input text cannot be empty.")

    if not keyword:
        return err("Keyword must contain alphabetic characters.")

    try:
        result = (
            playfair.encrypt(text, keyword)
            if mode == "encrypt"
            else playfair.decrypt(text, keyword)
        )

        resp = {"result": result}

        if show_steps:
            resp["steps"] = playfair.steps(text, keyword, mode)
        else:
            resp["matrix"] = playfair.build_matrix(keyword)

        return jsonify(resp)

    except Exception as e:
        return err(str(e))


@app.route("/api/playfair/matrix", methods=["POST"])
def api_playfair_matrix():
    d = body()

    keyword = "".join(
        c for c in d.get("keyword", "")
        if c.isalpha()
    )

    if not keyword:
        return err("Keyword required.")

    m = playfair.build_matrix(keyword)

    kw_chars = list(
        set(keyword.upper().replace("J", "I"))
    )

    return jsonify({
        "matrix": m,
        "kwChars": kw_chars
    })


# ── Vigenère ──────────────────────────────────────────────────────────────────
@app.route("/api/vigenere", methods=["POST"])
def api_vigenere():
    d = body()
    text = d.get("text", "")
    keyword = "".join(
        c for c in d.get("keyword", "")
        if c.isalpha()
    )
    mode = d.get("mode", "encrypt")
    show_steps = d.get("showSteps", False)

    if not text.strip():
        return err("Input text cannot be empty.")

    if not keyword:
        return err("Keyword must contain alphabetic characters.")

    try:
        result = (
            vigenere.encrypt(text, keyword)
            if mode == "encrypt"
            else vigenere.decrypt(text, keyword)
        )

        resp = {"result": result}

        if show_steps:
            resp["steps"] = vigenere.steps(
                text,
                keyword,
                mode
            )

        return jsonify(resp)

    except Exception as e:
        return err(str(e))


# ── Hill ──────────────────────────────────────────────────────────────────────
@app.route("/api/hill", methods=["POST"])
def api_hill():
    d = body()

    text = d.get("text", "")
    raw = d.get(
        "matrix",
        [
            [3, 3],
            [2, 5]
        ]
    )

    mode = d.get("mode", "encrypt")
    show_steps = d.get("showSteps", False)

    if not text.strip():
        return err("Input text cannot be empty.")

    try:
        matrix = [
            [int(v) for v in row]
            for row in raw
        ]
    except (ValueError, TypeError):
        return err("All matrix values must be integers.")

    ok, msg, _ = hill.validate(matrix)

    if not ok:
        return err(msg)

    try:
        result = (
            hill.encrypt(text, matrix)
            if mode == "encrypt"
            else hill.decrypt(text, matrix)
        )

        resp = {"result": result}

        if show_steps:
            resp["steps"] = hill.steps(
                text,
                matrix,
                mode
            )

        return jsonify(resp)

    except Exception as e:
        return err(str(e))


@app.route("/api/hill/validate", methods=["POST"])
def api_hill_validate():
    d = body()

    raw = d.get(
        "matrix",
        [
            [3, 3],
            [2, 5]
        ]
    )

    try:
        matrix = [
            [int(v) for v in row]
            for row in raw
        ]

        ok, msg, _ = hill.validate(matrix)

        return jsonify({
            "valid": ok,
            "message": msg
        })

    except Exception as e:
        return jsonify({
            "valid": False,
            "message": str(e)
        })


# ── Transposition ─────────────────────────────────────────────────────────────
@app.route("/api/transposition", methods=["POST"])
def api_transposition():
    d = body()

    text = d.get("text", "")
    keyword = "".join(
        c for c in d.get("keyword", "")
        if c.isalpha()
    )
    mode = d.get("mode", "encrypt")
    show_steps = d.get("showSteps", False)

    if not text.strip():
        return err("Input text cannot be empty.")

    if not keyword:
        return err("Key must contain alphabetic characters.")

    try:
        result = (
            transposition.encrypt(text, keyword)
            if mode == "encrypt"
            else transposition.decrypt(text, keyword)
        )

        resp = {"result": result}

        if show_steps:
            resp["steps"] = transposition.steps(
                text,
                keyword,
                mode
            )

        return jsonify(resp)

    except Exception as e:
        return err(str(e))


# ── Start Flask + Automatically Open Browser ──────────────────────────────────
if __name__ == "__main__":

    HOST = "127.0.0.1"
    PORT = 5000
    URL = f"http://{HOST}:{PORT}"

    print()
    print("  🔐  Classical Cryptography Suite")
    print("  ─────────────────────────────────────")
    print(f"  Starting server at {URL}")
    print("  Press Ctrl+C to stop")
    print()

    Timer(
        1.0,
        lambda: webbrowser.open(URL)
    ).start()

    app.run(
        host=HOST,
        port=PORT,
        debug=False
    )
