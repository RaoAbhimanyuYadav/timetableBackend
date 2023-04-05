# from django.forms.models import model_to_dict
# import json

import uuid
from rest_framework.response import Response
from django.db.utils import IntegrityError
from timetable.models import Time_Off
from django.core.exceptions import ValidationError


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


def create_handler(request, ModelSerializer, IntegrityErrMsg, **kwargs):
    try:
        serializer = ModelSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(owner=request.user, **kwargs)
            return Response(
                status=200,
                data={
                    "message": "Entry Created Successfully",
                    "data": ModelSerializer(instance, many=False).data
                })
        else:
            return Response(status=400, data={"message": serializer.errors})
    except Time_Off.DoesNotExist as err:
        return Response(
            status=406,
            data={
                "message": err.args[0],
                "data": ModelSerializer(err.args[1], many=False).data
            }
        )
    except IntegrityError as err:
        return Response(
            status=400,
            data={
                "message": err.args[0]
            })
    except Exception as err:
        return Response(
            status=400,
            data={
                "message": err.args[0]
            }
        )


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
    return Response(status=200, data={"message": f"{name} deleted successfully."})


def update_handler(request, query, ModelSerializer, Model, **kwargs):
    if 'id' not in request.data:
        return Response(status=400, data={"message": "Please send Id"})
    id = request.data['id']
    if not is_valid_uuid(id):
        return Response(status=400, data={"message": "Not a valid UUID"})
    try:
        instance = query.get(id=id)
        serializer = ModelSerializer(instance, data=request.data)
        if serializer.is_valid():
            try:
                instance = serializer.save(owner=request.user, **kwargs)
                return Response(
                    status=200,
                    data={
                        "message": "Entry Updated Successfully",
                        "data": ModelSerializer(instance, many=False).data
                    })
            except IntegrityError as err:
                return Response(
                    status=400,
                    data={
                        "message": err.args[0]
                    })
        else:
            return Response(status=400, data={"message": serializer.errors})
    except Model.DoesNotExist as err:
        return Response(status=400, data={"message": err.args[0]})
    except Time_Off.DoesNotExist as err:
        return Response(
            status=406,
            data={
                "message": err.args[0],
                "data": ModelSerializer(err.args[1], many=False).data
            }
        )
    except Exception as err:
        return Response(
            status=400,
            data={
                "message": err.args[0]
            }
        )


def add_time_off_handler(instance, validated_data, ):
    instance.time_off.clear()
    for data in validated_data.get('time_off', []):
        try:
            t_inst = Time_Off.objects.get(
                bell_timing=data.get('bell_timing', {}).get('id', ""),
                working_day=data.get('working_day', {}).get('id', "")
            )
            instance.time_off.add(t_inst)
            instance.save()
        except Time_Off.DoesNotExist:
            raise Time_Off.DoesNotExist(
                "Please enter correct time off", instance)
        except ValidationError:
            raise Time_Off.DoesNotExist(
                "Please enter correct time off", instance)
