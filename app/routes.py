from app import app
from app.forms import SignupForm
from flask import render_template, flash, redirect
from app.sandbox import Alert


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Alex'}
    return render_template('index.html', title='Index', user=user)


@app.route('/alerts')
def alerts():
    return render_template('alerts.html', title='Alerts', alert=Alert)
# TODO: Refresh API call every time the webpage is accessed/refreshed


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('signup.html', title='Sign In', form=form)

