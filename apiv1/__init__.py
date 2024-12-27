from flask_restplus import Api
api = Api(title="Pipeline Tracker", version="1.0")

from .stage import create_api as create_stage
api.add_namespace(create_stage())
from .pipeline import create_api as create_pipeline
api.add_namespace(create_pipeline())
from .state import create_api as create_state
api.add_namespace(create_state())
