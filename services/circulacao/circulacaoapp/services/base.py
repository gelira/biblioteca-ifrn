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
        dt = timezone.localtime() + timezone.timedelta(seconds=delay_seconds)

    if not dt.tzinfo:
        dt = timezone.make_aware(dt)

    return dt

def handle_kwargs(kw):
    args = kw.get('args', [])
    kwargs = kw.get('kwargs', {})
    headers = kw.get('headers', {})

    kw.update({
        'args': json.dumps(args),
        'kwargs': json.dumps(kwargs),
        'headers': json.dumps(headers),
    })

    return kw

@circuit(failure_threshold = 1)
def send_task(task_name, **kw):
    app.send_task(task_name, **kw)

@circuit(failure_threshold = 1)
def send_task_group(task_name, contexts):
    func = lambda context: app.signature(task_name, **context)
    group(list(map(func, contexts)))()

def save_clocked_task(dt=None, delay_seconds=60, **kw):
    '''
    name    -> nome único da task
    task    -> nome da task
    headers -> { 'periodic_task_name': ... }
    args    -> lista de argumentos
    kwargs  -> dicionário de argumentos
    queue   -> nome da fila
    one_off -> boolean
    '''
    dt = handle_datetime(dt, delay_seconds)
    kw = handle_kwargs(kw)

    clock = ClockedSchedule.objects.create(clocked_time=dt)

    PeriodicTask.objects.create(clocked=clock, **kw)

def save_batch_clocked_tasks(dt=None, delay_seconds=60, contexts=[]):
    '''
    name    -> nome único da task
    task    -> nome da task
    headers -> { 'periodic_task_name': ... }
    args    -> lista de argumentos
    kwargs  -> dicionário de argumentos
    queue   -> nome da fila
    one_off -> boolean
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
