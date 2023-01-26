from .serializers import Bell_Timing, Working_Day
# from django.forms.models import model_to_dict
# import json

import uuid


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def get_handler(instance, serializer, name):
    return {
        "message": f"{name} fetched successfully",
        "data": serializer(instance.all(), many=True).data
    }


def set_handler(model, user, data, list, serializer, name):
    kwargs = {}
    for key in list:
        kwargs[key] = data[key]
    instance = model.objects.create(owner=user, **kwargs)
    # dict_obj = model_to_dict(instance)
    # print(json.dumps(dict_obj))
    return {
        "message": f"{name} added successfully.",
        "data": serializer(instance, many=False).data
    }


def set_handler_with_time_off(model, user, data, list, ):
    kwargs = {}
    for key in list:
        kwargs[key] = data[key]
    instance = model.objects.create(owner=user, **kwargs)
    return instance


def delete_handler(query, request, name):
    if 'id' not in request.data:
        return {"message": "Please send Id", "success": False}
    id = request.data['id']
    if not is_valid_uuid(id):
        return {"message": "Not a valid UUID", "success": False}
    instance = query.filter(id=id)
    if not instance.exists():
        return {"message": "Invalid ID", "success": False}
    instance.delete()
    return {"message": f"{name} deleted successfully.", "success": True}


def set_time_off_handler(data, instance, user, key,  time_off_model):
    kwargs = {}
    kwargs['bell_timing'] = Bell_Timing.objects.get(
        id=data['bell_timing']['id'])
    kwargs['working_day'] = Working_Day.objects.get(
        id=data['working_day']['id'])
    kwargs[key] = instance
    return time_off_model.objects.create(owner=user, **kwargs)
