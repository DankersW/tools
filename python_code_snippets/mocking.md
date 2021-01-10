# Mocking with Python

## Mock a property variable (class variable)

```python
from mock import PropertyMock

class A:
    def __init__(self):
        self.var_a = 12

a = A()
mock_var_a_property = PropertyMock(return_value=15)
type(a).var_a = mock_var_a_property
```

## Mocking the return value

Using function descriptor
```python
from unittest.mock import patch

class A:
    def __init__(self):
        self.var_a = 12
    def get_var_a(self):
        return self.var_a
    def multiply_var_a(self, num):
        return self.get_var_a() * num

@patch.object(A, 'get_var_a')
def test_function(mock_get_var_a):
    a = A()
    mock_get_var_a.return_value = 15
    result = a.multiply_var_a(2) # result is 30 now, not 24 
```

Using with
```python
from unittest.mock import patch

class A:
    def __init__(self):
        self.var_a = 12
    def get_var_a(self):
        return self.var_a
    def multiply_var_a(self, num):
        return self.get_var_a() * num

def test_function():
    var_a = 15
    with patch.object(A, 'get_var_a', return_value=var_a):
        a = A()
        result = a.multiply_var_a(2) # result is 30 now, not 24
```

## Mocking an entire class
```python
from unittest import mock

class A:
    pass
    
class MockA:
    pass
    
    
@mock.patch("project.path.to.A")
def test_function(mock_get_var_a):
    mock_get_var_a.return_value = MockA
    
```


