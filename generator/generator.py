from django.core.files.base import ContentFile
from datetime import datetime, timedelta
from io import StringIO
import csv
import random
import string
import time

from .util import PROCESSING_STATUS, READY_STATUS
from .models import DataSet, SchemaTemplate

INTEGER = 'Integer'
EMAIL = 'Email'
DATE = 'Date'
TEXT = 'Text'
FULL_NAME = 'Full Name'


def generate_csvfile(schema_id, length):
    schema = SchemaTemplate.objects.get(id=schema_id)
    dataset = DataSet(schema=schema, status=PROCESSING_STATUS)
    dataset.save()
    columns = schema.columns.prefetch_related('column_type')
    # sort by order
    columns = sorted(columns, key=lambda x: x.order)
    headers = []
    types = []

    for column in columns:
        headers.append(column.name)
        types.append((column.column_type.name,
                      column.range_from, column.range_to))

    rows = (tuple(randval(*t) for t in types) for i in range(length))

    file = _generate_csvfile(headers, rows)
    name = generate_filename()

    dataset.status = READY_STATUS
    dataset.link.save(name, file)


def generate_filename(length=8):
    filename = 'file' + \
        str(time.time()) + randstr(length) + '.csv'

    return filename


def _generate_csvfile(headers, rows):
    buffer = StringIO()
    writer = csv.writer(buffer, delimiter=',')
    # write headers
    writer.writerow(headers)
    for row in rows:
        writer.writerow(row)

    fakefile = ContentFile(buffer.getvalue().encode('utf-8'))
    buffer.close()

    return fakefile


def randval(type, range_from, range_to):
    if type == INTEGER:
        value = randnum(range_from, range_to)
    elif type == EMAIL:
        value = randemail()
    elif type == DATE:
        value = randdate()
    elif type == TEXT:
        value = randstr(random.randint(range_from, range_to))
    elif type == FULL_NAME:
        value = randname() + ' ' + randname()
    else:
        value = randstr(8)

    return value


def randname():
    return randstr(random.randint(3, 5)).capitalize()


def randdate():
    days_to_add = random.randint(1, 365 * 40)
    date_from = datetime(1970, 1, 1)

    return str(date_from + timedelta(days=days_to_add))


def randemail():
    domain = randstr(random.randint(2, 4)) + '.' + \
        randstr(random.randint(2, 3))
    username = randstr(6)

    return f"{username}@{domain}"


def randnum(range_from, range_to):
    return random.randint(range_from, range_to)


def randstr(length):
    letters = string.ascii_lowercase
    result = ''.join(random.choice(letters) for i in range(length))

    return result
