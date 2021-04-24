from django.shortcuts import render
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib.auth.models import User
import random
import string
import json
from accounts.models import AccountPath as AP
from .serializers import UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser



# Create your models here.

def CreateUserID(request):
    xcheck = False
    user_id = ran_gen(6,'ABCDEFGHIJKLMPQRSTUVWXYZ123456789')
    while xcheck:
        check_id = AP.objects.filter(username=user_id)
        if check_id.exists():
            user_id = ran_gen(6,'ABCDEFGHIJKLMPQRSTUVWXYZ123456789')
            xcheck = False
        else:
            xcheck = True
    status = {
        'status': 200,
        'user_id':'CB-'+user_id,
    }
    return JsonResponse(status, safe=False)


class UserRecordView(APIView):
    """
    API View to create or get a list of all the registered
    users. GET request returns the registered users whereas
    a POST request allows to create a new user.
    """
    permission_classes = [IsAdminUser]
    # http_method_names = ['get', 'head', 'post']

    def get(self, format=None):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=ValueError):
            serializer.create(validated_data=request.data)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            {
                "error": True,
                "error_msg": serializer.error_messages,
            },
            status=status.HTTP_400_BAD_REQUEST
        )




    


#================= FUCTIONS =================#
def ran_gen(size, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for x in range(size))