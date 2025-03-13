cmake_minimum_required(VERSION 3.31)

project(web_splat)

add_executable(web_splat main.cpp)
set_target_properties(web_splat
    PROPERTIES
    CXX_STANDARD 20
    CXX_EXTENSIONS off
    )

add_subdirectory(third_party/drogon)
add_subdirectory(third_party/splat)

target_link_libraries(web_splat PRIVATE splat drogon)