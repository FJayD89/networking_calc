from math import log, floor

symbols: dict[int, str] = {
		-4: 'a',
		-3: 'n',
		-2: 'μ',
		-1: 'm',
		0: "",
		1: "k",
		2: 'M',
		3: 'G',
		4: 'T'
	}


def get_pretty(value: float) -> str:
	if value == 0:
		return "0.0"
	# mantissa between 1 and 999

	exp = floor(log(abs(value), 1000))
	mantissa = value * 1000 ** -exp
	mant_rnd = round(mantissa, 5)
	return str(mant_rnd) + symbols[exp]
