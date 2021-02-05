#include "catch.hpp"
#include "SimpleMath.h"


TEST_CASE("Testing the simple Math module")
{
    SimpleMath simple_math = SimpleMath();
    
    SECTION("Test simple ADD")
    {
        int sum = simple_math.add(1,2);
        REQUIRE(sum == 3);

        sum = simple_math.add(2,2);
        REQUIRE(sum == 4);
    }
}

