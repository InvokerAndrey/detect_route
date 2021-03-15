from trains.models import Train


def dfs_paths(graph, start, goal):
    """Функция поиска всех возможных маршрутов из одного города в другой.
    Вариант посещения одного и того же города более одного раза не рассматривается"""

    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        if vertex in graph.keys():
            for next_ in graph[vertex] - set(path):
                if next_ == goal:
                    yield path + [next_]
                else:
                    stack.append((next_, path + [next_]))


def get_graph(queryset):
    graph = dict()
    for query in queryset:
        graph.setdefault(query.from_city_id, set())
        graph[query.from_city_id].add(query.to_city_id)
    return graph


def get_routes(request, form) -> dict:
    context = {'form': form}
    queryset = Train.objects.all().select_related('from_city', 'to_city')
    graph = get_graph(queryset)
    data = form.cleaned_data
    from_city = data['from_city']
    to_city = data['to_city']
    total_travel_time = data['total_travel_time']
    cities = data['cities']
    all_paths = list(dfs_paths(graph, from_city.id, to_city.id))
    if not len(all_paths):
        raise ValueError('Bad trip beach, we wont let you through it')
    if cities:
        _cities = [city.id for city in cities]
        paths = []
        for route in all_paths:
            if all(city in route for city in _cities):
                paths.append(route)
        if not paths:
            raise ValueError("Yo Man, no[o]ne's traveling through these godforsaken towns")
    else:
        paths = all_paths
    routes = []
    all_trains = {}
    for query in queryset:
        all_trains.setdefault((query.from_city_id, query.to_city_id), [])
        all_trains[(query.from_city_id, query.to_city_id)].append(query)
    for path in paths:
        tmp = {}
        tmp['trains'] = []
        total_time = 0
        for i in range(len(path) - 1):
            queryset = all_trains[(path[i], path[i + 1])]
            query = queryset[0]
            total_time += query.travel_time
            tmp['trains'].append(query)
        tmp['total_time'] = total_time
        if total_time <= total_travel_time:
            routes.append(tmp)
    if not routes:
        raise ValueError('Total travel time is low-flexing too much. Raise up the bar kid')
    sorted_routes = []
    if len(routes) == 1:
        sorted_routes = routes
    else:
        times = list(set(route['total_time'] for route in routes))
        times = sorted(times)
        for time in times:
            for route in routes:
                if time == route['total_time']:
                    sorted_routes.append(route)
    context['routes'] = sorted_routes
    context['cities'] = {'from_city': from_city, 'to_city': to_city}
    return context