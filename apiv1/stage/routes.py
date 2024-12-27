from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list stages")
    @api.marshal_list_with(model)
    def get(self):
      '''list many stages'''
      return listStages()

  @api.route('/<int:id>')
  class Instance(Resource):
    pass