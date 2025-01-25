from products.models import ProductPrice
from baskets.models import WeeklyBasketItem
from orders.models import DistributorOrder, DistributorOrderBasket
from datetime import time, timedelta


TASKS = {
    'manage_weekly_basket': {
        'db_object': [WeeklyBasketItem],
        'description': 'Create and manage weekly basket',
        'operation_order': 0,
        'icon_svg_markup': '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4h1.5L8 16m0 0h8m-8 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm8 0a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm.75-3H7.5M11 7H6.312M17 4v6m-3-3h6"/> </svg>',
        'time_slots': [
            {'day_of_week': 0, 'time_start': time(0, 0), 'duration': timedelta(hours=72), 'min_req_volunteers': 1},
        ],
    },
    'update_product_prices': {
        'db_object': [ProductPrice],
        'description': 'Update latest product prices fetched from distributor',
        'operation_order': 1,
        'icon_svg_markup': '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.6 16.733c.234.269.548.456.895.534a1.4 1.4 0 0 0 1.75-.762c.172-.615-.446-1.287-1.242-1.481-.796-.194-1.41-.861-1.241-1.481a1.4 1.4 0 0 1 1.75-.762c.343.077.654.26.888.524m-1.358 4.017v.617m0-5.939v.725M4 15v4m3-6v6M6 8.5 10.5 5 14 7.5 18 4m0 0h-3.5M18 4v3m2 8a5 5 0 1 1-10 0 5 5 0 0 1 10 0Z"/> </svg>',
        'time_slots': [
            {'day_of_week': None, 'time_start': None, 'duration': None, 'min_req_volunteers': 1},
        ],
        'time_slots': [
            {'day_of_week': 3, 'time_start': time(9, 0), 'duration': timedelta(hours=1), 'min_req_volunteers': 1},
        ],
    },
    'prepare_distributor_order_purchase_list': {
        'db_object': [DistributorOrder, DistributorOrderBasket],
        'description': 'Compile Member orders to generate a distributor order list',
        'operation_order': 2,
        'icon_svg_markup': '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 4h3a1 1 0 0 1 1 1v15a1 1 0 0 1-1 1H6a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1h3m0 3h6m-3 5h3m-6 0h.01M12 16h3m-6 0h.01M10 3v4h4V3h-4Z"/> </svg>',
        'time_slots': [
            {'day_of_week': 3, 'time_start': time(16, 0), 'duration': timedelta(hours=24), 'min_req_volunteers': 1},
        ],
    },
    'purchase_order_at_distributor': {
        'db_object': [],
        'description': 'Purchase member orders at distributor',
        'operation_order': 3,
        'icon_svg_markup': '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 13V4M7 14H5a1 1 0 0 0-1 1v4a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-4a1 1 0 0 0-1-1h-2m-1-5-4 5-4-5m9 8h.01"/> </svg>',
        'time_slots': [
            {'day_of_week': 4, 'time_start': time(8, 0), 'duration': timedelta(hours=2), 'min_req_volunteers': 3},
        ],
    },
    'prepare_baskets': {
        'db_object': [],
        'description': 'Prepare baskets for member pick-up point',
        'operation_order': 4,
        'icon_svg_markup': '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> <path stroke="currentColor" stroke-linecap="round" stroke-width="2" d="M18.796 4H5.204a1 1 0 0 0-.753 1.659l5.302 6.058a1 1 0 0 1 .247.659v4.874a.5.5 0 0 0 .2.4l3 2.25a.5.5 0 0 0 .8-.4v-7.124a1 1 0 0 1 .247-.659l5.302-6.059c.566-.646.106-1.658-.753-1.658Z"/> </svg>',
        'time_slots': [
            {'day_of_week': 4, 'time_start': time(9, 0), 'duration': timedelta(hours=2.5), 'min_req_volunteers': 3},
        ],
    },
    'distribute_baskets': {
        'db_object': [],
        'description': 'Distribute baskets to members at pick-up point',
        'operation_order': 5,
        'icon_svg_markup': '<svg class="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24"> <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 8v8m0-8a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 8a2 2 0 1 0 0 4 2 2 0 0 0 0-4Zm8-8a2 2 0 1 0 0-4 2 2 0 0 0 0 4Zm0 0a4 4 0 0 1-4 4h-1a3 3 0 0 0-3 3"/> </svg>',
        'time_slots': [
            {'day_of_week': 4, 'time_start': time(11, 30), 'duration': timedelta(hours=2), 'min_req_volunteers': 2},
            {'day_of_week': 4, 'time_start': time(17, 30), 'duration': timedelta(hours=2), 'min_req_volunteers': 2},
        ],
    },
}
