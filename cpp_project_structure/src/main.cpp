#include <iostream>
#include "SimpleMath.h"


int main(int argc, char** argv)
{
    std::cout << "Hello world" << std::endl;

    SimpleMath simple_math = SimpleMath();

    int a = 1, b = 1;
    int sum = simple_math.add(a,b);
    
    std::cout << a << " + " << b << " = " << sum<< std::endl;
}
