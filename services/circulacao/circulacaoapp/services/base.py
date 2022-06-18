import json
from celery import group
from django.utils import timezone
from circuitbreaker import circuit
from django_celery_beat.models import PeriodicTask, ClockedSchedule

from circulacao.celery import app

def datetime_name(name):
    dt = timezone.localtime()
    dt_str = dt.strftime('%Y%m%d.%H%M%S.%f')

    return f'{dt_str}-{name}'

def handle_datetime(dt=None, delay_seconds=60):
    if not dt:
        dt = timezone.localtime()

    if delay_seconds > 0:
        dt += timezone.timedelta(seconds=delay_seconds)

    if not dt.tzinfo:
        dt = timezone.make_aware(dt)

    return dt

def handle_kwargs(kw):
    name = kw.get('name')
    args = kw.get('args', [])
    kwargs = kw.get('kwargs', {})
    headers = kw.get('headers', {})

    if name:
        headers['periodic_task_name'] = name

    kw.update({
        'args': json.dumps(args),
        'kwargs': json.dumps(kwargs),
        'headers': json.dumps(headers),
        'one_off': True,
    })

    return kw

@circuit(failure_threshold = 1, recovery_timeout = 30)
def send_task(task_name, **kw):
    app.send_task(task_name, ignore_result=True, **kw)

@circuit(failure_threshold = 1, recovery_timeout = 30)
def send_task_group(task_name, contexts):
    func = lambda context: app.signature(task_name, ignore_result=True, **context)
    group(list(map(func, contexts)))()

def save_clocked_task(dt=None, delay_seconds=60, **kw):
    '''
    name    -> nome único da task
    task    -> nome da task
    args    -> lista de argumentos
    kwargs  -> dicionário de argumentos
    queue   -> nome da fila
    '''
    dt = handle_datetime(dt, delay_seconds)
    kw = handle_kwargs(kw)

    clock = ClockedSchedule.objects.create(clocked_time=dt)

    PeriodicTask.objects.create(clocked=clock, **kw)

def save_batch_clocked_tasks(dt=None, delay_seconds=60, contexts=[]):
    '''
    name    -> nome único da task
    task    -> nome da task
    args    -> lista de argumentos
    kwargs  -> dicionário de argumentos
    queue   -> nome da fila
    '''
    if not contexts:
        return

    dt = handle_datetime(dt, delay_seconds)

    clock = ClockedSchedule.objects.create(clocked_time=dt)

    PeriodicTask.objects.bulk_create([
        PeriodicTask(
            clocked=clock, 
            **handle_kwargs(context)
        ) for context in contexts
    ])

def try_to_send(task_name, **kwargs):
    '''
    args    -> lista de argumentos
    queue   -> nome da fila
    '''

    try:
        send_task(task_name, **kwargs)

    except:
        kwargs.update({
            'name': datetime_name(task_name),
            'task': task_name,
        })
        
        save_clocked_task(**kwargs)

def try_to_send_group(task_name, contexts, func):
    '''
    func        -> lambda function
    contexts    -> lista
    '''

    contexts = list(map(func, contexts))

    try:
        send_task_group(task_name, contexts)

    except:
        for context in contexts:
            context.update({
                'name': datetime_name(task_name),
                'task': task_name,
            })

        save_batch_clocked_tasks(contexts=contexts)
