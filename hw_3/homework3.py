"""task3"""

from flask import Flask, render_template, request
from hw_3.models import db, User
from flask_wtf.csrf import CSRFProtect
from hw_3.form import RegistrationForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db.init_app(app)
app.config['SECRET_KEY'] = b'5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'
csrf = CSRFProtect(app)

@app.route('/')
def index():
    return 'Hi'

@app.cli.command("init-db")
def create():
    db.create_all()
    print('Ok')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate():
        firstname = form.firstname.data
        user = User(firstname = form.firstname.data,
                    lastname = form.lastname.data,
                    email = form.email.data,
                    password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return render_template('hello.html', username = firstname)
        ...
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)