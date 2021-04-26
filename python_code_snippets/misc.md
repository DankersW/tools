# Misc Python snippets

## Dictionary: Safe deep get of nested dict
```python
def safe_deep_get(dct: dict, default: str, *keys: str) -> str:
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return default
    return dct

example_dct = {'a': {'b': 'test'}}
result = safe_deep_get(example_dct, 'NA', 'a', 'b')  # Result = 'test'
result = safe_deep_get(example_dct, 'NA', 'a', 'c')  # Result = 'NA'
```

## Convert dictionary to namedTuple
```python
from collections import namedtuple
from typing import NamedTuple


def convert_dict_to_named_tuple(tuple_name: str, dictionary: dict) -> NamedTuple:
    return namedtuple(tuple_name, dictionary.keys())(**dictionary)


dct = {"a": 1, "b": 2}
my_tuple = convert_dict_to_named_tuple(tuple_name="my_tuple", dictionary=dct)

on_line_conv = namedtuple("tuple_name", dct.keys())(**dct)

print(my_tuple.a)
print(on_line_conv.a)
```

## Looping over static functions from a different class 
```python
class Functions:
    @staticmethod
    def fun_a():
        return 'fun_a'

    @staticmethod
    def fun_b():
        return 'fun_b'

    functions = [fun_a.__get__(object), fun_b.__get__(object)] # dummy context (which will be ignored anyway)

def main():
    f_obj = Functions()
    for fun in f_obj.functions:
        print(fun())

if __name__ == '__main__':
    main()
```

## Yattag simple HTML doc with css styling
```python
from yattag import Doc

class HtmlGenerator:
    def __init__(self) -> None:
        self.doc, self.tag, self.text = Doc().tagtext()

    def get_html_str(self) -> str:
        self._set_styling()
        with self.tag('html'):
            with self.tag('body'):
                with self.tag('h2'):
                    self.text('Example text')
        return self.doc.getvalue()

    def _set_styling(self):
        header2_style = '{text-align:center}'
        with self.tag('style'):
            self.doc.asis(f'h2 {header2_style}')

if __name__ == '__main__':
    html_generator = HtmlGenerator()
    html_doc = html_generator.get_html_str()
```

## OOP: Python approach to function overloading
Combination of the facade pattern and function overloading
```python
from typing import Union

class A:
    def print(self, msg: Union[int, float, str, list]) -> str:
        type_map = {
            str: self._print,
            int: self._print_decimal,
            float: self._print_decimal,
            list: self._print_list
        }       
        return type_map.get(type(msg), self._print_type_error)(msg=msg)
    
    def _print_type_error(self, msg):
        raise TypeError('bad type')
    
    @staticmethod
    def _print(msg: str) -> str:
        return msg    

    def _print_decimal(self, msg: Union[int, float]) -> str:
        return self.print(msg=str(msg))
    
    def _print_list(self, msg: list) -> str:
        return self.print(msg="".join(msg))

if __name__ == '__main__':
    a = A()
    a.print(12)
    a.print('12')
    a.print(['1', '2'])
```
