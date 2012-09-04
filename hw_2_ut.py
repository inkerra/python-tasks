#!/usr/bin/env python
import sys
import argparse
import itertools

def test_time_me(time_me):
	def time_func(counter=[0]):
		counter[0] += 1
		return counter[0]

	data_storage = {}
	timed = time_me(time_func, data_storage)(lambda x : None)

	timed(1)
	timed(2)
	timed("asdd")

	assert data_storage['num_calls'] == 3, "time_me produced wrong call count"
	assert data_storage['cum_time'] == 3, "time_me produced wrong call timings. " + \
										   "\nNote - you should call time func exactly " + \
										   "two times per func call, or this test will fail"

def test_bind(bind):
	def my_func(x, y, z, f):
		return x, y, z, f

	f1 = bind(my_func, 1, f=2)

	assert f1(2, 3) == (1, 2, 3, 2)
	assert f1(3, z=3) == (1, 3, 3, 2)
	assert f1(y=True, z=3) == (1, True, 3, 2)

def test_me_haskell(me_haskell):
	@me_haskell
	def my_func(x, y, z, f):
		return x, y, z, f
	
	f = my_func(1)(2, 3)
	assert f(4) == (1, 2, 3, 4)

def test_check_me(check_me):

	@check_me
	def my_func(x, y, z, f):
		"""
		@param x: int
		@param y: str
		@param z: str
		"""
		return x, y, z, f

	assert my_func(1, "2", "3", [True]) == (1, "2", "3", [True])

	try:
		my_func("1", "2", "3", True)
	except ValueError:
		pass
	else:
		assert False


	try:
		my_func(1, 2, "3", True)
	except ValueError:
		pass
	else:
		assert False

def test_map_rq(map_rq):
	assert list(map_rq(lambda x : x ** 2, [])) == []
	assert list(map_rq(lambda x : x ** 2, [1, 2, 3])) == [1, 4, 9]
	sys.setrecursionlimit(40)
	try:
		map_rq(lambda x : x, range(sys.getrecursionlimit() + 1))
	except RuntimeError:
		pass
	else:
		assert False, "You map don't looks like recursive function"

def inf_ints():
	i = 0
	while True:
		yield i
		i += 1

def test_map_yield(map_yield):
	assert list(map_yield(lambda x : x ** 2, [])) == []
	assert list(map_yield(lambda x : x ** 2, [1, 2, 3])) == [1, 4, 9]
	it = map_yield(lambda x : x ** 2, inf_ints())
	tw = lambda x : x < 10
	assert list(itertools.takewhile(tw, it)) == [0, 1, 4, 9]


def test_map_rq_yield(map_yield_rq):
	assert list(map_yield_rq(lambda x : x ** 2, [])) == []
	assert list(map_yield_rq(lambda x : x ** 2, [1, 2, 3])) == [1, 4, 9]

def main(argv):
	parser = argparse.ArgumentParser()
	parser.add_argument("func_name", 
						metavar='FUNC_NAME', 
                   		help='homework function name',
                   		choices=('me_haskell', 'bind', 'time_me', 'check_me', 'map_rq', 'map_yield', 'map_rq_yield'))

	parser.add_argument("tested_module", 
						metavar='TESTED_MODULE_PY', 
                   		help='python file with function FUNC_NAME')

	args = parser.parse_args(argv[1:])

	assert args.tested_module.endswith('.py'), "Second argument should be a python file name"
	assert '/' not in args.tested_module, "tested file should be in the current directory"
	sys.path.insert(0, '.')
	
	try:
		module = __import__(args.tested_module[:-3])
	except ImportError:
		sys.stderr.write("ERROR: Can't import module " + args.tested_module[:-3] + "\n")
		raise

	globals()['test_' + args.func_name](getattr(module, args.func_name))


if __name__ == "__main__":
	sys.exit(main(sys.argv))
