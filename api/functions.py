from .serializers import Bell_Timing, Working_Day


def get_handler(instance, serializer):
    return serializer(instance.all(), many=True).data


def set_handler(model, user, data, list):
    kwargs = {}
    for key in list:
        kwargs[key] = data[key]
    return model.objects.create(owner=user, **kwargs)


def set_time_off_handler(data, id, user, key, model, time_off_model):
    kwargs = {}
    kwargs['bell_timing'] = Bell_Timing.objects.get(
        id=data['bell_timing']['id'])
    kwargs['working_day'] = Working_Day.objects.get(
        id=data['working_day']['id'])
    kwargs[key] = model.objects.get(id=id)
    return time_off_model.objects.create(owner=user, **kwargs)
