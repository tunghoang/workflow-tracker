from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('state', {
    'idState': Integer,
    'idStage': Integer,
    'start': DateTime,
    'status': Integer 
  },mask='*');
  return model