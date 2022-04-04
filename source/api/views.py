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
        if request.user.has_perm('view_quote'):
            quotes = Quote.objects.all()
            serializer = QuoteSerializer(quotes, many=True)
            return Response(serializer.data)
        else:
            quotes = Quote.objects.filter(is_status=True)
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
        if request.user.has_perm('view_quote'):
            serializer = QuoteSerializer(quote)
            return Response(serializer.data)
        if quote.is_status == True:
            serializer = QuoteSerializer(quote)
            return Response(serializer.data)
        else:
            return Response({"err":"К сожалению у вас нет доступа для просмотра"}, status=HTTPStatus.BAD_REQUEST)


class QuoteUpdateApiView(APIView):
    def put(self, request, *args, **kwargs):
        if request.user.has_perm('change_quote'):
            quote = Quote.objects.get(pk=kwargs['pk'])
            serializer = QuoteSerializer(data=request.data, instance=quote)
            try:
                serializer.is_valid()
                serializer.save()
                return Response(serializer.data, status=HTTPStatus.OK)
            except ValidationError as err:
                return Response(data=err.detail, status=HTTPStatus.BAD_REQUEST)
        else:
            return Response({"err": "К сожалению у вас нет доступа для редактирования"}, status=HTTPStatus.BAD_REQUEST)
#
class QuoteDeleteApiView(APIView):
    def delete(self, request, *args, **kwargs):
        if request.user.has_perm('delete_quote'):
            quote = get_object_or_404(Quote, pk=kwargs['pk'])
            quote.delete()
            return JsonResponse({'pk' : kwargs['pk']}, status=204)
        else:
            return Response({"err": "К сожалению у вас нет доступа для удаления"}, status=HTTPStatus.BAD_REQUEST)

class AddRateApiView(APIView):
    def get(self, request, *args, **kwargs):
        quote = Quote.objects.get(pk=kwargs['pk'])
        quote.rate += 1
        quote.save()
        return Response({'answer' : quote.rate}, status=HTTPStatus.OK)

class RemoveRateApiView(APIView):
    def get(self, request, *args, **kwargs):
        quote = Quote.objects.get(pk=kwargs['pk'])
        quote.rate -= 1
        quote.save()
        return JsonResponse({}, status=HTTPStatus.OK)