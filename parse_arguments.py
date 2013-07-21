import argparse

def argParseFunction():
	parser = argparse.ArgumentParser()
	parser.add_argument("-p", "--port", help="specify the port to connect", type=int, required=True)
	parser.add_argument("-H", "--host", help="specify the host to connect", default="")
	return parser.parse_args()