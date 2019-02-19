
from flask import Flask

#csrf = CsrfProtect()
app = Flask(__name__)

#csrf.init_app(app)

from aks import routes


