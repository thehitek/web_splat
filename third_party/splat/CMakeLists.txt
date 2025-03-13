project(splat)

add_library(${PROJECT_NAME} itwom3.0.cpp splat.cpp)
set_target_properties(${PROJECT_NAME}
    PROPERTIES
    CXX_STANDARD 11
    CXX_EXTENSIONS off
)