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