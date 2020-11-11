# Misc Python snippits

## Starting a pool of threats concurrently 

```python
import concurrent.futures

def foo(threat_name, more_param):
    print(f'threat {threat_name} started with params {more_param}')


threaths = ['a', 'b', 'c']
with concurrent.futures.ThreadPoolExecutor() as executor:
    [executor.submit(foo, threat_name, more_param=12) for threat_name in threaths]

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