from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql+psycopg2://postgres:cringe@localhost:5432/phonebase'
db.init_app(app)


class Contact(db.Model):  # Создаём контакт в базе данных
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    phone = db.Column(db.String(12), nullable=False)


@app.route('/')
def index():  # Обработка запроса к корневому URL
    contacts = Contact.query.all() # Получение контактов из базы данных
    return render_template('index.html', contacts=contacts)  # Возвращение всех контактов из базы данных


@app.route('/add_contact', methods=["POST"])
def add_contact():  # Добавление контакта
    name = request.form['name']
    phone = request.form['phone']
    new_contact = Contact(name=name, phone=phone)
    db.session.add(new_contact)  # Добавление контакта в базу данных
    db.session.commit()
    return redirect('/')  # Перенаправление на главную страницу


@app.route('/clear_msg', methods=['POST'])
def clear_msg():
    Contact.query.delete()  # Очищение базы данных
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание базы данных
    app.run()
