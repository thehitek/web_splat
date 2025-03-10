cmake_minimum_required(VERSION 3.31)

project(web_splat)

set(CMAKE_CXX_STANDARD 23)
# set(CMAKE_SYSTEM_NAME Linux)
# set(CMAKE_SYSTEM_PROCESSOR arm)


add_subdirectory(third_party/drogon)
add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE drogon)