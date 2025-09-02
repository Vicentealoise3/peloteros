from flask import Flask, render_template, jsonify
import standings_cascade_points_desc as standings
import time

app = Flask(__name__)

# ====== Configuración de caché ======
CACHE = {
    "data": None,
    "timestamp": 0
}
CACHE_TTL = 300  # segundos (5 minutos)


def get_cached_standings():
    """Devuelve standings, usando caché en memoria para evitar recomputar siempre."""
    now = time.time()
    # Si la caché está vacía o expirada → recargar
    if CACHE["data"] is None or (now - CACHE["timestamp"] > CACHE_TTL):
        print("⏳ Recomputando standings desde la API...")
        rows = standings.compute_rows()
        CACHE["data"] = rows
        CACHE["timestamp"] = now
    else:
        print("✅ Usando standings en caché...")
    return CACHE["data"]


@app.route("/")
def index():
    # Solo devuelve la página, el JS pedirá los datos después
    return render_template("index.html")


@app.route("/api/standings")
def api_standings():
    rows = get_cached_standings()
    return jsonify(rows)
@app.route("/api/full")
def api_full():
    rows = get_cached_standings()
    return jsonify({
        "standings": rows,
        "games_today": standings.get_games_today()  # asegúrate de que exista esta función
    })

if __name__ == "__main__":
    app.run(debug=True)

