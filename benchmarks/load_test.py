
import argparse
import json
import math
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.request import Request, urlopen


def send_request(index, endpoint, model):
    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": (
                    f"Request {index}: Explain CPU caching "
                    "in two sentences."
                ),
            }
        ],
        "max_tokens": 32,
        "stream": False,
    }

    req = Request(
        endpoint,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )

    start = time.perf_counter()

    try:
        with urlopen(req, timeout=120) as response:
            data = json.load(response)

        return {
            "request_id": index,
            "success": True,
            "latency_s": time.perf_counter() - start,
            "output_tokens": data.get("usage", {}).get(
                "completion_tokens", 0
            ),
        }
    except Exception as exc:
        return {
            "request_id": index,
            "success": False,
            "latency_s": time.perf_counter() - start,
            "error": str(exc),
        }


def percentile(values, percentage):
    values = sorted(values)
    if not values:
        return None
    index = math.ceil(percentage / 100 * len(values)) - 1
    return values[max(0, index)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=1)
    parser.add_argument("--requests", type=int, default=12)
    parser.add_argument("--model", default="Qwen/Qwen3-0.6B")
    parser.add_argument(
        "--endpoint",
        default="http://localhost:8000/v1/chat/completions",
    )
    parser.add_argument("--out", default="results/baseline.json")
    args = parser.parse_args()

    if args.concurrency < 1 or args.requests < 1:
        parser.error("Concurrency and requests must be positive")

    # Warm up before taking measurements.
    warmup = send_request(-1, args.endpoint, args.model)
    if not warmup["success"]:
        raise RuntimeError(f"Warmup failed: {warmup['error']}")

    start = time.perf_counter()

    with ThreadPoolExecutor(
        max_workers=args.concurrency
    ) as pool:
        futures = [
            pool.submit(
                send_request, i, args.endpoint, args.model
            )
            for i in range(args.requests)
        ]
        results = [f.result() for f in as_completed(futures)]

    wall_time = time.perf_counter() - start
    successful = [r for r in results if r["success"]]
    latencies = [r["latency_s"] for r in successful]
    tokens = sum(r["output_tokens"] for r in successful)

    summary = {
        "model": args.model,
        "endpoint": args.endpoint,
        "concurrency": args.concurrency,
        "total_requests": args.requests,
        "successful_requests": len(successful),
        "wall_time_s": wall_time,
        "p50_latency_s": percentile(latencies, 50),
        "p95_latency_s": percentile(latencies, 95),
        "requests_per_s": len(successful) / wall_time,
        "output_tokens_per_s": tokens / wall_time,
        "results": sorted(
            results, key=lambda r: r["request_id"]
        ),
    }

    output = Path(args.out)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(summary, indent=2))

    print(json.dumps(
        {k: v for k, v in summary.items() if k != "results"},
        indent=2,
    ))


if __name__ == "__main__":
    main()
