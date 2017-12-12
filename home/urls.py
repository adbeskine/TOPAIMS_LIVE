from django.conf.urls import url
from .views import homepage, login, unlock, new_job, jobs, job, new_note, update_job, new_schedule_item, schedule_item, purchase_order, shopping_list, acquired, mark_on_site, mark_showroom, reject_delivery, purchase_order, purchase_orders, delete

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^login/$', login, name='login'),
    url(r'^unlock/(?P<unlock_password>.+?)/$', unlock, name='unlock'),
    url(r'^new_job_form/$', new_job, name='new_job_form'),
    url(r'^jobs/$', jobs, name='jobs'),
    url(r'^job/(?P<job_id>.+?)/$', job, name='job'),
    url(r'^new_note/(?P<job_id>.+?)/$', new_note, name='new_note'),
    url(r'^update_job/(?P<job_id>.+?)/(?P<status>.+?)/$', update_job, name='update_job'),
    url(r'^new_schedule_item/(?P<job_id>.+?)/$', new_schedule_item, name='new_schedule_item'), # going to refract all CRUD operations into one url per object. TODO refract this into schedule_item
    url(r'^schedule_item/(?P<function>.+?)/(?P<pk>.+?)/$', schedule_item, name='schedule_item'),
    url(r'^purchase_order/(?P<job_id>.+?)/$', purchase_order, name='purchase_order'),
    url(r'^purchase_order/$', purchase_order, name='purchase_order_homepage'),
    url(r'^shopping_list/(?P<function>.+?)/$', shopping_list, name='shopping_list_create'),
    url(r'^acquired/(?P<pk>.+?)/$', acquired, name='acquired'),
    url(r'^shopping_list/$', shopping_list, name='shopping_list'),
    url(r'^mark_on_site/(?P<pk>.+?)/$', mark_on_site, name='mark_on_site'),
    url(r'^mark_showroom/(?P<pk>.+?)/$', mark_showroom, name='mark_showroom'),
    url(r'^reject_delivery/(?P<pk>.+?)/$', reject_delivery, name='reject_delivery'),
    url(r'^purchase_orders/$', purchase_orders, name='purchase_orders_browser'),
    url(r'^purchase_orders/(?P<order_no>.+?)/$', purchase_orders, name='purchase_orders'),
    url(r'^delete/(?P<model>.+?)/(?P<pk>.+?)/$', delete, name='delete'),
    url(r'^delete/$', delete, name='delete_job'),
]


