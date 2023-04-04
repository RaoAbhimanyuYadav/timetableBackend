from .serializers import Bell_Timing, Working_Day
# from django.forms.models import model_to_dict
# import json

import uuid
from rest_framework.response import Response
from django.db.utils import IntegrityError


def is_valid_uuid(val):
    try:
        uuid.UUID(str(val))
        return True
    except ValueError:
        return False


def get_handler(instance, serializer, name):
    return Response(
        status=200,
        data={
            "message": f"{name} fetched successfully",
            "data": serializer(instance.all(), many=True).data
        })


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


def create_handler(request, ModelSerializer, IntegrityErrMsg, **kwargs):
    # try:
    serializer = ModelSerializer(data=request.data)
    if serializer.is_valid():
        try:
            instance = serializer.save(owner=request.user, **kwargs)
            return Response(
                status=200,
                data={
                    "data": ModelSerializer(instance, many=False).data
                })
        except IntegrityError:
            return Response(
                status=400,
                data={
                    "message": IntegrityErrMsg
                })
    else:
        return Response(status=400, data={"message": serializer.errors})
    # except:
    #     return Response(status=500, data={"message": "Unexpected happen"})


def delete_handler(query, request, name):
    if 'id' not in request.data:
        return Response(status=400, data={"message": "Please send Id"})
    id = request.data['id']
    if not is_valid_uuid(id):
        return Response(status=400, data={"message": "Not a valid UUID"})
    instance = query.filter(id=id)
    if not instance.exists():
        return Response(status=400, data={"message": "Invalid ID"})
    instance.delete()
    return Response(status=400, data={"message": f"{name} deleted successfully."})


def update_handler(request, query, ModelSerializer, Model, **kwargs):
    # try:
    if 'id' not in request.data:
        return Response(status=400, data={"message": "Please send Id"})
    id = request.data['id']
    if not is_valid_uuid(id):
        return Response(status=400, data={"message": "Not a valid UUID"})
    try:
        instance = query.get(id=id)
        serializer = ModelSerializer(instance, data=request.data)
        if serializer.is_valid():
            instance = serializer.save(**kwargs)
            return Response(
                status=200,
                data={
                    "data": ModelSerializer(instance, many=False).data
                })
        else:
            return Response(status=400, data={"message": serializer.errors})
    except Model.DoesNotExist:
        return Response(status=400, data={"message": "Invalid ID"})
    # except:
    #     return Response(status=500, data={"message": "Unexpected happen"})


def set_time_off_handler(data, instance, user, key,  time_off_model):
    kwargs = {}
    kwargs['bell_timing'] = Bell_Timing.objects.get(
        id=data['bell_timing']['id'])
    kwargs['working_day'] = Working_Day.objects.get(
        id=data['working_day']['id'])
    kwargs[key] = instance
    return time_off_model.objects.create(owner=user, **kwargs)
