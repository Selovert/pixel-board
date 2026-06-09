cmake_minimum_required(VERSION 3.22)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
project(display)

set(MATRIX_DIR  ${CMAKE_SOURCE_DIR}/rpi-rgb-led-matrix)
set(LIB_DIR     ${MATRIX_DIR}/lib)
set(INC_DIR     ${MATRIX_DIR}/include)
set(RP1_DIR     ${LIB_DIR}/rp1/rp1_pio_vendor)

add_executable(display display.cc
    ${LIB_DIR}/bdf-font.cc
    ${LIB_DIR}/content-streamer.cc
    ${LIB_DIR}/framebuffer.cc
    ${LIB_DIR}/gpio.cc
    ${LIB_DIR}/graphics.cc
    ${LIB_DIR}/hardware-mapping.c
    ${LIB_DIR}/led-matrix.cc
    ${LIB_DIR}/led-matrix-c.cc
    ${LIB_DIR}/multiplex-mappers.cc
    ${LIB_DIR}/options-initialize.cc
    ${LIB_DIR}/pixel-mapper.cc
    ${LIB_DIR}/rp1/rp1_pio_backend.cc
    ${LIB_DIR}/rp1/rp1_pio_support.c
    ${LIB_DIR}/rp1/rp1_rio_backend.cc
    ${LIB_DIR}/thread.cc
)

target_include_directories(display PRIVATE
    ${INC_DIR}
    ${RP1_DIR}/piolib/include
    ${RP1_DIR}/include
)

target_compile_options(display PRIVATE -O3 -Wall)
target_link_libraries(display pthread rt)
