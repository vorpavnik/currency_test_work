import time
import pytz
from datetime import datetime, timezone
from venv import logger

import redis
import requests
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import ExchangeRate
from .serializers import ExchangeRateSerializer

r = redis.Redis(host='localhost', port=6379, db=0)
class DollarRateView(APIView):
    # Храним время последнего запроса и курс
    last_fetch_time = 0
    last_rate_rub_per_usd = None
    min_interval = 10  # секунды

    def get(self, request):
        current_time = time.time()

        # Проверяем, прошло ли достаточно времени с последнего запроса
        if self.last_rate_rub_per_usd is not None and current_time - self.last_fetch_time < self.min_interval:
            # Возвращаем закэшированный результат
            return Response({
                "source": "cached",
                "rub_per_usd": self.last_rate_rub_per_usd,
                "timestamp": self.last_fetch_time
            })

        # Делаем новый запрос к внешнему API
        try:
            response = requests.get("https://api.exchangerate-api.com/v4/latest/RUB")
            data = response.json()

            usd_rate_rub_to_usd = data["rates"]["USD"]  # RUB → USD
            rub_rate_usd_to_rub = round(1 / usd_rate_rub_to_usd, 4)  # USD → RUB

            # Обновляем кэш
            self.last_rate_rub_per_usd = rub_rate_usd_to_rub
            self.last_fetch_time = current_time

            # Сохраняем в БД через сериализатор
            moscow_tz = pytz.timezone("Europe/Moscow")
            moscow_time = datetime.fromtimestamp(current_time, tz=moscow_tz)
            exchange_data = {
                "rate": rub_rate_usd_to_rub,
                "timestamp": moscow_time
            }

            serializer = ExchangeRateSerializer(data=exchange_data)
            if serializer.is_valid():
                serializer.save()
            else:
                logger.warning(f"Ошибка сохранения модели: {serializer.errors}")

            # Ограничиваем количество записей до 10 штук
            if ExchangeRate.objects.count() > 10:
                oldest = ExchangeRate.objects.order_by('timestamp').first()
                oldest.delete()

            return Response({
                "source": "live",
                "rub_per_usd": rub_rate_usd_to_rub,
                "updated": data.get("date"),
                "saved": exchange_data
            }, status=status.HTTP_200_OK)

        except requests.exceptions.RequestException as e:
            return Response({
                "error": "Не удалось получить данные с внешнего API",
                "details": str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)


class ExchangeRateListView(APIView):
    def get(self, request):
        rates = ExchangeRate.objects.all().order_by('-timestamp')
        serializer = ExchangeRateSerializer(rates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)