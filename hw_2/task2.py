"""
Создать страницу, на которой будет форма для ввода имени и электронной почты, при отправке которой будет
создан cookie-файл с данными пользователя, а также будет произведено перенаправление на страницу приветствия,
где будет отображаться имя пользователя.
На странице приветствия должна быть кнопка «Выйти», при нажатии на которую будет удалён cookie-файл с данными
пользователя и произведено перенаправление на страницу ввода имени и электронной почты.
"""

from flask import Flask, request, redirect, url_for, make_response, session
from flask import render_template

app = Flask(__name__)
app.secret_key = '5f214cacbd30c2ae4784b520f17912ae0d5d8c16ae98128e3f549546221265e4'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        username = request.form['username']
        return redirect(url_for('welcome', username=username))
    return render_template('form.html')


@app.route('/welcome/<username>')
def welcome(username):
    if 'username' in session:
        return render_template('login.html', username=username)
    else:
        return redirect(url_for('login'))


@app.route('/setcookie', methods=['POST', 'GET'])
def setcookie():
    resp = make_response('Setting the cookie')
    resp.set_cookie('username', 'username')
    return resp


@app.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/getcookie/')
def get_cookies():
    name = request.cookies.get('username')
    return f"Значение cookie: {name}"


if __name__ == '__main__':
    app.run(debug=True)
