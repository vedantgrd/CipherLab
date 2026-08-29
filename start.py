"""
Classical Cryptography Suite — Launcher
Run: python start.py
"""
import os, sys, webbrowser, threading, time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))

def open_browser():
    time.sleep(1.4)
    webbrowser.open("http://localhost:5000")

if __name__ == "__main__":
    threading.Thread(target=open_browser, daemon=True).start()
    from backend.app import app
    print("\n  🔐  Classical Cryptography Suite")
    print("  ─────────────────────────────────────────────────")
    print("  → Opening http://localhost:5000 in your browser")
    print("  → Press Ctrl+C to stop\n")
    app.run(debug=False, port=5000, use_reloader=False)
