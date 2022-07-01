cmake_minimum_required(VERSION 3.19)
set(TARGET_NAME adapter)

file(GLOB_RECURSE sources ./**.cpp ./**.hpp)
add_library(${TARGET_NAME} STATIC ${sources})
#target_link_libraries(${TARGET_NAME} PRIVATE CONAN_PKG::glm CONAN_PKG::boost)
#target_link_libraries(${TARGET_NAME} PUBLIC CONAN_PKG::glm)
target_link_libraries(${TARGET_NAME} PRIVATE core)
target_include_directories(${TARGET_NAME} INTERFACE ..)
