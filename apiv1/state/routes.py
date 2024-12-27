from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list states")
    @api.marshal_list_with(model)
    def get(self):
      '''list many states'''
      return listStates()
    @api.doc('delete state')
    #@api.expect(model)
    #@api.marshal_list_with(model)
    def put(self):
      '''find a state by criteria'''
      print(api.payload)
      return findState(api.payload)
    @api.doc('create state', body=model)
    #@api.expect(model)
    #@api.marshal_with(model)
    def post(self):
      '''create a state'''
      return newState(api.payload)
    @api.doc('create state', body=model)
    def delete(self):
      '''create a state'''
      return removeState(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get state')
    @api.marshal_with(model)
    def get(self, id):
      '''find a state by idState'''
      return getState(id)
    @api.doc('modify state', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''modify state with specific idState'''
      return updateState(id, api.payload)
    @api.doc('delete state')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete a state by idState'''
      return deleteState(id)
    pass

  @api.route('/action')
  class Action(Resource):
    @api.doc('perform action')
    def post(self):
      '''Perform action'''
      print(api.payload)
      return applyAction(api.payload)
  @api.route('/workers')
  class Workers(Resource):
    @api.doc('Get worker list')
    def get(self):
      '''Get list of workers'''
      return doGetWorkers()

