Why could serving 10 requests concurrently increase total token throughput while making individual requests slower?

During decode, a GPU must read the model’s weights. With batching, those weights can serve multiple requests in the same step, increasing useful computation per weight read. That improves overall GPU efficiency and total tokens per second.

But a batch of 10 also requires more computation and more KV-cache access per step. Each step can therefore take longer, so each request receives its next token less frequently.

# Day 1 — Initial LLM Inference Baseline

**Date:** November 9, 2026

## Objective

Understand how concurrent inference requests influence latency and throughput.

## Environment

- Hardware: Macbook M3 Pro
- GPU and available VRAM: 18GB
- Operating system: MacOS
- Inference engine and version: Ollama (For now)
- Model: qwen3:0.6b
- Python version: Python 3.13.2

## Experiment

Executed 12 requests at concurrency levels of 1 and 4 using the same model, prompt pattern, and output-token limit.

## Results

| Metric | Concurrency 1 | Concurrency 4 |
|---|---|---|
| Successful requests | 12 | 12 |
| p50 latency (seconds) | 0.279 | 0.834 |
| p95 latency (seconds) | 0.283 | 0.918 |
| Requests per second | 3.578 | 4.602 |
| Output tokens per second | 114.5 | 147.2 |

## Observations

1. What changed when concurrency increased?
Overall time reduced, rps increased as expected and output tokens per second increased, but p50 and p95 latencies both dropped, that means the worst and even bottom half of the requests were comparably slower even though the overall run finished earlier.
2. Did throughput improve?
Definitely, I am assuming here we consider RPS as throughput? or Tokens per second as throughput? Both can be metrics, but both of them improved so we can say throughput improved.
3. Did request latency change? Why might that be?
It's because of more computation and more KV-cache access per step, each step thus takes longer. I need more confidence on my understanding of this answer.
4. Was the result different from what I expected?
Not really, it makes sense, we are always constrained by resources, as we increase the load on a system it's bound to slow down on individual requests.

## Limitations

- Only 12 requests per configuration.
- Client-side end-to-end latency measured, not TTFT.
- No repeated trials or confidence intervals yet.
- Workload uses short, similar prompts.
- Hardware and engine-specific effects have not been isolated.

## Next steps

Implement streaming TTFT measurement, introduce longer prompt lengths, and run repeated experiments with controlled arrival rates.