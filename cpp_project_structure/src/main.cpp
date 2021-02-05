#include <iostream>
#include "SimpleMath.h"
#include "Logger.h"


int main(int argc, char** argv)
{
    std::cout << "Hello world" << std::endl;

    SimpleMath simple_math = SimpleMath();
    Logger logger = Logger();

    int a = 1, b = 1;
    int sum = simple_math.add(a,b);
    
    std::cout << a << " + " << b << " = " << sum<< std::endl;
    
    logger.log_number(std::to_string(sum));
}
