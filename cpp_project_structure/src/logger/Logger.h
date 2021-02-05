#include <iostream>

class Logger
{
    private:
        bool _status = true;
    public:
        Logger(/* args */);
        ~Logger();
        void log_number(std::string message);
        bool get_status();
};
