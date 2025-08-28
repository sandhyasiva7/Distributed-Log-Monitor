**Build a Python-based system that:**
    Collects logs from multiple sources (simulated microservices).
    Aggregates metrics and error counts.
    Triggers alerts based on thresholds.
    Demonstrates concurrency, configuration management, and monitoring.
    
**Key Features**
    Log Generation: Simulate logs for multiple services.
    Log Parsing & Deduplication: Parse logs, handle duplicates/errors.
    Aggregation & Metrics: Rolling counts of errors, request rate, etc.
    Alerting: Trigger alerts when thresholds are exceeded.
    Configuration: YAML/JSON to define services, thresholds, polling interval.
    Concurrency: Process logs from multiple services simultaneously.
    Monitoring: Output metrics to console, file, or Prometheus.
    Failure Simulation: Inject errors, malformed logs, missing files.
    
**Tech Stack**
    Python (asyncio/multiprocessing for concurrency)
    YAML/JSON for configs
    Optional: Docker, Prometheus/Grafana for monitoring
