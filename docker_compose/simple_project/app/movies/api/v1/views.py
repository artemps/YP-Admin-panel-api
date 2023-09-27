from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db import connection

from movies.models import Filmwork, PersonFilmworkRole


class MoviesApiMixin:
    """
    Основной миксин для представлений MoviesApi.

    Содержит указания на модели и описание запроса для
    выдачи релевантной информации о кинопроизведениях в нужной форме.
    """

    model = Filmwork
    http_method_names = ['get']

    def get_queryset(self):
        return (
            Filmwork.objects.all()
            .prefetch_related('genres', 'persons')
            .values(
                'id',
                'title',
                'description',
                'creation_date',
                'rating',
                'type',
            ).annotate(
                genres=ArrayAgg(
                    'genres__name',
                    distinct=True
                ),
                actors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonFilmworkRole.ACTOR),
                    distinct=True
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonFilmworkRole.DIRECTOR),
                    distinct=True
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    filter=Q(personfilmwork__role=PersonFilmworkRole.WRITER),
                    distinct=True
                ),
            ).order_by('title')
        )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    """Класс представления списка кинопроизведений для API."""

    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()

        paginator, page, qs, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next':  page.next_page_number() if page.has_next() else None,
            'results': list(qs),
        }
        return context


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    """Класс детального представления информации о кинопроизведении."""

    def get_context_data(self, **kwargs):
        return self.get_object()
