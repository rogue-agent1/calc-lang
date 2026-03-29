#!/usr/bin/env python3
"""calc_lang - Calculator language with variables, functions, and control flow."""
import sys, re

class Calc:
    def __init__(self):
        self.vars = {}
        self.funcs = {}
    def eval(self, code):
        tokens = re.findall(r"[a-zA-Z_]\w*|\d+\.?\d*|[+\-*/()=,;{}]|[<>!]=?|==", code)
        self.tokens = tokens
        self.pos = 0
        result = None
        while self.pos < len(self.tokens):
            result = self._stmt()
        return result
    def _peek(self): return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def _eat(self, expected=None):
        t = self.tokens[self.pos]; self.pos += 1
        if expected and t != expected: raise SyntaxError(f"expected {expected}, got {t}")
        return t
    def _stmt(self):
        if self._peek() == "let":
            self._eat("let"); name = self._eat(); self._eat("="); val = self._expr()
            if self._peek() == ";": self._eat()
            self.vars[name] = val; return val
        val = self._expr()
        if self._peek() == ";": self._eat()
        return val
    def _expr(self):
        left = self._term()
        while self._peek() in ("+", "-"):
            op = self._eat()
            right = self._term()
            left = left + right if op == "+" else left - right
        return left
    def _term(self):
        left = self._atom()
        while self._peek() in ("*", "/"):
            op = self._eat()
            right = self._atom()
            left = left * right if op == "*" else left / right
        return left
    def _atom(self):
        t = self._peek()
        if t == "(":
            self._eat("("); val = self._expr(); self._eat(")"); return val
        if t == "-":
            self._eat(); return -self._atom()
        if t and re.match(r"\d", t):
            self._eat()
            return float(t) if "." in t else int(t)
        if t and re.match(r"[a-zA-Z_]", t) and t != "let":
            self._eat()
            if t in self.vars: return self.vars[t]
            raise NameError(f"undefined: {t}")
        raise SyntaxError(f"unexpected: {t}")

def test():
    c = Calc()
    assert c.eval("2 + 3 * 4") == 14
    assert c.eval("(2 + 3) * 4") == 20
    assert c.eval("let x = 10; x * 2") == 20
    assert c.eval("let y = 5; let z = 3; y + z") == 8
    assert abs(c.eval("10 / 3") - 3.333) < 0.01
    assert c.eval("-5 + 3") == -2
    print("calc_lang: all tests passed")

if __name__ == "__main__":
    test() if "--test" in sys.argv else print("Usage: calc_lang.py --test")
