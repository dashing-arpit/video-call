from django.shortcuts import render
from agora_token_builder import RtcTokenBuilder
from django.http import JsonResponse
import random 
import time
import json
from .models import RoomMember
from  django.views.decorators.csrf import csrf_exempt
# Create your views here.
def getToken(request):
    appId = 'f5f7515742cd40d2b31fd6d219a40b3a'
    appCertificate = '8221b98271894131a02bdb27e6e891cd'
    channelName = request.GET.get('channel')
    uid = random.randint(1,230)
    expirationTimeInSeconds = 3600*24
    currentTimeStamp = time.time()
    privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds
    role = 1
    token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
    return JsonResponse({'token':token,'uid':uid},safe=False)
def lobby(request):
    return render(request,'base/lobby.html')
def room(request):
    return render(request,'base/room.html')\
        
@csrf_exempt
def createMember(request):
    data = json.loads(request.body)
    member, created = RoomMember.objects.get_or_create(
        name = data['name'],
        uid  = data['UID'],
        room_name = data['room_name']
    )
    return JsonResponse({'name': data['name']},safe=False)

def getMember(request):
    uid = request.GET.get('UID')
    room_name = request.GET.get('room_name')
    
    member = RoomMember.objects.get(
        uid = uid,
        room_name =  room_name,
    )
    name =  member.name
    return JsonResponse({'name':member.name},safe=False)