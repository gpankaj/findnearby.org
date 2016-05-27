from sqlalchemy import Table,Column, DateTime, String, Integer, ForeignKey, func
from app import create_app,login_manager
import os
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import UserMixin

sqlalchemy_obj = SQLAlchemy(app=create_app(os.getenv('FLASK_CONFIG') or 'default'),use_native_unicode=True)


class User(sqlalchemy_obj.Model,UserMixin):
    __tablename__ = 'users'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)
    email = sqlalchemy_obj.Column(sqlalchemy_obj.String(100), unique=True, nullable=False)
    name = sqlalchemy_obj.Column(sqlalchemy_obj.String(100), nullable=True)
    tokens = sqlalchemy_obj.Column(sqlalchemy_obj.Text)
    created_at = sqlalchemy_obj.Column(DateTime, default=func.now())
    active = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)
    phone_number=sqlalchemy_obj.Column(sqlalchemy_obj.Numeric)
    is_customer = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)
    is_service_provider = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=False)

    # One person may have multiple establishments
    establishments = sqlalchemy_obj.relationship('Establishment',backref='owner',lazy='dynamic')


#User can be customer and/or service_provider and/or both



class Customer(sqlalchemy_obj.Model):
    __tablename__ = 'customers'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)
    is_verified = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)
    #Where this customer live or need services for
    geo_cordinates = sqlalchemy_obj.Column(sqlalchemy_obj.String(256), nullable=True)
    loyality_points =  sqlalchemy_obj.Column(sqlalchemy_obj.String(64), nullable=True)
    my_requirements = sqlalchemy_obj.relationship('Customer_Requirement', backref='customer', lazy='dynamic')


# A user can have multiple establishments
class Establishment(sqlalchemy_obj.Model):
    __tablename__ = 'establishments'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)

    user_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('users.id'))
    #available_service_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('available_services.id'))

    is_verified = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=False)
    establishment_name = sqlalchemy_obj.Column(sqlalchemy_obj.String(256), nullable=False)
    website = sqlalchemy_obj.Column(sqlalchemy_obj.String(128), nullable=True)
    proprietor = sqlalchemy_obj.Column(sqlalchemy_obj.String(128), nullable=True)
    phone = sqlalchemy_obj.Column(sqlalchemy_obj.String(64), nullable=True)
    email = sqlalchemy_obj.Column(sqlalchemy_obj.String(64), nullable=True)
    geo_cordinates = sqlalchemy_obj.Column(sqlalchemy_obj.String(256), nullable=True)
    address = sqlalchemy_obj.Column(sqlalchemy_obj.String(256), nullable=True)
    is_active = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)
    created_at = sqlalchemy_obj.Column(DateTime, default=func.now())

    type = sqlalchemy_obj.Column(sqlalchemy_obj.String(64), unique=True, nullable=False) # shop for selling items or I provide services

    establishment_description = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)
    home_delivery_option_details =  sqlalchemy_obj.Column(sqlalchemy_obj.String(512), nullable=True) # not valid, available, not-available

    open_days =  sqlalchemy_obj.Column(sqlalchemy_obj.String(512), nullable=True)
    open_time = sqlalchemy_obj.Column(sqlalchemy_obj.String(512), nullable=True)


    # This creates a field with the name owner in Service_Provider_Service, so i can query by Service_Provider_Service.owner()
    # above query will give us Service_Provider model. It;s a virtual column not a physical column.

    # I can also query in this class by saying Service_Provider.categories() will return a query with all the categories this establishment has.
    services = sqlalchemy_obj.relationship('All_Service', backref='owner', lazy='dynamic')
    # 1 establishment multiple items
    items = sqlalchemy_obj.relationship('Establishment_Item', backref='owner', lazy='dynamic')

    offers = sqlalchemy_obj.relationship('Offer', backref='owner', lazy='dynamic')
    establishment_responses = sqlalchemy_obj.relationship('Customer_Requirement_Response', backref='establishment', lazy='dynamic')

class Establishment_Item(sqlalchemy_obj.Model):
    __tablename__ = 'establishment_items'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)

    establishments_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('establishments.id'))
    name = sqlalchemy_obj.Column(sqlalchemy_obj.String(256), nullable=False)
    description = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)

    is_active = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)

    in_stock = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=False) # if it's service this field is not valid.

    price_range = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)
    created_at = sqlalchemy_obj.Column(DateTime, default=func.now())




class All_Service(sqlalchemy_obj.Model):
    __tablename__ = 'all_services'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)

    # Sell/Buy product
    # Multiple
    # Merchandise
    # electronics
    # PG (Service)
    # Day care and PreSchool (Service)
    # CA (Service)
    # Doctor (Service)
    #
    establishment_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('establishments.id'))

    requirement_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('customer_requirements.id'))

    service_name = sqlalchemy_obj.Column(sqlalchemy_obj.String(1), unique=True, nullable=False)

    created_at = sqlalchemy_obj.Column(DateTime, default=func.now())




class Customer_Requirement(sqlalchemy_obj.Model):
    __tablename__ = 'customer_requirements'

    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)

    is_verified = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=False)
    customer_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('customers.id'))

    #contact this number for my requirement (if different number from your profile) and if user expected to be contacted by Phone
    phone_number=sqlalchemy_obj.Column(sqlalchemy_obj.Numeric, default=False)
    contact_between_date_time = sqlalchemy_obj.Column(sqlalchemy_obj.String(512),nullable=True)

    description = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)
    expected_price_range = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)

    is_active = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)
    categories = sqlalchemy_obj.relationship('All_Service', backref='customer_categories', lazy='dynamic')
    #Need Service or product?
    # product/service name
    # product/service_category
    # product/service_description
    #announce?
    #responses = sqlalchemy_obj.relationship('Customer_Requirement_Response', backref='customer_requirement', lazy='dynamic')
    active_till = sqlalchemy_obj.Column(DateTime)
    created_at = sqlalchemy_obj.Column(DateTime, default=func.now())
    requirement_response = sqlalchemy_obj.relationship('Customer_Requirement_Response', backref='requirement',
                                                          lazy='dynamic')





class Offer(sqlalchemy_obj.Model):
    __tablename__ = 'offers'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)
    is_active = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean, default=True)
    validity = sqlalchemy_obj.Column(DateTime, nullable=False)
    establishments_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('establishments.id'))
    offer_picture = sqlalchemy_obj.Column(sqlalchemy_obj.Binary)
    offer_description = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)
    customer_responses = sqlalchemy_obj.relationship('Customer_Requirement_Response',backref='offer',lazy='dynamic')

class Customer_Requirement_Response(sqlalchemy_obj.Model):
    __tablename__='customer_requirement_responses'
    id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, primary_key=True)

    response_text = sqlalchemy_obj.Column(sqlalchemy_obj.String(5026), nullable=True)
    establishment_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('establishments.id'))

    customer_requirements_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('customer_requirements.id'))
    offer_id = sqlalchemy_obj.Column(sqlalchemy_obj.Integer, ForeignKey('offers.id'))

    # We mush specify weather it's customer or establishment response
    customer_response = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean)
    establishment_response = sqlalchemy_obj.Column(sqlalchemy_obj.Boolean)
    # It may be marked by customer or establishment as offending response.
    marked_as_offending = sqlalchemy_obj.Column(sqlalchemy_obj.String(128), nullable=True)




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from requests_oauthlib import OAuth2Session

def get_google_auth(state=None, token=None):
    print "I received token as " + str(token)
    print "I received state as " + str(state)
    from config import Auth
    if token:
        return OAuth2Session(Auth.CLIENT_ID, token=token)
    if state:
        return OAuth2Session(
            Auth.CLIENT_ID,
            state=state,
            redirect_uri=Auth.REDIRECT_URI)
    oauth = OAuth2Session(
        Auth.CLIENT_ID,
        redirect_uri=Auth.REDIRECT_URI,
        scope=Auth.SCOPE)
    return oauth



sqlalchemy_obj.create_all()