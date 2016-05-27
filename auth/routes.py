from . import auth

from flask import render_template, url_for, flash, redirect, request, abort, g, session
from flask.ext.login import login_user, login_required, current_user, logout_user


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    #session.pop('email', '')
    #session.pop('oauth_state','')
    flash('You have been logged out.')
    return redirect(url_for('service_provider.index'))


@auth.route('/login')
def login():
    from models import get_google_auth, sqlalchemy_obj, User
    from config import Auth
    if current_user.is_authenticated():
        flash("You are already authenticated ")
        print "You are already authorized, just return"
        return render_template('index.html')
    print "Trying to authorize"
    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state
    return render_template('login.html', auth_url=auth_url)




#################################################
# Purpose: CallBack
#
#
#
#
#
#################################################


import json
from urllib2 import HTTPError

@auth.route('/gCallback')
def callback():
    from config import Auth
    #from src.model import get_google_auth
    #from src.model import User, db
    from models import get_google_auth, sqlalchemy_obj, User
    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated():
        print("You are already authorized...woo")
        flash("Your previous session was valid")
        return redirect(url_for('service_provider.index'))
    if 'error' in request.args:
        print "There was a error in request arguments"
        if request.args.get('error') == 'access_denied':
            return 'You denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        print "simply redirecting"
        return redirect(url_for('auth.login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.

        google = get_google_auth()
        print "Got google auth"
        """
        if ( 'oauth_state' in session):
            print "Google auth is in session"
            google = get_google_auth(state=session['oauth_state'])
            print "Google auth is in session"
        try:
            print "trying to fetch google token"
            print "Auth.TOKEN_URI is : " + str(Auth.TOKEN_URI)
            print "Auth.CLIENT_SECRET is : " + str(Auth.CLIENT_SECRET)
            print "request.url is : " + str(request.url)
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url)
            print "Fetched token is " + str(token)
        except HTTPError:
            print "Error from HTTP"
            return 'HTTPError occurred.'
        """
        token = google.fetch_token(
            Auth.TOKEN_URI,
            client_secret=Auth.CLIENT_SECRET,
            authorization_response=request.url)
        google = get_google_auth(token=token)
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            print "Email id is " + email
            user = User.query.filter_by(email=email).first()
            exited = True
            if user is None:
                exited = False
                user = User()
                user.email = email
            user.name = user_data['name']
            print "User name is "+ user.name
            user.tokens = json.dumps(token)
            user.avatar = user_data['picture']
            sqlalchemy_obj.session.add(user)
            sqlalchemy_obj.session.commit()
            login_user(user)
            if (not exited):
                flash("Successfully logged in, have a check on your preferences")
                return redirect(url_for('service_provider.index'))
            else:
                return redirect(url_for('service_provider.index'))
        return 'Could not fetch your information.'