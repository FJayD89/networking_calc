from typing import Callable

operator_dict: dict[str, Callable[[float, float], float]] = {
	'*': lambda x, y: x*y,
	'/': lambda x, y: x/y,
	'e': lambda x, y: x * 10 ** y,
	'-': lambda x, y: x-y,
	'+': lambda x, y: x+y,
	'^': lambda x, y: x**y
}

infix_operators = ['*', '/', 'e', '-', '+']


def getExprValue(expr: str, stored: dict[str, float]) -> float:
	if expr == '':
		return 1

	if expr[0] == '-':
		abs_expr = expr[1:]
		sign = -1
	else:
		abs_expr = expr
		sign = 1

	if abs_expr == '':
		return sign

	if abs_expr in stored.keys():
		return stored[abs_expr]

	prepend = '1' if abs_expr[0] == 'e' else ''
	pr_expr = (prepend + abs_expr).strip()
	# a = 1.45e5
	value: float
	for operator in infix_operators:
		if operator in pr_expr:
			oper_split = pr_expr.split(operator)
			num_str = ''.join(oper_split[:-1])
			num_val = getExprValue(num_str, stored)
			denom_str = oper_split[-1]
			denom_val = getExprValue(denom_str, stored)
			value = operator_dict[operator](num_val, denom_val)
			break

	else:
		value = getStrValue(pr_expr)

	return sign * value


def getStrValue(str_expr: str):
	if str_expr[0] == 'e':
		return float('1' + str_expr)
	return float(str_expr)
