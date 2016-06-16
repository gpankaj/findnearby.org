from . import service_provider
from models import sqlalchemy_obj
from flask import render_template, url_for, flash, redirect, request, abort, g, session, Session, jsonify
from form import NewEstablishmentForm,AddOfferForm,EditOfferForm
from flask.ext.login import login_user, login_required, current_user, logout_user

#############################################
# ADD NEW Establishment
#############################################
@service_provider.route('/addest', methods=['POST','GET'])
@login_required
def Establishment():
    form = NewEstablishmentForm()
    print "Reaached here.."
    from models import Establishment_Type

    #form.type.choices = [(int(type.id), type.name) for type in Establishment_Type.query.all()]


    print form.errors

    if form.is_submitted():
        print "submitted"

    if form.validate():
        print "valid"

    print form.errors

    if form.validate_on_submit() and request.method=='POST':
        from models import Establishment, sqlalchemy_obj
        new_establishment_obj = Establishment(user_id=current_user.id,
                                              establishment_name=request.form['establishment_name'])

        if ('choices_from_form' in request.form and request.form['choices_from_form']):
            new_establishment_obj.type = request.form['choices_from_form']

        if ('establishment_description' in request.form and request.form['establishment_description']):
            new_establishment_obj.establishment_description = request.form['establishment_description']

        home_delivery = 'NA'
        if ('optradio1' in request.form and request.form['optradio1']):
            home_delivery = "available"
        elif ('optradio2' in request.form and request.form['optradio2']):
            home_delivery =  "not available"

        new_establishment_obj.home_delivery_option_details = home_delivery


        if ('proprietor' in request.form and request.form['proprietor']):
            new_establishment_obj.proprietor = request.form['proprietor']

        open_days = ""
        if('open_day_monday' in request.form):
            print "On Monday its : " + request.form['open_day_monday']
            open_days = request.form['open_day_monday']

        if ('open_day_tuesday' in request.form):
            open_days = open_days + ","+ request.form['open_day_tuesday']

        if ('open_day_wednesday' in request.form):
            open_days = open_days + ","+ request.form['open_day_wednesday']

        if ('open_day_thrusday' in request.form):
            open_days = open_days + ","+ request.form['open_day_thrusday']

        if ('open_day_friday' in request.form):
            open_days = open_days + ","+ request.form['open_day_friday']

        if ('open_day_saturday' in request.form):
            open_days = open_days + ","+ request.form['open_day_saturday']

        if ('open_day_sunday' in request.form):
            open_days = open_days + "," + request.form['open_day_sunday']

        new_establishment_obj.open_days = open_days



        if ('phone' in request.form and request.form['phone']):
            new_establishment_obj.phone = request.form['phone']

        if ('email' in request.form and request.form['email']):
            new_establishment_obj.email = request.form['email']

        if ('website' in request.form and request.form['website']):
            new_establishment_obj.website = request.form['website']


        timings=""
        if ('open_time' in request.form and request.form['open_time']):
            timings = "From " + request.form['open_time']
        if ('close_time' in request.form and request.form['close_time']):
            timings = timings + " To: " + request.form['close_time']
        new_establishment_obj.open_time = timings



        if ('name_of_shopping_complex' in request.form and request.form['name_of_shopping_complex']):
            new_establishment_obj.name_of_shopping_complex = request.form['name_of_shopping_complex']


        if ('geo_cordinates' in request.form and request.form['geo_cordinates']):
            print "get cordinates " + request.form['geo_cordinates']
            new_establishment_obj.geo_cordinates = request.form['geo_cordinates']

        if ('address' in request.form and request.form['address']):
            print "Address " + request.form['address']
            new_establishment_obj.address = request.form['address']



        sqlalchemy_obj.session.add(new_establishment_obj)
        sqlalchemy_obj.session.commit()

        """

                                              website=form.website.data,proprietor=form.proprietor.data,phone=form.phone.data,
                                              email=form.email.data,geo_cordinates=form.geo_cordinates.data,address=form.address.data,
                                              establishment_description=form.establishment_description.data,
                                              home_delivery_option_details=form.home_delivery_option_details.data,
                                              open_days=form.open_days.data, open_time=form.open_time.data,type=form.type.data
                                              )

        sqlalchemy_obj.session.add(new_establishment_obj)
        sqlalchemy_obj.session.commit()


        flash("Your establishment is added successfully, now add offers")

        return redirect(url_for('service_provider.Offer',establishment_id=new_establishment_obj.id))
        """
        #new_establishment_obj.id
        #return render_template('service_provider/add_new_offer.html')

    return render_template('service_provider/add_new_establishment.html',latlang=(session['lat'],session['long']),form=form)

#############################################
# Edit Establishment
#############################################
@service_provider.route('/editest/<int:establishment_id>', methods=['POST','GET'])
@login_required
def EditEstablishment(establishment_id):
    from models import Establishment
    from form import EditEstablishmentForm
    establishment_update_obj = Establishment.query.filter_by(id=establishment_id).first()
    edit_form = EditEstablishmentForm(obj=establishment_update_obj)
    if edit_form.validate_on_submit():
        edit_form.populate_obj(establishment_update_obj)
        sqlalchemy_obj.session.commit()
        flash("Your establishment details are successfully updated")
        return redirect(url_for('service_provider.index'))
        # new_establishment_obj.id
        # return render_template('service_provider/add_new_offer.html')
    return render_template('service_provider/add_new_establishment.html', latlang=(session['lat'],session['long']),form=edit_form)



"""
@service_provider.route('/location',methods=['POST'])
def location():
    print "I got your location"
    print request.form['lat']
    print request.form['long']
    print dir(request)
    from flask import jsonify
    return jsonify({})
"""

@service_provider.route('/location',methods=['GET'])
def location():
    if('lat' in session and 'long' in session):
        print "Session already exists in session object"

    if (request.args.get('lat') and request.args.get('long')):
        print "Got lat long from client side"
        session['lat'] = request.args.get('lat')
        session['long'] = request.args.get('long')
    else:
        print "Could not get lat long from client side .."
    return jsonify({'result': 'success'})

@service_provider.route('/email',methods=['GET'])
def email():
    if (request.args.get('id') and request.args.get('offer_id')):

        print "Email id was " +request.args.get('id')
        from flask_mail import Message

        from models import Offer
        offer_obj = Offer.query.filter_by(id=request.args.get('offer_id')).first()

        html = render_template('service_provider/single_offer_email.html', offer = offer_obj)

        path_to_static = 'C:/Users/pankajg/Desktop/flask/livedeals/static/'
        pictures = offer_obj.offer_pictures_location.split(',')
        send_simple_message("liveDeals - Offer for you",html,path_to_static + pictures[0],request.args.get('id'))
    return jsonify({'status': 'success'})

def send_simple_message(subject, body, picture, to):
    import requests
    return requests.post(
        "https://api.mailgun.net/v3/sandbox027b2780d1db430d8d9a336f2883aa75.mailgun.org/messages",
        auth=("api", "key-9e6f3ad5ff5e24140f18e1fe35015228"),
        files={"inline":("image", open(picture))},
        data={"from": "Mailgun Sandbox <postmaster@sandbox027b2780d1db430d8d9a336f2883aa75.mailgun.org>",
              "to": to,
              "subject": subject,
              "text": "Testing some Mailgun awesomness!",
              "html": body})


@service_provider.route('/sms',methods=['GET'])
def sms():
    if (request.args.get('id') and request.args.get('offer_id')):

        import requests
        request_location_url='http://maps.googleapis.com/maps/api/geocode/json?latlng='+request.args.get('lat')+","+request.args.get('long')
        print request_location_url
        location_response = requests.get(request_location_url).json()
        users_address = location_response.get('results')[0]['formatted_address']

        from models import Establishment, Offer

        offer_obj = Offer.query.filter_by(id=request.args.get('offer_id')).first()
        establishment_obj = Establishment.query.filter_by(id=offer_obj.establishments_id).first()

        from common import sms
        message = "Callback #" + str(request.args.get('id')) + " for offer id " + request.args.get('offer_id') + " \nHis approx location: " + users_address+ "\n\n"

        print "We have sent message " + message
        print "To " + establishment_obj.phone

        sms_obj = sms.send_sms(establishment_obj.phone, message)
        print "Message was sent with this return value " + str(sms_obj.send())
    return jsonify({'status': 'success'})



@service_provider.route('/')
@service_provider.route('/searches',methods=['GET'])
@service_provider.route('/alloffers',methods=['GET'])
@service_provider.route('/alloffers/<int:establishment_id>',methods=['GET'])
def index(establishment_id=None):
    print "inside index, list all the offers"
    from models import get_google_auth
    from config import Auth

    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state

    print "Reached inside index again.... #########################"
    print "request.remote_addr ADDRESS IS HERE" + str(request.remote_addr)

    #include offers
    from models import Offer, Establishment,All_Service
    all_offers = Offer.query.filter(Offer.owner).filter_by(is_active=1).filter_by(category='activities').all()
    allowed_distance = 40

    if(establishment_id):
        all_offers = Offer.query.filter(Offer.owner).filter_by(is_active=1).filter_by(establishment_id=establishment_id).all()
        allowed_distance=100
    elif (request.script_root == '/alloffers'):
        all_offers = Offer.query.filter(Offer.owner).filter_by(is_active=1)
        allowed_distance=100

    if (request.args.get('distance') and request.args.get('category')):
        #Offer.query.filter(Offer.owner).filter_by(is_active=1, )
        all_offers = Offer.query.filter(Offer.owner).filter_by(is_active=1).filter_by(category=request.args.get('category').rstrip()).all()
        allowed_distance=request.args.get('distance')

        #all_offers = Offer.query.filter(Offer.owner).filter_by(is_active=1).all()
        #all_offers = Offer.query.filter(Offer.owner).filter_by(is_active=1).all()

    new_offers = []
    take_out = False
    suggest_distance = None
    if (session.get('lat') and session.get('long')):
        print "Your lat is " + session.get('lat', 'lat not found')
        print "Your long is " + session.get('long', 'Longitude not found')
        print "Your distance requirement is " + str(allowed_distance)
        if 'category' in request.args:
            print "Your category is " + request.args.get('category')

        client_location = (session.get('lat'), session.get('long'))

        for offer in all_offers:
            vendor_location = offer.owner.geo_cordinates
            # https://pypi.python.org/pypi/geopy
            from geopy.distance import great_circle
            distance = great_circle(client_location, vendor_location).kilometers
            if(distance < int(allowed_distance)):
                offer.current_distance =  int(distance)
                print "Allowed distance was " + str(allowed_distance) + " actual distance was " + str(distance)
                new_offers.append(offer)
            else:
                if(take_out==True):
                    if (distance > suggest_distance):
                        suggest_distance=distance
                        print "Distance is set to " + str(suggest_distance)
                else:
                    print "Turned taken out to true for taken_out"
                    take_out=True
                    suggest_distance=distance
                    print "Distance is set to " + str(suggest_distance)
                print "Offer is taken out, offer id : " + str(offer.id) + " distance was " + str(distance)
    else:
        new_offers = all_offers


    if(len(new_offers) < 1):
        if(take_out==True):
            flash("Please broden your search criteria by changing distance to .. " + str(suggest_distance))
        else:
            flash("There is no result for this category, please change the category ")

    return render_template('service_provider/index.html',auth_url=auth_url,offers = new_offers)




@service_provider.route('/my_establishments')
@login_required
def my_establishments():
    from models import Establishment
    my_establishments_list = Establishment.query.filter_by(user_id=current_user.id).all()

    # If there is no establishemnts
    if(not my_establishments_list):
        flash('Currently there is no Establishment added by you')
        return redirect(url_for('service_provider.index'))
    return render_template('service_provider/my_list_of_establishment.html',my_list=my_establishments_list)



@service_provider.route('/my_offers_establishment')
@login_required
def my_offers():
    from models import Offer,Establishment
    my_offers_list = Offer.query.filter_by(user_id=current_user.id).all()
    new_my_offers_list = []

    for offer in my_offers_list:
        establishment_offer = Establishment.query.filter_by(id=offer.establishments_id).first()
        offer.establishment_name = establishment_offer.establishment_name
        new_my_offers_list.append(offer)

    # if there are no offers
    if (not new_my_offers_list):
        flash('Currently there are no offers added by you')
        return redirect(url_for('service_provider.index'))

    return render_template('service_provider/my_list_of_offers.html', my_list=new_my_offers_list)


@service_provider.route('/my_active_offers_establishment')
@login_required
def my_active_offers():
    from models import Offer, Establishment
    my_offers_list = Offer.query.filter_by(user_id=current_user.id,is_active=1).all()
    new_my_offers_list = []

    for offer in my_offers_list:
        establishment_offer = Establishment.query.filter_by(id=offer.establishments_id).first()
        offer.establishment_name = establishment_offer.establishment_name
        new_my_offers_list.append(offer)

    # if there are no offers
    if (not new_my_offers_list):
        flash('Currently there are no offers added by you')
        return redirect(url_for('service_provider.index'))

    return render_template('service_provider/my_list_of_offers.html', my_list=new_my_offers_list)



@service_provider.route('/addoffer/<int:establishment_id>', methods=['POST','GET'])
@service_provider.route('/addoffer', methods=['POST','GET'])
@login_required
def Offer(establishment_id=None):
    form=AddOfferForm()
    from models import Establishment

    if(establishment_id==None):
        all_my_establishments = Establishment.query.filter_by(user_id=current_user.id).all()

        if(not all_my_establishments):
            flash('Please add establishment detail before its offers')
            return redirect(url_for('service_provider.Establishment'))
        form.establsihment.choices = [(establishment.id,establishment.establishment_name) for establishment in all_my_establishments]
    else:

        my_establishment = Establishment.query.filter_by(id=establishment_id).first()
        if (not my_establishment):
            flash('Please add establishment detail before its offers')
            return redirect(url_for('service_provider.Establishment'))
        form.establsihment.choices = [(establishment_id,my_establishment.establishment_name)]

    if form.validate_on_submit():
        from models import Offer, sqlalchemy_obj
        from werkzeug import secure_filename
        import os
        from manage import my_app_obj

        print "Your establishment code is " + str(form.establsihment.data)

        new_offer_obj = Offer(offer_description=form.offer_description.data, validity=form.validity.data,
                              establishments_id=form.establsihment.data, conditions=form.conditions.data, user_id=current_user.id)

        sqlalchemy_obj.session.add(new_offer_obj)
        sqlalchemy_obj.session.commit()

        file_path_string_comma_seperated = ""
        #http://stackoverflow.com/questions/23706370/wtforms-multi-selection-file-upload
        picture_count = 0
        for a_picture in request.files.getlist("offer_picture"):
            #uploaded_files = request.files.getlist("offer_picture[]")

            ###############################################Uploading pictures
            print "Uploading " + a_picture.filename
            file_name = secure_filename(a_picture.filename)

            picture_storage_path = os.path.join(os.getcwd(),'static','gallery' , str(form.establsihment.data), str(new_offer_obj.id))

            file_storage_path = "/".join(['gallery' , str(form.establsihment.data), str(new_offer_obj.id)])
            print "Path of file storage is " + file_storage_path

            if not os.path.exists(picture_storage_path):
                os.makedirs(picture_storage_path)

            file_path_with_name =  os.path.join(os.getcwd(),'static','gallery' , str(form.establsihment.data), str(new_offer_obj.id), file_name)

            if (picture_count==0):
                file_path_string_comma_seperated = str(file_storage_path+"/" + file_name)
                picture_count = picture_count + 1
            else:
                file_path_string_comma_seperated = file_path_string_comma_seperated + "," + str(file_storage_path+"/" + file_name)


            print "Complete path is " + file_path_with_name
            a_picture.save(file_path_with_name)
            image_size(file_path_with_name)
            ###############################################Uploading pictures####################
        new_offer_obj.offer_pictures_location = file_path_string_comma_seperated
        sqlalchemy_obj.session.commit()

        flash("Your offer is added, congratulations - Let's see customers now")
        return redirect(url_for('service_provider.index'))

    return render_template('service_provider/edit_offer.html', form=form)



@service_provider.route('/editoffer/<int:offer_id>', methods=['POST','GET'])
@login_required
def EditOffer(offer_id):
    from models import Offer,Establishment

    offer_obj = Offer.query.filter_by(id=offer_id).first()

    establishment_obj = Offer.query.join(Establishment,Offer.establishments_id==Establishment.id) \
            .add_columns(Offer.establishments_id, Offer.id,Establishment.id,Establishment.establishment_name)\
                .filter(Offer.id==offer_id).all()

    edit_form=EditOfferForm(obj=offer_obj)
    edit_form.establsihment.choices = [(offer_obj.id,establishment_obj[0].establishment_name)]

    if edit_form.validate_on_submit():
        from models import sqlalchemy_obj
        from werkzeug import secure_filename
        import os
        from manage import my_app_obj

        print "Your establishment code is " + str(edit_form.establsihment.data)
        if(edit_form.offer_picture.data) :
            filename = secure_filename(edit_form.offer_picture.data.filename)
            edit_form.offer_picture.data.save(os.path.join(my_app_obj.config['UPLOAD_FOLDER'] + filename))

        edit_form.populate_obj(offer_obj)
        sqlalchemy_obj.session.commit()
        flash("Your offer details are successfully updated")
        return redirect(url_for('service_provider.index'))

    return render_template('service_provider/edit_offer.html', form=edit_form)


@service_provider.route('/showoffer/<int:offer_id>', methods=['GET'])
def ShowOffer(offer_id):
    from models import Offer, Establishment

    offer_obj = Offer.query.filter_by(id=offer_id).first()

    # from offer id find establishment name.

    establishment_obj = Establishment.query.filter_by(id=offer_obj.establishments_id).first()

    offer_obj.establishment = establishment_obj
    print "Establishment Name is " + establishment_obj.establishment_name
    print "Establishment id is " + str(establishment_obj.id)

    from models import get_google_auth
    from config import Auth

    google = get_google_auth()
    auth_url, state = google.authorization_url(
        Auth.AUTH_URI, access_type='offline')
    session['oauth_state'] = state

    return render_template('service_provider/single_offer_display.html', auth_url=auth_url, offer=offer_obj)

#showalloffers

def image_size(filename):
    from common import image_resize
    image_resize.resize_file(filename, (640, 427))
