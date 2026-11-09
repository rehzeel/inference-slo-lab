# VLLM benchmarks

## Max Concurrency 1 

============ Serving Benchmark Result ============
Successful requests:                     50        
Failed requests:                         0         
Maximum request concurrency:             1         
Benchmark duration (s):                  37.76     
Total input tokens:                      12800     
Total generated tokens:                  3200      
Request throughput (req/s):              1.32      
Output token throughput (tok/s):         84.74     
Peak output token throughput (tok/s):    88.00     
Peak concurrent requests:                3.00      
Total token throughput (tok/s):          423.71    
---------------Time to First Token----------------
Mean TTFT (ms):                          87.94     
Median TTFT (ms):                        88.84     
P50 TTFT (ms):                           88.84     
P95 TTFT (ms):                           89.85     
P99 TTFT (ms):                           91.19     
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          10.59     
Median TPOT (ms):                        10.57     
P50 TPOT (ms):                           10.57     
P95 TPOT (ms):                           10.77     
P99 TPOT (ms):                           10.79     
----------------End-to-end Latency----------------
Mean E2EL (ms):                          754.97    
Median E2EL (ms):                        754.81    
P50 E2EL (ms):                           754.81    
P95 E2EL (ms):                           767.15    
P99 E2EL (ms):                           768.43    
==================================================


## Max Concurrency 4

============ Serving Benchmark Result ============
Successful requests:                     50        
Failed requests:                         0         
Maximum request concurrency:             4         
Benchmark duration (s):                  10.47     
Total input tokens:                      12800     
Total generated tokens:                  3200      
Request throughput (req/s):              4.78      
Output token throughput (tok/s):         305.63    
Peak output token throughput (tok/s):    324.00    
Peak concurrent requests:                12.00     
Total token throughput (tok/s):          1528.13   
---------------Time to First Token----------------
Mean TTFT (ms):                          74.71     
Median TTFT (ms):                        68.70     
P50 TTFT (ms):                           68.70     
P95 TTFT (ms):                           162.20    
P99 TTFT (ms):                           167.20    
-----Time per Output Token (excl. 1st token)------
Mean TPOT (ms):                          11.63     
Median TPOT (ms):                        11.62     
P50 TPOT (ms):                           11.62     
P95 TPOT (ms):                           11.83     
P99 TPOT (ms):                           11.88     
----------------End-to-end Latency----------------
Mean E2EL (ms):                          807.52    
Median E2EL (ms):                        800.68    
P50 E2EL (ms):                           800.68    
P95 E2EL (ms):                           897.01    
P99 E2EL (ms):                           899.17    
==================================================