from sqlalchemy import ForeignKey, Column, BigInteger, Integer, Float, String, Boolean, Date, DateTime, Text
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.exc import *
from ..db_utils import DbInstance
from ..app_utils import *
from werkzeug.exceptions import *
from flask import session,request,after_this_request
import dateutil.parser as dparser

import json
import sys, os
import traceback

#sys.path.append('/home/tunghx/workspace/apom_pipeline' if os.getenv('POP_COMMON_DIR') is None else os.getenv('PIPELINE_BASE'))
from master import enqueueJob, getWorkers

__db = DbInstance.getInstance()



class State(__db.Base):
  __tablename__ = "state"
  idState = Column(Integer, primary_key = True)
  idStage = Column(Integer, ForeignKey('stage.idStage'))
  start = Column(DateTime)
  status = Column(Integer)

  constraints = list()
  constraints.append(UniqueConstraint('idStage','start'))
  if len(constraints) > 0:
    __table_args__ = tuple(constraints)
 
  def __init__(self, dictModel):
    if ("idState" in dictModel) and (dictModel["idState"] != None):
      self.idState = dictModel["idState"]
    if ("idStage" in dictModel) and (dictModel["idStage"] != None):
      self.idStage = dictModel["idStage"]
    if ("start" in dictModel) and (dictModel["start"] != None):
      self.start = dictModel["start"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

  def __repr__(self):
    return '<State idState={} idStage={} start={} status={} >'.format(self.idState, self.idStage, self.start, self.status, )

  def json(self):
    return {
      "idState":self.idState,"idStage":self.idStage,"start":str(self.start),"status":self.status,
    }

  def update(self, dictModel):
    if ("idState" in dictModel) and (dictModel["idState"] != None):
      self.idState = dictModel["idState"]
    if ("idStage" in dictModel) and (dictModel["idStage"] != None):
      self.idStage = dictModel["idStage"]
    if ("start" in dictModel) and (dictModel["start"] != None):
      self.start = dictModel["start"]
    if ("status" in dictModel) and (dictModel["status"] != None):
      self.status = dictModel["status"]

def __recover():
  __db.newSession()

def __doList():
  result = __db.session().query(State).all()
  __db.session().commit()
  return result  
  
def __doNew(model):
  pipelineName = model.get("pipeline", None)
  stageName = model.get("stage", None)
  startDate = model.get("start", None)
  status = model.get("status", None)
  if all(v is None for v in [pipelineName, stageName, startDate, status]):
    raise Exception("Parameter missing")
  
  params = {"pipelineName": pipelineName, "stageName": stageName, "startDate": dparser.isoparse(startDate).isoformat(), "status": int(status)}
  
  results = __doFind(model)
  if len(results) == 0:
    # Create new Instance
    insertQuery = f"""
INSERT INTO "state"("idStage", "start", "status") 
  SELECT "stage"."idStage" "idStage", :startDate "start", :status "status"
    FROM "stage" JOIN "pipeline" ON "stage"."idPipeline" = "pipeline"."idPipeline"
    WHERE "pipeline"."name" = :pipelineName AND "stage"."title" = :stageName
"""
    result = __db.session().execute(insertQuery, params)
    __db.session().commit()
    if result.rowcount == 0:
      return {"success": False}
  else:
    # Update existing instance
    updateQuery = f"""
UPDATE "state" set "status" = "temp"."status" 
FROM (
  SELECT :status as "status", "stage"."idStage" as "idStage"
  FROM "stage" JOIN "pipeline" ON "stage"."idPipeline" = "pipeline"."idPipeline"
  WHERE "stage"."title" = :stageName AND "pipeline"."name" = :pipelineName
) as "temp"
WHERE "state"."start" = :startDate AND "state"."idStage" = "temp"."idStage"
"""
    result = __db.session().execute(updateQuery, params)
    __db.session().commit()
  return {"success": True}

def __doGet(id):
  instance = __db.session().query(State).filter(State.idState == id).scalar()
  doLog("__doGet: {}".format(instance))
  __db.session().commit()
  return instance

def __doUpdate(id, model):
  instance = getState(id)
  if instance == None:
    return {}
  instance.update(model)
  __db.session().commit()
  return instance
def __doDelete(id):
  instance = getState(id)
  __db.session().delete(instance)
  __db.session().commit()
  return instance.json()
def __doFind(model):
  pipelineName = model.get("pipeline", None)
  stageName = model.get("stage", None)
  startDate = model.get("start", None)
  fromDate = model.get("fromDate", None)
  params = {}
  whereClause = "WHERE 1=1 "

  print(" +++++++++++++++++++++++ ", pipelineName, "-------------------")

  if pipelineName:
    if type(pipelineName) == list and len(pipelineName) > 0:
      inStatement = ""
      for idx, p in enumerate(pipelineName):
          if idx == 0:
              inStatement = inStatement + f"'{p}'"
          else:
              inStatement = inStatement + f",'{p}'"
      whereClause = whereClause + f"AND \"pipeline\".\"name\" in ( {inStatement} )  "
      params["pipelineName"] = pipelineName
    elif type(pipelineName) == str:
      whereClause = whereClause + "AND \"pipeline\".\"name\" = :pipelineName "
      params["pipelineName"] = pipelineName
  else:
    print("kakakakakakakakakakaka")
    whereClause = whereClause + "AND 1 = 0 "
  if stageName:
    whereClause = whereClause + "AND \"stage\".\"title\" = :stageName "
    params["stageName"] = stageName
  if startDate:
    whereClause = whereClause + "AND \"state\".\"start\" = :startDate "
    params["startDate"] = dparser.isoparse(startDate).isoformat()
  if fromDate:
    whereClause = whereClause + "AND \"state\".\"start\" >= :fromDate "
    params["fromDate"] = dparser.isoparse(fromDate).isoformat()
  query = f'''
SELECT "state"."idState", "state"."start", "state"."status", "stage"."idStage", "pipeline"."idPipeline", "pipeline"."name", "stage"."title", "stage"."level" FROM "state" 
INNER JOIN "stage" ON "state"."idStage" = "stage"."idStage"
INNER JOIN "pipeline" ON "stage"."idPipeline" = "pipeline"."idPipeline"
{whereClause}
ORDER BY "state"."start", "stage"."level"
'''
  results = __db.session().execute(query, params).fetchall()
  __db.session().commit()
  return list(map(lambda x: {'idState': x[0], 'startDate': str(x[1]), 'status': x[2], 'idStage': x[3], 'idPipeline': x[4], 'pipeline': x[5], 'stage': x[6], 'level': x[7]}, results))

def __doRemove(model):
  results = __doFind(model)
  if len(results) > 0:
    print(results[0])
    return __doDelete(int(results[0]['idState']))
  return {}

def listStates():
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

def newState(model):
  doLog("new DAO function. model: {}".format(model))
  res = False
  try:
    return __doNew(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doNew(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def getState(id):
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

def updateState(id, model):
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

def deleteState(id):
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

def findState(model):
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
def removeState(model):
  doLog("find DAO function %s" % model)
  try:
    return __doRemove(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doRemove(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def __doAction(model):
  action = model.get('action', None)
  pipeline = model.get('pipeline', None)
  stage = model.get('stage', None)
  startDate = model.get('start', None)
  if any( v is None for v in (action, pipeline, stage, startDate)):
    raise Exception("Missing parameters")
  if action == 'RUN':
    text = enqueueJob(f'{pipeline}.tasks.{stage}', startDate)
    print("------++++-------", { 'success': True, 'message': text })
    return { 'success': True, 'message': text }
  elif action == 'FORCE_RUN':
    __doRemove(model)
    text = enqueueJob(f'{pipeline}.tasks.{stage}', startDate)
    print("------++++-------", { 'success': True, 'message': text })
    return { 'success': True, 'message': text }
  else:
    pass
  raise Exception("Not implemented")

def applyAction(model):
  doLog('apply action %s' % model)
  try:
    return __doAction(model)
  except OperationalError as e:
    doLog(e)
    __recover()
    return __doAction(model)
  except SQLAlchemyError as e:
    __db.session().rollback()
    raise e

def doGetWorkers():
  doLog('get workers')
  try:
    return getWorkers()
  except:
    traceback.print_exc()
