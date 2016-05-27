from flask import Blueprint
service_provider = Blueprint('service_provider', __name__)
print "blueprint created"

from . import routes