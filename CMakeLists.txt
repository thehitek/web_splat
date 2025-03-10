cmake_minimum_required(VERSION 3.31)

project(web_splat)

add_subdirectory(third_party/drogon)

add_executable(${PROJECT_NAME} main.cpp)
target_link_libraries(${PROJECT_NAME} PRIVATE drogon)