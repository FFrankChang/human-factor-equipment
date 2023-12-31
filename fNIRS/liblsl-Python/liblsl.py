# This file was automatically generated by SWIG (http://www.swig.org).
# Version 2.0.9
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.



from sys import version_info
if version_info >= (2,6,0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_liblsl', [dirname(__file__)])
        except ImportError:
            import _liblsl
            return _liblsl
        if fp is not None:
            try:
                _mod = imp.load_module('_liblsl', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _liblsl = swig_import_helper()
    del swig_import_helper
else:
    import _liblsl
del version_info
try:
    _swig_property = property
except NameError:
    pass # Python < 2.2 doesn't have 'property'.
def _swig_setattr_nondynamic(self,class_type,name,value,static=1):
    if (name == "thisown"): return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name,None)
    if method: return method(self,value)
    if (not static):
        self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)

def _swig_setattr(self,class_type,name,value):
    return _swig_setattr_nondynamic(self,class_type,name,value,0)

def _swig_getattr(self,class_type,name):
    if (name == "thisown"): return self.this.own()
    method = class_type.__swig_getmethods__.get(name,None)
    if method: return method(self)
    raise AttributeError(name)

def _swig_repr(self):
    try: strthis = "proxy of " + self.this.__repr__()
    except: strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except AttributeError:
    class _object : pass
    _newclass = 0


class SwigPyIterator(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, SwigPyIterator, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, SwigPyIterator, name)
    def __init__(self, *args, **kwargs): raise AttributeError("No constructor defined - class is abstract")
    __repr__ = _swig_repr
    __swig_destroy__ = _liblsl.delete_SwigPyIterator
    __del__ = lambda self : None;
    def value(self): return _liblsl.SwigPyIterator_value(self)
    def incr(self, n=1): return _liblsl.SwigPyIterator_incr(self, n)
    def decr(self, n=1): return _liblsl.SwigPyIterator_decr(self, n)
    def distance(self, *args): return _liblsl.SwigPyIterator_distance(self, *args)
    def equal(self, *args): return _liblsl.SwigPyIterator_equal(self, *args)
    def copy(self): return _liblsl.SwigPyIterator_copy(self)
    def next(self): return _liblsl.SwigPyIterator_next(self)
    def __next__(self): return _liblsl.SwigPyIterator___next__(self)
    def previous(self): return _liblsl.SwigPyIterator_previous(self)
    def advance(self, *args): return _liblsl.SwigPyIterator_advance(self, *args)
    def __eq__(self, *args): return _liblsl.SwigPyIterator___eq__(self, *args)
    def __ne__(self, *args): return _liblsl.SwigPyIterator___ne__(self, *args)
    def __iadd__(self, *args): return _liblsl.SwigPyIterator___iadd__(self, *args)
    def __isub__(self, *args): return _liblsl.SwigPyIterator___isub__(self, *args)
    def __add__(self, *args): return _liblsl.SwigPyIterator___add__(self, *args)
    def __sub__(self, *args): return _liblsl.SwigPyIterator___sub__(self, *args)
    def __iter__(self): return self
SwigPyIterator_swigregister = _liblsl.SwigPyIterator_swigregister
SwigPyIterator_swigregister(SwigPyIterator)

cf_float32 = _liblsl.cf_float32
cf_double64 = _liblsl.cf_double64
cf_string = _liblsl.cf_string
cf_int32 = _liblsl.cf_int32
cf_int16 = _liblsl.cf_int16
cf_int8 = _liblsl.cf_int8
cf_int64 = _liblsl.cf_int64
cf_undefined = _liblsl.cf_undefined

def protocol_version():
  return _liblsl.protocol_version()
protocol_version = _liblsl.protocol_version

def library_version():
  return _liblsl.library_version()
library_version = _liblsl.library_version

def local_clock():
  return _liblsl.local_clock()
local_clock = _liblsl.local_clock
class stream_info(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, stream_info, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, stream_info, name)
    __repr__ = _swig_repr
    def name(self): return _liblsl.stream_info_name(self)
    def type(self): return _liblsl.stream_info_type(self)
    def channel_count(self): return _liblsl.stream_info_channel_count(self)
    def nominal_srate(self): return _liblsl.stream_info_nominal_srate(self)
    def channel_format(self): return _liblsl.stream_info_channel_format(self)
    def source_id(self): return _liblsl.stream_info_source_id(self)
    def version(self): return _liblsl.stream_info_version(self)
    def created_at(self): return _liblsl.stream_info_created_at(self)
    def uid(self): return _liblsl.stream_info_uid(self)
    def session_id(self): return _liblsl.stream_info_session_id(self)
    def hostname(self): return _liblsl.stream_info_hostname(self)
    def desc(self, *args): return _liblsl.stream_info_desc(self, *args)
    def as_xml(self): return _liblsl.stream_info_as_xml(self)
    def channel_bytes(self): return _liblsl.stream_info_channel_bytes(self)
    def sample_bytes(self): return _liblsl.stream_info_sample_bytes(self)
    def impl(self, *args): return _liblsl.stream_info_impl(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_stream_info(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _liblsl.delete_stream_info
    __del__ = lambda self : None;
stream_info_swigregister = _liblsl.stream_info_swigregister
stream_info_swigregister(stream_info)
cvar = _liblsl.cvar
IRREGULAR_RATE = cvar.IRREGULAR_RATE
DEDUCED_TIMESTAMP = cvar.DEDUCED_TIMESTAMP
FOREVER = cvar.FOREVER

class stream_outlet(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, stream_outlet, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, stream_outlet, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _liblsl.new_stream_outlet(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_sample(self, *args): return _liblsl.stream_outlet_push_sample(self, *args)
    def push_numeric_raw(self, *args): return _liblsl.stream_outlet_push_numeric_raw(self, *args)
    def have_consumers(self): return _liblsl.stream_outlet_have_consumers(self)
    def wait_for_consumers(self, *args): return _liblsl.stream_outlet_wait_for_consumers(self, *args)
    def info(self): return _liblsl.stream_outlet_info(self)
    __swig_destroy__ = _liblsl.delete_stream_outlet
    __del__ = lambda self : None;
stream_outlet_swigregister = _liblsl.stream_outlet_swigregister
stream_outlet_swigregister(stream_outlet)


def resolve_streams(wait_time=1.0):
  return _liblsl.resolve_streams(wait_time)
resolve_streams = _liblsl.resolve_streams

def resolve_stream(*args):
  return _liblsl.resolve_stream(*args)
resolve_stream = _liblsl.resolve_stream
class continuous_resolver(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, continuous_resolver, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, continuous_resolver, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _liblsl.new_continuous_resolver(*args)
        try: self.this.append(this)
        except: self.this = this
    def results(self): return _liblsl.continuous_resolver_results(self)
    __swig_destroy__ = _liblsl.delete_continuous_resolver
    __del__ = lambda self : None;
continuous_resolver_swigregister = _liblsl.continuous_resolver_swigregister
continuous_resolver_swigregister(continuous_resolver)

class stream_inlet(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, stream_inlet, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, stream_inlet, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _liblsl.new_stream_inlet(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _liblsl.delete_stream_inlet
    __del__ = lambda self : None;
    def info(self, *args): return _liblsl.stream_inlet_info(self, *args)
    def open_stream(self, *args): return _liblsl.stream_inlet_open_stream(self, *args)
    def close_stream(self): return _liblsl.stream_inlet_close_stream(self)
    def time_correction(self, *args): return _liblsl.stream_inlet_time_correction(self, *args)
    def pull_sample(self, *args): return _liblsl.stream_inlet_pull_sample(self, *args)
    def pull_numeric_raw(self, *args): return _liblsl.stream_inlet_pull_numeric_raw(self, *args)
    def samples_available(self): return _liblsl.stream_inlet_samples_available(self)
    def was_clock_reset(self): return _liblsl.stream_inlet_was_clock_reset(self)
stream_inlet_swigregister = _liblsl.stream_inlet_swigregister
stream_inlet_swigregister(stream_inlet)

class xml_element(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, xml_element, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, xml_element, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _liblsl.new_xml_element(*args)
        try: self.this.append(this)
        except: self.this = this
    def first_child(self): return _liblsl.xml_element_first_child(self)
    def last_child(self): return _liblsl.xml_element_last_child(self)
    def parent(self): return _liblsl.xml_element_parent(self)
    def child(self, *args): return _liblsl.xml_element_child(self, *args)
    def next_sibling(self, *args): return _liblsl.xml_element_next_sibling(self, *args)
    def previous_sibling(self, *args): return _liblsl.xml_element_previous_sibling(self, *args)
    def empty(self): return _liblsl.xml_element_empty(self)
    def is_text(self): return _liblsl.xml_element_is_text(self)
    def name(self): return _liblsl.xml_element_name(self)
    def value(self): return _liblsl.xml_element_value(self)
    def child_value(self, *args): return _liblsl.xml_element_child_value(self, *args)
    def append_child_value(self, *args): return _liblsl.xml_element_append_child_value(self, *args)
    def prepend_child_value(self, *args): return _liblsl.xml_element_prepend_child_value(self, *args)
    def set_child_value(self, *args): return _liblsl.xml_element_set_child_value(self, *args)
    def set_name(self, *args): return _liblsl.xml_element_set_name(self, *args)
    def set_value(self, *args): return _liblsl.xml_element_set_value(self, *args)
    def append_child(self, *args): return _liblsl.xml_element_append_child(self, *args)
    def prepend_child(self, *args): return _liblsl.xml_element_prepend_child(self, *args)
    def append_copy(self, *args): return _liblsl.xml_element_append_copy(self, *args)
    def prepend_copy(self, *args): return _liblsl.xml_element_prepend_copy(self, *args)
    def remove_child(self, *args): return _liblsl.xml_element_remove_child(self, *args)
    def ptr(self): return _liblsl.xml_element_ptr(self)
    __swig_destroy__ = _liblsl.delete_xml_element
    __del__ = lambda self : None;
xml_element_swigregister = _liblsl.xml_element_swigregister
xml_element_swigregister(xml_element)

class lost_error(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, lost_error, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, lost_error, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _liblsl.new_lost_error(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _liblsl.delete_lost_error
    __del__ = lambda self : None;
lost_error_swigregister = _liblsl.lost_error_swigregister
lost_error_swigregister(lost_error)

class timeout_error(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, timeout_error, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, timeout_error, name)
    __repr__ = _swig_repr
    def __init__(self, *args): 
        this = _liblsl.new_timeout_error(*args)
        try: self.this.append(this)
        except: self.this = this
    __swig_destroy__ = _liblsl.delete_timeout_error
    __del__ = lambda self : None;
timeout_error_swigregister = _liblsl.timeout_error_swigregister
timeout_error_swigregister(timeout_error)

class vectorf(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorf, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorf, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectorf_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectorf___nonzero__(self)
    def __bool__(self): return _liblsl.vectorf___bool__(self)
    def __len__(self): return _liblsl.vectorf___len__(self)
    def pop(self): return _liblsl.vectorf_pop(self)
    def __getslice__(self, *args): return _liblsl.vectorf___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectorf___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectorf___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectorf___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectorf___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectorf___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectorf_append(self, *args)
    def empty(self): return _liblsl.vectorf_empty(self)
    def size(self): return _liblsl.vectorf_size(self)
    def clear(self): return _liblsl.vectorf_clear(self)
    def swap(self, *args): return _liblsl.vectorf_swap(self, *args)
    def get_allocator(self): return _liblsl.vectorf_get_allocator(self)
    def begin(self): return _liblsl.vectorf_begin(self)
    def end(self): return _liblsl.vectorf_end(self)
    def rbegin(self): return _liblsl.vectorf_rbegin(self)
    def rend(self): return _liblsl.vectorf_rend(self)
    def pop_back(self): return _liblsl.vectorf_pop_back(self)
    def erase(self, *args): return _liblsl.vectorf_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectorf(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectorf_push_back(self, *args)
    def front(self): return _liblsl.vectorf_front(self)
    def back(self): return _liblsl.vectorf_back(self)
    def assign(self, *args): return _liblsl.vectorf_assign(self, *args)
    def resize(self, *args): return _liblsl.vectorf_resize(self, *args)
    def insert(self, *args): return _liblsl.vectorf_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectorf_reserve(self, *args)
    def capacity(self): return _liblsl.vectorf_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectorf
    __del__ = lambda self : None;
vectorf_swigregister = _liblsl.vectorf_swigregister
vectorf_swigregister(vectorf)

class vectord(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectord, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectord, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectord_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectord___nonzero__(self)
    def __bool__(self): return _liblsl.vectord___bool__(self)
    def __len__(self): return _liblsl.vectord___len__(self)
    def pop(self): return _liblsl.vectord_pop(self)
    def __getslice__(self, *args): return _liblsl.vectord___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectord___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectord___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectord___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectord___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectord___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectord_append(self, *args)
    def empty(self): return _liblsl.vectord_empty(self)
    def size(self): return _liblsl.vectord_size(self)
    def clear(self): return _liblsl.vectord_clear(self)
    def swap(self, *args): return _liblsl.vectord_swap(self, *args)
    def get_allocator(self): return _liblsl.vectord_get_allocator(self)
    def begin(self): return _liblsl.vectord_begin(self)
    def end(self): return _liblsl.vectord_end(self)
    def rbegin(self): return _liblsl.vectord_rbegin(self)
    def rend(self): return _liblsl.vectord_rend(self)
    def pop_back(self): return _liblsl.vectord_pop_back(self)
    def erase(self, *args): return _liblsl.vectord_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectord(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectord_push_back(self, *args)
    def front(self): return _liblsl.vectord_front(self)
    def back(self): return _liblsl.vectord_back(self)
    def assign(self, *args): return _liblsl.vectord_assign(self, *args)
    def resize(self, *args): return _liblsl.vectord_resize(self, *args)
    def insert(self, *args): return _liblsl.vectord_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectord_reserve(self, *args)
    def capacity(self): return _liblsl.vectord_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectord
    __del__ = lambda self : None;
vectord_swigregister = _liblsl.vectord_swigregister
vectord_swigregister(vectord)

class vectorl(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorl, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorl, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectorl_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectorl___nonzero__(self)
    def __bool__(self): return _liblsl.vectorl___bool__(self)
    def __len__(self): return _liblsl.vectorl___len__(self)
    def pop(self): return _liblsl.vectorl_pop(self)
    def __getslice__(self, *args): return _liblsl.vectorl___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectorl___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectorl___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectorl___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectorl___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectorl___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectorl_append(self, *args)
    def empty(self): return _liblsl.vectorl_empty(self)
    def size(self): return _liblsl.vectorl_size(self)
    def clear(self): return _liblsl.vectorl_clear(self)
    def swap(self, *args): return _liblsl.vectorl_swap(self, *args)
    def get_allocator(self): return _liblsl.vectorl_get_allocator(self)
    def begin(self): return _liblsl.vectorl_begin(self)
    def end(self): return _liblsl.vectorl_end(self)
    def rbegin(self): return _liblsl.vectorl_rbegin(self)
    def rend(self): return _liblsl.vectorl_rend(self)
    def pop_back(self): return _liblsl.vectorl_pop_back(self)
    def erase(self, *args): return _liblsl.vectorl_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectorl(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectorl_push_back(self, *args)
    def front(self): return _liblsl.vectorl_front(self)
    def back(self): return _liblsl.vectorl_back(self)
    def assign(self, *args): return _liblsl.vectorl_assign(self, *args)
    def resize(self, *args): return _liblsl.vectorl_resize(self, *args)
    def insert(self, *args): return _liblsl.vectorl_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectorl_reserve(self, *args)
    def capacity(self): return _liblsl.vectorl_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectorl
    __del__ = lambda self : None;
vectorl_swigregister = _liblsl.vectorl_swigregister
vectorl_swigregister(vectorl)

class vectori(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectori, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectori, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectori_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectori___nonzero__(self)
    def __bool__(self): return _liblsl.vectori___bool__(self)
    def __len__(self): return _liblsl.vectori___len__(self)
    def pop(self): return _liblsl.vectori_pop(self)
    def __getslice__(self, *args): return _liblsl.vectori___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectori___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectori___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectori___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectori___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectori___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectori_append(self, *args)
    def empty(self): return _liblsl.vectori_empty(self)
    def size(self): return _liblsl.vectori_size(self)
    def clear(self): return _liblsl.vectori_clear(self)
    def swap(self, *args): return _liblsl.vectori_swap(self, *args)
    def get_allocator(self): return _liblsl.vectori_get_allocator(self)
    def begin(self): return _liblsl.vectori_begin(self)
    def end(self): return _liblsl.vectori_end(self)
    def rbegin(self): return _liblsl.vectori_rbegin(self)
    def rend(self): return _liblsl.vectori_rend(self)
    def pop_back(self): return _liblsl.vectori_pop_back(self)
    def erase(self, *args): return _liblsl.vectori_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectori(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectori_push_back(self, *args)
    def front(self): return _liblsl.vectori_front(self)
    def back(self): return _liblsl.vectori_back(self)
    def assign(self, *args): return _liblsl.vectori_assign(self, *args)
    def resize(self, *args): return _liblsl.vectori_resize(self, *args)
    def insert(self, *args): return _liblsl.vectori_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectori_reserve(self, *args)
    def capacity(self): return _liblsl.vectori_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectori
    __del__ = lambda self : None;
vectori_swigregister = _liblsl.vectori_swigregister
vectori_swigregister(vectori)

class vectors(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectors, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectors, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectors_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectors___nonzero__(self)
    def __bool__(self): return _liblsl.vectors___bool__(self)
    def __len__(self): return _liblsl.vectors___len__(self)
    def pop(self): return _liblsl.vectors_pop(self)
    def __getslice__(self, *args): return _liblsl.vectors___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectors___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectors___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectors___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectors___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectors___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectors_append(self, *args)
    def empty(self): return _liblsl.vectors_empty(self)
    def size(self): return _liblsl.vectors_size(self)
    def clear(self): return _liblsl.vectors_clear(self)
    def swap(self, *args): return _liblsl.vectors_swap(self, *args)
    def get_allocator(self): return _liblsl.vectors_get_allocator(self)
    def begin(self): return _liblsl.vectors_begin(self)
    def end(self): return _liblsl.vectors_end(self)
    def rbegin(self): return _liblsl.vectors_rbegin(self)
    def rend(self): return _liblsl.vectors_rend(self)
    def pop_back(self): return _liblsl.vectors_pop_back(self)
    def erase(self, *args): return _liblsl.vectors_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectors(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectors_push_back(self, *args)
    def front(self): return _liblsl.vectors_front(self)
    def back(self): return _liblsl.vectors_back(self)
    def assign(self, *args): return _liblsl.vectors_assign(self, *args)
    def resize(self, *args): return _liblsl.vectors_resize(self, *args)
    def insert(self, *args): return _liblsl.vectors_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectors_reserve(self, *args)
    def capacity(self): return _liblsl.vectors_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectors
    __del__ = lambda self : None;
vectors_swigregister = _liblsl.vectors_swigregister
vectors_swigregister(vectors)

class vectorstr(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorstr, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorstr, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectorstr_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectorstr___nonzero__(self)
    def __bool__(self): return _liblsl.vectorstr___bool__(self)
    def __len__(self): return _liblsl.vectorstr___len__(self)
    def pop(self): return _liblsl.vectorstr_pop(self)
    def __getslice__(self, *args): return _liblsl.vectorstr___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectorstr___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectorstr___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectorstr___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectorstr___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectorstr___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectorstr_append(self, *args)
    def empty(self): return _liblsl.vectorstr_empty(self)
    def size(self): return _liblsl.vectorstr_size(self)
    def clear(self): return _liblsl.vectorstr_clear(self)
    def swap(self, *args): return _liblsl.vectorstr_swap(self, *args)
    def get_allocator(self): return _liblsl.vectorstr_get_allocator(self)
    def begin(self): return _liblsl.vectorstr_begin(self)
    def end(self): return _liblsl.vectorstr_end(self)
    def rbegin(self): return _liblsl.vectorstr_rbegin(self)
    def rend(self): return _liblsl.vectorstr_rend(self)
    def pop_back(self): return _liblsl.vectorstr_pop_back(self)
    def erase(self, *args): return _liblsl.vectorstr_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectorstr(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectorstr_push_back(self, *args)
    def front(self): return _liblsl.vectorstr_front(self)
    def back(self): return _liblsl.vectorstr_back(self)
    def assign(self, *args): return _liblsl.vectorstr_assign(self, *args)
    def resize(self, *args): return _liblsl.vectorstr_resize(self, *args)
    def insert(self, *args): return _liblsl.vectorstr_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectorstr_reserve(self, *args)
    def capacity(self): return _liblsl.vectorstr_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectorstr
    __del__ = lambda self : None;
vectorstr_swigregister = _liblsl.vectorstr_swigregister
vectorstr_swigregister(vectorstr)

class vectorinfo(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, vectorinfo, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, vectorinfo, name)
    __repr__ = _swig_repr
    def iterator(self): return _liblsl.vectorinfo_iterator(self)
    def __iter__(self): return self.iterator()
    def __nonzero__(self): return _liblsl.vectorinfo___nonzero__(self)
    def __bool__(self): return _liblsl.vectorinfo___bool__(self)
    def __len__(self): return _liblsl.vectorinfo___len__(self)
    def pop(self): return _liblsl.vectorinfo_pop(self)
    def __getslice__(self, *args): return _liblsl.vectorinfo___getslice__(self, *args)
    def __setslice__(self, *args): return _liblsl.vectorinfo___setslice__(self, *args)
    def __delslice__(self, *args): return _liblsl.vectorinfo___delslice__(self, *args)
    def __delitem__(self, *args): return _liblsl.vectorinfo___delitem__(self, *args)
    def __getitem__(self, *args): return _liblsl.vectorinfo___getitem__(self, *args)
    def __setitem__(self, *args): return _liblsl.vectorinfo___setitem__(self, *args)
    def append(self, *args): return _liblsl.vectorinfo_append(self, *args)
    def empty(self): return _liblsl.vectorinfo_empty(self)
    def size(self): return _liblsl.vectorinfo_size(self)
    def clear(self): return _liblsl.vectorinfo_clear(self)
    def swap(self, *args): return _liblsl.vectorinfo_swap(self, *args)
    def get_allocator(self): return _liblsl.vectorinfo_get_allocator(self)
    def begin(self): return _liblsl.vectorinfo_begin(self)
    def end(self): return _liblsl.vectorinfo_end(self)
    def rbegin(self): return _liblsl.vectorinfo_rbegin(self)
    def rend(self): return _liblsl.vectorinfo_rend(self)
    def pop_back(self): return _liblsl.vectorinfo_pop_back(self)
    def erase(self, *args): return _liblsl.vectorinfo_erase(self, *args)
    def __init__(self, *args): 
        this = _liblsl.new_vectorinfo(*args)
        try: self.this.append(this)
        except: self.this = this
    def push_back(self, *args): return _liblsl.vectorinfo_push_back(self, *args)
    def front(self): return _liblsl.vectorinfo_front(self)
    def back(self): return _liblsl.vectorinfo_back(self)
    def assign(self, *args): return _liblsl.vectorinfo_assign(self, *args)
    def resize(self, *args): return _liblsl.vectorinfo_resize(self, *args)
    def insert(self, *args): return _liblsl.vectorinfo_insert(self, *args)
    def reserve(self, *args): return _liblsl.vectorinfo_reserve(self, *args)
    def capacity(self): return _liblsl.vectorinfo_capacity(self)
    __swig_destroy__ = _liblsl.delete_vectorinfo
    __del__ = lambda self : None;
vectorinfo_swigregister = _liblsl.vectorinfo_swigregister
vectorinfo_swigregister(vectorinfo)

# This file is compatible with both classic and new-style classes.


