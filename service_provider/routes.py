from . import service_provider
from models import sqlalchemy_obj
from flask import render_template, url_for, flash, redirect, request, abort, g, session
from form import NewEstablishmentForm
from flask.ext.login import login_user, login_required, current_user, logout_user

@service_provider.route('/addest', methods=['POST'])
def Establishment():
    form = NewEstablishmentForm()
    if form.validate_on_submit():
        from models import Establishment, sqlalchemy_obj
        new_establishment_obj = Establishment(user_id=current_user.id,establishment_name=form.establishment_name.data,
                                              website=form.website.data,proprietor=form.proprietor.data,phone=form.phone.data,
                                              email=form.email.data,geo_cordinates=form.geo_cordinates.data,address=form.address.data,
                                              establishment_description=form.establishment_description.data,
                                              home_delivery_option_details=form.home_delivery_option_details.data,
                                              open_days=form.open_days.data, open_time=form.open_time.data,type=form.type.data
                                              )

        sqlalchemy_obj.session.add(new_establishment_obj)
        sqlalchemy_obj.session.commit()
        return render_template('service_provider/add_new_offer.html')

    return render_template('service_provider/add_new_establishment.html',form=form)

@service_provider.route('/')
def index():
    form = NewEstablishmentForm()
    print "inside index"
    return render_template('service_provider/index.html',form=form)
