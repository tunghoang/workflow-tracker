from flask_restplus.fields import Integer, Float, String, String as Text, Date, DateTime, Boolean

def create_model(api):
  model = api.model('stage', {
    'idStage': Integer,
    'title': String,
    'idPipeline': Integer 
  },mask='*');
  return model