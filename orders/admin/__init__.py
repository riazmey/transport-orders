
from django.contrib import admin

from orders.models import (
    Counterparty,
    Marketplace,
    TransportOrder,
    TransportOrderTruckReqts,
    TransportOrderTruckReqtsLoadingType,
    TransportOrderExternalID,
    TransportOrderCargo,
    TransportOrderRoutepoint
)

from .counterparty import CounterpartyAdmin
from .marketplace import MarketplaceAdmin
from .transport_order import TransportOrderAdmin
from .transport_order_truck_reqts import TransportOrderTruckReqtsAdmin
from .transport_order_truck_reqts_loading_type import TransportOrderTruckReqtsLoadingTypeAdmin
from .transport_order_external_id import TransportOrderExternalIDAdmin
from .transport_order_cargo import TransportOrderCargoAdmin
from .transport_order_routepoint import TransportOrderRoutepointAdmin


admin.site.register(Counterparty, CounterpartyAdmin)
admin.site.register(Marketplace, MarketplaceAdmin)
admin.site.register(TransportOrder, TransportOrderAdmin)
admin.site.register(TransportOrderTruckReqts, TransportOrderTruckReqtsAdmin)
admin.site.register(TransportOrderTruckReqtsLoadingType, TransportOrderTruckReqtsLoadingTypeAdmin)
admin.site.register(TransportOrderExternalID, TransportOrderExternalIDAdmin)
admin.site.register(TransportOrderCargo, TransportOrderCargoAdmin)
admin.site.register(TransportOrderRoutepoint, TransportOrderRoutepointAdmin)
