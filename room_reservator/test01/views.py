from datetime import datetime

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Roomreservation, Meetingroom
from .serializer import TestDataSerializer, TestDataSerializer2

'''
def index(request):
    return render(request,"index.html")


def index(request):
    meetingroom = Meetingroom.objects.all()

    context = {
        'meetingroom' : meetingroom
    }
    return render(request,"index.html", context=context)
'''

#@api_view(['GET'])
def index(request): #찾고자 하는 회의실ID 가져옴
    avaliableroom=[]
    count=0
    queryset = Meetingroom.objects.filter(meetingroomcapacity__gt = 5,isbeamprojector=1).values() #.values_list('meetingroomid', flat=True)

    for i in range(len(queryset)):
        context_i={}
        data = Roomreservation.objects.filter(reserveroom=queryset[i]['meetingroomid'],reservedate='2022-11-19').select_related('reserveroom').order_by('reservestarttime')
        #i번 방에 대한 예약이 특정일에 없는 경우
        if not data:
            context_i['meetingroomid'] = queryset[i]['meetingroomid']
            context_i['meetingroomname'] = queryset[i]['meetingroomname']
            context_i['meetingroomcapacity'] = queryset[i]['meetingroomcapacity']
            context_i['reservestarttime'] = '00:00:00'
            context_i['reserveendtime'] = '24:00:00'
            avaliableroom.append(context_i)
            count = count + 1
            #프론트에 전달
        else: #다 같은 방
            for j in range(len(data)):  # 현재 예약되어 있는 회의실
                context_j={}
                if(j==0 and data[j].reservestarttime is not '00:00:00'):
                    context_fisrt = {}
                    context_second = {}

                    context_fisrt['meetingroomid'] = data[j].reserveroom.meetingroomid
                    context_fisrt['meetingroomname'] = data[j].reserveroom.meetingroomname
                    context_fisrt['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                    context_fisrt['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                    context_fisrt['reservestarttime'] =  '00:00:00'
                    context_fisrt['reserveendtime'] =  data[j].reservestarttime.strftime("%H:%M:%S")
                    avaliableroom.append(context_fisrt)
                    count = count + 1

                    context_second['meetingroomid'] = data[j].reserveroom.meetingroomid
                    context_second['meetingroomname'] = data[j].reserveroom.meetingroomname
                    context_second['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                    context_second['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                    context_second['reservestarttime'] =  data[j].reserveendtime.strftime("%H:%M:%S")
                    context_second['reserveendtime'] =  data[j+1].reservestarttime.strftime("%H:%M:%S")
                    avaliableroom.append(context_second)
                    count = count + 1

                elif(j==len(data)-1 and data[j].reserveendtime is not '24:00:00'):
                    context_j['meetingroomid'] = data[j].reserveroom.meetingroomid
                    context_j['meetingroomname'] = data[j].reserveroom.meetingroomname
                    context_j['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                    context_j['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                    context_j['reservestarttime'] = data[j].reserveendtime.strftime("%H:%M:%S")
                    context_j['reserveendtime'] = '24:00:00'
                    avaliableroom.append(context_j)
                    count = count + 1
                else:
                    context_j['meetingroomid'] = data[j].reserveroom.meetingroomid
                    context_j['meetingroomname'] = data[j].reserveroom.meetingroomname
                    context_j['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                    context_j['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                    context_j['reservestarttime'] = data[j].reserveendtime.strftime("%H:%M:%S")
                    context_j['reserveendtime'] = data[j + 1].reservestarttime.strftime("%H:%M:%S")
                    avaliableroom.append(context_j)
                    count = count + 1
                print()

    #serializer = TestDataSerializer(context, many=True)
        #return Response(serializer.data)
    print(avaliableroom)

    context = {
        'avaliableroom' : avaliableroom
    }

    return render(request, "index.html", context=context)


@api_view(['POST'])
def postMember(request):
    reqData = request.data
    serializer = TestDataSerializer(data=reqData)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
