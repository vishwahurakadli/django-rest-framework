from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Person
from .serializer import PeopleSerializer, LoginSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.core.paginator import Paginator
# Create your views here.


@api_view(['GET', 'POST', 'PUT'])
def index(request):
    if request.method == 'GET':
        name = request.GET.get('name')
        print(name)
        framework = {
            'name': 'Django REST Framework',
            'version': '3.12.4',
            'Status': 'Working',
        }
        print(framework)
        return Response(framework)
    elif request.method == 'POST':
        print(request.data)
        return Response({'msg': 'POST worked'})
    elif request.method == 'PUT':
        print(request.data)
        return Response({'msg': 'PUT worked'})


class PersonAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get(self, request):
        print(request.user)
        objs = Person.objects.filter()
        page = request.GET.get('page',1)
        pag_size = 3
        paginator = Paginator(objs, pag_size)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)
    
    def put(self, request):
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)


    def patch(self, request):
        data = request.data
        obj = Person.objects.get(id=data['id'])

        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    def delete(self,request):
        data = request.data
        obj = Person.objects.get(id=data["id"])
        obj.delete

        return Response({"message": 'Person record Deleted'})


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def person(request):
    if request.method == 'GET':
        objs = Person.objects.filter(color__isnull=False)
        serializer = PeopleSerializer(objs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PUT':
        data = request.data
        serializer = PeopleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    elif request.method == 'PATCH':
        data = request.data
        obj = Person.objects.get(id=data['id'])

        serializer = PeopleSerializer(obj, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

    else:
        data = request.data
        obj = Person.objects.get(id=data["id"])
        obj.delete

        return Response({"message": 'Person record Deleted'})


@api_view(['POST'])
def login(request):
    data = request.data
    serializer = LoginSerializer(data=data)
    print(data)
    if serializer.is_valid():
        data = serializer.data
        return Response({'message': 'Login Success'})

    return Response(serializer.errors)


class PeopleViewSet(viewsets.ModelViewSet):
    serializer_class = PeopleSerializer
    queryset = Person.objects.all()

    def list(self,request):
        search = request.GET.get('search')
        queryset = self.queryset

        if search:
            queryset = queryset.filter(name__startswith=search)

        serializer = PeopleSerializer(queryset, many=True)
        return Response({'Status':200, 'data':serializer.data})
    

class RegisterAPI(APIView):

    def post(self,request):
        data = request.data

        serializer = RegisterSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'status':True, 'message':'user created'}, status.HTTP_201_CREATED)


class LoginAPI(APIView):

    def post(self,request):
        data = request.data
        serializer = LoginSerializer(data = data)
        if not serializer.is_valid():
            return Response({
                'status': False,
                'message': serializer.errors
            }, status.HTTP_400_BAD_REQUEST)
        
        print(serializer.data)
        user = authenticate(username = serializer.data['username'], password=serializer.data['password'])
        if not user:
            return Response({
                'status': False,
                'message': 'invalid credentials'
            }, status.HTTP_400_BAD_REQUEST)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'status':True,
            'message': 'Login Succesful',
            'token':str(token)},
            status.HTTP_201_CREATED)