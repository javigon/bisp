# ex:set ts=2:

from simlog import *

class SimInterface:
  def __init__ (self):
    self.l = None
    self.table = {}
  def register_get (self, key, obj, fun):
    if not self.table.has_key(key):
      self.table[key] = {}
    self.table[key]["get"] = {"o": obj, "f": fun}
  def register_set (self, key, obj, fun):
    if not self.table.has_key(key):
      self.table[key] = {}
    self.table[key]["set"] = {"o": obj, "f": fun}
  def register (self, key, gobj, gfun, sobj, sfun):
    self.register_get(key, gobj, gfun)
    self.register_set(key, sobj, sfun)
  def get_getters (self):
    return sorted(filter(lambda e: self.table[e].has_key("get"), self.table.keys()))
  def get_setters (self):
    return sorted(filter(lambda e: self.table[e].has_key("set"), self.table.keys()))
  def get_union (self):
    return list(set(self.get_getters()) | set(self.get_setters()))
  def has_getter (self, key):
    return self.table[key].has_key("get")
  def has_setter (self, key):
    return self.table[key].has_key("set")
  def get (self, key):
    return self.table[key]["get"]["f"](self.table[key]["get"]["o"])
  def set (self, key, value):
    self.table[key]["set"]["f"](self.table[key]["set"]["o"], value)
  def attach_log (self, filename):
    self.l = SimLog(filename)
    self.l.legend(self.get_getters())
  def log (self):
    if self.l != None:
      self.l.append(map(lambda e: self.get(e), self.get_getters()))
    
  

