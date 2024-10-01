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

	# prepend = '1' if abs_expr[0] == 'e' else ''
	# pr_expr = (prepend + abs_expr).strip()

	value: float
	for operator in infix_operators:
		if operator in abs_expr:
			oper_split = abs_expr.split(operator)
			first_segment = ''.join(oper_split[:-1])
			first_val = getExprValue(first_segment, stored)
			second_segment = oper_split[-1]
			second_val = getExprValue(second_segment, stored)
			value = operator_dict[operator](first_val, second_val)
			break

	else:
		value = float(abs_expr)

	return sign * value


def getStrValue(str_expr: str):
	if str_expr[0] == 'e':
		return float('1' + str_expr)
	return float(str_expr)
