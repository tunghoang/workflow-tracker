from .model import create_model
from .routes import init_routes
from .db import State
from flask_restplus import Namespace

def create_api():
  api = Namespace('state', description="states of stages of piplines")
  model = create_model(api)
  init_routes(api, model)
  return api