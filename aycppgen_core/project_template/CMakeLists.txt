cmake_minimum_required(VERSION 3.19)
set(project_version 1.2.3)
set(project_description "template_project_name")
set(project_homepage "template_project_name")
set(project_name "template_project_name")

project(FlayedStar
        VERSION ${project_version}
        DESCRIPTION ${project_description}
        HOMEPAGE_URL ${project_homepage}
        LANGUAGES C CXX
        )

set(CMAKE_CXX_STANDARD 23)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()
conan_basic_setup(TARGETS)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

add_subdirectory(sources/${project_name})
add_subdirectory(sources/${project_name}Adapter)
add_subdirectory(sources/${project_name}Adapter_demo)
add_subdirectory(sources/${project_name}Core)
add_subdirectory(sources/${project_name}Core_test)

