from django.core.exceptions import ValidationError
from django.test import TestCase

from cities.models import City
from django.urls import reverse
from trains.models import Train
from routes import views as routes_views
from cities import views as cities_views
from routes.utils import dfs_paths, get_graph
from routes.forms import RouteForm


class AllTestCases(TestCase):

    def setUp(self) -> None:
        self.city_A = City.objects.create(name='A')
        self.city_B = City.objects.create(name='B')
        self.city_C = City.objects.create(name='C')
        self.city_D = City.objects.create(name='D')
        self.city_E = City.objects.create(name='E')

        trains = [
            Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=9),
            Train(name='t2', from_city=self.city_A, to_city=self.city_C, travel_time=7),
            Train(name='t3', from_city=self.city_A, to_city=self.city_C, travel_time=10),
            Train(name='t4', from_city=self.city_B, to_city=self.city_A, travel_time=11),
            Train(name='t5', from_city=self.city_C, to_city=self.city_B, travel_time=6),
            Train(name='t6', from_city=self.city_B, to_city=self.city_D, travel_time=8),
            Train(name='t7', from_city=self.city_B, to_city=self.city_E, travel_time=3),
            Train(name='t8', from_city=self.city_D, to_city=self.city_E, travel_time=4),
            Train(name='t9', from_city=self.city_E, to_city=self.city_D, travel_time=5),
        ]

        Train.objects.bulk_create(trains)

    def test_model_city_duplicate(self):
        '''Testing Cities for doppelgangers'''
        city = City(name='A')
        with self.assertRaises(ValidationError):
            city.full_clean()


    def test_model_train_duplicate(self):
        '''Testing Trains for doppelgangers (testing for and to city parameters)'''
        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=228)
        with self.assertRaises(ValidationError):
            train.full_clean()

    def test_model_train_time_duplicate(self):
        '''Testing Trains for doppelgangers (testing travel time)'''
        train = Train(name='t1', from_city=self.city_A, to_city=self.city_B, travel_time=228)
        with self.assertRaises(ValidationError):
            train.full_clean()
        try:
            train.full_clean()
        except ValidationError as err:
            self.assertEqual({'name': ['Train with this Train already exists.']}, err.message_dict)
            self.assertIn('Train with this Train already exists.', err.messages)

    def test_home_routes_views(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='routes/home.html')
        self.assertEqual(response.resolver_match.func, routes_views.home)

    def test_cities_cbv_detail_views(self):
        response = self.client.get(reverse('cities:detail', kwargs={'pk': self.city_A.id}))
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, template_name='cities/detail.html')
        self.assertEqual(response.resolver_match.func.__name__, cities_views.CityDetailView.as_view().__name__)

    def test_find_all_routes(self):
        queryset = Train.objects.all()
        graph = get_graph(queryset)
        all_routes = dfs_paths(graph, self.city_A.id, self.city_E.id)
        self.assertEqual(len(list(all_routes)), 4)

    def test_valid_route_form(self):
        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_B.id,
            'total_travel_time': 9,
            'cities': [self.city_E.id, self.city_D.id]
        }
        form = RouteForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_route_form(self):
        data = {
            'to_city': self.city_B.id,
            'total_travel_time': 9,
            'cities': [self.city_E.id, self.city_D.id]
        }
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())

        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_B.id,
            'total_travel_time': 13.77,
            'cities': [self.city_E.id, self.city_D.id]
        }
        form = RouteForm(data=data)
        self.assertFalse(form.is_valid())

    def test_message_error_exceeding_time(self):
        data = {
            'from_city': self.city_A.id,
            'to_city': self.city_E.id,
            'total_travel_time': 9,
            'cities': [self.city_C.id],
        }
        response = self.client.post('/find_routes/', data)
        self.assertContains(response, 'Total travel time is low-flexing too much. Raise up the bar kid', 1, 200)

    # def test_message_error_through_cities(self):
    #     data = {
    #         'from_city': self.city_B.id,
    #         'to_city': self.city_E.id,
    #         'total_travel_time': 322,
    #         'cities': [self.city_C.id],
    #     }
    #     response = self.client.post('/find_routes/', data)
    #     self.assertContains(response, "Yo Man, no[o]ne's traveling through these godforsaken towns", 1, 200)