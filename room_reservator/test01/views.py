from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Roomreservation, Meetingroom, Employee


@api_view(['GET','POST'])
def index(request):

    avaliableroom=[]

    if(request.method == 'GET' and bool(request.GET)): #프론트에서 전달하는 값이 있을때만 DB 에서 추출 #bool(request.GET)
        isbeam = 0
        if (request.GET.get("vim_check") == "on"):
            isbeam = 1
        queryset = Meetingroom.objects.filter(meetingroomcapacity__gt=request.GET['count'],
                                              isbeamprojector=isbeam).values()  # .values_list('meetingroomid', flat=True)
        for i in range(len(queryset)):
            context_i = {}
            data = Roomreservation.objects.filter(reserveroom=queryset[i]['meetingroomid'],
                                                  reservedate=request.GET['date']).select_related('reserveroom').order_by('reservestarttime')
            # 선택한 날짜에 방(id = i)에 대한 예약이 1개도 없는 경우
            if not data:
                context_i['meetingroomid'] = queryset[i]['meetingroomid']
                context_i['meetingroomname'] = queryset[i]['meetingroomname']
                context_i['meetingroomloc'] = queryset[i]['meetingroomloc']
                context_i['meetingroomcapacity'] = queryset[i]['meetingroomcapacity']
                context_i['isbeamprojector'] = queryset[i]['isbeamprojector']
                context_i['reservestarttime'] = '00:00:00'
                context_i['reserveendtime'] = '24:00:00'
                avaliableroom.append(context_i)
                continue
            else:
                for j in range(len(data)):  # 현재 예약되어 있는 회의실
                    context_fisrt = {}
                    context_second = {}

                    context_fisrt['meetingroomid'] = data[j].reserveroom.meetingroomid
                    context_fisrt['meetingroomname'] = data[j].reserveroom.meetingroomname
                    context_fisrt['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                    context_fisrt['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                    context_fisrt['isbeamprojector'] = data[j].reserveroom.isbeamprojector

                    if(len(data) == 1) : #선택한 날짜에 예약이 1개
                        context_fisrt['reservestarttime'] = '00:00:00'
                        context_fisrt['reserveendtime'] = data[j].reservestarttime.strftime("%H:%M:%S")
                        avaliableroom.append(context_fisrt)

                        context_second['meetingroomid'] = data[j].reserveroom.meetingroomid
                        context_second['meetingroomname'] = data[j].reserveroom.meetingroomname
                        context_second['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                        context_second['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                        context_second['isbeamprojector'] = data[j].reserveroom.isbeamprojector
                        context_second['reservestarttime'] = data[j].reserveendtime.strftime("%H:%M:%S")
                        context_second['reserveendtime'] = '24:00:00'
                        avaliableroom.append(context_second)
                        continue

                    if (j == 0 and data[j].reservestarttime != '00:00:00'):

                        context_fisrt['reservestarttime'] = '00:00:00'
                        context_fisrt['reserveendtime'] = data[j].reservestarttime.strftime("%H:%M:%S")
                        avaliableroom.append(context_fisrt)

                        context_second['meetingroomid'] = data[j].reserveroom.meetingroomid
                        context_second['meetingroomname'] = data[j].reserveroom.meetingroomname
                        context_second['meetingroomloc'] = data[j].reserveroom.meetingroomloc
                        context_second['meetingroomcapacity'] = data[j].reserveroom.meetingroomcapacity
                        context_second['reservestarttime'] = data[j].reserveendtime.strftime("%H:%M:%S")
                        context_second['reserveendtime'] = data[j + 1].reservestarttime.strftime("%H:%M:%S")
                        avaliableroom.append(context_second)

                    elif (j == len(data) - 1 and data[j].reserveendtime != '24:00:00'):
                        context_fisrt['reservestarttime'] = data[j].reserveendtime.strftime("%H:%M:%S")
                        context_fisrt['reserveendtime'] = '24:00:00'
                        avaliableroom.append(context_fisrt)

                    else:
                        context_fisrt['reservestarttime'] = data[j].reserveendtime.strftime("%H:%M:%S")
                        context_fisrt['reserveendtime'] = data[j + 1].reservestarttime.strftime("%H:%M:%S")
                        avaliableroom.append(context_fisrt)


        queryset = Employee.objects.filter(employeeid=request.GET['reserverid']).values('name')

        context = {
            'avaliableroom': avaliableroom,
            'reserver_name' : queryset[0]['name'],
            'reserve_date' :  request.GET['date']
        }
        return render(request, "index.html", context=context)

    elif(request.method == 'POST' and bool(request.POST)):   # DB에 예약 정보 저장

        # object instance 추출 필요
        meetingroom_data = Meetingroom.objects.filter(meetingroomname=request.POST['reserveroom'])
        user_data = Employee.objects.filter(name=request.POST['name'])

        reservation_data = Roomreservation()
        reservation_data.reserveroom = meetingroom_data[0]
        reservation_data.reserver = user_data[0]
        reservation_data.reservedate = request.POST['date']
        reservation_data.reservestarttime = request.POST['reservestarttime']
        reservation_data.reserveendtime = request.POST['reserveendtime']
        reservation_data.save()
        return render(request, "index.html")

    else:  # 단순 새로고침
        return render(request, "index.html")
