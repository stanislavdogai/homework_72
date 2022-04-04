from http import HTTPStatus

from django.http import JsonResponse, HttpResponseNotAllowed
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.exceptions import ValidationError

from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import QuoteSerializer
from webapp.models import Quote

@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return JsonResponse({})
    return HttpResponseNotAllowed('Only GET request are allowed')

class QuoteListApiView(APIView):
    def get(self, request, *args, **kwargs):
        quotes = Quote.objects.all()
        serializer = QuoteSerializer(quotes, many=True)
        return Response(serializer.data)

class QuoteCreateApiView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = QuoteSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.CREATED)
        except ValidationError as err:
            return Response(data=err.detail, status=HTTPStatus.BAD_REQUEST)

class QuoteDetailApiView(APIView):
    def get(self, request, *args, **kwargs):
        quote = Quote.objects.get(pk=kwargs['pk'])
        serializer = QuoteSerializer(quote)
        return Response(serializer.data)

class QuoteUpdateApiView(APIView):
    def put(self, request, *args, **kwargs):
        quote = Quote.objects.get(pk=kwargs['pk'])
        serializer = QuoteSerializer(data=request.data, instance=quote)
        try:
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        except ValidationError as err:
            return Response(data=err.detail, status=HTTPStatus.BAD_REQUEST)
#
class QuoteDeleteApiView(APIView):
    def delete(self, request, *args, **kwargs):
        print(kwargs)
        quote = get_object_or_404(Quote, pk=kwargs['pk'])
        print('quote', quote)
        quote.delete()
        return Response({'pk' : kwargs['pk']}, status=204)