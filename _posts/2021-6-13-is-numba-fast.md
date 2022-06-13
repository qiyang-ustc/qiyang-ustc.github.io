---
layout: post
title:  "is Numba fast?"
date:   2022-06-13 12:11:09 +0800
categories: physics learning chinese
---

In this post, we are going to talk about some basic operation in Julia, Python and C++. The code used are simple(so they are not optimized quite well...).

## C++

We used codes in [Looping-Performance-in-C++](https://unclejimbo.github.io/2017/04/03/Looping-Performance-in-C++/). Though, in that article, the result is not printed so when compiling this code with "-O3" and native(optimization for special CPU architecture and instructions set) optimization, the loop will be optimized to nothing. So we modified this in the following

```bash
	g++-11 -O3  -march=native ./loop_performance/c.cpp 
```


```cpp
#include <vector>
#include <chrono>
#include <iostream>

#define _NLOOPS 4800000
int sum(int &accum,std::vector<float> &buffer)
{
	for (size_t j = 0; j < buffer.size(); ++j) 
	{
			if (buffer[j] < 1.0f)
				accum++ ;
		}
	return accum;
}

int main()
{
	auto buffer = std::vector<float>(_NLOOPS*6, 0.5f);
	int s = 0;

	auto tstart = std::chrono::high_resolution_clock::now();
	s = sum(s,buffer);
	auto tend = std::chrono::high_resolution_clock::now();
    
	std::cout << s <<std::endl ;
	auto duration = tend - tstart;
	std::cout << "Raw loop(ms): " << std::chrono::duration_cast<std::chrono::microseconds>(duration).count() << std::endl;
}
```

The result is (micro seconds):

```bash
Raw loop(ms): 7233
```

## Julia

This is a easy program

```julia
using BenchmarkTools
const N = 4800000

buffer = rand(Float32,6,N)
buffer .= 0.5f0
acc = 0
function fun(acc::Int,buffer::Matrix{Float32})
    for i=1:6
        for j=1:N
            if (buffer[i,j] < 1.0f0)
                acc = acc+1
            end
        end
    end
    return acc
end
@benchmark fun(acc, buffer)
#===result
BenchmarkTools.Trial: 90 samples with 1 evaluation.
 Range (min … max):  49.368 ms … 71.426 ms  ┊ GC (min … max): 0.00% … 0.00%
 Time  (median):     54.485 ms              ┊ GC (median):    0.00%
 Time  (mean ± σ):   55.642 ms ±  3.855 ms  ┊ GC (mean ± σ):  0.00% ± 0.00%
 ===#
```

The result is disappointing. It seems simple Julia program is not as fast as C++.

Though if we adopt the local memory layout and close out-of-boundary check:

```julia

using BenchmarkTools
const N = 4800000

buffer = rand(Float32,N*6)
buffer .= 0.5f0
acc = 0
function fun(acc::Int,buffer::Vector{Float32})
    @inbounds for j=1:6*N
        if (buffer[j] < 1.0f0)
            acc = acc+1
        end
    end
    return acc
end
@benchmark fun(acc, buffer)
#=
BenchmarkTools.Trial: 561 samples with 1 evaluation.
 Range (min … max):  7.915 ms … 61.952 ms  ┊ GC (min … max): 0.00% … 0.00%
 Time  (median):     8.644 ms              ┊ GC (median):    0.00%
 Time  (mean ± σ):   8.908 ms ±  2.662 ms  ┊ GC (mean ± σ):  0.00% ± 0.00%
 =#
```

This result is reasonable. Their performance should be close to each other!

## Python

So, what about Python? With Numba?

```python
from numba import jit
import numpy as np
N = 4800000*6
A = np.random.rand(N)
A.dtype=np.float32
@jit
def fun(A):
    sum = 0
    for i in range(4800000*6):
        if A[i] > 0.5:
            sum += 1
    return sum

%timeit fun(A)
8.72 ms ± 361 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
```

You see... Python with numba is almost reliable to be as fast as Julia and C++ can...
