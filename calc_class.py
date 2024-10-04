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
		self.stored = {
			"c": 2.99774e8
		}

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
		self.history.append(f"{name} = {val}")

	def links(self):
		link_count = int(input("link count\n"))

		packet_no = int(input("no of packets\n"))
		packet_sizes: list[float] = [0]*packet_no

		for packet_index in range(packet_no):
			size_expr = input(f"size of packet {packet_index} [b] BITS!!! \n")
			packet_sizes[packet_index] = getExprValue(size_expr, self.stored)

		link_lengths: list[float] = [0]*link_count
		link_bw: list[float] = [0]*link_count
		prop_speeds: list[float] = [0]*link_count

		for link_index in range(link_count):
			len_expr = input(f"length of link {link_index} [m] \n")
			link_lengths[link_index] = getExprValue(len_expr, self.stored)
			bw_expr = input(f"bw of link {link_index} [b/s] \n")
			link_bw[link_index] = getExprValue(bw_expr, self.stored)
			prop_expr = input(f"propagation speed of link {link_index} [m/s] \n")
			prop_speeds[link_index] = getExprValue(prop_expr, self.stored)

		packet_delay = 0
		# Transmission delay from start-host
		for i in range(packet_no):
			trans_delay_i = packet_sizes[i] / link_bw[0]
			packet_delay += trans_delay_i

		packet_delay += (link_lengths[0] / prop_speeds[0])
		# Adding first propogation delay.

		# Transmission through routers
		for i in range(1, link_count):
			prop_delay = (link_lengths[i] / prop_speeds[i])
			trans_delay = (packet_sizes[-1] / link_bw[i])

			# queueing_delay = 0
			prev_packet_trans = 0

			# Calculate queueing delay.
			if i != link_count-1:
				for p in range(packet_no-1):
					prev_packet_trans += packet_sizes[p] / link_bw[i+1]

			queueing_delay = 0 if (trans_delay > prev_packet_trans) else (prev_packet_trans - trans_delay)
			packet_delay += prop_delay + queueing_delay + trans_delay

		print("total packet delay:")
		self.show_pretty(str(packet_delay))
		# return packet_delay



	@staticmethod
	def show_help(_, topic: str = ""):
		match topic:
			# case "":
			# 	pass
			case _:
				help_str = \
					"""
				Usage:
					help <topic>
					opers: explain operators
					zero(): resets value to zero
					end(): ends calc
					back(): goes a step back
					hist(): shows history of session
					show(|expr): shows current value, or evaluates expr
					store(name, |val) stores val (or current value, if empty) 
						into variable name 
					help(): 3 guesses, buddy
					"""
		print(help_str)

	cmds: dict[str, Callable[["Calc", str], int]] = {
		'%': show_percent,
		'zero': set_zero,
		'end': end,
		'back': revert,
		'hist': show_hist,
		'show': show_pretty,
		'store': store,
		'help': show_help,
		'links': links
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
