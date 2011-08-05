from gluon.serializers import json
from plugin_celery import actions


response.menu += [
    (T('Celery Console'),False,None,
     [(T('Task Monitor (Meta)'),False,URL('task_monitor')),
      (T('Periodic Task Monitor (Meta)'),False,URL('periodic_task_monitor')),
      (T('Task Monitor (Camera)'),False,URL('taskstate_monitor')),
      (T('Periodic Task Monitor (Camera)'),False,URL('taskstate_monitor')),
      (T('Workers Monitor'),False,URL('workers_monitor'))])]

pc = plugin_celery
db = plugin_celery.db

def index():
    return locals()

def submit_task():
    name = request.args(0)
    vars = request.vars
    response.headers['Content-Type'] = "application/json"
    return json(actions.submit_task(name,**vars))

def registered_tasks():
    response.headers['Content-Type'] = "application/json"
    return json(actions.registered_tasks())

def task_status():
    """Returns task status and result in JSON format."""
    task_id = request.args(0)
    response.headers['Content-Type'] = "application/json"
    return json(actions.task_status(task_id))

def delete_task():
    task_id = request.args(0)
    print db(pc.taskmeta.task_id==task_id).delete()
    return 
 
def revoke_task():
    task_id = request.args(0)
    return str(actions.revoke_task(task_id))

def terminate_task():
    task_id = request.args(0)
    return str(actions.terminate_task(task_id))

def kill_task():
    task_id = request.args(0)
    return str(actions.kill_task(task_id))

def view_task():
    task_id = request.args(0)
    return dict(task=actions.task_status(task_id))

def task_monitor():
    page = int(request.vars.page or 0)
    tasks = db(pc.taskmeta).select(
        orderby=~pc.taskmeta.date_done,
        limitby=(100*page, 100*(page+1)))    
    return dict(tasks=tasks,page=page)

def view_taskstate():
    task_id = request.args(0)
    return dict(task=pc.taskstate(task_id=task_id))

def taskstate_monitor():
    page = int(request.vars.page or 0)
    tasks = db(pc.taskstate).select(
        orderby=~pc.taskstate.tstamp,
        limitby=(100*page, 100*(page+1)))
    return dict(tasks=tasks,page=page)

def periodic_task_monitor():
    pass

def workers_monitor():
    #return dict(workers=actions.list_workers())
    workers = db(pc.workerstate).select(
        orderby=~pc.workerstate.last_heartbeat)
    return dict(workers=workers)

def inspect_worker():
    return dict(info=actions.inspect_workers([request.args(0)]))

def shutdown_worker():
    return str(actions.shutdown_workers([request.args(0)]))
