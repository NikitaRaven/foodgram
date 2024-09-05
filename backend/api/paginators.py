from rest_framework.pagination import LimitOffsetPagination


class SubscriptionPagination(LimitOffsetPagination):
    max_limit = 100

    def get_limit(self, request):
        limit = request.query_params.get('recipes_limit', None)
        if limit is not None:
            return min(int(limit), self.max_limit)
        return super().get_limit(request)
