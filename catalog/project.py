from flask import Flask, render_template, url_for
from flask import request, redirect, flash, make_response, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Data_Setup import Base, TabletCompanyName, TabletName, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests
import datetime

engine = create_engine('sqlite:///tablets.db',
                       connect_args={'check_same_thread': False}, echo=True)
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json',
                            'r').read())['web']['client_id']
APPLICATION_NAME = "Tablets Store"

DBSession = sessionmaker(bind=engine)
session = DBSession()
tb_car = session.query(TabletCompanyName).all()


@app.route('/login')
def showLogin():
    ''' Login to application '''

    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in range(32))
    login_session['state'] = state
    tb_car = session.query(TabletCompanyName).all()
    crs = session.query(TabletName).all()
    return render_template('login.html',
                           STATE=state, tb_car=tb_car, crs=crs)


@app.route('/gconnect', methods=['POST'])
def gconnect():

    ''' Validate state token '''

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    ''' Obtain authorization code '''
    code = request.data

    try:
        ''' Upgrade the authorization code into a credentials object '''
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Check that the access token is valid. '''
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    ''' If there was an error in the access token info, abort. '''
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Verify that the access token is used for the intended user.'''
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    '''Verify that the access token is valid for this app.'''
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print ("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    ''' Store the access token in the session for later use.'''
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    ''' see if user exists, if it doesn't make a new one '''
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px;'
    '-webkit-border-radius: 150px; -moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print ("done!")
    return output


def createUser(login_session):
    ''' User Helper Functions '''
    U1 = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(U1)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception as error:
        print(error)
        return None

# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/')
@app.route('/home')
def home():
    ''' Display the Home page '''
    tb_car = session.query(TabletCompanyName).all()
    return render_template('myhome.html', tb_car=tb_car)

# Tablet Category for admins


@app.route('/tabletStore')
def TabletStore():
    '''Diaplayed by the Main Page of TabletStore '''
    try:
        if login_session['username']:
            name = login_session['username']
            tb_car = session.query(TabletCompanyName).all()
            tb = session.query(TabletCompanyName).all()
            crs = session.query(TabletName).all()
            return render_template('myhome.html', tb_car=tb_car,
                                   tb=tb, crs=crs, uname=name)
    except:
        return redirect(url_for('showLogin'))


@app.route('/tabletStore/<int:crid>/AllCompanys')
def showTablets(crid):
    ''' Showing tablets based on tablet category '''
    tb_car = session.query(TabletCompanyName).all()
    tb = session.query(TabletCompanyName).filter_by(id=crid).one()
    crs = session.query(TabletName).filter_by(tabletcompanynameid=crid).all()
    try:
        if login_session['username']:
            return render_template('showTablets.html', tb_car=tb_car,
                                   tb=tb, crs=crs,
                                   uname=login_session['username'])
    except:
        return render_template('showTablets.html',
                               tb_car=tb_car, tb=tb, crs=crs)


@app.route('/tabletStore/addTabletCompany', methods=['POST', 'GET'])
def addTabletCompany():
    ''' Add New TabletCompany '''
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    if request.method == 'POST':
        company = TabletCompanyName(name=request.form['name'],
                                    user_id=login_session['user_id'])
        session.add(company)
        session.commit()
        return redirect(url_for('TabletStore'))
    else:
        return render_template('addTabletCompany.html', tb_car=tb_car)


@app.route('/tabletStore/<int:crid>/edit', methods=['POST', 'GET'])
def editTabletCategory(crid):
    ''' Edit Tablet Category '''
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    editTablet = session.query(TabletCompanyName).filter_by(id=crid).one()
    creator = getUserInfo(editTablet.user_id)
    user = getUserInfo(login_session['user_id'])
    # If logged in user != item owner redirect them
    if creator.id != login_session['user_id']:
        flash("You cannot edit this Tablet Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('TabletStore'))
    if request.method == "POST":
        if request.form['name']:
            editTablet.name = request.form['name']
        session.add(editTablet)
        session.commit()
        flash("Tablet Category Edited Successfully")
        return redirect(url_for('TabletStore'))
    else:
        return render_template('editTabletCategory.html',
                               cr=editTablet, tb_car=tb_car)


@app.route('/tabletStore/<int:crid>/delete', methods=['POST', 'GET'])
def deleteTabletCategory(crid):
    ''' Delete Tablet Category '''
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    cr = session.query(TabletCompanyName).filter_by(id=crid).one()
    creator = getUserInfo(cr.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You cannot Delete this Tablet Category."
              "This is belongs to %s" % creator.name)
        return redirect(url_for('TabletStore'))
    if request.method == "POST":
        session.delete(cr)
        session.commit()
        flash("Tablet Category Deleted Successfully")
        return redirect(url_for('TabletStore'))
    else:
        return render_template('deleteTabletCategory.html',
                               cr=cr, tb_car=tb_car)


@app.route('/tabletStore/addCompany/addTabletDetails/<string:crname>/add',
           methods=['GET', 'POST'])
def addTabletDetails(crname):
    '''
     Add New Tablet Name Details '''
    if 'username' not in login_session:
        flash("Please log in to continue.")
        return redirect(url_for('showLogin'))
    tb = session.query(TabletCompanyName).filter_by(name=crname).one()
    ''' See if the logged in user is not the owner of car '''
    creator = getUserInfo(tb.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You can't add new book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showTablets', crid=tb.id))
    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        discription = request.form['discription']
        power = request.form['power']
        tabletdetails = TabletName(name=name,
                                   price=price,
                                   discription=discription,
                                   power=power,
                                   tabletcompanynameid=tb.id,
                                   user_id=login_session['user_id'])
        session.add(tabletdetails)
        session.commit()
        return redirect(url_for('showTablets', crid=tb.id))
    else:
        return render_template('addTabletDetails.html',
                               crname=tb.name, tb_car=tb_car)


@app.route('/tabletStore/<int:crid>/<string:crsname>/edit',
           methods=['GET', 'POST'])
def editTablet(crid, crsname):
    ''' Edit Tablet details '''
    cr = session.query(TabletCompanyName).filter_by(id=crid).one()
    tabletdetails = session.query(TabletName).filter_by(name=crsname).one()
    ''' See if the logged in user is not the owner of tablet '''
    creator = getUserInfo(cr.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You can't edit this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showTablets', crid=cr.id))
    ''' POST methods '''
    if request.method == 'POST':
        tabletdetails.name = request.form['name']
        tabletdetails.price = request.form['price']
        tabletdetails.discription = request.form['discription']
        tabletdetails.power = request.form['power']
        session.add(tabletdetails)
        session.commit()
        flash("Tablet Edited Successfully")
        return redirect(url_for('showTablets', crid=crid))
    else:
        return render_template('editTablet.html',
                               crid=crid, tabletdetails=tabletdetails,
                               tb_car=tb_car)


@app.route('/tabletStore/<int:crid>/<string:crsname>/delete',
           methods=['GET', 'POST'])
def deleteTablet(crid, crsname):
    ''' Delte Tablet Edit '''
    cr = session.query(TabletCompanyName).filter_by(id=crid).one()
    tabletdetails = session.query(TabletName).filter_by(name=crsname).one()
    ''' See if the logged in user is not the owner of car '''
    creator = getUserInfo(cr.user_id)
    user = getUserInfo(login_session['user_id'])
    if creator.id != login_session['user_id']:
        flash("You can't delete this book edition"
              "This is belongs to %s" % creator.name)
        return redirect(url_for('showTablets', crid=cr.id))
    if request.method == "POST":
        session.delete(tabletdetails)
        session.commit()
        flash("Deleted Tablet Successfully")
        return redirect(url_for('showTablets', crid=cr.id))
    else:
        return render_template('deleteTablet.html',
                               crid=crid, tabletdetails=tabletdetails,
                               tb_car=tb_car)


@app.route('/logout')
def logout():
    ''' Logout from current user '''
    access_token = login_session['access_token']
    print ('In gdisconnect access token is %s', access_token)
    print ('User name is: ')
    print (login_session['username'])
    if access_token is None:
        print ('Access Token is None')
        response = make_response(
            json.dumps('Current user not connected....'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = login_session['access_token']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = \
        h.request(uri=url, method='POST', body=None,
                  headers={'content-type':
                           'application/x-www-form-urlencoded'})[0]

    print (result['status'])
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps
                                 ('Successfully disconnected user..'), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("Successful logged out")
        return redirect(url_for('showLogin'))
        # return response
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
'''Json Files'''


@app.route('/tabletStore/JSON')
def allTabletsJSON():
    tabletcategories = session.query(TabletCompanyName).all()
    category_dict = [c.serialize for c in tabletcategories]
    for c in range(len(category_dict)):
        tablets = [i.serialize for i in session.query(TabletName).filter_by(
           tabletcompanynameid=category_dict[c]["id"]).all()]
        if tablets:
            category_dict[c]["car"] = tablets
    return jsonify(TabletCompanyName=category_dict)


@app.route('/tabletStore/tabletCategories/JSON')
def categoriesJSON():
    tablets = session.query(TabletCompanyName).all()
    return jsonify(tabletCategories=[c.serialize for c in tablets])


@app.route('/tabletStore/tablets/JSON')
def itemsJSON():
    items = session.query(TabletName).all()
    return jsonify(tablets=[i.serialize for i in items])


@app.route('/tabletStore/<path:tablet_name>/tablets/JSON')
def categoryItemsJSON(tablet_name):
    tabletCategory = session.query(TabletCompanyName).filter_by(
        name=tablet_name).one()
    tablets = session.query(TabletName).filter_by(
        tabletcompanyname=tabletCategory).all()
    return jsonify(tabletEdtion=[i.serialize for i in tablets])


@app.route('/tabletStore/<path:tabname>/<path:medtablet_name>/JSON')
def ItemsJSON(tabname, medtablet_name):
    tcname = session.query(TabletCompanyName).filter_by(
        name=tabname).one()
    medTabletName = session.query(TabletName).filter_by(
        name=medtablet_name, tabletcompanyname=tcname).one()
    return jsonify(medTabletName=[medTabletName.serialize])

if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host='127.0.0.1', port=8000)
