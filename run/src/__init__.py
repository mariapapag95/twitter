from flask import Flask

from .controllers.public import controller as public_controller
from .controllers.private import controller as private_controller

omnibus = Flask(__name__)

# SESSION ??

omnibus.register_blueprint(public_controller)
omnibus.register_blueprint(private_controller)

#ERROR HANDLER FUNNY 404 PAGES


