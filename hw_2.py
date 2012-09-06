import time
import inspect
import functools

def map_rq(func, lst):
	it = iter(lst)
	for i in it:
		return [func(i)] + map_rq(func, it)
	else:
		return []

def map_yield(func, lst):
	for i in lst:
		yield func(i)

def map_rq_yield(func, lst):
	it = iter(lst)
	for i in it:
		yield func(i)
		for val in map_rq_yield(func, it):
			yield val
		break


def time_me(tfunc, data_storage):
	data_storage.setdefault('num_calls', 0)
	data_storage.setdefault('cum_time', 0)

	def closure(func):
		@functools.wraps(func)
		def closure_2(*dt, **mp):
			t1 = tfunc()
			res = func(*dt, **mp)
			dtime = tfunc() - t1

			data_storage['num_calls'] += 1
			data_storage['cum_time'] += dtime
			
			return res
		return closure_2
	return closure

def bind(func, *dt, **mp):
	@functools.wraps(func)
	def closure(*dt2, **mp2):
		mp2.update(mp)
		return func(*(dt + dt2), **mp2)
	return closure

PARAM_DOC_PREFIX = "@param"
SUPPORTED_TYPES = {'str': str,
				   'int': int}
def check_me(func):
	var_data = inspect.getargspec(func)

	types_lines = [i.strip()[len(PARAM_DOC_PREFIX):] 
						for i in func.__doc__.split('\n') 
							if i.strip().startswith(PARAM_DOC_PREFIX)]
	name_types = {}
	for name_tp in types_lines:
		name, tp = [i.strip() for i in name_tp.split(":")]

		if tp not in SUPPORTED_TYPES:
			raise ValueError("Type {} not supported".format(tp))
		
		name_types[name] = SUPPORTED_TYPES[tp]


	@functools.wraps(func)
	def closure(*dt, **mp):
		for val, name in zip(dt, var_data.args):
			if name in name_types:
				if not isinstance(val, name_types[name]):
					raise ValueError("Variable {} have wrong type {}, {} expected".format(
										name, type(val), name_types[name]))

		for name, val in mp.items():
			if name in name_types:
				if not isinstance(val, name_types[name]):
					raise ValueError("Variable {} have wrong type {}, {} expected".format(
										name, type(val), name_types[name]))
		return func(*dt, **mp)
	return closure


mess_keys_overl = "TypeError: {}() got multiple values for keyword arguments '{}'"
mess_wrong_func_proto = "varargs, keywords and dafaults aren't enabled for haskellifyed fucntion"

def all_params_ready(func, dt, mp, argspec):

	overlapped_keys = set(argspec.args[:len(dt)]) & set(mp)
	
	if len(overlapped_keys) != 0:
		raise TypeError(mess_keys_overl.format(func.__name__, 
							",".join(overlapped_keys)))

	return len(argspec.args) <= len(dt) + len(mp)


def me_haskell(func, dt=None, mp=None, argspec=None):
	if dt is None:
		dt = tuple()

	if mp is None:
		mp = {}

	if argspec is None:
		argspec = inspect.getargspec(func)

	if argspec.varargs or argspec.keywords or argspec.defaults:
		raise TypeError(mess_wrong_func_proto)

	@functools.wraps(func)
	def closure(*_dt, **_mp):
		new_dt = dt + _dt
		new_mp = mp.copy()

		overlapped_keys = set(new_mp) & set(_mp)
		if len(overlapped_keys) != 0:
			raise TypeError(
						mess_keys_overl.format(
							func.__name__, 
							",".join(overlapped_keys)))

		new_mp.update(_mp)
		
		if all_params_ready(func, new_dt, new_mp, argspec):
			return func(*new_dt, **new_mp)
		return me_haskell(func, new_dt, new_mp, argspec)

	return closure

