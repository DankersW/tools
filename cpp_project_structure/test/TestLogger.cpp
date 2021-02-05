#include "catch.hpp"
#include "Logger.h"

TEST_CASE("Simple logger")
{
    Logger logger = Logger();

    SECTION("Test simple ADD")
    {
        bool status = logger.get_status();
        REQUIRE(status);
    }
}