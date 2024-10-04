from argparse import ArgumentError

from calc_class import Calc

prefix_operators = ['/', '*', '^']

a = Calc.cmds


def input_loop(calc: Calc):

	while True:
		line = input()
		try:
			ret_value = calc.execute(line)
		except ValueError as e:
			print(e)
			continue
		except TypeError as e:
			print(e)
			continue
		except ArgumentError as e:
			print(e)
			continue
		except KeyError as e:
			print(e)
			continue

		if ret_value == -1:
			break


if __name__ == "__main__":
	calculator = Calc()
	input_loop(calculator)
	# test_line = " e4 /e3 * 2 / 3e-1"
	# print(getExprValue(test_line))
	print("Program ended successfully")
