class QbitError(RuntimeError):
   def __init__(self, arg):
      self.args = arg
      
class QregisterError(RuntimeError):
   def __init__(self, arg):
      self.args = arg

class QgateError(RuntimeError):
   def __init__(self, arg):
      self.args = arg
