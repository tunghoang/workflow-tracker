from flask_restplus import Resource
from .db import *

def init_routes(api, model):
  @api.route('/')
  class ListInstances(Resource):
    @api.doc("list pipelines")
    @api.marshal_list_with(model)
    def get(self):
      '''list many pipelines'''
      return listPipelines()
    @api.doc('create pipeline', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def post(self):
      '''create a pipeline'''
      return newPipeline(api.payload)

  @api.route('/<int:id>')
  class Instance(Resource):
    @api.doc('get pipeline')
    @api.marshal_with(model)
    def get(self, id):
      '''find a pipeline by idPipeline'''
      return getPipeline(id)
    @api.doc('modify pipeline', body=model)
    @api.expect(model)
    @api.marshal_with(model)
    def put(self, id):
      '''modify pipeline with specific idPipeline'''
      return updatePipeline(id, api.payload)
    @api.doc('delete pipeline')
    @api.marshal_with(model)
    def delete(self, id):
      '''delete a pipeline by idPipeline'''
      return deletePipeline(id)
    pass