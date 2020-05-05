from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


def hello_world(request):
    return Response('Hello World!!!!')

def truth_table(request):
    return Response(request.params.get("formula", "No input!"))


if __name__ == '__main__':
    with Configurator() as config:
        config.add_route('hello', '/')
        config.add_view(hello_world, route_name='hello')

        config.add_route('truth_table', '/truth_table')
        config.add_view(truth_table, route_name='truth_table')

        app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()