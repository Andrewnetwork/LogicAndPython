from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'logic'}


@view_config(route_name='truth_table', renderer='../templates/truthTable.jinja2')
def truth_table(request):
    return {'formula': request.params.get('formula', 'No Name Provided')}


@view_config(route_name='test', renderer='json')
def test(request):
    formula = request.params.get('formula', 'No Name Provided')
    return {'content': {'head': ["A", "B", formula],
                        'body': [["T", "T", "F"], ["T", "T", "F"], ["T", "T", "F"], ["T", "T", "F"]]}}


def symbolic_fn(sym):
    if sym == "∧":
        return lambda a, b: a and b
    elif sym == "∨":
        return lambda a, b: a or b
    elif sym == "→":
        return lambda a, b: (not a) or b
    elif sym == "¬":
        return lambda a: not a


def parse_formula(str):
    return {'fn': symbolic_fn(str[1]), 'n_args': 1 if str[0] == str[2] else 2}
