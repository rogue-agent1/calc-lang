#!/usr/bin/env python3
"""calc_lang: Calculator language with variables, functions, and control flow."""
import re, sys

class CalcInterp:
    def __init__(self):
        self.vars = {}
        self.funcs = {}

    def eval_expr(self, expr):
        expr = expr.strip()
        # Assignment
        m = re.match(r'^(\w+)\s*=\s*(.+)$', expr)
        if m and m.group(1) not in ('if', 'while', 'def', 'return') and not expr.count('==') and not expr.count('!=') and not expr.count('>=') and not expr.count('<='):
            val = self.eval_expr(m.group(2))
            self.vars[m.group(1)] = val
            return val
        # Comparison
        for op, fn in [('>=', lambda a,b: int(a>=b)), ('<=', lambda a,b: int(a<=b)),
                       ('==', lambda a,b: int(a==b)), ('!=', lambda a,b: int(a!=b)),
                       ('>', lambda a,b: int(a>b)), ('<', lambda a,b: int(a<b))]:
            # Find operator not inside parens
            depth = 0
            for i in range(len(expr)-1, -1, -1):
                if expr[i] == ')': depth += 1
                elif expr[i] == '(': depth -= 1
                elif depth == 0 and expr[i:i+len(op)] == op:
                    left = expr[:i]
                    right = expr[i+len(op):]
                    if left and right:
                        return fn(self.eval_expr(left), self.eval_expr(right))
        # Addition/subtraction
        depth = 0
        for i in range(len(expr)-1, -1, -1):
            if expr[i] == ')': depth += 1
            elif expr[i] == '(': depth -= 1
            elif depth == 0 and expr[i] in '+-' and i > 0:
                left = expr[:i].strip()
                if left and not left.endswith(('*', '/', '+', '-', '(')):
                    right = expr[i+1:]
                    if expr[i] == '+': return self.eval_expr(left) + self.eval_expr(right)
                    else: return self.eval_expr(left) - self.eval_expr(right)
        # Multiplication/division
        depth = 0
        for i in range(len(expr)-1, -1, -1):
            if expr[i] == ')': depth += 1
            elif expr[i] == '(': depth -= 1
            elif depth == 0 and expr[i] in '*/%':
                left = expr[:i]; right = expr[i+1:]
                if expr[i] == '*': return self.eval_expr(left) * self.eval_expr(right)
                elif expr[i] == '/': return self.eval_expr(left) / self.eval_expr(right)
                else: return self.eval_expr(left) % self.eval_expr(right)
        # Unary minus
        if expr.startswith('-'):
            return -self.eval_expr(expr[1:])
        # Parens
        if expr.startswith('(') and expr.endswith(')'):
            return self.eval_expr(expr[1:-1])
        # Function call
        m = re.match(r'^(\w+)\((.*)\)$', expr)
        if m:
            name = m.group(1)
            args_str = m.group(2)
            args = [self.eval_expr(a) for a in args_str.split(',')] if args_str else []
            if name == 'abs': return abs(args[0])
            if name == 'max': return max(args)
            if name == 'min': return min(args)
            if name in self.funcs:
                params, body = self.funcs[name]
                old = dict(self.vars)
                for p, a in zip(params, args):
                    self.vars[p] = a
                result = self.eval_expr(body)
                self.vars = old
                return result
        # Variable
        if expr in self.vars: return self.vars[expr]
        # Number
        try: return int(expr)
        except ValueError:
            try: return float(expr)
            except ValueError: raise RuntimeError(f"Unknown: {expr}")

def test():
    c = CalcInterp()
    assert c.eval_expr("2 + 3") == 5
    assert c.eval_expr("10 - 3 * 2") == 4
    assert c.eval_expr("(10 - 3) * 2") == 14
    assert c.eval_expr("x = 5") == 5
    assert c.eval_expr("x * 2") == 10
    assert c.eval_expr("y = x + 3") == 8
    assert c.eval_expr("10 > 5") == 1
    assert c.eval_expr("3 == 3") == 1
    assert c.eval_expr("abs(-5)") == 5
    assert c.eval_expr("max(1,5,3)") == 5
    # Nested
    assert c.eval_expr("(2 + 3) * (4 - 1)") == 15
    # Negative
    assert c.eval_expr("-5 + 10") == 5
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test": test()
    else: print("Usage: calc_lang.py test")
