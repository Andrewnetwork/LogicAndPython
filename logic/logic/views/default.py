from pyramid.view import view_config
import re

@view_config(route_name='home', renderer='../templates/mytemplate.jinja2')
def my_view(request):
    return {'project': 'logic'}


@view_config(route_name='truth_table', renderer='../templates/truthTable.jinja2')
def truth_table(request):
    return {'formula': request.params.get('formula', 'No Name Provided')}


@view_config(route_name='test', renderer='json')
def test(request):
    formula = request.params.get('formula', 'No Name Provided')
    formula_parse = parse_formula(formula)
    if formula_parse is None:
        return None
    else:
        return {'content': {'head': formula_variable_names(formula)+[formula],
                            'body': generate_table(formula_parse)}}


def formula_variable_names(forumla):
    return sorted(list(set(re.findall("[A-z]", forumla))))


def truth_str_array(num, width):
    return list(map(lambda c: "F" if c == '0' else "T", "{0:b}".format(num).rjust(width, '0')))


def generate_table(args):
    out = []
    for i in range(2**args["n_args"]):
        truth_values = truth_str_array(i, args["n_args"])
        truth_values.append("T" if args["fn"](*list(map(lambda x: x == "T", truth_values))) else "F")
        out.append(truth_values)
    return out


def parse_op(str, alpha_stack=[], op_stack=[], res=None):
    if len(str) == 0:
        return res
    else:
        head = str[0]

        if head.isalpha():
            if len(op_stack) != 0:
                op_pop = op_stack.pop()
                if res is None:
                    alpha_pop = alpha_stack.pop()
                    res = lambda values_dict: op_pop(values_dict[alpha_pop], values_dict[head])
                else:
                    res_old = res
                    res = lambda values_dict: op_pop(values_dict[head], res_old(values_dict))
            else:
                alpha_stack.append(head)

        elif head == "(":
            pass
        elif head == ")":
            pass
        else:
            symbolic_fn_res = symbolic_fn(head)
            if symbolic_fn_res is None:
                raise Exception("ERROR")
            else:
                op_stack.append(symbolic_fn_res)

        return parse_op(str[1:], alpha_stack, op_stack, res)




def symbolic_fn(sym):
    if sym == "∧":
        return lambda a, b: a and b
    elif sym == "∨":
        return lambda a, b: a or b
    elif sym == "→":
        return lambda a, b: (not a) or b
    elif sym == "¬":
        return lambda a: not a
    else:
        return None


def parse_formula(formula):
    if len(formula) == 3:
        return {'fn': symbolic_fn(formula[1]), 'n_args': 1 if formula[0] == formula[2] else 2}
    else:
        return None
