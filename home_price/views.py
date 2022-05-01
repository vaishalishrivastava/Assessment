from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import pandas as pd
from .models import HouseData
from django.db.models import Q
import time
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


@never_cache
@csrf_exempt
@api_view(['POST'])
def register_user(request):
    """ API for registering a user """
    try:
        start_time = time.time()
        first_name = request.GET.get('firstname')
        last_name = request.GET.get('lastname')
        username = request.GET.get('username')
        password = request.GET.get('password')
        user_obj = get_user_model().objects.create(first_name=first_name, last_name=last_name, username=username, password=make_password(password), is_active=True)
        user_obj.save()
        duration = time.time() - start_time
        return JsonResponse({'response_time': duration, 'result': 'Success'}, safe=False)
    except Exception as e:
        return JsonResponse({'result': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

@never_cache
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def import_csv_data(request):
    """ API for importing csv data into table """
    try:
        start_time = time.time()
        data_df = pd.read_csv('home_price/data_home.csv')
        data_list = data_df.to_dict('records')
        obj_list = [HouseData(**data_dict) for data_dict in data_list]
        HouseData.objects.bulk_create(obj_list)
        duration = time.time() - start_time
        return JsonResponse({'response_time': duration, 'result': 'Success'}, safe=False)
    except Exception as e:
        return JsonResponse({'result': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)


@never_cache
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def budget_homes(request):
    """ API for getting house details based on max and min prices """
    try:
        start_time = time.time()
        max_price = request.GET.get('maxPrice')
        min_price = request.GET.get('minPrice')
        if not (max_price and min_price):
            return JsonResponse({'result': "Please provide max_price and min_price"},status=status.HTTP_400_BAD_REQUEST, safe=False)

        if not max_price:
            return JsonResponse({'result': "Please provide max_price"},status=status.HTTP_400_BAD_REQUEST, safe=False)

        if not min_price:
            return JsonResponse({'result': "Please provide min_price"},status=status.HTTP_400_BAD_REQUEST, safe=False)

        home_obj = list(HouseData.objects.filter(price__range=(min_price, max_price)).values())
        if not home_obj:
            return JsonResponse({'result': "No house data found within this range"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

        duration = time.time() - start_time
        return JsonResponse({'response_time': duration,'result': home_obj}, safe=False)
    except Exception as e:
        return JsonResponse({'result': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)


@never_cache
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def sqft_homes(request):
    """ API for getting house data based on minsqft """
    try:
        start_time = time.time()
        min_sqft = request.GET.get('minSqft')
        if not min_sqft:
            return JsonResponse({'result': "Please provide min_sqft"},status=status.HTTP_400_BAD_REQUEST, safe=False)

        home_obj = list(HouseData.objects.filter(sqft_living__gte=min_sqft).values())
        if not home_obj:
            return JsonResponse({'result': "No house data found which is greater than this min_sqft"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

        duration = time.time() - start_time
        return JsonResponse({'response_time': duration,'result': home_obj}, safe=False)
    except Exception as e:
        return JsonResponse({'result': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)


@never_cache
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def age_homes(request):
    """ API for get house data based on year """
    try:
        start_time = time.time()
        year = request.GET.get('year')
        if not year:
            return JsonResponse({'result': "Please provide year"},status=status.HTTP_400_BAD_REQUEST, safe=False)

        home_obj = list(HouseData.objects.filter(Q(yr_built__gte=year) | Q(yr_renovated__gte=year)).values())
        if not home_obj:
            return JsonResponse({'result': "No house data found which is greater than this year"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)

        duration = time.time() - start_time
        return JsonResponse({'response_time': duration,'result': home_obj}, safe=False)
    except Exception as e:
        return JsonResponse({'result': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)


@never_cache
@csrf_exempt
@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def predict_std_prices(request):
    """ API to get house data with new updated prdicted price """
    try:
        start_time = time.time()
        home_value = pd.DataFrame(list(HouseData.objects.values().all()))
        home_value['price'] = home_value.apply(lambda home_obj: (((home_obj['bedrooms'] * home_obj['bathrooms'] * (home_obj['sqft_living']/home_obj['sqft_lot']) * home_obj['floors']) + home_obj['waterfront'] + home_obj['view']) * home_obj['condition'] * (home_obj['sqft_above'] + home_obj['sqft_basement']) - 10 * (2022 - max(home_obj['yr_built'], home_obj['yr_renovated']))) * 100, axis=1)
        home_obj = home_value.to_dict('records')
        duration = time.time() - start_time
        return JsonResponse({'response_time': duration,'result': home_obj}, safe=False)
    except Exception as e:
        return JsonResponse({'result': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, safe=False)
