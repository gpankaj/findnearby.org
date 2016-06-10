from flask_wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField, SelectMultipleField, TextAreaField,DateTimeField, DateField, FileField
from wtforms.validators import Required, Length, Email, EqualTo, Optional


class NewEstablishmentForm(Form):
    establishment_name = StringField('Name of Establishment',render_kw={"placeholder": "Name of Your Establishment"})
    from models import Establishment_Type

    type = SelectField('Establishment Type',coerce=int, choices=[(int(type.id), str(type.name)) for type in Establishment_Type.query.all()], validators=[Optional()])

    establishment_description = TextAreaField('Establishment Description')
    home_delivery_option_details = StringField('Home Delivery',render_kw={"placeholder": "Your terms for home delivery of product if applicable"})
    proprietor = StringField('Proprietor name')
    open_days = StringField('Open Days')
    open_time = StringField('Open time')
    website = StringField('Website URL')
    phone = StringField('Phone Number')
    email = StringField('Email')
    geo_cordinates = StringField('Geo Cordinates')
    name_of_shopping_complex = StringField('Name of shipping Complex if inside')
    address = StringField('Complete Address')
    submit = SubmitField('submit')
    # city, State, Pin. TBD


class EditOfferForm(Form):
    offer_description = StringField('Heading of the offer')
    offer_picture = FileField('Add New Pictures')
    validity = StringField('Specify a date/time till this offer is valid')
    conditions = StringField('Specify your terms and conditions')
    establsihment = SelectField('establishment name', choices=[], coerce=int)
    submit = SubmitField('submit')


class AddOfferForm(Form):
    offer_description = StringField('Heading of the offer')
    offer_picture = FileField('Add picture related to offer',render_kw={'multiple': True},)
    from models import All_Service
    category = SelectField('Category', coerce=int,choices=[(int(category.id), str(category.service_name)) for category in All_Service.query.all()],validators=[Optional()])
    tags = StringField('Specify some tags to identify your business')
    validity = StringField('Specify a date/time till this offer is valid')
    conditions = TextAreaField('Specify your terms and conditions')
    establsihment = SelectField('establishment name',choices=[('est1','establishemnt 1')],coerce=int)
    submit = SubmitField('submit')



class EditEstablishmentForm(Form):
    establishment_name = StringField('Name of Establishment',validators=[Required()],render_kw={"placeholder": "Name of Your Establishment"})

    type = SelectField('establishment_type',default='Shop', choices=[('shop', 'Shop - Sell Products like Electronics'),
                        ('services', 'Service Provider - Sell Services like Packers, Child Care Centre, Hotels')])

    establishment_description = TextAreaField('Establishment Description')
    home_delivery_option_details = StringField('Home Delivery',render_kw={"placeholder": "Your terms for home delivery of product if applicable"})
    proprietor = StringField('Proprietor name')
    open_days = StringField('Open Days')
    open_time = StringField('Open time')
    website = StringField('Website')
    phone = StringField('Phone Number')
    email = StringField('Email')
    is_active=BooleanField('is_active')
    geo_cordinates = StringField('Geo Cordinates')
    name_of_shopping_complex = StringField('Name of shipping Complex if inside')
    address = TextAreaField('Complete Address')
    submit = SubmitField('Save Changes')
    # city, State, Pin. TBD
