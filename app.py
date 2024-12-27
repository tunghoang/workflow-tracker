from flask import Flask, session, request
from apiv1 import api
from apiv1.db_utils import DbInstance
from apiv1.app_utils import *
#from flask_session import Session
from werkzeug.exceptions import *
from werkzeug.contrib.fixers import ProxyFix
import os

db = DbInstance.getInstance()

app = Flask("PipelineTracker")
app.wsgi_app = ProxyFix(app.wsgi_app)
app.config["DEBUG"] = True
app.config['SERVER_NAME'] = os.getenv('SERVER_NAME') or "192.168.0.91:8000"
#app.config['SESSION_TYPE'] = 'filesystem'
#app.config['SESSION_FILE_DIR'] = '/tmp'
app.secret_key = os.urandom(16)
api.init_app(app)

print("HEHEHEHEHEHEHEHE")
#Session(app)

@app.before_request
def before_request():
  key = request.cookies.get('key')
  jwt = request.cookies.get('jwt')
  key = key if key is not None else request.headers.get('auth-key')
  jwt = jwt if jwt is not None else request.headers.get('authorization')
  no_auth_routes = ( '/', '/favicon.ico', '/swagger.json' )
  no_auth_prefixes = ( '/', '/swaggerui', )

  if request.path in no_auth_routes or matchOneOf(request.path, no_auth_prefixes) :
    return None
  elif jwt is None or key is None:
    print("jwt or key", jwt, key)
    raise Unauthorized("Invalid request")
  elif key in session:
    salt = session[key]
    try:
      sessionData = doParseJWT(jwt, salt)
    except:
      raise Unauthorized("Invalid session")
  else:
    raise Unauthorized("Not login")

  return None

db.Base.metadata.create_all(db.engine)

if __name__ == "__main__":
  app.run()
