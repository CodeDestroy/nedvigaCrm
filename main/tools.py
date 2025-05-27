from django.db import models


def object_to_dict(obj):
    opts = obj._meta
    data = {}
    for f in opts.concrete_fields + opts.many_to_many:
        if isinstance(f, models.ManyToManyField):
            if obj.pk is None:
                data[f.name] = []
            else:
                data[f.name] = list(f.value_from_object(obj).values_list('pk', flat=True))
        elif isinstance(f, models.DateTimeField) and f.value_from_object(obj) is not None:
            data[f.name] = f.value_from_object(obj).strftime('%Y-%m-%d %H:%M')
        elif isinstance(f, models.DateField) and f.value_from_object(obj) is not None:
            data[f.name] = f.value_from_object(obj).strftime('%Y-%m-%d')
        elif isinstance(f, models.TimeField) and f.value_from_object(obj) is not None:
            data[f.name] = f.value_from_object(obj).strftime('%H:%M')
        elif isinstance(f, models.FileField):
            data[f.name] = ''
        else:
            data[f.name] = f.value_from_object(obj)
    return data
