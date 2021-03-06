from django.shortcuts import render
from django.http import JsonResponse, HttpResponse  # This is handler methods
from app.models import Employee
from app.serializers import EmployeeSerializer, UserSerializer
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework import status

# Create your views here.


@csrf_exempt
def employeeView(request):
    if(request.method == 'GET'):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif(request.method == 'POST'):
        serializer = EmployeeSerializer(data=JSONParser().parse(request))
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)


@csrf_exempt
def employeeDetailView(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return

    if(request.method == "DELETE"):
        employee.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    elif(request.method == "GET"):
        serializer = EmployeeSerializer(employee)
        return JsonResponse(serializer.data, safe=False)

    elif(request.method == "PUT"):
        serializer = EmployeeSerializer(
            employee, data=JSONParser().parse(request))
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)


def UserlistView(request):
    users = User.objects.all()
    print(User.objects.get())
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)
