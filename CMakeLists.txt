cmake_minimum_required(VERSION 3.14)
project(encDetector)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11 -s -O3")

message(STATUS "start running cmake...")

find_package(Boost 1.69.0 COMPONENTS system filesystem REQUIRED)

if(Boost_FOUND)

    message(STATUS "Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
    message(STATUS "Boost_LIBRARIES: ${Boost_LIBRARIES}")
    message(STATUS "Boost_VERSION: ${Boost_VERSION}")

    include_directories(${Boost_INCLUDE_DIRS})

endif()

add_executable(encDetector is_enc.cpp)

if(Boost_FOUND)

    target_link_libraries(encDetector ${Boost_LIBRARIES})

endif()

