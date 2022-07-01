cmake_minimum_required(VERSION 3.19)
set(TARGET_NAME adapter_demo)

file(GLOB_RECURSE sources ./**.cpp ./**.hpp)
add_executable(${TARGET_NAME} ${sources})
#target_link_libraries(${TARGET_NAME} PRIVATE CONAN_PKG::boost CONAN_PKG::sdl CONAN_PKG::sdl_ttf CONAN_PKG::sdl_net)
target_link_libraries(${TARGET_NAME} PRIVATE adapter)
