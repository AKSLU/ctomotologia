from sqlalchemy import Column, Integer, String, Date, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import datetime
from flask import Flask, request, render_template

app = Flask(__name__)
Base = declarative_base()

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    healing_price = Column(Integer)
    status = Column(Integer)

class Note(Base):
    __tablename__ = "notes"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    date = Column(Date, default=datetime.date.today)
    client_id = Column(Integer)

engine = create_engine("sqlite:///example.db", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/")
def index():
    print("vgh")
    return render_template("index.html")

@app.route("/api/add_user", methods=["POST"])
def add_user():
    data = request.form
    session = Session()
    new_client = Client(
        name=data["name"],
        healing_price=int(data["healing_price"]),
        status=int(data["status"])
    )
    session.add(new_client)
    session.commit()
    return "Пользователь добавлен"

@app.route("/api/add_note", methods=["POST"])
def add_note():
    data = request.form
    session = Session()
    new_note = Note(
        title=data["title"],
        description=data["description"],
        date=datetime.date.today(),
        client_id=int(data["client_id"])
    )
    session.add(new_note)
    session.commit()
    return "Заметка добавлена"

@app.route("/api/remove_user", methods=["POST"])
def remove_user():
    data = request.form
    session = Session()
    client = session.query(Client).get(int(data["id"]))
    if client:
        session.delete(client)
        session.commit()
        return "Пользователь удалён"
    return "Пользователь не найден"

@app.route("/api/remove_note", methods=["POST"])
def remove_note():
    data = request.form
    session = Session()
    note = session.query(Note).get(int(data["id"]))
    if note:
        session.delete(note)
        session.commit()
        return "Заметка удалена"
    return "Заметка не найдена"

@app.route("/api/get_stats", methods=["GET"])
def get_stats():
    session = Session()
    clients = session.query(Client).all()
    result = ""
    for c in clients:
        result += f"{c.id} | {c.name} | {c.healing_price} | {c.status}\n"
    return result

@app.route("/api/get_notes", methods=["GET"])
def get_notes():
    session = Session()
    notes = session.query(Note).all()
    result = ""
    for note in notes:
        result += f"{note.id} | {note.title} | {note.description} | {note.date} | client_id: {note.client_id}\n"
    return result

if __name__ == "__main__":
    app.run(debug=True,port = 5001)

