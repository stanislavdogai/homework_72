from django.urls import path

from api.views import QuoteListApiView, QuoteCreateApiView, QuoteDetailApiView, QuoteUpdateApiView, QuoteDeleteApiView, \
    get_token_view, AddRateApiView, RemoveRateApiView

app_name= 'quote'

urlpatterns = [
    path('', QuoteListApiView.as_view(), name='quote_list'),
    path('create/', QuoteCreateApiView.as_view(), name='quote_create'),
    path('<int:pk>/detail/', QuoteDetailApiView.as_view(), name='quote_detail'),
    path('<int:pk>/update/', QuoteUpdateApiView.as_view(), name='quote_update'),
    path('<int:pk>/delete/', QuoteDeleteApiView.as_view(), name='quote_delete'),
    path('<int:pk>/add/rate/', AddRateApiView.as_view(), name='quote_add_rate'),
    path('<int:pk>/remove/rate/', RemoveRateApiView.as_view(), name='quote_remove_rate'),
    path('csrftoken/', get_token_view, name='get_token_view'),
]