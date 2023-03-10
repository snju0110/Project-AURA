from django.shortcuts import render
from django.http import JsonResponse
from dataLoggingApi.models import *
from .serializers import *
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum
from datetime import datetime, date


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


def DemMainPage(request):
    try:
        MonthStartDate = request.GET["fdate"]
        today = request.GET["tdate"]
        answer = request.GET['Select']
        print("ret")
    except:
        today = date.today()
        startdate = str(date.today()).split('-')
        MonthStartDate = str(startdate[0]) + '-' + str(startdate[1]) + '-01'
        print("excpet")
    user = 'Avinash'


    monthlydata = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user).values('type').annotate(
    total_amount=Sum('amount'))

    category_data = demDailyData.objects.filter(date__range=[MonthStartDate, today], user=user).values(
    'primaryCat').annotate(total_amount=Sum('amount'))

    last5 = demDailyData.objects.filter(user=user).order_by('-date')[:5]
    customstranscation = demDailyData.objects.filter(date__range=["2023-02-20", "2023-02-28"], user='Avinash')
    print("-----temp-------------------", category_data)
    cat = []
    catVal = []
    for i in category_data:
        if i['primaryCat'] != 'Received_NC':
            cat.append(i['primaryCat'])
            catVal.append(i['total_amount'])

    context = {
        'monthlydata': monthlydata,
        'set1': last5,
        'cat': cat,
        'catVal': catVal,
        'customstranscation': customstranscation
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

    context = {
        'set': set,
        'set1': set1,
        'cat': cat,
        'catVal': catVal,
        
    }

    return render(request, "CustomTransaction.html", context)


def MonthTable(request):
    try:
        MonthStartDate = request.GET["fdate"]
        today = request.GET["tdate"]
    except:
        today = date.today()
        startdate = str(date.today()).split('-')
        MonthStartDate = str(startdate[0]) + '-' + str(startdate[1]) + '-01'
    user = 'Avinash'

    set = demDailyData.objects.filter(date__range=[MonthStartDate, today] , user = user).order_by('-date')

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

