
import sys 

from typing import Dict, Tuple

class Singleton:
    """
    A non-thread-safe helper class to ease implementing singletons.
    This should be used as a decorator -- not a metaclass -- to the
    class that should be a singleton.

    The decorated class can define one `__init__` function that
    takes only the `self` argument. Other than that, there are
    no restrictions that apply to the decorated class.

    To get the singleton instance, use the `Instance` method. Trying
    to use `__call__` will result in a `TypeError` being raised.

    Limitations: The decorated class cannot be inherited from.

    """

    def __init__(self, decorated):
        self._decorated = decorated

    def Instance(self):
        """
        Returns the singleton instance. Upon its first call, it creates a
        new instance of the decorated class and calls its `__init__` method.
        On all subsequent calls, the already created instance is returned.

        """
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated()
            return self._instance

    def __call__(self):
        raise TypeError('Singletons must be accessed through `Instance()`.')

    def __instancecheck__(self, inst):
        return isinstance(inst, self._decorated)

@Singleton
class StringShortener():
    """
        This helper class could be used for string shortening problem,
        replacing each two adjacent distinct characters by another character until the string is shortened.
        It is designed to be a singelton class,
        meaning that it will be instantiated only once,
        and its public methods (shorten_solution1, shorten_solution2) could be called by any other 
        class/function that wants to shorten a string
    """
    __instance = None
    
    def __init__(self):
        self.valid_chars = ['a', 'b', 'c']
        self.replacments: Dict[Tuple[str, str], str] = {
            ('a', 'b'): 'c',
            ('a', 'c'): 'b',
            ('b', 'a'): 'c',
            ('b', 'c'): 'a',
            ('c', 'a'): 'b',
            ('c', 'b'): 'a',
        }
        
    def shorten(self, string: str) -> str:
        """
            Algorithm:
             1- begin with input string
             2- try every substitution of two adjacent disctinct characters
             3- choose the output string with the best score (compute_score function)
             4- consider the best scored string as input string again
             5- repeat step 1 again until the string size if less than 2 or there are not adjacent distinct characters left
             
            Complexity:
             Time:
              - O(N * (((N * (N + 1)) / 2) * 2)) ~~ O(N^2)
             Space:
              - O(N)
              
            Alternative Solution:
             - An alternative solution that can compute the length of the shortened string only, but cannot 
             find the shortened string itself
        """
        
        # throw exception if string is not valid
        if(self.__check_valid_string(string) == False):
            raise Exception("string is not valid")
        
        cur_str = string

        while(len(cur_str) >= 2 and self.__get_adjacent_distinct_count(cur_str) != 0):
            
            next_str: str = ""
            best_score: int = sys.maxsize
            
            for i in range(1, len(cur_str)):
                if(cur_str[i] != cur_str[i - 1]): # disticnt adjacent
                    new_string: str = cur_str[0:i - 1] + self.replacments[(cur_str[i], cur_str[i - 1])] + cur_str[i + 1:len(cur_str)]
                    score: int = self.__compute_score(new_string)
                    if(score < best_score):
                        best_score = score
                        next_str = new_string
            
            cur_str = next_str

        return cur_str
    
    def __get_adjacent_distinct_count(self, string: str) -> int:
        """
            Count the number of adjacent distinct characters
        """
        adjacent_disticnt: int = 0
        for i in range(1, len(string)):
            adjacent_disticnt += (string[i] != string[i - 1])
        return adjacent_disticnt

    def __compute_score(self, string: str) -> int:
        """
            The shortened string score is evaluated by considering the number of adjacent disctinct characters
        """
        return len(string) - self.__get_adjacent_distinct_count(string)
    
    def __check_valid_string(self, string: str) -> bool:
        """
            Check if the input string contains characters that are not valid (not 'a' or 'b' or 'c')
        """
        for c in string:
            if(c not in self.valid_chars):
                return False
        return True
