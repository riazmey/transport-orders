"""
    Script to import data from .json files
    To execute this script run:
        1) python manage.py shell
        2) from orders.filling import filling_all
        3) filling_all()
        4) exit()
"""

from .filling import (
    filling_all,
    filling_enum_marketplace_type,
    filling_enum_routepoint_action,
    filling_enum_truck_loading_type,
    filling_enum_transport_order_status)

__all__ = [
    filling_all,
    filling_enum_marketplace_type,
    filling_enum_routepoint_action,
    filling_enum_truck_loading_type,
    filling_enum_transport_order_status]
