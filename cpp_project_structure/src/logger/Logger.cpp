#include "Logger.h"

Logger::Logger(/* args */)
{
}

Logger::~Logger()
{
}

void Logger::log_number(std::string message)
{
    std::cout << "log message: " << message << std::endl;
}

bool Logger::get_status()
{
    return _status;
}