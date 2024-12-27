from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request

__db = DbInstance.getInstance()



class Stage(__db.Base):
  __tablename__ = "stage"
  idStage = Column(Integer, primary_key = True)
  title = Column(String(150))
  idPipeline = Column(Integer, ForeignKey('pipeline.idPipeline'))
  level = Column(Integer)

  constraints = list()
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idStage" in dictModel) and (dictModel["idStage"] != None):
      self.idStage = dictModel["idStage"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("idPipeline" in dictModel) and (dictModel["idPipeline"] != None):
      self.idPipeline = dictModel["idPipeline"]
    if ('level' in dictModel) and (dictModel['level'] != None):
      self.level = dictModel['level']

  def __repr__(self):
    return '<Stage idStage={} title={} idPipeline={} level={}>'.format(self.idStage, self.title, self.idPipeline, self.level )

  def json(self):
    return {
      "idStage":self.idStage,"title":self.title,"idPipeline":self.idPipeline, "level":self.level
    }

  def update(self, dictModel):
    if ("idStage" in dictModel) and (dictModel["idStage"] != None):
      self.idStage = dictModel["idStage"]
    if ("title" in dictModel) and (dictModel["title"] != None):
      self.title = dictModel["title"]
    if ("idPipeline" in dictModel) and (dictModel["idPipeline"] != None):
      self.idPipeline = dictModel["idPipeline"]
    if ("level" in dictModel) and (dictModel["idPipeline"] != None):
      self.level = dictModel["level"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(Stage).all()
  __db.session().commit()
  return result  
  
def __doNew(instance):
  __db.session().add(instance)
  __db.session().commit()
  return instance

def __doGet(id):
  instance = __db.session().query(Stage).filter(Stage.idStage == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getStage(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getStage(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance
def __doFind(model):
  results = __db.session().query(Stage).filter_by(**model).all()
  __db.session().commit()
  return results


def listStages():
  doLog("list DAO function")
  try:
    return __doList()
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doList()
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doList()
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def newStage(model):
  doLog("new DAO function. model: {}".format(model))
  instance = Stage(model)
  res = False
  try:
    return __doNew(instance)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(instance)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def getStage(id):
  doLog("get DAO function", id)
  try:
    return __doGet(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except InterfaceError as e:
    doLog(e)
    __recover()
    return __doGet(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def updateStage(id, model):
  doLog("update DAO function. Model: {}".format(model))
  try:
    return __doUpdate(id, model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doUpdate(id, model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def deleteStage(id):
  doLog("delete DAO function", id)
  try:
    return __doDelete(id)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doDelete(id)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def findStage(model):
  doLog("find DAO function %s" % model)
  try:
    return __doFind(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doFind(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e
