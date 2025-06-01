# Photon Synchronization
 - A Python/C/Cython project to estimate the time delay between two binary photon‐detection streams by computing a cross‐correlation peak. Ideal for high‐throughput, low‐latency applications where you need to align two 1 GHz streams of 0/1 photon detections.
---
## Overview
We have two infinite logical streams of photon‐detection readings (0s and 1s). One stream (“regular”) arrives without delay; the other stream (“delayed”) is passed through a variable‐length fiber spool, inducing a time shift (on the order of 1000 ns ± jitter). Both streams contain noise (lost 1s, spurious 1s, small local shifts) and occasional large jumps in delay.

The goal is, in each 10⁵‐sample chunk (at 1 GHz sampling rate), to:
 - Slide a 1000‐sample window over the “regular” stream in the ±50‐sample range around an expected 1000 ns delay.
 - For each candidate offset, compute the number of coinciding 1s between the delayed chunk and that window.
 - Identify the offset with the maximum coincidence count (the “peak correlation”)—this gives the estimated delay for that chunk.
 - Optionally, record the correlation values for offsets “bestDelay ± 5” to characterize the peak shape.

This repo provides:
 - generate_inputs.py: A Python script that simulates two 10⁵‐sample streams with realistic time evolving delay, jitter, and noise. It writes regular_input.txt and delayed_input.txt.
 - load_stream_module.c: A custom C extension (load_stream_module) that reads a newline‐separated text file of 0s and 1s, filters out whitespace via mmap, and converts the result to a Python integer (base 2). This is faster than pure Python for large files.
 - find_coinciding.pyx: A Cython extension that implements findCoinciding(delayedInt, regularInt) → (bestDelay, bestCount, surroundingList). It loops from 950 to 1050, bit‐shifts/ands the two Python ints, calls .bit_count(), and returns both the optimal delay and surrounding correlation counts.
 - main.py: Ties everything together. In each iteration, it calls generate_inputs.generate_delayed_stream(), uses load_stream_module.load_stream to load two 10⁵‐bit integers, and then calls find_coinciding.findCoinciding to get the delay estimate.
