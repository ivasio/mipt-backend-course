from flask import Flask, session, request, redirect, url_for, render_template
import model

app = Flask(__name__)
app.secret_key = b'87iqu$62@f4.0p679oi329}'


@app.route('/', methods=['GET'])
def index():
	if 'email' in session:
		return render_template('index.html', email=session['email'])
	else:
		return redirect(url_for('login'))


@app.route('/login/', methods=['GET', 'POST'])
def login():
	if request.method == 'POST' and 'email' in request.form:
		email = request.form['email']
		if model.check_user_is_registered(email):
			session['email'] = email
			return redirect(url_for('index'))
		else:
			return render_template('login.html', error_message=f'No user with email {email} \
				was registered!')
	else:
		return render_template('login.html')


@app.route('/register/', methods=['GET', 'POST'])
def register():
	if request.method == 'POST' and 'email' in request.form:
		email = request.form['email']
		if model.check_user_is_registered(email):
			return render_template('login.html', error_message=f'User with email {email} is \
				already registered!')
		else:
			model.register_user(email)
			return render_template('confirmation_sent.html', email=email)
	else:
		return render_template('register.html')


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('email', None)
    return render_template('logout.html')


@app.route('/confirm/<token>', methods=['GET'])
def confirm(token):
	email = model.confirm_email_by_token(token)
	if email:
		return render_template('confirmation.html', confirmed=True, email=email)
	else:
		return render_template('confirmation.html', confirmed=False)


app.run()