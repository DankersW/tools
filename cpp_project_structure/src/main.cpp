#include <iostream>
#include "SimpleMath.h"


int main(int argc, char** argv)
{
    std::cout << "Hello world" << std::endl;

    int a = 1, b = 1;

    SimpleMath simple_math = SimpleMath();
    std::cout << simple_math.add(a,b) << std::endl;
}
