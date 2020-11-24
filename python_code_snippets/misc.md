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
