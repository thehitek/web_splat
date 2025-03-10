#include <iostream>
#include <drogon/drogon.h>

int main(int argc, char *argv[]){
    drogon::app().setLogPath("./")
         .setLogLevel(trantor::Logger::kWarn)
         .addListener("0.0.0.0", 80)
         .setThreadNum(16)
         .run();
    return 0;
}