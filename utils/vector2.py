from typing import TypeVar, Generic

_T = TypeVar("_T", int, float)

class Vector2(Generic[_T]):
    
    class ArgumentException(Exception):
        def __init__(self, message: str, code: int):
            super().__init__(message)
            self.code: int = code
    
    def __init__(self, x: _T, y: _T):
        self.__check_args(x, y)
        self.x: _T = x
        self.y: _T = y
        self.__type: str = "" 
        
    def __get_type(self):
        if type(self.x) is float or type(self.y) is float:
            self.__type = "f"
        else:
            self.__type = "i"
            
    def __check_args(self, x:_T, y:_T):
        if type(x) is not int and type(x) is not float:
            raise self.ArgumentException(f"\033[1;31m[ERROR] - Argument x is of type: {type(x)}. Allowed types are: float and int\033[0m", 401)
        else:
            if type(y) is not int and type(y) is not float:
                raise self.ArgumentException(f"\033[1;31m[ERROR] - Argument y is of type: {type(y)}. Allowed types are: float and int\033[0m", 401)
            
            
    def __repr__(self):
        self.__get_type()
        return f"Vector2{self.__type}({self.x}, {self.y})"