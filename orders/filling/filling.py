
import os
import json

from django.db import transaction
from orders.models import (
    EnumMarketplaceType,
    EnumRoutepointAction,
    EnumTruckLoadingType,
    EnumTransportOrderStatus)


@transaction.atomic
def filling_enum_marketplace_type():
    print('Filling enumerate Marketplace types:')
    path_file = f'{os.getcwd()}/orders/filling/enum_marketplace_type.json'
    with open(path_file, 'r') as file:
        json_data = json.load(file)
        for item_data in json_data:
            code_str = item_data.get('code_str', '')
            comment = item_data.get('_comment', '')
            if comment:
                continue
            defaults = {'repr': item_data.get('repr', '')}
            data_object, created = EnumMarketplaceType.objects.update_or_create(
                code_str=code_str, defaults=defaults)
            if created == True:
                print(f' Created marketplace type: {data_object.repr}')
            else:
                print(f' Update marketplace type: {data_object.repr}')
        print('')

@transaction.atomic
def filling_enum_routepoint_action():
    print('Filling enumerate routerpoints actions:')
    path_file = f'{os.getcwd()}/orders/filling/enum_routepoint_action.json'
    with open(path_file, 'r') as file:
        json_data = json.load(file)
        for item_data in json_data:
            code_str = item_data.get('code_str', '')
            comment = item_data.get('_comment', '')
            if comment:
                continue
            defaults = {'repr': item_data.get('repr', '')}
            data_object, created = EnumRoutepointAction.objects.update_or_create(
                code_str=code_str, defaults=defaults)
            if created == True:
                print(f' Created routerpoint action: {data_object.repr}')
            else:
                print(f' Update routerpoint action: {data_object.repr}')
        print('')

@transaction.atomic
def filling_enum_truck_loading_type():
    print('Filling enumerate Truck loading types:')
    path_file = f'{os.getcwd()}/orders/filling/enum_truck_loading_type.json'
    with open(path_file, 'r') as file:
        json_data = json.load(file)
        for item_data in json_data:
            code_str = item_data.get('code_str', '')
            comment = item_data.get('_comment', '')
            if comment:
                continue
            defaults = {'repr': item_data.get('repr', '')}
            data_object, created = EnumTruckLoadingType.objects.update_or_create(
                code_str=code_str, defaults=defaults)
            if created == True:
                print(f' Created truck loading type: {data_object.repr}')
            else:
                print(f' Update truck loading type: {data_object.repr}')
        print('')

@transaction.atomic
def filling_enum_transport_order_status():
    print('Filling enumerate Transport order statuses:')
    path_file = f'{os.getcwd()}/orders/filling/enum_transport_order_status.json'
    with open(path_file, 'r') as file:
        json_data = json.load(file)
        for item_data in json_data:
            code_str = item_data.get('code_str', '')
            comment = item_data.get('_comment', '')
            if comment:
                continue
            defaults = {'repr': item_data.get('repr', '')}
            data_object, created = EnumTransportOrderStatus.objects.update_or_create(
                code_str=code_str, defaults=defaults)
            if created == True:
                print(f' Created transport order status: {data_object.repr}')
            else:
                print(f' Update transport order status: {data_object.repr}')
        print('')

def filling_all():
    filling_enum_marketplace_type()
    filling_enum_routepoint_action()
    filling_enum_truck_loading_type()
    filling_enum_transport_order_status()
