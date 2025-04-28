// src/fast_bitcount.h

// ALL OF THIS IS NOT ACTUALLY USED IN THE PROJECT
#pragma once
#include <cstdint>

#if defined(__GNUC__) || defined(__clang__)
// Use the compiler-builtin (POPCNT instruction if available)
inline int fast_popcount(uint64_t x) {
    return __builtin_popcountll(x);
}

#elif defined(_MSC_VER)
// MSVC intrinsic
#include <intrin.h>
inline int fast_popcount(uint64_t x) {
    return static_cast<int>(__popcnt64(x));
}

#else
// Portable SWAR fallback
inline int fast_popcount(uint64_t x) {
    x = x - ((x >> 1) & 0x5555555555555555ULL);
    x = (x & 0x3333333333333333ULL) + ((x >> 2) & 0x3333333333333333ULL);
    x = (x + (x >> 4)) & 0x0F0F0F0F0F0F0F0FULL;
    return static_cast<int>((x * 0x0101010101010101ULL) >> 56);
}
#endif
