#Alunos: Mateus Amaral e Gabriel Almeida
from flask import Flask, render_template, request, session, redirect
from flask_session import Session

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if session.get("notes") is None:
        session["notes"] = []
    
    if session.get("titles") is None:
        session["titles"] = []

    session["index"] = -1
    session["title_edit"] = ""
    session["note_edit"] = ""

    if request.method == "POST":
        if "edit" in request.form["name"]: 
            session["index"] = int(request.form["name"][4:])
            session["title_edit"] = session["titles"][session["index"]]
            session["note_edit"] = session["notes"][session["index"]]
            return redirect("/edit_post")

    return render_template("index.html", notes=session["notes"], titles=session["titles"], len=len(session["notes"]))


@app.route("/edit_post", methods=["GET", "POST"])
def edit_post():
    if request.method == "POST" and request.form["name"]=="save":
        title = request.form.get("title")
        note = request.form.get("note")
        if session["index"] != -1:
            session["titles"][session["index"]] = title
            session["notes"][session["index"]] = note
        else:
            session["titles"].append(title)
            session["notes"].append(note)
        return redirect("/")
    
    if request.method == "POST" and request.form["name"]=="delete":
        session["titles"].remove(session["title_edit"])
        session["notes"].remove(session["note_edit"])
        return redirect("/")
    
    return render_template("edit_post.html", notes=session["notes"], titles=session["titles"], len=len(session["notes"]), title_edit=session["title_edit"], note_edit=session["note_edit"])

    
        
