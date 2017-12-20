from django.conf.urls import url
from Item_Flow.views import new_schedule_item, schedule_item, purchase_order, acquired, mark_on_site, mark_showroom, reject_delivery, purchase_orders, update_PO_supplier_ref, delete

urlpatterns=[

	url(r'^new_schedule_item/(?P<job_id>.+?)/$', new_schedule_item, name='new_schedule_item'), # going to refract all CRUD operations into one url per object. TODO refract this into schedule_item
    url(r'^schedule_item/(?P<function>.+?)/(?P<pk>.+?)/$', schedule_item, name='schedule_item'), 
    url(r'^purchase_order/(?P<job_id>.+?)/$', purchase_order, name='purchase_order'), # purchase order redirects to job after form processing
    url(r'^purchase_order/$', purchase_order, name='purchase_order_homepage'), # redirects to homepage after PO
    url(r'^acquired/(?P<pk>.+?)/$', acquired, name='acquired'),
    url(r'^mark_on_site/(?P<pk>.+?)/$', mark_on_site, name='mark_on_site'),
    url(r'^mark_showroom/(?P<pk>.+?)/$', mark_showroom, name='mark_showroom'),
    url(r'^reject_delivery/(?P<pk>.+?)/$', reject_delivery, name='reject_delivery'),
    url(r'^purchase_orders/$', purchase_orders, name='purchase_orders_browser'),
    url(r'^purchase_orders/(?P<order_no>.+?)/$', purchase_orders, name='purchase_orders'),
    url(r'^update_po_s_ref/(?P<pk>.+?)/$', update_PO_supplier_ref, name='update_PO_supplier_ref'),
    url(r'^delete/(?P<model>.+?)/(?P<pk>.+?)/$', delete, name='delete'),
	
]