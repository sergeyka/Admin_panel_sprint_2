from asyncio import SafeChildWatcher
from pprint import pprint

from django.db.models.query import QuerySet
from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator, Page
from django.db.models import Q, F
from django.http import JsonResponse
from django.views.generic.detail import BaseDetailView
from django.views.generic.list import BaseListView

from movie_admin.models import FilmWork


# from django.db.models.query import QuerySet


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        """ Get film_works with associated actors, directors, writes and genres as arrays """
        queryset: QuerySet = super().get_queryset().prefetch_related('film_work_genre', 'genres', 'film_work_person',
                                                                     'persons', ) \
            .annotate(
            actors=ArrayAgg('persons__person__full_name', filter=Q(persons__role__exact='actor'), distinct=True),
            directors=ArrayAgg('persons__person__full_name', filter=Q(persons__role__exact='director'), distinct=True),
            writers=ArrayAgg('persons__person__full_name', filter=Q(persons__role__exact='writer'), distinct=True),
            genres=ArrayAgg('film_genres__genre__name', distinct=True)
        )

        return queryset.values()

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class Movies(MoviesApiMixin, BaseListView):
    """ Get list of movies """
    model = FilmWork
    paginate_by = 50
    ordering = 'title'

    http_method_names = ['get']  # Список методов, которые реализует обработчик

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        paginator: Paginator = context['paginator']
        page: Page = context['page_obj']
        page_items: QuerySet = context['object_list']

        context = {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(page_items),
        }

        return context


class MovieDetail(MoviesApiMixin, BaseDetailView):
    def get_object(self, queryset=None):
        try:
            return self.get_queryset().filter(id=self.kwargs['pk']).get()
        except FilmWork.DoesNotExist as err:
            return None

    def get_context_data(self, object, **kwargs):
        """
        Details of a single movie
        Raise 404 exception if ID is not found """
        print(object)
        try:
            context = {
                'results': object,
            }
        except Exception as err:
            print(err)
            print("Exception!!")

        return context
