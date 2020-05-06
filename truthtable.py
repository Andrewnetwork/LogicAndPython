# truthtable.py
# Andrew Ribeiro
# May 6, 2020


def parse_op(str, alpha_stack=[], op_stack=[], res=None):
    if len(str) == 0:
        return res
    else:
        head = str[0]

        if head.isalpha():
            if len(op_stack) != 0:
                # We have an operation on the stack and have encountered a variable.
                op_pop = op_stack.pop()
                if res is None:
                    alpha_pop = alpha_stack.pop()
                    res = lambda values_dict: op_pop(values_dict[alpha_pop], values_dict[head])
                else:
                    res_old = res
                    res = lambda values_dict: op_pop(values_dict[head], res_old(values_dict))
            else:
                # We have no operations by which to consume the variable, we must store it for future consumption.
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


class PropTree:
    def __init__(self, root = None, children=[]):
        self.root = root
        self.children = children

    def push(self, lexeme):
        fn_res = PropTree.symbolic_fn(lexeme)
        if fn_res is None:
            self.children.append(lexeme)
        else:
            if self.root is None:
                self.root = fn_res
            else:
                # We have a new tree root.
                newTree = PropTree(self.root, self.children)
                self.root = fn_res
                self.children = [newTree]

    def parse(self, formula):
        for c in formula:
            self.push(c)

    def call(self, truth_value_dict):
        return self.root(*self.resolve_child_values(truth_value_dict))

    def resolve_child_values(self, truth_value_dict):
        out = []
        for child in self.children:
            if isinstance(child, PropTree):
                out.append(child.call(truth_value_dict))
            else:
                out.append(truth_value_dict[child])

        return out


    @staticmethod
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


if __name__ == '__main__':
    a = PropTree()
    a.parse("T∧S∨H")
    print(a.call({"T": False, "S": False, "H": False}))

    #print(parse_op("T∧S")({"T": True, "S": True}))
    #print(parse_op("T∧S∧Q")({"T": True, "S": True, "Q": False}))
