from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField,SelectField, SelectMultipleField, TextAreaField,DateTimeField, DateField
from wtforms.validators import Required, Length, Email, EqualTo


class NewEstablishmentForm(Form):
    establishment_name = StringField('Name of Establishment',validators=[Required()],render_kw={"placeholder": "Name of Your Establishment"})

    type = SelectField('establishment_type',default='Shop', choices=[('shop', 'Shop - Sell Products like Electronics'),
                        ('services', 'Service Provider - Sell Services like Packers, Child Care Centre, Hotels')])

    establishment_description = TextAreaField('Establishment Description')
    home_delivery_option_details = StringField('Home Delivery',render_kw={"placeholder": "Your terms for home delivery of product if applicable"})
    proprietor = StringField('Proprietor name')
    open_days = StringField('Open Days')
    open_time = DateTimeField('Open time')
    website = StringField('Website')
    phone = StringField('Phone Number')
    email = StringField('Email')
    geo_cordinates = StringField('Geo Cordinates')
    address = TextAreaField('Complete Address')
    submit = SubmitField('submit')


    # city, State, Pin. TBD

