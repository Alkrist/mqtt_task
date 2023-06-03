from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from rest_framework.generics import UpdateAPIView
from .serializers import CoinSerializer
from .models import Coin

# Class reprezentuje view tabulky Coins a operaci nad ní.


class CoinAPIView(APIView):
    serializer_class = CoinSerializer

    # Pomocná funkce pro přístup k objektum tabulky Coins.

    def get_queryset(self):
        items = Coin.objects.all()
        return items

    # zpracování GET-requestu pro tabulku Coins.

    def get(self, request, *args, **kwargs):
        coins = self.get_queryset()
        serializer = CoinSerializer(coins, many=True)
        return Response(serializer.data)

    # zpracování POST-requestu pro tabulku Coins pomoci JSON:
    # Format:
    # type: "update" - pro editaci záznamu, jíné - pro filtrování záznamů
    # PRO EDITACI:
    # id: id coinu, který se bude měnit.
    # další možné parametry: identifier, rank, symbol, supply - budou se měnit tyto udaje pro coin
    # PRO FILTROVANI:
    # symbol: podle jakého symbolu filtrovat, např. "BTC" nebo "ETH".
    def post(self, request, *args, **kwargs):
        coins = self.get_queryset()
        if (request.query_params.get('type') == 'update'):
            serializer = CoinSerializer(coins)
            item = coins.get(id=request.query_params.get('id'))
            item = serializer.update(item, request.query_params)
            serializer = CoinSerializer(coins, many=True)
            return Response(serializer.data)
        else:
            coin_symbol = request.query_params.get('symbol')
            if (coin_symbol is not None):
                coins = coins.filter(symbol=coin_symbol)
            serializer = CoinSerializer(coins, many=True)
            return Response(serializer.data)
