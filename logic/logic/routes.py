def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('truth_table', '/truth_table')
    config.add_route('test', '/test')
