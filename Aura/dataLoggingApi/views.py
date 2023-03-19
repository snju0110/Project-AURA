from django.shortcuts import render, redirect
from django.http import JsonResponse
from dataLoggingApi.models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, date
from datetime import timedelta
from django.contrib.auth.models import User, auth
from django.contrib import messages


@api_view(['GET', 'POST'])
def demDataloggingGet(requests):
    if requests.method == 'GET':
        data = demDatatable.objects.all()
        print(data)
        serializer = demDataLoggingSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)

    if requests.method == 'POST':
        serializer = demDataLoggingSerializer(data=requests.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
def DemDailyData(requests):
    if requests.method == 'GET':
        queryset = demDailyData.objects.all()
        # queryset = demDailyData.objects.filter(primaryCat = 'Travel')
        serializer = demDailyDataSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if requests.method == 'POST':
        serializer = demDailyDataSerializer(data=requests.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if requests.method == 'PUT':
        serializer = demDailyDataSerializer(data=requests.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET', 'POST', 'PUT'])
def getdata(requests):
    if requests.method == 'GET':
        queryset = demDailyData.objects.filter(user='Sanjay').order_by('-date')[:1]
        serializer = demDailyDataSerializer(queryset, many=True)
        return JsonResponse(serializer.data, safe=False)

    if requests.method == 'POST':
        serializer = demDailyDataSerializer(data=requests.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if requests.method == 'PUT':
        serializer = demDailyDataSerializer(data=requests.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def index(request):
    # create a dictionary
    queryset = demDailyData.objects.all()
    set = demDailyData.objects.filter(user='Sanjay')
    results = request.GET.get("results")
    context = {
        'queryset': queryset,
        'set': set
    }
    # return response
    return render(request, "index1.html", context)


def date1(request):
    # queryset = demDailyData.objects.filter(date='2023-02-26')

    date = request.GET["dateF"]
    # print("----------------------------------------------------------------------------||" , request.GET["dateF"])
    set = demDailyData.objects.filter(date__range=["2023-02-20", date], user='Sanjay').values('primaryCat').annotate(
        total_amount=Sum('amount'))
    queryset = demDailyData.objects.all()
    print("-------------------------------------------------------------", set)
    queryset = demDailyData.objects.filter(date=date)
    # print(demDailyData.objects.last().date)
    results = request.GET.get("results")
    context = {
        'queryset': queryset,
        'set': set
    }

    # return response
    return render(request, "index1.html", context)


def Login(request):
    if request.method == 'POST':
        name = request.POST['uname']
        password = request.POST['psw']
        # validation

        user = auth.authenticate(username=name, password=password)
        print("USER", user)
        if user is not None:
            print("Right login")
            auth.login(request, user)
            return redirect('main')
        else:
            messages.info(request, "Check User name or password")
            return render(request, "Login.html")


    else:
        print("sdkhbdsgibdgubg not logged in ")

    return render(request, "Login.html")


def Logout(request):
    auth.logout(request)
    print("logged out")
    return redirect("/")


def NLogin(request):
    print("Nlogin")
    if request.method == 'POST':
        name = request.POST['UserName']
        password = request.POST['password']
        user = auth.authenticate(username=name, password=password)
        print("USER", user)
        if user is not None:
            print("Right login")
            auth.login(request, user)
            return redirect('main')
        else:
            messages.info(request, "Check User name or password")
            return render(request, "LoginNew.html")


    else:
        print("sdkhbdsgibdgubg not logged in ")

    return render(request, "LoginNew.html")


def Jarvis_Headsup(request):
    return render(request, "jarvis_UI.html")


def DemMainPage(request):
    # print("------------------" , user.username)
    try:
        current_user = request.user
        print(current_user.id)
        MonthStartDate = request.GET["fdate"]

        today = request.GET["tdate"]

        print("--- mss", today, MonthStartDate)
        yesterday = today - timedelta(days=1)
        print("---- input got from front end")
    except:
        today = date.today()
        startdate = str(date.today()).split('-')
        MonthStartDate = str(startdate[0]) + '-' + str(startdate[1]) + '-01'
        yesterday = today - timedelta(days=1)
        print(yesterday, today)
        print("excpet")
    current_user = request.user
    user = current_user.username

    monthlydata = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user).values('type').annotate(total_amount=Sum('amount'))

    datewisespent = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user , type='Sent').values('date').annotate(
        total_amount=Sum('amount'))
    datewiserecv = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user, type='Received').values(
        'date').annotate(
        total_amount=Sum('amount'))

    ydata = demDailyData.objects.filter(date=yesterday, user=user).values('type').annotate(
        total_amount=Sum('amount'))
    category_data = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user).values(
        'primaryCat').annotate(total_amount=Sum('amount'))

    last5 = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user).order_by('-date')[:5]

    cat , catVal = [] , []
    days, day_spent = [], []
    dayr, day_recv = [], []

    for i in category_data:
        if i['primaryCat'] not in ('Received_NC', 'Others'):
            cat.append(i['primaryCat'])
            catVal.append(i['total_amount'])

    for i in datewisespent:
        q_date = i['date']
        f_date = q_date.strftime("%Y-%m-%d")
        days.append(f_date)
        day_spent.append(i['total_amount'])
    for i in datewiserecv:
        q_date = i['date']
        f_date = q_date.strftime("%Y-%m-%d")
        dayr.append(f_date)
        day_recv.append(i['total_amount'])
    print(days , day_spent)
    print(dayr, day_recv)
    print(cat, catVal)
    context = {
        'monthlydata': monthlydata,
        'set1': last5,
        'cat': cat,
        'catVal': catVal,
        'days':days,
        'day_spent':day_spent,
        'dayr': dayr,
        'day_recv': day_recv,
        'category_data': category_data,
        'ydata': ydata,

    }

    return render(request, "DEM.html", context)


def Temp1(request):
    fromdate = request.GET["fdate"]
    todate = request.GET["tdate"]
    set = demDailyData.objects.filter(date__range=["2023-02-20", "2023-02-28"]).values('user', 'type').annotate(
        total_amount=Sum('amount'))
    category_data = demDailyData.objects.filter(date__range=["2023-02-20", "2023-03-03"]).values('primaryCat').annotate(
        total_amount=Sum('amount'))
    set1 = demDailyData.objects.filter(user='Sanjay').order_by('-date')[:5]

    cat = []
    catVal = []
    for i in category_data:
        cat.append(i['primaryCat'])
        catVal.append(i['total_amount'])

    print(cat.index('others'))
    print(catVal[cat.index('others')])

    context = {
        'set': set,
        'set1': set1,
        'cat': cat,
        'catVal': catVal,

    }

    return render(request, "CustomTransaction.html", context)


def MonthTable(request):
    current_user = request.user
    user = current_user.username
    try:
        print("inside")
        MonthStartDate = request.GET["fdate"]
        today = request.GET["tdate"]
    except:
        today = date.today()
        startdate = str(date.today()).split('-')
        MonthStartDate = str(startdate[0]) + '-' + str(startdate[1]) + '-01'

    set = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user).order_by('-date')

    context = {
        'set': set
    }
    return render(request, "Monthlytable.html", context)


def user(request):
    set = demDailyData.objects.filter(user='Sanjay')
    print("-----------------------------------------------------------------------", set)

    context = {
        'set': set
    }
    return render(request, "Monthlytable.html", context)


def News(request):
    set = demDailyData.objects.filter(date__range=["2023-02-20", "2023-02-28"]).values('user', 'type').annotate(
        total_amount=Sum('amount'))
    set1 = demDailyData.objects.filter(user='Sanjay')
    print("-----temp------------------------------------------------------------------", set)

    context = {
        'set': set,
        'set1': set1
    }

    return render(request, "index.html", context)
