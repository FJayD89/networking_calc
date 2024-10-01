from argparse import ArgumentError
from typing import Callable

from get_value import operator_dict, getExprValue
from show_pretty import get_pretty


def get_protected_names():
	return list(operator_dict.keys()) + list(Calc.cmds.keys())


class Calc:
	history: list[float | str]
	value: float
	stored: dict[str, float]

	def __init__(self):
		self.history = [0]
		self.value = 0.0
		self.stored = {}

		print("Started")

	@staticmethod
	def get_prefix_operators():
		return ['/', '*', '^']

	def show_pretty(self, expr: str = ''):
		val = self.value
		if expr != '':
			val = getExprValue(expr, self.stored)
		print(get_pretty(val))
		# print("\033[0m", end="")

	def show_percent(self):
		# print("\033[92m", end="")
		print(f"{self.value * 100:.5}%")
		# print("\033[0m", end="")

	def end(self):
		self.show_pretty()
		print("ending")
		return -1

	def set_zero(self):
		self.show_pretty()
		print("resetting")
		self.setValue(0)

	def setValue(self, new_val: float):
		self.value = new_val

	def revert(self):
		if len(self.history) == 1:
			print("no history")
			return 0
		self.history.pop()
		self.value = self.history[-1]
		self.show_pretty()

	def show_hist(self):
		print("History:")
		[
			print(get_pretty(val)) if val is float
			else print(val)
			for val in self.history]

	def store(self, name, new_value_str: str = ''):
		val = self.value
		if new_value_str.strip() != '':
			new_value = getExprValue(new_value_str, self.stored)
			val = new_value

		if name in get_protected_names():
			raise ArgumentError(
				None,
				f"Can't use the protected name {name} as a variable name!")

		if name in self.stored:
			print(f"rewriting {name} from {self.stored[name]} to {val}.")
		self.stored[name] = val
		self.history.append(f"{name} = {self.value}")

	cmds: dict[str, Callable[["Calc", str], int]] = {
		'%': show_percent,
		'zero': set_zero,
		'end': end,
		'back': revert,
		'hist': show_hist,
		'show': show_pretty,
		'store': store
	}

	def execute(self, line: str) -> int:
		line = line.strip()
		if line == '':
			return 0

		space_split = line.split(' ')
		if space_split[0] in Calc.cmds.keys():
			cmd = space_split[0]
			args = space_split[1:]
			return_value = Calc.cmds[cmd](self, *args)  # this is fine actually
			if return_value == -1:
				return -1
			return 0

		operator = '+'
		to_eval = line.strip()
		if to_eval[0] in self.get_prefix_operators():
			operator = to_eval[0]
			to_eval = to_eval[1:]

		expr_value = getExprValue(to_eval, self.stored)
		newValue = operator_dict[operator](self.value, expr_value)
		self.setValue(newValue)
		self.show_pretty()
		self.history.append(newValue)
