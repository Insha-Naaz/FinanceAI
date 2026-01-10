import time
from threading import Lock


class MetricsStore:
    def __init__(self):
        self._lock = Lock()
        self._metrics = {
            "logins": 0,
            "queries": 0,
            "errors": 0,
            "permission_denials": 0,
            "total_query_time": 0.0,
        }

    def increment(self, key: str, value: int = 1):
        with self._lock:
            if key in self._metrics:
                self._metrics[key] += value

    def record_query_time(self, duration: float):
        with self._lock:
            self._metrics["queries"] += 1
            self._metrics["total_query_time"] += duration

    def snapshot(self) -> dict:
        with self._lock:
            avg_time = (
                self._metrics["total_query_time"] / self._metrics["queries"]
                if self._metrics["queries"] > 0
                else 0.0
            )
            return {
                **self._metrics,
                "avg_query_time": round(avg_time, 4),
            }


metrics = MetricsStore()
