from prometheus_client import Counter, Histogram, Gauge

# Total number of tasks executed, labeled by task name and status
tasks_executed_total = Counter(
    "tasks_executed_total",
    "Total number of tasks executed",
    ["task_name", "status"],
)

# Duration of task execution
task_duration_seconds = Histogram(
    "task_duration_seconds",
    "Duration of task execution in seconds",
    ["task_name"],
)

# Gauge for currently running tasks
tasks_running = Gauge(
    "tasks_running",
    "Number of tasks currently running",
)