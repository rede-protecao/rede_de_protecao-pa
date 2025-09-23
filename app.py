from flask import Flask, render_template, request, redirect, url_for, session, flash
import json, os

app = Flask(__name__)
app.secret_key = "chave-secreta"

ADMIN_USER = "admin"
ADMIN_PASS = "1234"

NOTICIAS_FILE = "noticias.json"
DENUNCIAS_FILE = "denuncias.json"

def carregar_json(file):
    if os.path.exists(file):
        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def salvar_json(file, data):
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Admin login
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("Usuário ou senha incorretos", "danger")
    return render_template("admin_login.html")

@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    noticias = carregar_json(NOTICIAS_FILE)
    denuncias = carregar_json(DENUNCIAS_FILE)
    return render_template("admin_dashboard.html", noticias=noticias, denuncias=denuncias)

# CRUD Notícias
@app.route("/admin/noticias/add", methods=["POST"])
def admin_add_noticia():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    noticias = carregar_json(NOTICIAS_FILE)
    nova = {
        "titulo": request.form["titulo"],
        "resumo": request.form["resumo"],
        "link": request.form.get("link", "#")
    }
    noticias.append(nova)
    salvar_json(NOTICIAS_FILE, noticias)
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/noticias/edit/<int:index>", methods=["POST"])
def admin_edit_noticia(index):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    noticias = carregar_json(NOTICIAS_FILE)
    noticias[index]["titulo"] = request.form["titulo"]
    noticias[index]["resumo"] = request.form["resumo"]
    noticias[index]["link"] = request.form.get("link", "#")
    salvar_json(NOTICIAS_FILE, noticias)
    return redirect(url_for("admin_dashboard"))

# Atualizar status de denúncias
@app.route("/admin/denuncias/update/<int:index>", methods=["POST"])
def admin_update_denuncia(index):
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    denuncias = carregar_json(DENUNCIAS_FILE)
    denuncias[index]["status"] = request.form["status"]
    salvar_json(DENUNCIAS_FILE, denuncias)
    return redirect(url_for("admin_dashboard"))

if __name__ == "__main__":
    app.run(debug=True)
