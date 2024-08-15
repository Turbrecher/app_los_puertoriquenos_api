from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from puntuaciones.serializers import  UserSerializer
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from datetime import datetime


#LOGIN
@api_view(['POST'])
def login(request):
    
    try:
        user = get_object_or_404(User, username = request.data['username'].upper())
        
        if not user.check_password(request.data['password']):
            return JsonResponse({"error":"Contraseña no válida", "status":400}, status=400)
        
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(instance=user)
        
        #Guardamos la ultima fecha en la que el usuario se conecto a la app.
        user.last_login = datetime.now()
        user.save()
            
        return JsonResponse({"message":"Te has autenticado correctamente","token": token.key ,"user":serializer.data, "status":200}, status=200)
    except KeyError:
        return JsonResponse({"error":"Debes ingresar un usuario y una contraseña", "status":400}, status=400)


#REGISTER
@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.username = user.username.upper()
        user.save()
        
        token = Token.objects.create(user=user)
        return JsonResponse({"user":serializer.data,"token":token.key,"data":None, "status":200}, status=200)
    
    return JsonResponse({"message":"Ha ocurrido un error", "status":400, "errors":serializer.errors})



#PERFIL
@api_view(['POST'])
def profile(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError
        
        serializer = UserSerializer(instance=request.user)
        
        return JsonResponse( {"message":"Este es tu perfil","data":serializer.data}, status=200)
    
    except PermissionError:
        return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
    

#EDIT PERFIL
@api_view(['POST'])
def edit_profile(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError
        
        print(request.data)
        
        usuario = User.objects.get(id=request.user.id)
        serializer = UserSerializer(data=request.data, instance = usuario)     
            
        
        if serializer.is_valid():
            usuario.username = request.data['username'].upper()
            usuario.email = request.data['email'].upper()
            
            #Si no se cambia la contraseña.
            if request.data['password'] == request.user.password:
                usuario.password = usuario.password
            else:#En caso de establecer una nueva contraseña.
                usuario.set_password(request.data['password'])
            
            usuario.save()
            
            return JsonResponse({"message":"¡Tu perfil ha sido editado con éxito!"}, status = 200)
        
        return JsonResponse( {"message":"Ha ocurrido un error", "errors":serializer.errors}, status = 400)
    
    except PermissionError:
        return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
 
#BORRAR USUARIO   
@api_view(['DELETE'])
def delete_user(request):
    try:
        if not request.user.is_authenticated:
            raise PermissionError
        
        usuario = User.objects.get(id=request.user.id)
        usuario.delete()
               
        return JsonResponse({"message":"¡Tu usuario ha sido ELIMINADO con éxito!"}, status = 200)
    
    except PermissionError:
        return JsonResponse({"message":"Debes identificarte para acceder a este recurso", "status":401}, status=401)
    
    
#OBTENER NOMBRE DE USUARIO A PARTIR DE ID
@api_view(['GET'])
def get_user_name(request, id):
    try:
        
        usuario = User.objects.get(id=id)
                  
        return JsonResponse({"usuario":usuario.username}, status = 200)
    
    except User.DoesNotExist:
        return JsonResponse({"message":"El usuario que buscas no existe"}, status=404)
    
    except:
        return JsonResponse({"message":"No hemos podido encontrar tu usuario"}, status=500)
    
    