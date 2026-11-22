from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProbeRequest(_message.Message):
    __slots__ = ("probe", "app", "min_ready")
    PROBE_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    MIN_READY_FIELD_NUMBER: _ClassVar[int]
    probe: str
    app: str
    min_ready: int
    def __init__(self, probe: _Optional[str] = ..., app: _Optional[str] = ..., min_ready: _Optional[int] = ...) -> None: ...

class ProbeAnswer(_message.Message):
    __slots__ = ("ok", "reason")
    OK_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ok: bool
    reason: str
    def __init__(self, ok: _Optional[bool] = ..., reason: _Optional[str] = ...) -> None: ...

class GetStatusRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListProcessesRequest(_message.Message):
    __slots__ = ("app", "release", "all")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    ALL_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    all: bool
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., all: _Optional[bool] = ...) -> None: ...

class Processes(_message.Message):
    __slots__ = ("version", "hostname", "mode", "started_unix_ms", "sampled_unix_ms", "figures", "root", "limits", "state_dir")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    SAMPLED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    FIGURES_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    STATE_DIR_FIELD_NUMBER: _ClassVar[int]
    version: str
    hostname: str
    mode: str
    started_unix_ms: int
    sampled_unix_ms: int
    figures: InstanceFigures
    root: Process
    limits: CgroupLimits
    state_dir: str
    def __init__(self, version: _Optional[str] = ..., hostname: _Optional[str] = ..., mode: _Optional[str] = ..., started_unix_ms: _Optional[int] = ..., sampled_unix_ms: _Optional[int] = ..., figures: _Optional[_Union[InstanceFigures, _Mapping]] = ..., root: _Optional[_Union[Process, _Mapping]] = ..., limits: _Optional[_Union[CgroupLimits, _Mapping]] = ..., state_dir: _Optional[str] = ...) -> None: ...

class CgroupLimits(_message.Message):
    __slots__ = ("cgroup", "cpu_quota", "cpus", "memory_max", "memory_used", "memory_left", "headroom", "workers_memory", "host_memory", "guard", "guard_note", "last_replaced", "last_replaced_unix_ms")
    CGROUP_FIELD_NUMBER: _ClassVar[int]
    CPU_QUOTA_FIELD_NUMBER: _ClassVar[int]
    CPUS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MAX_FIELD_NUMBER: _ClassVar[int]
    MEMORY_USED_FIELD_NUMBER: _ClassVar[int]
    MEMORY_LEFT_FIELD_NUMBER: _ClassVar[int]
    HEADROOM_FIELD_NUMBER: _ClassVar[int]
    WORKERS_MEMORY_FIELD_NUMBER: _ClassVar[int]
    HOST_MEMORY_FIELD_NUMBER: _ClassVar[int]
    GUARD_FIELD_NUMBER: _ClassVar[int]
    GUARD_NOTE_FIELD_NUMBER: _ClassVar[int]
    LAST_REPLACED_FIELD_NUMBER: _ClassVar[int]
    LAST_REPLACED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    cgroup: str
    cpu_quota: float
    cpus: int
    memory_max: int
    memory_used: int
    memory_left: int
    headroom: int
    workers_memory: int
    host_memory: int
    guard: str
    guard_note: str
    last_replaced: str
    last_replaced_unix_ms: int
    def __init__(self, cgroup: _Optional[str] = ..., cpu_quota: _Optional[float] = ..., cpus: _Optional[int] = ..., memory_max: _Optional[int] = ..., memory_used: _Optional[int] = ..., memory_left: _Optional[int] = ..., headroom: _Optional[int] = ..., workers_memory: _Optional[int] = ..., host_memory: _Optional[int] = ..., guard: _Optional[str] = ..., guard_note: _Optional[str] = ..., last_replaced: _Optional[str] = ..., last_replaced_unix_ms: _Optional[int] = ...) -> None: ...

class InstanceFigures(_message.Message):
    __slots__ = ("requests_per_second", "errors_per_second", "p50_ms", "p95_ms", "in_flight", "websockets", "connections", "tls_handshakes_per_second", "received_bytes_per_second", "sent_bytes_per_second")
    REQUESTS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    ERRORS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    P50_MS_FIELD_NUMBER: _ClassVar[int]
    P95_MS_FIELD_NUMBER: _ClassVar[int]
    IN_FLIGHT_FIELD_NUMBER: _ClassVar[int]
    WEBSOCKETS_FIELD_NUMBER: _ClassVar[int]
    CONNECTIONS_FIELD_NUMBER: _ClassVar[int]
    TLS_HANDSHAKES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_BYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    SENT_BYTES_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    requests_per_second: float
    errors_per_second: float
    p50_ms: float
    p95_ms: float
    in_flight: int
    websockets: int
    connections: int
    tls_handshakes_per_second: float
    received_bytes_per_second: float
    sent_bytes_per_second: float
    def __init__(self, requests_per_second: _Optional[float] = ..., errors_per_second: _Optional[float] = ..., p50_ms: _Optional[float] = ..., p95_ms: _Optional[float] = ..., in_flight: _Optional[int] = ..., websockets: _Optional[int] = ..., connections: _Optional[int] = ..., tls_handshakes_per_second: _Optional[float] = ..., received_bytes_per_second: _Optional[float] = ..., sent_bytes_per_second: _Optional[float] = ...) -> None: ...

class Process(_message.Message):
    __slots__ = ("pid", "os_parent_pid", "role", "what", "app", "release", "group", "index", "user", "started_unix_ms", "cpu_percent", "rss_bytes", "readopted", "figures", "groups", "children", "interface", "state", "oom_score_adj")
    PID_FIELD_NUMBER: _ClassVar[int]
    OS_PARENT_PID_FIELD_NUMBER: _ClassVar[int]
    ROLE_FIELD_NUMBER: _ClassVar[int]
    WHAT_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    CPU_PERCENT_FIELD_NUMBER: _ClassVar[int]
    RSS_BYTES_FIELD_NUMBER: _ClassVar[int]
    READOPTED_FIELD_NUMBER: _ClassVar[int]
    FIGURES_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    OOM_SCORE_ADJ_FIELD_NUMBER: _ClassVar[int]
    pid: int
    os_parent_pid: int
    role: str
    what: str
    app: str
    release: str
    group: str
    index: int
    user: str
    started_unix_ms: int
    cpu_percent: float
    rss_bytes: int
    readopted: bool
    figures: Figures
    groups: _containers.RepeatedCompositeFieldContainer[GroupFigures]
    children: _containers.RepeatedCompositeFieldContainer[Process]
    interface: str
    state: str
    oom_score_adj: int
    def __init__(self, pid: _Optional[int] = ..., os_parent_pid: _Optional[int] = ..., role: _Optional[str] = ..., what: _Optional[str] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., group: _Optional[str] = ..., index: _Optional[int] = ..., user: _Optional[str] = ..., started_unix_ms: _Optional[int] = ..., cpu_percent: _Optional[float] = ..., rss_bytes: _Optional[int] = ..., readopted: _Optional[bool] = ..., figures: _Optional[_Union[Figures, _Mapping]] = ..., groups: _Optional[_Iterable[_Union[GroupFigures, _Mapping]]] = ..., children: _Optional[_Iterable[_Union[Process, _Mapping]]] = ..., interface: _Optional[str] = ..., state: _Optional[str] = ..., oom_score_adj: _Optional[int] = ...) -> None: ...

class Figures(_message.Message):
    __slots__ = ("requests_per_second", "busy", "slots", "queue", "p95_ms", "gil_wait_p95_ms", "loop_lag_p95_ms", "departed")
    REQUESTS_PER_SECOND_FIELD_NUMBER: _ClassVar[int]
    BUSY_FIELD_NUMBER: _ClassVar[int]
    SLOTS_FIELD_NUMBER: _ClassVar[int]
    QUEUE_FIELD_NUMBER: _ClassVar[int]
    P95_MS_FIELD_NUMBER: _ClassVar[int]
    GIL_WAIT_P95_MS_FIELD_NUMBER: _ClassVar[int]
    LOOP_LAG_P95_MS_FIELD_NUMBER: _ClassVar[int]
    DEPARTED_FIELD_NUMBER: _ClassVar[int]
    requests_per_second: float
    busy: int
    slots: int
    queue: int
    p95_ms: float
    gil_wait_p95_ms: float
    loop_lag_p95_ms: float
    departed: int
    def __init__(self, requests_per_second: _Optional[float] = ..., busy: _Optional[int] = ..., slots: _Optional[int] = ..., queue: _Optional[int] = ..., p95_ms: _Optional[float] = ..., gil_wait_p95_ms: _Optional[float] = ..., loop_lag_p95_ms: _Optional[float] = ..., departed: _Optional[int] = ...) -> None: ...

class GroupFigures(_message.Message):
    __slots__ = ("group", "figures")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    FIGURES_FIELD_NUMBER: _ClassVar[int]
    group: str
    figures: Figures
    def __init__(self, group: _Optional[str] = ..., figures: _Optional[_Union[Figures, _Mapping]] = ...) -> None: ...

class Status(_message.Message):
    __slots__ = ("version", "pid", "state_dir", "run_dir", "socket", "listeners", "started_unix_ms", "app_count", "release_count", "edge_pid", "metrics", "dashboard", "budget", "websockets", "kind", "app", "release", "project", "no_host", "config", "log_dir", "cache_dir", "limits", "instance_id", "hostname", "name")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    STATE_DIR_FIELD_NUMBER: _ClassVar[int]
    RUN_DIR_FIELD_NUMBER: _ClassVar[int]
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    LISTENERS_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    APP_COUNT_FIELD_NUMBER: _ClassVar[int]
    RELEASE_COUNT_FIELD_NUMBER: _ClassVar[int]
    EDGE_PID_FIELD_NUMBER: _ClassVar[int]
    METRICS_FIELD_NUMBER: _ClassVar[int]
    DASHBOARD_FIELD_NUMBER: _ClassVar[int]
    BUDGET_FIELD_NUMBER: _ClassVar[int]
    WEBSOCKETS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    NO_HOST_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    LOG_DIR_FIELD_NUMBER: _ClassVar[int]
    CACHE_DIR_FIELD_NUMBER: _ClassVar[int]
    LIMITS_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_ID_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    version: str
    pid: int
    state_dir: str
    run_dir: str
    socket: str
    listeners: _containers.RepeatedScalarFieldContainer[str]
    started_unix_ms: int
    app_count: int
    release_count: int
    edge_pid: int
    metrics: str
    dashboard: str
    budget: str
    websockets: int
    kind: str
    app: str
    release: str
    project: str
    no_host: str
    config: str
    log_dir: str
    cache_dir: str
    limits: CgroupLimits
    instance_id: str
    hostname: str
    name: str
    def __init__(self, version: _Optional[str] = ..., pid: _Optional[int] = ..., state_dir: _Optional[str] = ..., run_dir: _Optional[str] = ..., socket: _Optional[str] = ..., listeners: _Optional[_Iterable[str]] = ..., started_unix_ms: _Optional[int] = ..., app_count: _Optional[int] = ..., release_count: _Optional[int] = ..., edge_pid: _Optional[int] = ..., metrics: _Optional[str] = ..., dashboard: _Optional[str] = ..., budget: _Optional[str] = ..., websockets: _Optional[int] = ..., kind: _Optional[str] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., project: _Optional[str] = ..., no_host: _Optional[str] = ..., config: _Optional[str] = ..., log_dir: _Optional[str] = ..., cache_dir: _Optional[str] = ..., limits: _Optional[_Union[CgroupLimits, _Mapping]] = ..., instance_id: _Optional[str] = ..., hostname: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ListWebSocketsRequest(_message.Message):
    __slots__ = ("app", "limit")
    APP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    app: str
    limit: int
    def __init__(self, app: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class WebSocketList(_message.Message):
    __slots__ = ("open", "endpoints", "sockets")
    OPEN_FIELD_NUMBER: _ClassVar[int]
    ENDPOINTS_FIELD_NUMBER: _ClassVar[int]
    SOCKETS_FIELD_NUMBER: _ClassVar[int]
    open: int
    endpoints: _containers.RepeatedCompositeFieldContainer[WebSocketEndpoint]
    sockets: _containers.RepeatedCompositeFieldContainer[OpenWebSocket]
    def __init__(self, open: _Optional[int] = ..., endpoints: _Optional[_Iterable[_Union[WebSocketEndpoint, _Mapping]]] = ..., sockets: _Optional[_Iterable[_Union[OpenWebSocket, _Mapping]]] = ...) -> None: ...

class WebSocketEndpoint(_message.Message):
    __slots__ = ("app", "pattern", "open")
    APP_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    OPEN_FIELD_NUMBER: _ClassVar[int]
    app: str
    pattern: str
    open: int
    def __init__(self, app: _Optional[str] = ..., pattern: _Optional[str] = ..., open: _Optional[int] = ...) -> None: ...

class OpenWebSocket(_message.Message):
    __slots__ = ("request_id", "client", "app", "release", "host", "group", "mount", "path", "worker", "opened_unix_ms", "received", "sent", "received_bytes", "sent_bytes")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MOUNT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    WORKER_FIELD_NUMBER: _ClassVar[int]
    OPENED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    SENT_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_BYTES_FIELD_NUMBER: _ClassVar[int]
    SENT_BYTES_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    client: str
    app: str
    release: str
    host: str
    group: str
    mount: str
    path: str
    worker: int
    opened_unix_ms: int
    received: int
    sent: int
    received_bytes: int
    sent_bytes: int
    def __init__(self, request_id: _Optional[str] = ..., client: _Optional[str] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., host: _Optional[str] = ..., group: _Optional[str] = ..., mount: _Optional[str] = ..., path: _Optional[str] = ..., worker: _Optional[int] = ..., opened_unix_ms: _Optional[int] = ..., received: _Optional[int] = ..., sent: _Optional[int] = ..., received_bytes: _Optional[int] = ..., sent_bytes: _Optional[int] = ...) -> None: ...

class GetRequestRequest(_message.Message):
    __slots__ = ("request_id",)
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    def __init__(self, request_id: _Optional[str] = ...) -> None: ...

class RequestRecord(_message.Message):
    __slots__ = ("request_id", "in_progress", "started_unix_ms", "client", "app", "release", "host", "virtual_host", "group", "mount", "snapshot", "method", "target", "version", "listener", "status", "reason", "bytes", "received", "worker", "retried", "queue_ms", "app_ms", "total_ms", "redirects", "client_class", "handoff", "connection", "request_headers", "response_headers", "compression", "panels", "worker_part", "from_worker", "captures")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    IN_PROGRESS_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    VIRTUAL_HOST_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MOUNT_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LISTENER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    WORKER_FIELD_NUMBER: _ClassVar[int]
    RETRIED_FIELD_NUMBER: _ClassVar[int]
    QUEUE_MS_FIELD_NUMBER: _ClassVar[int]
    APP_MS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MS_FIELD_NUMBER: _ClassVar[int]
    REDIRECTS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CLASS_FIELD_NUMBER: _ClassVar[int]
    HANDOFF_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_HEADERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    PANELS_FIELD_NUMBER: _ClassVar[int]
    WORKER_PART_FIELD_NUMBER: _ClassVar[int]
    FROM_WORKER_FIELD_NUMBER: _ClassVar[int]
    CAPTURES_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    in_progress: bool
    started_unix_ms: int
    client: str
    app: str
    release: str
    host: str
    virtual_host: str
    group: str
    mount: str
    snapshot: int
    method: str
    target: str
    version: str
    listener: str
    status: int
    reason: str
    bytes: int
    received: int
    worker: int
    retried: bool
    queue_ms: float
    app_ms: float
    total_ms: float
    redirects: _containers.RepeatedScalarFieldContainer[str]
    client_class: str
    handoff: str
    connection: RequestConnection
    request_headers: _containers.RepeatedCompositeFieldContainer[RecordedHeader]
    response_headers: _containers.RepeatedCompositeFieldContainer[RecordedHeader]
    compression: RequestCompression
    panels: _containers.RepeatedCompositeFieldContainer[Panel]
    worker_part: str
    from_worker: WorkerPart
    captures: _containers.RepeatedCompositeFieldContainer[RequestCapture]
    def __init__(self, request_id: _Optional[str] = ..., in_progress: _Optional[bool] = ..., started_unix_ms: _Optional[int] = ..., client: _Optional[str] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., host: _Optional[str] = ..., virtual_host: _Optional[str] = ..., group: _Optional[str] = ..., mount: _Optional[str] = ..., snapshot: _Optional[int] = ..., method: _Optional[str] = ..., target: _Optional[str] = ..., version: _Optional[str] = ..., listener: _Optional[str] = ..., status: _Optional[int] = ..., reason: _Optional[str] = ..., bytes: _Optional[int] = ..., received: _Optional[int] = ..., worker: _Optional[int] = ..., retried: _Optional[bool] = ..., queue_ms: _Optional[float] = ..., app_ms: _Optional[float] = ..., total_ms: _Optional[float] = ..., redirects: _Optional[_Iterable[str]] = ..., client_class: _Optional[str] = ..., handoff: _Optional[str] = ..., connection: _Optional[_Union[RequestConnection, _Mapping]] = ..., request_headers: _Optional[_Iterable[_Union[RecordedHeader, _Mapping]]] = ..., response_headers: _Optional[_Iterable[_Union[RecordedHeader, _Mapping]]] = ..., compression: _Optional[_Union[RequestCompression, _Mapping]] = ..., panels: _Optional[_Iterable[_Union[Panel, _Mapping]]] = ..., worker_part: _Optional[str] = ..., from_worker: _Optional[_Union[WorkerPart, _Mapping]] = ..., captures: _Optional[_Iterable[_Union[RequestCapture, _Mapping]]] = ...) -> None: ...

class RequestCapture(_message.Message):
    __slots__ = ("kind", "at_unix_ms", "message", "worker", "pid", "reason", "stack", "threads", "related")
    KIND_FIELD_NUMBER: _ClassVar[int]
    AT_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    WORKER_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    RELATED_FIELD_NUMBER: _ClassVar[int]
    kind: str
    at_unix_ms: int
    message: str
    worker: str
    pid: int
    reason: str
    stack: str
    threads: _containers.RepeatedCompositeFieldContainer[CaptureThread]
    related: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, kind: _Optional[str] = ..., at_unix_ms: _Optional[int] = ..., message: _Optional[str] = ..., worker: _Optional[str] = ..., pid: _Optional[int] = ..., reason: _Optional[str] = ..., stack: _Optional[str] = ..., threads: _Optional[_Iterable[_Union[CaptureThread, _Mapping]]] = ..., related: _Optional[_Iterable[str]] = ...) -> None: ...

class CaptureThread(_message.Message):
    __slots__ = ("name", "request_id", "stack")
    NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    STACK_FIELD_NUMBER: _ClassVar[int]
    name: str
    request_id: str
    stack: str
    def __init__(self, name: _Optional[str] = ..., request_id: _Optional[str] = ..., stack: _Optional[str] = ...) -> None: ...

class WorkerPart(_message.Message):
    __slots__ = ("thread", "to_start_response", "to_first_byte", "to_last_byte", "to_close", "body_bytes", "body_source", "sent_by_edge", "outcome", "reason", "error_phase", "error", "traceback", "logs", "logs_dropped", "thread_wait", "gil_wait", "gil_waits", "gil_wait_first", "gc", "loop_lag", "loop_lag_at", "panels", "gil_wait_stretches", "loop_held_stretches", "module_loads", "modules_loaded", "modules_ms", "import_waits")
    THREAD_FIELD_NUMBER: _ClassVar[int]
    TO_START_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    TO_FIRST_BYTE_FIELD_NUMBER: _ClassVar[int]
    TO_LAST_BYTE_FIELD_NUMBER: _ClassVar[int]
    TO_CLOSE_FIELD_NUMBER: _ClassVar[int]
    BODY_BYTES_FIELD_NUMBER: _ClassVar[int]
    BODY_SOURCE_FIELD_NUMBER: _ClassVar[int]
    SENT_BY_EDGE_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ERROR_PHASE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    TRACEBACK_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    LOGS_DROPPED_FIELD_NUMBER: _ClassVar[int]
    THREAD_WAIT_FIELD_NUMBER: _ClassVar[int]
    GIL_WAIT_FIELD_NUMBER: _ClassVar[int]
    GIL_WAITS_FIELD_NUMBER: _ClassVar[int]
    GIL_WAIT_FIRST_FIELD_NUMBER: _ClassVar[int]
    GC_FIELD_NUMBER: _ClassVar[int]
    LOOP_LAG_FIELD_NUMBER: _ClassVar[int]
    LOOP_LAG_AT_FIELD_NUMBER: _ClassVar[int]
    PANELS_FIELD_NUMBER: _ClassVar[int]
    GIL_WAIT_STRETCHES_FIELD_NUMBER: _ClassVar[int]
    LOOP_HELD_STRETCHES_FIELD_NUMBER: _ClassVar[int]
    MODULE_LOADS_FIELD_NUMBER: _ClassVar[int]
    MODULES_LOADED_FIELD_NUMBER: _ClassVar[int]
    MODULES_MS_FIELD_NUMBER: _ClassVar[int]
    IMPORT_WAITS_FIELD_NUMBER: _ClassVar[int]
    thread: str
    to_start_response: float
    to_first_byte: float
    to_last_byte: float
    to_close: float
    body_bytes: int
    body_source: str
    sent_by_edge: bool
    outcome: str
    reason: str
    error_phase: str
    error: str
    traceback: str
    logs: _containers.RepeatedCompositeFieldContainer[RequestLog]
    logs_dropped: int
    thread_wait: float
    gil_wait: float
    gil_waits: int
    gil_wait_first: float
    gc: _containers.RepeatedCompositeFieldContainer[RequestGc]
    loop_lag: float
    loop_lag_at: float
    panels: _containers.RepeatedCompositeFieldContainer[Panel]
    gil_wait_stretches: _containers.RepeatedCompositeFieldContainer[Stretch]
    loop_held_stretches: _containers.RepeatedCompositeFieldContainer[Stretch]
    module_loads: _containers.RepeatedCompositeFieldContainer[ModuleLoad]
    modules_loaded: int
    modules_ms: float
    import_waits: _containers.RepeatedCompositeFieldContainer[ImportWait]
    def __init__(self, thread: _Optional[str] = ..., to_start_response: _Optional[float] = ..., to_first_byte: _Optional[float] = ..., to_last_byte: _Optional[float] = ..., to_close: _Optional[float] = ..., body_bytes: _Optional[int] = ..., body_source: _Optional[str] = ..., sent_by_edge: _Optional[bool] = ..., outcome: _Optional[str] = ..., reason: _Optional[str] = ..., error_phase: _Optional[str] = ..., error: _Optional[str] = ..., traceback: _Optional[str] = ..., logs: _Optional[_Iterable[_Union[RequestLog, _Mapping]]] = ..., logs_dropped: _Optional[int] = ..., thread_wait: _Optional[float] = ..., gil_wait: _Optional[float] = ..., gil_waits: _Optional[int] = ..., gil_wait_first: _Optional[float] = ..., gc: _Optional[_Iterable[_Union[RequestGc, _Mapping]]] = ..., loop_lag: _Optional[float] = ..., loop_lag_at: _Optional[float] = ..., panels: _Optional[_Iterable[_Union[Panel, _Mapping]]] = ..., gil_wait_stretches: _Optional[_Iterable[_Union[Stretch, _Mapping]]] = ..., loop_held_stretches: _Optional[_Iterable[_Union[Stretch, _Mapping]]] = ..., module_loads: _Optional[_Iterable[_Union[ModuleLoad, _Mapping]]] = ..., modules_loaded: _Optional[int] = ..., modules_ms: _Optional[float] = ..., import_waits: _Optional[_Iterable[_Union[ImportWait, _Mapping]]] = ...) -> None: ...

class ModuleLoad(_message.Message):
    __slots__ = ("module", "at_ms", "ms", "depth", "trigger", "deferred")
    MODULE_FIELD_NUMBER: _ClassVar[int]
    AT_MS_FIELD_NUMBER: _ClassVar[int]
    MS_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    DEFERRED_FIELD_NUMBER: _ClassVar[int]
    module: str
    at_ms: float
    ms: float
    depth: int
    trigger: str
    deferred: bool
    def __init__(self, module: _Optional[str] = ..., at_ms: _Optional[float] = ..., ms: _Optional[float] = ..., depth: _Optional[int] = ..., trigger: _Optional[str] = ..., deferred: _Optional[bool] = ...) -> None: ...

class ImportWait(_message.Message):
    __slots__ = ("module", "at_ms", "ms", "loader")
    MODULE_FIELD_NUMBER: _ClassVar[int]
    AT_MS_FIELD_NUMBER: _ClassVar[int]
    MS_FIELD_NUMBER: _ClassVar[int]
    LOADER_FIELD_NUMBER: _ClassVar[int]
    module: str
    at_ms: float
    ms: float
    loader: str
    def __init__(self, module: _Optional[str] = ..., at_ms: _Optional[float] = ..., ms: _Optional[float] = ..., loader: _Optional[str] = ...) -> None: ...

class Stretch(_message.Message):
    __slots__ = ("at_ms", "ms")
    AT_MS_FIELD_NUMBER: _ClassVar[int]
    MS_FIELD_NUMBER: _ClassVar[int]
    at_ms: float
    ms: float
    def __init__(self, at_ms: _Optional[float] = ..., ms: _Optional[float] = ...) -> None: ...

class RequestGc(_message.Message):
    __slots__ = ("generation", "collections", "ms")
    GENERATION_FIELD_NUMBER: _ClassVar[int]
    COLLECTIONS_FIELD_NUMBER: _ClassVar[int]
    MS_FIELD_NUMBER: _ClassVar[int]
    generation: str
    collections: int
    ms: float
    def __init__(self, generation: _Optional[str] = ..., collections: _Optional[int] = ..., ms: _Optional[float] = ...) -> None: ...

class RequestLog(_message.Message):
    __slots__ = ("at_ms", "level", "logger", "message")
    AT_MS_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    LOGGER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    at_ms: float
    level: str
    logger: str
    message: str
    def __init__(self, at_ms: _Optional[float] = ..., level: _Optional[str] = ..., logger: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class RequestConnection(_message.Message):
    __slots__ = ("id", "position", "idle_ms", "tls_handshake_ms", "closed_after")
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    IDLE_MS_FIELD_NUMBER: _ClassVar[int]
    TLS_HANDSHAKE_MS_FIELD_NUMBER: _ClassVar[int]
    CLOSED_AFTER_FIELD_NUMBER: _ClassVar[int]
    id: str
    position: int
    idle_ms: float
    tls_handshake_ms: float
    closed_after: bool
    def __init__(self, id: _Optional[str] = ..., position: _Optional[int] = ..., idle_ms: _Optional[float] = ..., tls_handshake_ms: _Optional[float] = ..., closed_after: _Optional[bool] = ...) -> None: ...

class RecordedHeader(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class RequestCompression(_message.Message):
    __slots__ = ("compressed", "encoding", "skipped")
    COMPRESSED_FIELD_NUMBER: _ClassVar[int]
    ENCODING_FIELD_NUMBER: _ClassVar[int]
    SKIPPED_FIELD_NUMBER: _ClassVar[int]
    compressed: bool
    encoding: str
    skipped: str
    def __init__(self, compressed: _Optional[bool] = ..., encoding: _Optional[str] = ..., skipped: _Optional[str] = ...) -> None: ...

class Panel(_message.Message):
    __slots__ = ("name", "title", "spans", "values", "tables", "dropped", "text", "markdown")
    NAME_FIELD_NUMBER: _ClassVar[int]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    SPANS_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    TABLES_FIELD_NUMBER: _ClassVar[int]
    DROPPED_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    MARKDOWN_FIELD_NUMBER: _ClassVar[int]
    name: str
    title: str
    spans: _containers.RepeatedCompositeFieldContainer[PanelSpan]
    values: _containers.RepeatedCompositeFieldContainer[PanelValue]
    tables: _containers.RepeatedCompositeFieldContainer[PanelTable]
    dropped: int
    text: str
    markdown: bool
    def __init__(self, name: _Optional[str] = ..., title: _Optional[str] = ..., spans: _Optional[_Iterable[_Union[PanelSpan, _Mapping]]] = ..., values: _Optional[_Iterable[_Union[PanelValue, _Mapping]]] = ..., tables: _Optional[_Iterable[_Union[PanelTable, _Mapping]]] = ..., dropped: _Optional[int] = ..., text: _Optional[str] = ..., markdown: _Optional[bool] = ...) -> None: ...

class PanelSpan(_message.Message):
    __slots__ = ("name", "start_ms", "duration_ms", "category", "children", "failed", "at_ms", "segments")
    NAME_FIELD_NUMBER: _ClassVar[int]
    START_MS_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    CATEGORY_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    FAILED_FIELD_NUMBER: _ClassVar[int]
    AT_MS_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    start_ms: float
    duration_ms: float
    category: str
    children: _containers.RepeatedCompositeFieldContainer[PanelSpan]
    failed: bool
    at_ms: float
    segments: _containers.RepeatedCompositeFieldContainer[PanelSegment]
    def __init__(self, name: _Optional[str] = ..., start_ms: _Optional[float] = ..., duration_ms: _Optional[float] = ..., category: _Optional[str] = ..., children: _Optional[_Iterable[_Union[PanelSpan, _Mapping]]] = ..., failed: _Optional[bool] = ..., at_ms: _Optional[float] = ..., segments: _Optional[_Iterable[_Union[PanelSegment, _Mapping]]] = ...) -> None: ...

class PanelSegment(_message.Message):
    __slots__ = ("start_ms", "duration_ms", "label", "detail")
    START_MS_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    LABEL_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    start_ms: float
    duration_ms: float
    label: str
    detail: str
    def __init__(self, start_ms: _Optional[float] = ..., duration_ms: _Optional[float] = ..., label: _Optional[str] = ..., detail: _Optional[str] = ...) -> None: ...

class PanelValue(_message.Message):
    __slots__ = ("name", "value")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...

class PanelTable(_message.Message):
    __slots__ = ("caption", "columns", "rows")
    CAPTION_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    caption: str
    columns: _containers.RepeatedScalarFieldContainer[str]
    rows: _containers.RepeatedCompositeFieldContainer[PanelRow]
    def __init__(self, caption: _Optional[str] = ..., columns: _Optional[_Iterable[str]] = ..., rows: _Optional[_Iterable[_Union[PanelRow, _Mapping]]] = ...) -> None: ...

class PanelRow(_message.Message):
    __slots__ = ("cells",)
    CELLS_FIELD_NUMBER: _ClassVar[int]
    cells: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, cells: _Optional[_Iterable[str]] = ...) -> None: ...

class ListRequestsRequest(_message.Message):
    __slots__ = ("app", "limit")
    APP_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    app: str
    limit: int
    def __init__(self, app: _Optional[str] = ..., limit: _Optional[int] = ...) -> None: ...

class RequestList(_message.Message):
    __slots__ = ("in_flight", "groups", "requests")
    IN_FLIGHT_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    in_flight: int
    groups: _containers.RepeatedCompositeFieldContainer[RequestGroup]
    requests: _containers.RepeatedCompositeFieldContainer[InFlightRequest]
    def __init__(self, in_flight: _Optional[int] = ..., groups: _Optional[_Iterable[_Union[RequestGroup, _Mapping]]] = ..., requests: _Optional[_Iterable[_Union[InFlightRequest, _Mapping]]] = ...) -> None: ...

class RequestGroup(_message.Message):
    __slots__ = ("app", "release", "group", "queued", "queued_oldest_ms", "threads", "threads_busy", "threads_of", "threads_oldest_ms", "event_loop", "event_loop_busy", "event_loop_oldest_ms")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    QUEUED_FIELD_NUMBER: _ClassVar[int]
    QUEUED_OLDEST_MS_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    THREADS_BUSY_FIELD_NUMBER: _ClassVar[int]
    THREADS_OF_FIELD_NUMBER: _ClassVar[int]
    THREADS_OLDEST_MS_FIELD_NUMBER: _ClassVar[int]
    EVENT_LOOP_FIELD_NUMBER: _ClassVar[int]
    EVENT_LOOP_BUSY_FIELD_NUMBER: _ClassVar[int]
    EVENT_LOOP_OLDEST_MS_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    group: str
    queued: int
    queued_oldest_ms: int
    threads: bool
    threads_busy: int
    threads_of: int
    threads_oldest_ms: int
    event_loop: bool
    event_loop_busy: int
    event_loop_oldest_ms: int
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., group: _Optional[str] = ..., queued: _Optional[int] = ..., queued_oldest_ms: _Optional[int] = ..., threads: _Optional[bool] = ..., threads_busy: _Optional[int] = ..., threads_of: _Optional[int] = ..., threads_oldest_ms: _Optional[int] = ..., event_loop: _Optional[bool] = ..., event_loop_busy: _Optional[int] = ..., event_loop_oldest_ms: _Optional[int] = ...) -> None: ...

class InFlightRequest(_message.Message):
    __slots__ = ("request_id", "client", "app", "release", "group", "method", "target", "state", "kind", "worker", "started_unix_ms", "age_ms")
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    CLIENT_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    WORKER_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    AGE_MS_FIELD_NUMBER: _ClassVar[int]
    request_id: str
    client: str
    app: str
    release: str
    group: str
    method: str
    target: str
    state: str
    kind: str
    worker: int
    started_unix_ms: int
    age_ms: int
    def __init__(self, request_id: _Optional[str] = ..., client: _Optional[str] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., group: _Optional[str] = ..., method: _Optional[str] = ..., target: _Optional[str] = ..., state: _Optional[str] = ..., kind: _Optional[str] = ..., worker: _Optional[int] = ..., started_unix_ms: _Optional[int] = ..., age_ms: _Optional[int] = ...) -> None: ...

class ListAppsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListAppsResponse(_message.Message):
    __slots__ = ("apps",)
    APPS_FIELD_NUMBER: _ClassVar[int]
    apps: _containers.RepeatedCompositeFieldContainer[App]
    def __init__(self, apps: _Optional[_Iterable[_Union[App, _Mapping]]] = ...) -> None: ...

class GetAppRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class App(_message.Message):
    __slots__ = ("name", "current_release", "previous_release", "resource_version", "created_unix_ms", "user", "group", "umask", "maintenance", "priority", "maintenance_overlay")
    NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_RELEASE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_RELEASE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
    CREATED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    USER_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    UMASK_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_OVERLAY_FIELD_NUMBER: _ClassVar[int]
    name: str
    current_release: str
    previous_release: str
    resource_version: int
    created_unix_ms: int
    user: str
    group: str
    umask: str
    maintenance: bool
    priority: int
    maintenance_overlay: str
    def __init__(self, name: _Optional[str] = ..., current_release: _Optional[str] = ..., previous_release: _Optional[str] = ..., resource_version: _Optional[int] = ..., created_unix_ms: _Optional[int] = ..., user: _Optional[str] = ..., group: _Optional[str] = ..., umask: _Optional[str] = ..., maintenance: _Optional[bool] = ..., priority: _Optional[int] = ..., maintenance_overlay: _Optional[str] = ...) -> None: ...

class DeployRequest(_message.Message):
    __slots__ = ("app", "source", "entrypoint", "interface", "python", "processes", "threads", "sync_threads", "concurrency", "preload", "hooks", "factory", "factory_phase", "release", "wait", "retain_ms", "max_requests", "max_lifetime_ms", "hard_timeout_ms", "hard_drain_grace_ms", "shutdown_timeout_ms", "memory_measure", "memory_soft_limit", "memory_soft_for_ms", "memory_reclaim_first", "memory_hard_limit", "memory_check_interval_ms", "env", "hold", "soft_timeout_ms", "accel_redirect", "cgi_local_redirect", "kind", "profile", "command", "bind", "instances", "readiness_path", "readiness_timeout_ms", "stop_signal", "sendfile_roots", "sendfile_header", "override_freeze", "reflection", "loop_stall_timeout_ms", "retain_workers", "grpc_web_origins", "websocket_drain_grace_ms", "gil_stall_timeout_ms", "fresh", "static_dirs", "build_when", "build_extras", "build_groups", "bytecode", "handoff", "build_source_builds", "build_compile_bytecode", "exit_grace_ms")
    APP_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ENTRYPOINT_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    PYTHON_FIELD_NUMBER: _ClassVar[int]
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    SYNC_THREADS_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    PRELOAD_FIELD_NUMBER: _ClassVar[int]
    HOOKS_FIELD_NUMBER: _ClassVar[int]
    FACTORY_FIELD_NUMBER: _ClassVar[int]
    FACTORY_PHASE_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    WAIT_FIELD_NUMBER: _ClassVar[int]
    RETAIN_MS_FIELD_NUMBER: _ClassVar[int]
    MAX_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    MAX_LIFETIME_MS_FIELD_NUMBER: _ClassVar[int]
    HARD_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    HARD_DRAIN_GRACE_MS_FIELD_NUMBER: _ClassVar[int]
    SHUTDOWN_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_MEASURE_FIELD_NUMBER: _ClassVar[int]
    MEMORY_SOFT_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_SOFT_FOR_MS_FIELD_NUMBER: _ClassVar[int]
    MEMORY_RECLAIM_FIRST_FIELD_NUMBER: _ClassVar[int]
    MEMORY_HARD_LIMIT_FIELD_NUMBER: _ClassVar[int]
    MEMORY_CHECK_INTERVAL_MS_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    HOLD_FIELD_NUMBER: _ClassVar[int]
    SOFT_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    ACCEL_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    CGI_LOCAL_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    BIND_FIELD_NUMBER: _ClassVar[int]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    READINESS_PATH_FIELD_NUMBER: _ClassVar[int]
    READINESS_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    STOP_SIGNAL_FIELD_NUMBER: _ClassVar[int]
    SENDFILE_ROOTS_FIELD_NUMBER: _ClassVar[int]
    SENDFILE_HEADER_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FREEZE_FIELD_NUMBER: _ClassVar[int]
    REFLECTION_FIELD_NUMBER: _ClassVar[int]
    LOOP_STALL_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    RETAIN_WORKERS_FIELD_NUMBER: _ClassVar[int]
    GRPC_WEB_ORIGINS_FIELD_NUMBER: _ClassVar[int]
    WEBSOCKET_DRAIN_GRACE_MS_FIELD_NUMBER: _ClassVar[int]
    GIL_STALL_TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    FRESH_FIELD_NUMBER: _ClassVar[int]
    STATIC_DIRS_FIELD_NUMBER: _ClassVar[int]
    BUILD_WHEN_FIELD_NUMBER: _ClassVar[int]
    BUILD_EXTRAS_FIELD_NUMBER: _ClassVar[int]
    BUILD_GROUPS_FIELD_NUMBER: _ClassVar[int]
    BYTECODE_FIELD_NUMBER: _ClassVar[int]
    HANDOFF_FIELD_NUMBER: _ClassVar[int]
    BUILD_SOURCE_BUILDS_FIELD_NUMBER: _ClassVar[int]
    BUILD_COMPILE_BYTECODE_FIELD_NUMBER: _ClassVar[int]
    EXIT_GRACE_MS_FIELD_NUMBER: _ClassVar[int]
    app: str
    source: str
    entrypoint: str
    interface: str
    python: str
    processes: int
    threads: int
    sync_threads: int
    concurrency: int
    preload: str
    hooks: str
    factory: bool
    factory_phase: str
    release: str
    wait: bool
    retain_ms: int
    max_requests: int
    max_lifetime_ms: int
    hard_timeout_ms: int
    hard_drain_grace_ms: int
    shutdown_timeout_ms: int
    memory_measure: str
    memory_soft_limit: int
    memory_soft_for_ms: int
    memory_reclaim_first: bool
    memory_hard_limit: int
    memory_check_interval_ms: int
    env: _containers.RepeatedCompositeFieldContainer[EnvEntry]
    hold: bool
    soft_timeout_ms: int
    accel_redirect: bool
    cgi_local_redirect: bool
    kind: str
    profile: str
    command: _containers.RepeatedScalarFieldContainer[str]
    bind: str
    instances: int
    readiness_path: str
    readiness_timeout_ms: int
    stop_signal: str
    sendfile_roots: _containers.RepeatedScalarFieldContainer[str]
    sendfile_header: str
    override_freeze: bool
    reflection: bool
    loop_stall_timeout_ms: int
    retain_workers: int
    grpc_web_origins: _containers.RepeatedScalarFieldContainer[str]
    websocket_drain_grace_ms: int
    gil_stall_timeout_ms: int
    fresh: bool
    static_dirs: _containers.RepeatedCompositeFieldContainer[StaticDir]
    build_when: str
    build_extras: _containers.RepeatedScalarFieldContainer[str]
    build_groups: _containers.RepeatedScalarFieldContainer[str]
    bytecode: str
    handoff: str
    build_source_builds: bool
    build_compile_bytecode: bool
    exit_grace_ms: int
    def __init__(self, app: _Optional[str] = ..., source: _Optional[str] = ..., entrypoint: _Optional[str] = ..., interface: _Optional[str] = ..., python: _Optional[str] = ..., processes: _Optional[int] = ..., threads: _Optional[int] = ..., sync_threads: _Optional[int] = ..., concurrency: _Optional[int] = ..., preload: _Optional[str] = ..., hooks: _Optional[str] = ..., factory: _Optional[bool] = ..., factory_phase: _Optional[str] = ..., release: _Optional[str] = ..., wait: _Optional[bool] = ..., retain_ms: _Optional[int] = ..., max_requests: _Optional[int] = ..., max_lifetime_ms: _Optional[int] = ..., hard_timeout_ms: _Optional[int] = ..., hard_drain_grace_ms: _Optional[int] = ..., shutdown_timeout_ms: _Optional[int] = ..., memory_measure: _Optional[str] = ..., memory_soft_limit: _Optional[int] = ..., memory_soft_for_ms: _Optional[int] = ..., memory_reclaim_first: _Optional[bool] = ..., memory_hard_limit: _Optional[int] = ..., memory_check_interval_ms: _Optional[int] = ..., env: _Optional[_Iterable[_Union[EnvEntry, _Mapping]]] = ..., hold: _Optional[bool] = ..., soft_timeout_ms: _Optional[int] = ..., accel_redirect: _Optional[bool] = ..., cgi_local_redirect: _Optional[bool] = ..., kind: _Optional[str] = ..., profile: _Optional[str] = ..., command: _Optional[_Iterable[str]] = ..., bind: _Optional[str] = ..., instances: _Optional[int] = ..., readiness_path: _Optional[str] = ..., readiness_timeout_ms: _Optional[int] = ..., stop_signal: _Optional[str] = ..., sendfile_roots: _Optional[_Iterable[str]] = ..., sendfile_header: _Optional[str] = ..., override_freeze: _Optional[bool] = ..., reflection: _Optional[bool] = ..., loop_stall_timeout_ms: _Optional[int] = ..., retain_workers: _Optional[int] = ..., grpc_web_origins: _Optional[_Iterable[str]] = ..., websocket_drain_grace_ms: _Optional[int] = ..., gil_stall_timeout_ms: _Optional[int] = ..., fresh: _Optional[bool] = ..., static_dirs: _Optional[_Iterable[_Union[StaticDir, _Mapping]]] = ..., build_when: _Optional[str] = ..., build_extras: _Optional[_Iterable[str]] = ..., build_groups: _Optional[_Iterable[str]] = ..., bytecode: _Optional[str] = ..., handoff: _Optional[str] = ..., build_source_builds: _Optional[bool] = ..., build_compile_bytecode: _Optional[bool] = ..., exit_grace_ms: _Optional[int] = ...) -> None: ...

class DeployPlan(_message.Message):
    __slots__ = ("app", "release", "new_app", "description", "settings", "builds", "serving", "settings_from", "hold", "retain_ms", "retain_workers", "refusals", "retained", "env")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    NEW_APP_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FIELD_NUMBER: _ClassVar[int]
    BUILDS_FIELD_NUMBER: _ClassVar[int]
    SERVING_FIELD_NUMBER: _ClassVar[int]
    SETTINGS_FROM_FIELD_NUMBER: _ClassVar[int]
    HOLD_FIELD_NUMBER: _ClassVar[int]
    RETAIN_MS_FIELD_NUMBER: _ClassVar[int]
    RETAIN_WORKERS_FIELD_NUMBER: _ClassVar[int]
    REFUSALS_FIELD_NUMBER: _ClassVar[int]
    RETAINED_FIELD_NUMBER: _ClassVar[int]
    ENV_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    new_app: bool
    description: str
    settings: _containers.RepeatedCompositeFieldContainer[DeploySetting]
    builds: bool
    serving: str
    settings_from: str
    hold: bool
    retain_ms: int
    retain_workers: int
    refusals: _containers.RepeatedScalarFieldContainer[str]
    retained: str
    env: _containers.RepeatedCompositeFieldContainer[DeployEnv]
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., new_app: _Optional[bool] = ..., description: _Optional[str] = ..., settings: _Optional[_Iterable[_Union[DeploySetting, _Mapping]]] = ..., builds: _Optional[bool] = ..., serving: _Optional[str] = ..., settings_from: _Optional[str] = ..., hold: _Optional[bool] = ..., retain_ms: _Optional[int] = ..., retain_workers: _Optional[int] = ..., refusals: _Optional[_Iterable[str]] = ..., retained: _Optional[str] = ..., env: _Optional[_Iterable[_Union[DeployEnv, _Mapping]]] = ...) -> None: ...

class DeployEnv(_message.Message):
    __slots__ = ("name", "secret", "as_file", "layer")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    AS_FILE_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    name: str
    secret: str
    as_file: bool
    layer: str
    def __init__(self, name: _Optional[str] = ..., secret: _Optional[str] = ..., as_file: _Optional[bool] = ..., layer: _Optional[str] = ...) -> None: ...

class DeploySetting(_message.Message):
    __slots__ = ("key", "value", "layer")
    KEY_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    key: str
    value: str
    layer: str
    def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ..., layer: _Optional[str] = ...) -> None: ...

class StaticDir(_message.Message):
    __slots__ = ("path", "dir")
    PATH_FIELD_NUMBER: _ClassVar[int]
    DIR_FIELD_NUMBER: _ClassVar[int]
    path: str
    dir: str
    def __init__(self, path: _Optional[str] = ..., dir: _Optional[str] = ...) -> None: ...

class EnvEntry(_message.Message):
    __slots__ = ("name", "value", "secret_store", "secret_key", "as_file")
    NAME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    SECRET_STORE_FIELD_NUMBER: _ClassVar[int]
    SECRET_KEY_FIELD_NUMBER: _ClassVar[int]
    AS_FILE_FIELD_NUMBER: _ClassVar[int]
    name: str
    value: str
    secret_store: str
    secret_key: str
    as_file: bool
    def __init__(self, name: _Optional[str] = ..., value: _Optional[str] = ..., secret_store: _Optional[str] = ..., secret_key: _Optional[str] = ..., as_file: _Optional[bool] = ...) -> None: ...

class ListReleasesRequest(_message.Message):
    __slots__ = ("app", "disk")
    APP_FIELD_NUMBER: _ClassVar[int]
    DISK_FIELD_NUMBER: _ClassVar[int]
    app: str
    disk: bool
    def __init__(self, app: _Optional[str] = ..., disk: _Optional[bool] = ...) -> None: ...

class ListReleasesResponse(_message.Message):
    __slots__ = ("releases",)
    RELEASES_FIELD_NUMBER: _ClassVar[int]
    releases: _containers.RepeatedCompositeFieldContainer[Release]
    def __init__(self, releases: _Optional[_Iterable[_Union[Release, _Mapping]]] = ...) -> None: ...

class GetReleaseRequest(_message.Message):
    __slots__ = ("app", "release")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ...) -> None: ...

class WaitReleaseRequest(_message.Message):
    __slots__ = ("app", "release", "states", "timeout_ms")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    STATES_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_MS_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    states: _containers.RepeatedScalarFieldContainer[str]
    timeout_ms: int
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., states: _Optional[_Iterable[str]] = ..., timeout_ms: _Optional[int] = ...) -> None: ...

class RollbackRequest(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: str
    def __init__(self, app: _Optional[str] = ...) -> None: ...

class DrainReleaseRequest(_message.Message):
    __slots__ = ("app", "release")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ...) -> None: ...

class PruneReleasesRequest(_message.Message):
    __slots__ = ("app", "keep", "force", "keep_logs", "dry_run")
    APP_FIELD_NUMBER: _ClassVar[int]
    KEEP_FIELD_NUMBER: _ClassVar[int]
    FORCE_FIELD_NUMBER: _ClassVar[int]
    KEEP_LOGS_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    app: str
    keep: int
    force: bool
    keep_logs: bool
    dry_run: bool
    def __init__(self, app: _Optional[str] = ..., keep: _Optional[int] = ..., force: _Optional[bool] = ..., keep_logs: _Optional[bool] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class RemoveAppRequest(_message.Message):
    __slots__ = ("app", "dry_run", "data")
    APP_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    app: str
    dry_run: bool
    data: bool
    def __init__(self, app: _Optional[str] = ..., dry_run: _Optional[bool] = ..., data: _Optional[bool] = ...) -> None: ...

class GetAppDataRequest(_message.Message):
    __slots__ = ("app", "sizes")
    APP_FIELD_NUMBER: _ClassVar[int]
    SIZES_FIELD_NUMBER: _ClassVar[int]
    app: str
    sizes: bool
    def __init__(self, app: _Optional[str] = ..., sizes: _Optional[bool] = ...) -> None: ...

class DataPart(_message.Message):
    __slots__ = ("name", "path", "resolved", "exists", "owner_uid", "owner", "mode", "filesystem", "network", "root", "bytes")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_FIELD_NUMBER: _ClassVar[int]
    EXISTS_FIELD_NUMBER: _ClassVar[int]
    OWNER_UID_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    FILESYSTEM_FIELD_NUMBER: _ClassVar[int]
    NETWORK_FIELD_NUMBER: _ClassVar[int]
    ROOT_FIELD_NUMBER: _ClassVar[int]
    BYTES_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    resolved: str
    exists: bool
    owner_uid: int
    owner: str
    mode: int
    filesystem: str
    network: bool
    root: bool
    bytes: int
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., resolved: _Optional[str] = ..., exists: _Optional[bool] = ..., owner_uid: _Optional[int] = ..., owner: _Optional[str] = ..., mode: _Optional[int] = ..., filesystem: _Optional[str] = ..., network: _Optional[bool] = ..., root: _Optional[bool] = ..., bytes: _Optional[int] = ...) -> None: ...

class AppData(_message.Message):
    __slots__ = ("app", "parts", "expected_uid", "expected_owner", "spool", "spool_shared", "warnings", "none")
    APP_FIELD_NUMBER: _ClassVar[int]
    PARTS_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_UID_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_OWNER_FIELD_NUMBER: _ClassVar[int]
    SPOOL_FIELD_NUMBER: _ClassVar[int]
    SPOOL_SHARED_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    NONE_FIELD_NUMBER: _ClassVar[int]
    app: str
    parts: _containers.RepeatedCompositeFieldContainer[DataPart]
    expected_uid: int
    expected_owner: str
    spool: str
    spool_shared: bool
    warnings: _containers.RepeatedScalarFieldContainer[str]
    none: str
    def __init__(self, app: _Optional[str] = ..., parts: _Optional[_Iterable[_Union[DataPart, _Mapping]]] = ..., expected_uid: _Optional[int] = ..., expected_owner: _Optional[str] = ..., spool: _Optional[str] = ..., spool_shared: _Optional[bool] = ..., warnings: _Optional[_Iterable[str]] = ..., none: _Optional[str] = ...) -> None: ...

class RemoveReleaseRequest(_message.Message):
    __slots__ = ("app", "release", "keep_logs", "dry_run")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    KEEP_LOGS_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    keep_logs: bool
    dry_run: bool
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., keep_logs: _Optional[bool] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class RemovedRelease(_message.Message):
    __slots__ = ("app", "id", "state", "created_unix_ms", "disk_bytes", "why", "error")
    APP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    CREATED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    DISK_BYTES_FIELD_NUMBER: _ClassVar[int]
    WHY_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    app: str
    id: str
    state: str
    created_unix_ms: int
    disk_bytes: int
    why: str
    error: str
    def __init__(self, app: _Optional[str] = ..., id: _Optional[str] = ..., state: _Optional[str] = ..., created_unix_ms: _Optional[int] = ..., disk_bytes: _Optional[int] = ..., why: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class KeptRelease(_message.Message):
    __slots__ = ("app", "id", "state", "why")
    APP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    WHY_FIELD_NUMBER: _ClassVar[int]
    app: str
    id: str
    state: str
    why: str
    def __init__(self, app: _Optional[str] = ..., id: _Optional[str] = ..., state: _Optional[str] = ..., why: _Optional[str] = ...) -> None: ...

class RemoveReleasesResponse(_message.Message):
    __slots__ = ("removed", "kept", "freed", "dry_run", "data_dir", "data_removed", "data_kept")
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    KEPT_FIELD_NUMBER: _ClassVar[int]
    FREED_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    DATA_DIR_FIELD_NUMBER: _ClassVar[int]
    DATA_REMOVED_FIELD_NUMBER: _ClassVar[int]
    DATA_KEPT_FIELD_NUMBER: _ClassVar[int]
    removed: _containers.RepeatedCompositeFieldContainer[RemovedRelease]
    kept: _containers.RepeatedCompositeFieldContainer[KeptRelease]
    freed: int
    dry_run: bool
    data_dir: str
    data_removed: bool
    data_kept: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, removed: _Optional[_Iterable[_Union[RemovedRelease, _Mapping]]] = ..., kept: _Optional[_Iterable[_Union[KeptRelease, _Mapping]]] = ..., freed: _Optional[int] = ..., dry_run: _Optional[bool] = ..., data_dir: _Optional[str] = ..., data_removed: _Optional[bool] = ..., data_kept: _Optional[_Iterable[str]] = ...) -> None: ...

class StartRolloutRequest(_message.Message):
    __slots__ = ("app", "release", "steps", "max_error_rate", "max_p95_ms", "min_requests", "approve_each_step", "override_freeze", "max_p99_ms", "max_worker_faults", "max_queue_wait_p95_ms", "probes")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    MAX_ERROR_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_P95_MS_FIELD_NUMBER: _ClassVar[int]
    MIN_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    APPROVE_EACH_STEP_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FREEZE_FIELD_NUMBER: _ClassVar[int]
    MAX_P99_MS_FIELD_NUMBER: _ClassVar[int]
    MAX_WORKER_FAULTS_FIELD_NUMBER: _ClassVar[int]
    MAX_QUEUE_WAIT_P95_MS_FIELD_NUMBER: _ClassVar[int]
    PROBES_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    steps: _containers.RepeatedCompositeFieldContainer[RolloutStep]
    max_error_rate: float
    max_p95_ms: int
    min_requests: int
    approve_each_step: bool
    override_freeze: bool
    max_p99_ms: int
    max_worker_faults: int
    max_queue_wait_p95_ms: int
    probes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[RolloutStep, _Mapping]]] = ..., max_error_rate: _Optional[float] = ..., max_p95_ms: _Optional[int] = ..., min_requests: _Optional[int] = ..., approve_each_step: _Optional[bool] = ..., override_freeze: _Optional[bool] = ..., max_p99_ms: _Optional[int] = ..., max_worker_faults: _Optional[int] = ..., max_queue_wait_p95_ms: _Optional[int] = ..., probes: _Optional[_Iterable[str]] = ...) -> None: ...

class RolloutStep(_message.Message):
    __slots__ = ("percent", "hold_ms")
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    HOLD_MS_FIELD_NUMBER: _ClassVar[int]
    percent: int
    hold_ms: int
    def __init__(self, percent: _Optional[int] = ..., hold_ms: _Optional[int] = ...) -> None: ...

class Rollout(_message.Message):
    __slots__ = ("app", "id", "candidate", "baseline", "steps", "state", "step", "percent", "message", "created_unix_ms", "updated_unix_ms", "max_error_rate", "max_p95_ms", "min_requests", "approve_each_step", "max_p99_ms", "max_worker_faults", "max_queue_wait_p95_ms", "probes")
    APP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_FIELD_NUMBER: _ClassVar[int]
    BASELINE_FIELD_NUMBER: _ClassVar[int]
    STEPS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    CREATED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    UPDATED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    MAX_ERROR_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_P95_MS_FIELD_NUMBER: _ClassVar[int]
    MIN_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    APPROVE_EACH_STEP_FIELD_NUMBER: _ClassVar[int]
    MAX_P99_MS_FIELD_NUMBER: _ClassVar[int]
    MAX_WORKER_FAULTS_FIELD_NUMBER: _ClassVar[int]
    MAX_QUEUE_WAIT_P95_MS_FIELD_NUMBER: _ClassVar[int]
    PROBES_FIELD_NUMBER: _ClassVar[int]
    app: str
    id: str
    candidate: str
    baseline: str
    steps: _containers.RepeatedCompositeFieldContainer[RolloutStep]
    state: str
    step: int
    percent: int
    message: str
    created_unix_ms: int
    updated_unix_ms: int
    max_error_rate: float
    max_p95_ms: int
    min_requests: int
    approve_each_step: bool
    max_p99_ms: int
    max_worker_faults: int
    max_queue_wait_p95_ms: int
    probes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app: _Optional[str] = ..., id: _Optional[str] = ..., candidate: _Optional[str] = ..., baseline: _Optional[str] = ..., steps: _Optional[_Iterable[_Union[RolloutStep, _Mapping]]] = ..., state: _Optional[str] = ..., step: _Optional[int] = ..., percent: _Optional[int] = ..., message: _Optional[str] = ..., created_unix_ms: _Optional[int] = ..., updated_unix_ms: _Optional[int] = ..., max_error_rate: _Optional[float] = ..., max_p95_ms: _Optional[int] = ..., min_requests: _Optional[int] = ..., approve_each_step: _Optional[bool] = ..., max_p99_ms: _Optional[int] = ..., max_worker_faults: _Optional[int] = ..., max_queue_wait_p95_ms: _Optional[int] = ..., probes: _Optional[_Iterable[str]] = ...) -> None: ...

class GetRolloutRequest(_message.Message):
    __slots__ = ("app", "rollout")
    APP_FIELD_NUMBER: _ClassVar[int]
    ROLLOUT_FIELD_NUMBER: _ClassVar[int]
    app: str
    rollout: str
    def __init__(self, app: _Optional[str] = ..., rollout: _Optional[str] = ...) -> None: ...

class ListRolloutsRequest(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: str
    def __init__(self, app: _Optional[str] = ...) -> None: ...

class ListRolloutsResponse(_message.Message):
    __slots__ = ("rollouts",)
    ROLLOUTS_FIELD_NUMBER: _ClassVar[int]
    rollouts: _containers.RepeatedCompositeFieldContainer[Rollout]
    def __init__(self, rollouts: _Optional[_Iterable[_Union[Rollout, _Mapping]]] = ...) -> None: ...

class RolloutControlRequest(_message.Message):
    __slots__ = ("app", "override_freeze")
    APP_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FREEZE_FIELD_NUMBER: _ClassVar[int]
    app: str
    override_freeze: bool
    def __init__(self, app: _Optional[str] = ..., override_freeze: _Optional[bool] = ...) -> None: ...

class PromoteReleaseRequest(_message.Message):
    __slots__ = ("app", "release", "override_freeze")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FREEZE_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    override_freeze: bool
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., override_freeze: _Optional[bool] = ...) -> None: ...

class SetScaleRequest(_message.Message):
    __slots__ = ("app", "release", "group", "processes", "unpin", "min_workers", "max_workers", "until_unix_ms", "cap_workers")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    UNPIN_FIELD_NUMBER: _ClassVar[int]
    MIN_WORKERS_FIELD_NUMBER: _ClassVar[int]
    MAX_WORKERS_FIELD_NUMBER: _ClassVar[int]
    UNTIL_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    CAP_WORKERS_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    group: str
    processes: int
    unpin: bool
    min_workers: int
    max_workers: int
    until_unix_ms: int
    cap_workers: int
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., group: _Optional[str] = ..., processes: _Optional[int] = ..., unpin: _Optional[bool] = ..., min_workers: _Optional[int] = ..., max_workers: _Optional[int] = ..., until_unix_ms: _Optional[int] = ..., cap_workers: _Optional[int] = ...) -> None: ...

class DashboardLoginRequest(_message.Message):
    __slots__ = ("token",)
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    token: bool
    def __init__(self, token: _Optional[bool] = ...) -> None: ...

class ApplicationUrlsRequest(_message.Message):
    __slots__ = ("app",)
    APP_FIELD_NUMBER: _ClassVar[int]
    app: str
    def __init__(self, app: _Optional[str] = ...) -> None: ...

class ApplicationUrlsResponse(_message.Message):
    __slots__ = ("app", "urls")
    APP_FIELD_NUMBER: _ClassVar[int]
    URLS_FIELD_NUMBER: _ClassVar[int]
    app: str
    urls: _containers.RepeatedCompositeFieldContainer[ApplicationUrl]
    def __init__(self, app: _Optional[str] = ..., urls: _Optional[_Iterable[_Union[ApplicationUrl, _Mapping]]] = ...) -> None: ...

class ApplicationUrl(_message.Message):
    __slots__ = ("url", "scheme", "name", "port", "path", "route", "host", "listener", "bound", "canonical", "why")
    URL_FIELD_NUMBER: _ClassVar[int]
    SCHEME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ROUTE_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    LISTENER_FIELD_NUMBER: _ClassVar[int]
    BOUND_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_FIELD_NUMBER: _ClassVar[int]
    WHY_FIELD_NUMBER: _ClassVar[int]
    url: str
    scheme: str
    name: str
    port: int
    path: str
    route: str
    host: str
    listener: str
    bound: str
    canonical: bool
    why: str
    def __init__(self, url: _Optional[str] = ..., scheme: _Optional[str] = ..., name: _Optional[str] = ..., port: _Optional[int] = ..., path: _Optional[str] = ..., route: _Optional[str] = ..., host: _Optional[str] = ..., listener: _Optional[str] = ..., bound: _Optional[str] = ..., canonical: _Optional[bool] = ..., why: _Optional[str] = ...) -> None: ...

class DashboardLoginLink(_message.Message):
    __slots__ = ("url", "expires_in_s", "code", "token")
    URL_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_S_FIELD_NUMBER: _ClassVar[int]
    CODE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    url: str
    expires_in_s: int
    code: str
    token: str
    def __init__(self, url: _Optional[str] = ..., expires_in_s: _Optional[int] = ..., code: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class SetMaintenanceRequest(_message.Message):
    __slots__ = ("app", "on", "host")
    APP_FIELD_NUMBER: _ClassVar[int]
    ON_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    app: str
    on: bool
    host: str
    def __init__(self, app: _Optional[str] = ..., on: _Optional[bool] = ..., host: _Optional[str] = ...) -> None: ...

class MaintenanceStatus(_message.Message):
    __slots__ = ("app", "on", "since_unix_ms", "host")
    APP_FIELD_NUMBER: _ClassVar[int]
    ON_FIELD_NUMBER: _ClassVar[int]
    SINCE_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    app: str
    on: bool
    since_unix_ms: int
    host: str
    def __init__(self, app: _Optional[str] = ..., on: _Optional[bool] = ..., since_unix_ms: _Optional[int] = ..., host: _Optional[str] = ...) -> None: ...

class OverrideAccessLogRequest(_message.Message):
    __slots__ = ("mode", "app", "paths", "duration_ms", "reset")
    MODE_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    RESET_FIELD_NUMBER: _ClassVar[int]
    mode: str
    app: str
    paths: _containers.RepeatedScalarFieldContainer[str]
    duration_ms: int
    reset: bool
    def __init__(self, mode: _Optional[str] = ..., app: _Optional[str] = ..., paths: _Optional[_Iterable[str]] = ..., duration_ms: _Optional[int] = ..., reset: _Optional[bool] = ...) -> None: ...

class AccessLogOverrides(_message.Message):
    __slots__ = ("overrides", "reset")
    OVERRIDES_FIELD_NUMBER: _ClassVar[int]
    RESET_FIELD_NUMBER: _ClassVar[int]
    overrides: _containers.RepeatedCompositeFieldContainer[AccessLogOverride]
    reset: int
    def __init__(self, overrides: _Optional[_Iterable[_Union[AccessLogOverride, _Mapping]]] = ..., reset: _Optional[int] = ...) -> None: ...

class AccessLogOverride(_message.Message):
    __slots__ = ("mode", "app", "paths", "until_unix_ms")
    MODE_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    UNTIL_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    mode: str
    app: str
    paths: _containers.RepeatedScalarFieldContainer[str]
    until_unix_ms: int
    def __init__(self, mode: _Optional[str] = ..., app: _Optional[str] = ..., paths: _Optional[_Iterable[str]] = ..., until_unix_ms: _Optional[int] = ...) -> None: ...

class GetScaleStatusRequest(_message.Message):
    __slots__ = ("app", "release")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ...) -> None: ...

class ScaleStatus(_message.Message):
    __slots__ = ("app", "release", "groups", "traffic")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    groups: _containers.RepeatedCompositeFieldContainer[GroupScale]
    traffic: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., groups: _Optional[_Iterable[_Union[GroupScale, _Mapping]]] = ..., traffic: _Optional[str] = ...) -> None: ...

class GroupScale(_message.Message):
    __slots__ = ("group", "mode", "min_workers", "max_workers", "desired", "ready", "pinned", "advisory", "slots_busy", "slots_total", "idle_workers", "queue_wait_p95_ms", "last_decision", "last_decision_age_ms", "reaps_last_hour", "churn_budget", "suspended", "policy", "scale_outs", "scale_ins", "floor", "ceiling", "capacity_from", "scale_in_held", "worker_cpu", "gil_wait_p95_ms", "loop_lag_p95_ms", "bottleneck", "diagnosis", "advice", "gc_share", "handoff_queue_wait_p95_ms", "cap", "cap_from")
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MIN_WORKERS_FIELD_NUMBER: _ClassVar[int]
    MAX_WORKERS_FIELD_NUMBER: _ClassVar[int]
    DESIRED_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    PINNED_FIELD_NUMBER: _ClassVar[int]
    ADVISORY_FIELD_NUMBER: _ClassVar[int]
    SLOTS_BUSY_FIELD_NUMBER: _ClassVar[int]
    SLOTS_TOTAL_FIELD_NUMBER: _ClassVar[int]
    IDLE_WORKERS_FIELD_NUMBER: _ClassVar[int]
    QUEUE_WAIT_P95_MS_FIELD_NUMBER: _ClassVar[int]
    LAST_DECISION_FIELD_NUMBER: _ClassVar[int]
    LAST_DECISION_AGE_MS_FIELD_NUMBER: _ClassVar[int]
    REAPS_LAST_HOUR_FIELD_NUMBER: _ClassVar[int]
    CHURN_BUDGET_FIELD_NUMBER: _ClassVar[int]
    SUSPENDED_FIELD_NUMBER: _ClassVar[int]
    POLICY_FIELD_NUMBER: _ClassVar[int]
    SCALE_OUTS_FIELD_NUMBER: _ClassVar[int]
    SCALE_INS_FIELD_NUMBER: _ClassVar[int]
    FLOOR_FIELD_NUMBER: _ClassVar[int]
    CEILING_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FROM_FIELD_NUMBER: _ClassVar[int]
    SCALE_IN_HELD_FIELD_NUMBER: _ClassVar[int]
    WORKER_CPU_FIELD_NUMBER: _ClassVar[int]
    GIL_WAIT_P95_MS_FIELD_NUMBER: _ClassVar[int]
    LOOP_LAG_P95_MS_FIELD_NUMBER: _ClassVar[int]
    BOTTLENECK_FIELD_NUMBER: _ClassVar[int]
    DIAGNOSIS_FIELD_NUMBER: _ClassVar[int]
    ADVICE_FIELD_NUMBER: _ClassVar[int]
    GC_SHARE_FIELD_NUMBER: _ClassVar[int]
    HANDOFF_QUEUE_WAIT_P95_MS_FIELD_NUMBER: _ClassVar[int]
    CAP_FIELD_NUMBER: _ClassVar[int]
    CAP_FROM_FIELD_NUMBER: _ClassVar[int]
    group: str
    mode: str
    min_workers: int
    max_workers: int
    desired: int
    ready: int
    pinned: bool
    advisory: bool
    slots_busy: float
    slots_total: float
    idle_workers: float
    queue_wait_p95_ms: float
    last_decision: str
    last_decision_age_ms: int
    reaps_last_hour: int
    churn_budget: int
    suspended: bool
    policy: str
    scale_outs: int
    scale_ins: int
    floor: int
    ceiling: int
    capacity_from: _containers.RepeatedScalarFieldContainer[str]
    scale_in_held: bool
    worker_cpu: float
    gil_wait_p95_ms: float
    loop_lag_p95_ms: float
    bottleneck: str
    diagnosis: str
    advice: str
    gc_share: float
    handoff_queue_wait_p95_ms: float
    cap: int
    cap_from: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, group: _Optional[str] = ..., mode: _Optional[str] = ..., min_workers: _Optional[int] = ..., max_workers: _Optional[int] = ..., desired: _Optional[int] = ..., ready: _Optional[int] = ..., pinned: _Optional[bool] = ..., advisory: _Optional[bool] = ..., slots_busy: _Optional[float] = ..., slots_total: _Optional[float] = ..., idle_workers: _Optional[float] = ..., queue_wait_p95_ms: _Optional[float] = ..., last_decision: _Optional[str] = ..., last_decision_age_ms: _Optional[int] = ..., reaps_last_hour: _Optional[int] = ..., churn_budget: _Optional[int] = ..., suspended: _Optional[bool] = ..., policy: _Optional[str] = ..., scale_outs: _Optional[int] = ..., scale_ins: _Optional[int] = ..., floor: _Optional[int] = ..., ceiling: _Optional[int] = ..., capacity_from: _Optional[_Iterable[str]] = ..., scale_in_held: _Optional[bool] = ..., worker_cpu: _Optional[float] = ..., gil_wait_p95_ms: _Optional[float] = ..., loop_lag_p95_ms: _Optional[float] = ..., bottleneck: _Optional[str] = ..., diagnosis: _Optional[str] = ..., advice: _Optional[str] = ..., gc_share: _Optional[float] = ..., handoff_queue_wait_p95_ms: _Optional[float] = ..., cap: _Optional[int] = ..., cap_from: _Optional[_Iterable[str]] = ...) -> None: ...

class Release(_message.Message):
    __slots__ = ("app", "id", "state", "message", "source", "entrypoint", "interface", "python", "processes", "threads", "sync_threads", "concurrency", "serving", "created_unix_ms", "resource_version", "workers", "retained_until_unix_ms", "kind", "profile", "instances", "command", "mounts", "groups", "detected_interface", "websockets", "python_version", "python_tag", "python_request", "environment", "build_when", "bytecode", "server_instances", "host_running", "disk_bytes", "disk_freed_bytes", "instrumentation", "gates", "traffic")
    APP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    ENTRYPOINT_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    PYTHON_FIELD_NUMBER: _ClassVar[int]
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    SYNC_THREADS_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    SERVING_FIELD_NUMBER: _ClassVar[int]
    CREATED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_VERSION_FIELD_NUMBER: _ClassVar[int]
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    RETAINED_UNTIL_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    INSTANCES_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    MOUNTS_FIELD_NUMBER: _ClassVar[int]
    GROUPS_FIELD_NUMBER: _ClassVar[int]
    DETECTED_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    WEBSOCKETS_FIELD_NUMBER: _ClassVar[int]
    PYTHON_VERSION_FIELD_NUMBER: _ClassVar[int]
    PYTHON_TAG_FIELD_NUMBER: _ClassVar[int]
    PYTHON_REQUEST_FIELD_NUMBER: _ClassVar[int]
    ENVIRONMENT_FIELD_NUMBER: _ClassVar[int]
    BUILD_WHEN_FIELD_NUMBER: _ClassVar[int]
    BYTECODE_FIELD_NUMBER: _ClassVar[int]
    SERVER_INSTANCES_FIELD_NUMBER: _ClassVar[int]
    HOST_RUNNING_FIELD_NUMBER: _ClassVar[int]
    DISK_BYTES_FIELD_NUMBER: _ClassVar[int]
    DISK_FREED_BYTES_FIELD_NUMBER: _ClassVar[int]
    INSTRUMENTATION_FIELD_NUMBER: _ClassVar[int]
    GATES_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    app: str
    id: str
    state: str
    message: str
    source: str
    entrypoint: str
    interface: str
    python: str
    processes: int
    threads: int
    sync_threads: int
    concurrency: int
    serving: bool
    created_unix_ms: int
    resource_version: int
    workers: _containers.RepeatedCompositeFieldContainer[Worker]
    retained_until_unix_ms: int
    kind: str
    profile: str
    instances: int
    command: _containers.RepeatedScalarFieldContainer[str]
    mounts: _containers.RepeatedCompositeFieldContainer[ReleaseMount]
    groups: _containers.RepeatedCompositeFieldContainer[ReleaseGroup]
    detected_interface: str
    websockets: int
    python_version: str
    python_tag: str
    python_request: str
    environment: str
    build_when: str
    bytecode: str
    server_instances: _containers.RepeatedCompositeFieldContainer[ServerInstance]
    host_running: bool
    disk_bytes: int
    disk_freed_bytes: int
    instrumentation: _containers.RepeatedScalarFieldContainer[str]
    gates: _containers.RepeatedCompositeFieldContainer[GatePassed]
    traffic: str
    def __init__(self, app: _Optional[str] = ..., id: _Optional[str] = ..., state: _Optional[str] = ..., message: _Optional[str] = ..., source: _Optional[str] = ..., entrypoint: _Optional[str] = ..., interface: _Optional[str] = ..., python: _Optional[str] = ..., processes: _Optional[int] = ..., threads: _Optional[int] = ..., sync_threads: _Optional[int] = ..., concurrency: _Optional[int] = ..., serving: _Optional[bool] = ..., created_unix_ms: _Optional[int] = ..., resource_version: _Optional[int] = ..., workers: _Optional[_Iterable[_Union[Worker, _Mapping]]] = ..., retained_until_unix_ms: _Optional[int] = ..., kind: _Optional[str] = ..., profile: _Optional[str] = ..., instances: _Optional[int] = ..., command: _Optional[_Iterable[str]] = ..., mounts: _Optional[_Iterable[_Union[ReleaseMount, _Mapping]]] = ..., groups: _Optional[_Iterable[_Union[ReleaseGroup, _Mapping]]] = ..., detected_interface: _Optional[str] = ..., websockets: _Optional[int] = ..., python_version: _Optional[str] = ..., python_tag: _Optional[str] = ..., python_request: _Optional[str] = ..., environment: _Optional[str] = ..., build_when: _Optional[str] = ..., bytecode: _Optional[str] = ..., server_instances: _Optional[_Iterable[_Union[ServerInstance, _Mapping]]] = ..., host_running: _Optional[bool] = ..., disk_bytes: _Optional[int] = ..., disk_freed_bytes: _Optional[int] = ..., instrumentation: _Optional[_Iterable[str]] = ..., gates: _Optional[_Iterable[_Union[GatePassed, _Mapping]]] = ..., traffic: _Optional[str] = ...) -> None: ...

class GatePassed(_message.Message):
    __slots__ = ("name", "stage", "run", "passed_unix_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STAGE_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    PASSED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    stage: str
    run: int
    passed_unix_ms: int
    def __init__(self, name: _Optional[str] = ..., stage: _Optional[str] = ..., run: _Optional[int] = ..., passed_unix_ms: _Optional[int] = ...) -> None: ...

class ServerInstance(_message.Message):
    __slots__ = ("index", "pid", "address", "started_unix_ms")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    index: int
    pid: int
    address: str
    started_unix_ms: int
    def __init__(self, index: _Optional[int] = ..., pid: _Optional[int] = ..., address: _Optional[str] = ..., started_unix_ms: _Optional[int] = ...) -> None: ...

class ReleaseMount(_message.Message):
    __slots__ = ("name", "path", "entrypoint", "interface", "internal", "threads", "max_threads", "detected_interface")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ENTRYPOINT_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    MAX_THREADS_FIELD_NUMBER: _ClassVar[int]
    DETECTED_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    name: str
    path: str
    entrypoint: str
    interface: str
    internal: bool
    threads: int
    max_threads: int
    detected_interface: str
    def __init__(self, name: _Optional[str] = ..., path: _Optional[str] = ..., entrypoint: _Optional[str] = ..., interface: _Optional[str] = ..., internal: _Optional[bool] = ..., threads: _Optional[int] = ..., max_threads: _Optional[int] = ..., detected_interface: _Optional[str] = ...) -> None: ...

class ReleaseGroup(_message.Message):
    __slots__ = ("name", "paths", "client_classes", "processes", "threads", "sync_threads", "concurrency", "optional", "hosts", "methods", "mounts")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATHS_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CLASSES_FIELD_NUMBER: _ClassVar[int]
    PROCESSES_FIELD_NUMBER: _ClassVar[int]
    THREADS_FIELD_NUMBER: _ClassVar[int]
    SYNC_THREADS_FIELD_NUMBER: _ClassVar[int]
    CONCURRENCY_FIELD_NUMBER: _ClassVar[int]
    OPTIONAL_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    METHODS_FIELD_NUMBER: _ClassVar[int]
    MOUNTS_FIELD_NUMBER: _ClassVar[int]
    name: str
    paths: _containers.RepeatedScalarFieldContainer[str]
    client_classes: _containers.RepeatedScalarFieldContainer[str]
    processes: int
    threads: int
    sync_threads: int
    concurrency: int
    optional: bool
    hosts: _containers.RepeatedScalarFieldContainer[str]
    methods: _containers.RepeatedScalarFieldContainer[str]
    mounts: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, name: _Optional[str] = ..., paths: _Optional[_Iterable[str]] = ..., client_classes: _Optional[_Iterable[str]] = ..., processes: _Optional[int] = ..., threads: _Optional[int] = ..., sync_threads: _Optional[int] = ..., concurrency: _Optional[int] = ..., optional: _Optional[bool] = ..., hosts: _Optional[_Iterable[str]] = ..., methods: _Optional[_Iterable[str]] = ..., mounts: _Optional[_Iterable[str]] = ...) -> None: ...

class Worker(_message.Message):
    __slots__ = ("index", "pid", "socket", "group", "state")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    SOCKET_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    index: int
    pid: int
    socket: str
    group: str
    state: str
    def __init__(self, index: _Optional[int] = ..., pid: _Optional[int] = ..., socket: _Optional[str] = ..., group: _Optional[str] = ..., state: _Optional[str] = ...) -> None: ...

class ListEventsRequest(_message.Message):
    __slots__ = ("after", "limit")
    AFTER_FIELD_NUMBER: _ClassVar[int]
    LIMIT_FIELD_NUMBER: _ClassVar[int]
    after: int
    limit: int
    def __init__(self, after: _Optional[int] = ..., limit: _Optional[int] = ...) -> None: ...

class ListEventsResponse(_message.Message):
    __slots__ = ("events",)
    EVENTS_FIELD_NUMBER: _ClassVar[int]
    events: _containers.RepeatedCompositeFieldContainer[Event]
    def __init__(self, events: _Optional[_Iterable[_Union[Event, _Mapping]]] = ...) -> None: ...

class WatchEventsRequest(_message.Message):
    __slots__ = ("after",)
    AFTER_FIELD_NUMBER: _ClassVar[int]
    after: int
    def __init__(self, after: _Optional[int] = ...) -> None: ...

class Event(_message.Message):
    __slots__ = ("sequence", "time_unix_ms", "type", "subject", "level", "message")
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    TIME_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sequence: int
    time_unix_ms: int
    type: str
    subject: str
    level: str
    message: str
    def __init__(self, sequence: _Optional[int] = ..., time_unix_ms: _Optional[int] = ..., type: _Optional[str] = ..., subject: _Optional[str] = ..., level: _Optional[str] = ..., message: _Optional[str] = ...) -> None: ...

class ShutdownRequest(_message.Message):
    __slots__ = ("drain",)
    DRAIN_FIELD_NUMBER: _ClassVar[int]
    drain: bool
    def __init__(self, drain: _Optional[bool] = ...) -> None: ...

class ShutdownResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class DebugRequest(_message.Message):
    __slots__ = ("app", "release", "op", "worker", "args_json", "group")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    OP_FIELD_NUMBER: _ClassVar[int]
    WORKER_FIELD_NUMBER: _ClassVar[int]
    ARGS_JSON_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    op: str
    worker: int
    args_json: str
    group: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., op: _Optional[str] = ..., worker: _Optional[int] = ..., args_json: _Optional[str] = ..., group: _Optional[str] = ...) -> None: ...

class DebugResponse(_message.Message):
    __slots__ = ("workers", "release", "host_json")
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    HOST_JSON_FIELD_NUMBER: _ClassVar[int]
    workers: _containers.RepeatedCompositeFieldContainer[WorkerDebug]
    release: str
    host_json: str
    def __init__(self, workers: _Optional[_Iterable[_Union[WorkerDebug, _Mapping]]] = ..., release: _Optional[str] = ..., host_json: _Optional[str] = ...) -> None: ...

class WorkerDebug(_message.Message):
    __slots__ = ("index", "pid", "ok", "error", "result_json", "group")
    INDEX_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    RESULT_JSON_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    index: int
    pid: int
    ok: bool
    error: str
    result_json: str
    group: str
    def __init__(self, index: _Optional[int] = ..., pid: _Optional[int] = ..., ok: _Optional[bool] = ..., error: _Optional[str] = ..., result_json: _Optional[str] = ..., group: _Optional[str] = ...) -> None: ...

class NoteBundleRequest(_message.Message):
    __slots__ = ("app", "release", "since_unix_ms", "until_unix_ms", "options")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    SINCE_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    UNTIL_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    OPTIONS_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    since_unix_ms: int
    until_unix_ms: int
    options: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., since_unix_ms: _Optional[int] = ..., until_unix_ms: _Optional[int] = ..., options: _Optional[_Iterable[str]] = ...) -> None: ...

class NoteBundleResponse(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOverlaysRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListOverlaysResponse(_message.Message):
    __slots__ = ("overlays",)
    OVERLAYS_FIELD_NUMBER: _ClassVar[int]
    overlays: _containers.RepeatedCompositeFieldContainer[OverlayInfo]
    def __init__(self, overlays: _Optional[_Iterable[_Union[OverlayInfo, _Mapping]]] = ...) -> None: ...

class OverlayInfo(_message.Message):
    __slots__ = ("name", "active", "state", "since_unix_ms", "until_unix_ms", "trigger", "changes", "starts_unix_ms", "condition", "condition_state")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SINCE_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    UNTIL_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    STARTS_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    CONDITION_STATE_FIELD_NUMBER: _ClassVar[int]
    name: str
    active: bool
    state: str
    since_unix_ms: int
    until_unix_ms: int
    trigger: str
    changes: _containers.RepeatedScalarFieldContainer[str]
    starts_unix_ms: int
    condition: str
    condition_state: str
    def __init__(self, name: _Optional[str] = ..., active: _Optional[bool] = ..., state: _Optional[str] = ..., since_unix_ms: _Optional[int] = ..., until_unix_ms: _Optional[int] = ..., trigger: _Optional[str] = ..., changes: _Optional[_Iterable[str]] = ..., starts_unix_ms: _Optional[int] = ..., condition: _Optional[str] = ..., condition_state: _Optional[str] = ...) -> None: ...

class ControlOverlayRequest(_message.Message):
    __slots__ = ("name", "action", "until_unix_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    UNTIL_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    action: str
    until_unix_ms: int
    def __init__(self, name: _Optional[str] = ..., action: _Optional[str] = ..., until_unix_ms: _Optional[int] = ...) -> None: ...

class ControlOverlayResponse(_message.Message):
    __slots__ = ("message", "files")
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    FILES_FIELD_NUMBER: _ClassVar[int]
    message: str
    files: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, message: _Optional[str] = ..., files: _Optional[_Iterable[str]] = ...) -> None: ...

class PreviewOverlayRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class PreviewOverlayResponse(_message.Message):
    __slots__ = ("changes", "condition", "condition_state", "condition_terms")
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    CONDITION_FIELD_NUMBER: _ClassVar[int]
    CONDITION_STATE_FIELD_NUMBER: _ClassVar[int]
    CONDITION_TERMS_FIELD_NUMBER: _ClassVar[int]
    changes: _containers.RepeatedScalarFieldContainer[str]
    condition: str
    condition_state: str
    condition_terms: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, changes: _Optional[_Iterable[str]] = ..., condition: _Optional[str] = ..., condition_state: _Optional[str] = ..., condition_terms: _Optional[_Iterable[str]] = ...) -> None: ...

class UpgradeDaemonRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class UpgradeDaemonResponse(_message.Message):
    __slots__ = ("executable", "version")
    EXECUTABLE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    executable: str
    version: str
    def __init__(self, executable: _Optional[str] = ..., version: _Optional[str] = ...) -> None: ...

class ApplyConfigRequest(_message.Message):
    __slots__ = ("document", "dry_run", "prune", "override_freeze", "hold", "no_wait", "retain_ms", "retain_workers")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    PRUNE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FREEZE_FIELD_NUMBER: _ClassVar[int]
    HOLD_FIELD_NUMBER: _ClassVar[int]
    NO_WAIT_FIELD_NUMBER: _ClassVar[int]
    RETAIN_MS_FIELD_NUMBER: _ClassVar[int]
    RETAIN_WORKERS_FIELD_NUMBER: _ClassVar[int]
    document: str
    dry_run: bool
    prune: bool
    override_freeze: bool
    hold: bool
    no_wait: bool
    retain_ms: int
    retain_workers: int
    def __init__(self, document: _Optional[str] = ..., dry_run: _Optional[bool] = ..., prune: _Optional[bool] = ..., override_freeze: _Optional[bool] = ..., hold: _Optional[bool] = ..., no_wait: _Optional[bool] = ..., retain_ms: _Optional[int] = ..., retain_workers: _Optional[int] = ...) -> None: ...

class DiffConfigRequest(_message.Message):
    __slots__ = ("document",)
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    document: str
    def __init__(self, document: _Optional[str] = ...) -> None: ...

class ConfigReport(_message.Message):
    __slots__ = ("errors", "warnings", "changes", "unchanged", "applied", "notes", "snapshot_error")
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    WARNINGS_FIELD_NUMBER: _ClassVar[int]
    CHANGES_FIELD_NUMBER: _ClassVar[int]
    UNCHANGED_FIELD_NUMBER: _ClassVar[int]
    APPLIED_FIELD_NUMBER: _ClassVar[int]
    NOTES_FIELD_NUMBER: _ClassVar[int]
    SNAPSHOT_ERROR_FIELD_NUMBER: _ClassVar[int]
    errors: _containers.RepeatedScalarFieldContainer[str]
    warnings: _containers.RepeatedScalarFieldContainer[str]
    changes: _containers.RepeatedCompositeFieldContainer[ConfigChange]
    unchanged: int
    applied: bool
    notes: _containers.RepeatedScalarFieldContainer[str]
    snapshot_error: str
    def __init__(self, errors: _Optional[_Iterable[str]] = ..., warnings: _Optional[_Iterable[str]] = ..., changes: _Optional[_Iterable[_Union[ConfigChange, _Mapping]]] = ..., unchanged: _Optional[int] = ..., applied: _Optional[bool] = ..., notes: _Optional[_Iterable[str]] = ..., snapshot_error: _Optional[str] = ...) -> None: ...

class ConfigChange(_message.Message):
    __slots__ = ("action", "subject", "detail", "outcome")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SUBJECT_FIELD_NUMBER: _ClassVar[int]
    DETAIL_FIELD_NUMBER: _ClassVar[int]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    action: str
    subject: str
    detail: str
    outcome: str
    def __init__(self, action: _Optional[str] = ..., subject: _Optional[str] = ..., detail: _Optional[str] = ..., outcome: _Optional[str] = ...) -> None: ...

class ExportConfigRequest(_message.Message):
    __slots__ = ("app", "effective", "resolve_rollouts")
    APP_FIELD_NUMBER: _ClassVar[int]
    EFFECTIVE_FIELD_NUMBER: _ClassVar[int]
    RESOLVE_ROLLOUTS_FIELD_NUMBER: _ClassVar[int]
    app: str
    effective: bool
    resolve_rollouts: bool
    def __init__(self, app: _Optional[str] = ..., effective: _Optional[bool] = ..., resolve_rollouts: _Optional[bool] = ...) -> None: ...

class ExportConfigResponse(_message.Message):
    __slots__ = ("document", "version", "node", "time_unix_ms", "state_version", "attributions", "layers")
    DOCUMENT_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    TIME_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    STATE_VERSION_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTIONS_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    document: str
    version: str
    node: str
    time_unix_ms: int
    state_version: int
    attributions: _containers.RepeatedScalarFieldContainer[str]
    layers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, document: _Optional[str] = ..., version: _Optional[str] = ..., node: _Optional[str] = ..., time_unix_ms: _Optional[int] = ..., state_version: _Optional[int] = ..., attributions: _Optional[_Iterable[str]] = ..., layers: _Optional[_Iterable[str]] = ...) -> None: ...

class ListHostsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListHostsResponse(_message.Message):
    __slots__ = ("hosts",)
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    hosts: _containers.RepeatedCompositeFieldContainer[Host]
    def __init__(self, hosts: _Optional[_Iterable[_Union[Host, _Mapping]]] = ...) -> None: ...

class Host(_message.Message):
    __slots__ = ("name", "names", "listeners", "tls", "certificate", "canonical", "https_redirect", "use_canonical_name", "default", "canonical_redirect", "max_body_size", "timeouts", "access_log", "compression", "request_headers", "response_headers", "maintenance", "access_log_format", "access_log_file", "access_log_query")
    class TimeoutsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    LISTENERS_FIELD_NUMBER: _ClassVar[int]
    TLS_FIELD_NUMBER: _ClassVar[int]
    CERTIFICATE_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_FIELD_NUMBER: _ClassVar[int]
    HTTPS_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    USE_CANONICAL_NAME_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    CANONICAL_REDIRECT_FIELD_NUMBER: _ClassVar[int]
    MAX_BODY_SIZE_FIELD_NUMBER: _ClassVar[int]
    TIMEOUTS_FIELD_NUMBER: _ClassVar[int]
    ACCESS_LOG_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_HEADERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_LOG_FORMAT_FIELD_NUMBER: _ClassVar[int]
    ACCESS_LOG_FILE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_LOG_QUERY_FIELD_NUMBER: _ClassVar[int]
    name: str
    names: _containers.RepeatedScalarFieldContainer[str]
    listeners: _containers.RepeatedScalarFieldContainer[str]
    tls: bool
    certificate: str
    canonical: str
    https_redirect: bool
    use_canonical_name: bool
    default: bool
    canonical_redirect: bool
    max_body_size: str
    timeouts: _containers.ScalarMap[str, str]
    access_log: str
    compression: str
    request_headers: str
    response_headers: str
    maintenance: bool
    access_log_format: str
    access_log_file: str
    access_log_query: str
    def __init__(self, name: _Optional[str] = ..., names: _Optional[_Iterable[str]] = ..., listeners: _Optional[_Iterable[str]] = ..., tls: _Optional[bool] = ..., certificate: _Optional[str] = ..., canonical: _Optional[str] = ..., https_redirect: _Optional[bool] = ..., use_canonical_name: _Optional[bool] = ..., default: _Optional[bool] = ..., canonical_redirect: _Optional[bool] = ..., max_body_size: _Optional[str] = ..., timeouts: _Optional[_Mapping[str, str]] = ..., access_log: _Optional[str] = ..., compression: _Optional[str] = ..., request_headers: _Optional[str] = ..., response_headers: _Optional[str] = ..., maintenance: _Optional[bool] = ..., access_log_format: _Optional[str] = ..., access_log_file: _Optional[str] = ..., access_log_query: _Optional[str] = ...) -> None: ...

class ListRoutesRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListRoutesResponse(_message.Message):
    __slots__ = ("routes",)
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    routes: _containers.RepeatedCompositeFieldContainer[Route]
    def __init__(self, routes: _Optional[_Iterable[_Union[Route, _Mapping]]] = ...) -> None: ...

class Route(_message.Message):
    __slots__ = ("host", "path", "app", "static_dir", "fallback_app", "traffic", "sticky", "hash_key", "internal", "accept_redirects_from", "auth", "upstream", "fallback_upstream", "upload", "max_body_size", "client_classes", "traffic_classes", "timeouts", "compression", "request_headers", "response_headers")
    class TrafficClassesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class TimeoutsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    HOST_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    STATIC_DIR_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_APP_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_FIELD_NUMBER: _ClassVar[int]
    STICKY_FIELD_NUMBER: _ClassVar[int]
    HASH_KEY_FIELD_NUMBER: _ClassVar[int]
    INTERNAL_FIELD_NUMBER: _ClassVar[int]
    ACCEPT_REDIRECTS_FROM_FIELD_NUMBER: _ClassVar[int]
    AUTH_FIELD_NUMBER: _ClassVar[int]
    UPSTREAM_FIELD_NUMBER: _ClassVar[int]
    FALLBACK_UPSTREAM_FIELD_NUMBER: _ClassVar[int]
    UPLOAD_FIELD_NUMBER: _ClassVar[int]
    MAX_BODY_SIZE_FIELD_NUMBER: _ClassVar[int]
    CLIENT_CLASSES_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_CLASSES_FIELD_NUMBER: _ClassVar[int]
    TIMEOUTS_FIELD_NUMBER: _ClassVar[int]
    COMPRESSION_FIELD_NUMBER: _ClassVar[int]
    REQUEST_HEADERS_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_HEADERS_FIELD_NUMBER: _ClassVar[int]
    host: str
    path: str
    app: str
    static_dir: str
    fallback_app: str
    traffic: _containers.RepeatedCompositeFieldContainer[TrafficShare]
    sticky: bool
    hash_key: str
    internal: bool
    accept_redirects_from: _containers.RepeatedScalarFieldContainer[str]
    auth: str
    upstream: str
    fallback_upstream: str
    upload: str
    max_body_size: str
    client_classes: _containers.RepeatedScalarFieldContainer[str]
    traffic_classes: _containers.ScalarMap[str, str]
    timeouts: _containers.ScalarMap[str, str]
    compression: str
    request_headers: str
    response_headers: str
    def __init__(self, host: _Optional[str] = ..., path: _Optional[str] = ..., app: _Optional[str] = ..., static_dir: _Optional[str] = ..., fallback_app: _Optional[str] = ..., traffic: _Optional[_Iterable[_Union[TrafficShare, _Mapping]]] = ..., sticky: _Optional[bool] = ..., hash_key: _Optional[str] = ..., internal: _Optional[bool] = ..., accept_redirects_from: _Optional[_Iterable[str]] = ..., auth: _Optional[str] = ..., upstream: _Optional[str] = ..., fallback_upstream: _Optional[str] = ..., upload: _Optional[str] = ..., max_body_size: _Optional[str] = ..., client_classes: _Optional[_Iterable[str]] = ..., traffic_classes: _Optional[_Mapping[str, str]] = ..., timeouts: _Optional[_Mapping[str, str]] = ..., compression: _Optional[str] = ..., request_headers: _Optional[str] = ..., response_headers: _Optional[str] = ...) -> None: ...

class ListUpstreamsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListUpstreamsResponse(_message.Message):
    __slots__ = ("upstreams",)
    UPSTREAMS_FIELD_NUMBER: _ClassVar[int]
    upstreams: _containers.RepeatedCompositeFieldContainer[Upstream]
    def __init__(self, upstreams: _Optional[_Iterable[_Union[Upstream, _Mapping]]] = ...) -> None: ...

class Upstream(_message.Message):
    __slots__ = ("name", "addresses", "protocol", "tls", "health_path", "trust_muru_headers")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ADDRESSES_FIELD_NUMBER: _ClassVar[int]
    PROTOCOL_FIELD_NUMBER: _ClassVar[int]
    TLS_FIELD_NUMBER: _ClassVar[int]
    HEALTH_PATH_FIELD_NUMBER: _ClassVar[int]
    TRUST_MURU_HEADERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    addresses: _containers.RepeatedScalarFieldContainer[str]
    protocol: str
    tls: bool
    health_path: str
    trust_muru_headers: bool
    def __init__(self, name: _Optional[str] = ..., addresses: _Optional[_Iterable[str]] = ..., protocol: _Optional[str] = ..., tls: _Optional[bool] = ..., health_path: _Optional[str] = ..., trust_muru_headers: _Optional[bool] = ...) -> None: ...

class TrafficShare(_message.Message):
    __slots__ = ("release", "percent")
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    PERCENT_FIELD_NUMBER: _ClassVar[int]
    release: str
    percent: int
    def __init__(self, release: _Optional[str] = ..., percent: _Optional[int] = ...) -> None: ...

class TailLogsRequest(_message.Message):
    __slots__ = ("app", "release", "follow", "lines", "access", "host", "edge", "daemon")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    FOLLOW_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    ACCESS_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    EDGE_FIELD_NUMBER: _ClassVar[int]
    DAEMON_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    follow: bool
    lines: int
    access: bool
    host: str
    edge: bool
    daemon: bool
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., follow: _Optional[bool] = ..., lines: _Optional[int] = ..., access: _Optional[bool] = ..., host: _Optional[str] = ..., edge: _Optional[bool] = ..., daemon: _Optional[bool] = ...) -> None: ...

class LogLine(_message.Message):
    __slots__ = ("app", "release", "line")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    line: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., line: _Optional[str] = ...) -> None: ...

class RunCommandRequest(_message.Message):
    __slots__ = ("app", "release", "argv", "name", "inputs", "secret_inputs", "detach")
    class InputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    class SecretInputsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    ARGV_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    SECRET_INPUTS_FIELD_NUMBER: _ClassVar[int]
    DETACH_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    argv: _containers.RepeatedScalarFieldContainer[str]
    name: str
    inputs: _containers.ScalarMap[str, str]
    secret_inputs: _containers.ScalarMap[str, str]
    detach: bool
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., argv: _Optional[_Iterable[str]] = ..., name: _Optional[str] = ..., inputs: _Optional[_Mapping[str, str]] = ..., secret_inputs: _Optional[_Mapping[str, str]] = ..., detach: _Optional[bool] = ...) -> None: ...

class ListCommandsRequest(_message.Message):
    __slots__ = ("app", "release")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ...) -> None: ...

class ListCommandsResponse(_message.Message):
    __slots__ = ("app", "release", "commands")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    commands: _containers.RepeatedCompositeFieldContainer[CommandInfo]
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., commands: _Optional[_Iterable[_Union[CommandInfo, _Mapping]]] = ...) -> None: ...

class CommandInfo(_message.Message):
    __slots__ = ("name", "description", "run", "call", "inputs", "timeout", "exclusive", "last_run", "schedule", "next_run_unix_ms", "gates", "every_start")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    CALL_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    EXCLUSIVE_FIELD_NUMBER: _ClassVar[int]
    LAST_RUN_FIELD_NUMBER: _ClassVar[int]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    NEXT_RUN_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    GATES_FIELD_NUMBER: _ClassVar[int]
    EVERY_START_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    run: _containers.RepeatedScalarFieldContainer[str]
    call: str
    inputs: _containers.RepeatedCompositeFieldContainer[CommandInputInfo]
    timeout: str
    exclusive: bool
    last_run: CommandRun
    schedule: str
    next_run_unix_ms: int
    gates: _containers.RepeatedScalarFieldContainer[str]
    every_start: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., run: _Optional[_Iterable[str]] = ..., call: _Optional[str] = ..., inputs: _Optional[_Iterable[_Union[CommandInputInfo, _Mapping]]] = ..., timeout: _Optional[str] = ..., exclusive: _Optional[bool] = ..., last_run: _Optional[_Union[CommandRun, _Mapping]] = ..., schedule: _Optional[str] = ..., next_run_unix_ms: _Optional[int] = ..., gates: _Optional[_Iterable[str]] = ..., every_start: _Optional[bool] = ...) -> None: ...

class CommandInputInfo(_message.Message):
    __slots__ = ("name", "description", "required", "default", "pattern", "secret")
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    REQUIRED_FIELD_NUMBER: _ClassVar[int]
    DEFAULT_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    SECRET_FIELD_NUMBER: _ClassVar[int]
    name: str
    description: str
    required: bool
    default: str
    pattern: str
    secret: bool
    def __init__(self, name: _Optional[str] = ..., description: _Optional[str] = ..., required: _Optional[bool] = ..., default: _Optional[str] = ..., pattern: _Optional[str] = ..., secret: _Optional[bool] = ...) -> None: ...

class CommandRun(_message.Message):
    __slots__ = ("release", "started_unix_ms", "duration_ms", "exit_code", "ok", "message")
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    DURATION_MS_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    release: str
    started_unix_ms: int
    duration_ms: int
    exit_code: int
    ok: bool
    message: str
    def __init__(self, release: _Optional[str] = ..., started_unix_ms: _Optional[int] = ..., duration_ms: _Optional[int] = ..., exit_code: _Optional[int] = ..., ok: _Optional[bool] = ..., message: _Optional[str] = ...) -> None: ...

class CommandOutput(_message.Message):
    __slots__ = ("release", "line", "stderr", "finished", "exit_code", "message", "ok", "run", "detached")
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    STDERR_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    RUN_FIELD_NUMBER: _ClassVar[int]
    DETACHED_FIELD_NUMBER: _ClassVar[int]
    release: str
    line: str
    stderr: bool
    finished: bool
    exit_code: int
    message: str
    ok: bool
    run: int
    detached: bool
    def __init__(self, release: _Optional[str] = ..., line: _Optional[str] = ..., stderr: _Optional[bool] = ..., finished: _Optional[bool] = ..., exit_code: _Optional[int] = ..., message: _Optional[str] = ..., ok: _Optional[bool] = ..., run: _Optional[int] = ..., detached: _Optional[bool] = ...) -> None: ...

class ListConditionsRequest(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class ListConditionsResponse(_message.Message):
    __slots__ = ("conditions",)
    CONDITIONS_FIELD_NUMBER: _ClassVar[int]
    conditions: _containers.RepeatedCompositeFieldContainer[ConditionStatus]
    def __init__(self, conditions: _Optional[_Iterable[_Union[ConditionStatus, _Mapping]]] = ...) -> None: ...

class ConditionStatus(_message.Message):
    __slots__ = ("name", "state", "held", "since_unix_ms", "source", "when", "clear_when", "clear_for", "min_requests", "unknown", "terms", "pending_since_unix_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    HELD_FIELD_NUMBER: _ClassVar[int]
    SINCE_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    WHEN_FIELD_NUMBER: _ClassVar[int]
    FOR_FIELD_NUMBER: _ClassVar[int]
    CLEAR_WHEN_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FOR_FIELD_NUMBER: _ClassVar[int]
    MIN_REQUESTS_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    TERMS_FIELD_NUMBER: _ClassVar[int]
    PENDING_SINCE_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    state: str
    held: str
    since_unix_ms: int
    source: str
    when: str
    clear_when: str
    clear_for: str
    min_requests: int
    unknown: str
    terms: _containers.RepeatedCompositeFieldContainer[ConditionTerm]
    pending_since_unix_ms: int
    def __init__(self, name: _Optional[str] = ..., state: _Optional[str] = ..., held: _Optional[str] = ..., since_unix_ms: _Optional[int] = ..., source: _Optional[str] = ..., when: _Optional[str] = ..., clear_when: _Optional[str] = ..., clear_for: _Optional[str] = ..., min_requests: _Optional[int] = ..., unknown: _Optional[str] = ..., terms: _Optional[_Iterable[_Union[ConditionTerm, _Mapping]]] = ..., pending_since_unix_ms: _Optional[int] = ..., **kwargs) -> None: ...

class ConditionTerm(_message.Message):
    __slots__ = ("term", "known", "value", "unknown")
    TERM_FIELD_NUMBER: _ClassVar[int]
    KNOWN_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    UNKNOWN_FIELD_NUMBER: _ClassVar[int]
    term: str
    known: bool
    value: float
    unknown: str
    def __init__(self, term: _Optional[str] = ..., known: _Optional[bool] = ..., value: _Optional[float] = ..., unknown: _Optional[str] = ...) -> None: ...

class ListCommandRunsRequest(_message.Message):
    __slots__ = ("app", "name")
    APP_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    app: str
    name: str
    def __init__(self, app: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class ListCommandRunsResponse(_message.Message):
    __slots__ = ("runs",)
    RUNS_FIELD_NUMBER: _ClassVar[int]
    runs: _containers.RepeatedCompositeFieldContainer[CommandRunRecord]
    def __init__(self, runs: _Optional[_Iterable[_Union[CommandRunRecord, _Mapping]]] = ...) -> None: ...

class GetCommandRunRequest(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: int
    def __init__(self, run: _Optional[int] = ...) -> None: ...

class TailCommandRunRequest(_message.Message):
    __slots__ = ("run", "lines", "follow")
    RUN_FIELD_NUMBER: _ClassVar[int]
    LINES_FIELD_NUMBER: _ClassVar[int]
    FOLLOW_FIELD_NUMBER: _ClassVar[int]
    run: int
    lines: int
    follow: bool
    def __init__(self, run: _Optional[int] = ..., lines: _Optional[int] = ..., follow: _Optional[bool] = ...) -> None: ...

class StopCommandRunRequest(_message.Message):
    __slots__ = ("run",)
    RUN_FIELD_NUMBER: _ClassVar[int]
    run: int
    def __init__(self, run: _Optional[int] = ...) -> None: ...

class CommandRunRecord(_message.Message):
    __slots__ = ("run", "app", "release", "name", "trigger", "requested_by", "detached", "inputs", "started_unix_ms", "ended_unix_ms", "under_way", "exit_code", "ok", "message", "log", "pid", "stopping")
    RUN_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    REQUESTED_BY_FIELD_NUMBER: _ClassVar[int]
    DETACHED_FIELD_NUMBER: _ClassVar[int]
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    STARTED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    ENDED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    UNDER_WAY_FIELD_NUMBER: _ClassVar[int]
    EXIT_CODE_FIELD_NUMBER: _ClassVar[int]
    OK_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    PID_FIELD_NUMBER: _ClassVar[int]
    STOPPING_FIELD_NUMBER: _ClassVar[int]
    run: int
    app: str
    release: str
    name: str
    trigger: str
    requested_by: str
    detached: bool
    inputs: str
    started_unix_ms: int
    ended_unix_ms: int
    under_way: bool
    exit_code: int
    ok: bool
    message: str
    log: str
    pid: int
    stopping: str
    def __init__(self, run: _Optional[int] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., name: _Optional[str] = ..., trigger: _Optional[str] = ..., requested_by: _Optional[str] = ..., detached: _Optional[bool] = ..., inputs: _Optional[str] = ..., started_unix_ms: _Optional[int] = ..., ended_unix_ms: _Optional[int] = ..., under_way: _Optional[bool] = ..., exit_code: _Optional[int] = ..., ok: _Optional[bool] = ..., message: _Optional[str] = ..., log: _Optional[str] = ..., pid: _Optional[int] = ..., stopping: _Optional[str] = ...) -> None: ...

class ReopenLogsRequest(_message.Message):
    __slots__ = ("workers",)
    WORKERS_FIELD_NUMBER: _ClassVar[int]
    workers: bool
    def __init__(self, workers: _Optional[bool] = ...) -> None: ...

class ReopenLogsResponse(_message.Message):
    __slots__ = ("edge", "hosts")
    EDGE_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    edge: bool
    hosts: int
    def __init__(self, edge: _Optional[bool] = ..., hosts: _Optional[int] = ...) -> None: ...

class ListLogsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class LogArchive(_message.Message):
    __slots__ = ("name", "size", "modified_unix_ms", "orphaned")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    ORPHANED_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    modified_unix_ms: int
    orphaned: bool
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ..., modified_unix_ms: _Optional[int] = ..., orphaned: _Optional[bool] = ...) -> None: ...

class LogInfo(_message.Message):
    __slots__ = ("name", "kind", "app", "release", "hosts", "size", "present", "archives", "archives_size", "total", "orphaned", "modified_unix_ms")
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    HOSTS_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    ARCHIVES_FIELD_NUMBER: _ClassVar[int]
    ARCHIVES_SIZE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ORPHANED_FIELD_NUMBER: _ClassVar[int]
    MODIFIED_UNIX_MS_FIELD_NUMBER: _ClassVar[int]
    name: str
    kind: str
    app: str
    release: str
    hosts: _containers.RepeatedScalarFieldContainer[str]
    size: int
    present: bool
    archives: _containers.RepeatedCompositeFieldContainer[LogArchive]
    archives_size: int
    total: int
    orphaned: bool
    modified_unix_ms: int
    def __init__(self, name: _Optional[str] = ..., kind: _Optional[str] = ..., app: _Optional[str] = ..., release: _Optional[str] = ..., hosts: _Optional[_Iterable[str]] = ..., size: _Optional[int] = ..., present: _Optional[bool] = ..., archives: _Optional[_Iterable[_Union[LogArchive, _Mapping]]] = ..., archives_size: _Optional[int] = ..., total: _Optional[int] = ..., orphaned: _Optional[bool] = ..., modified_unix_ms: _Optional[int] = ...) -> None: ...

class ListLogsResponse(_message.Message):
    __slots__ = ("directory", "logs", "total", "orphans_known")
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    LOGS_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    ORPHANS_KNOWN_FIELD_NUMBER: _ClassVar[int]
    directory: str
    logs: _containers.RepeatedCompositeFieldContainer[LogInfo]
    total: int
    orphans_known: bool
    def __init__(self, directory: _Optional[str] = ..., logs: _Optional[_Iterable[_Union[LogInfo, _Mapping]]] = ..., total: _Optional[int] = ..., orphans_known: _Optional[bool] = ...) -> None: ...

class LogTarget(_message.Message):
    __slots__ = ("app", "release", "access", "host", "all")
    APP_FIELD_NUMBER: _ClassVar[int]
    RELEASE_FIELD_NUMBER: _ClassVar[int]
    ACCESS_FIELD_NUMBER: _ClassVar[int]
    HOST_FIELD_NUMBER: _ClassVar[int]
    ALL_FIELD_NUMBER: _ClassVar[int]
    app: str
    release: str
    access: bool
    host: str
    all: bool
    def __init__(self, app: _Optional[str] = ..., release: _Optional[str] = ..., access: _Optional[bool] = ..., host: _Optional[str] = ..., all: _Optional[bool] = ...) -> None: ...

class TruncateLogsRequest(_message.Message):
    __slots__ = ("target", "keep", "dry_run")
    TARGET_FIELD_NUMBER: _ClassVar[int]
    KEEP_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    target: LogTarget
    keep: int
    dry_run: bool
    def __init__(self, target: _Optional[_Union[LogTarget, _Mapping]] = ..., keep: _Optional[int] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class TruncatedLog(_message.Message):
    __slots__ = ("name", "size", "kept", "freed", "in_place", "late", "error")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    KEPT_FIELD_NUMBER: _ClassVar[int]
    FREED_FIELD_NUMBER: _ClassVar[int]
    IN_PLACE_FIELD_NUMBER: _ClassVar[int]
    LATE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    kept: int
    freed: int
    in_place: bool
    late: int
    error: str
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ..., kept: _Optional[int] = ..., freed: _Optional[int] = ..., in_place: _Optional[bool] = ..., late: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...

class TruncateLogsResponse(_message.Message):
    __slots__ = ("logs", "freed", "dry_run")
    LOGS_FIELD_NUMBER: _ClassVar[int]
    FREED_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[TruncatedLog]
    freed: int
    dry_run: bool
    def __init__(self, logs: _Optional[_Iterable[_Union[TruncatedLog, _Mapping]]] = ..., freed: _Optional[int] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class RotateLogsRequest(_message.Message):
    __slots__ = ("target",)
    TARGET_FIELD_NUMBER: _ClassVar[int]
    target: LogTarget
    def __init__(self, target: _Optional[_Union[LogTarget, _Mapping]] = ...) -> None: ...

class RotatedLog(_message.Message):
    __slots__ = ("name", "size", "archive", "error")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    ARCHIVE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    archive: str
    error: str
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ..., archive: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class RotateLogsResponse(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[RotatedLog]
    def __init__(self, logs: _Optional[_Iterable[_Union[RotatedLog, _Mapping]]] = ...) -> None: ...

class PruneLogsRequest(_message.Message):
    __slots__ = ("keep", "older_than_s", "orphaned", "dry_run")
    KEEP_FIELD_NUMBER: _ClassVar[int]
    OLDER_THAN_S_FIELD_NUMBER: _ClassVar[int]
    ORPHANED_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    keep: int
    older_than_s: int
    orphaned: bool
    dry_run: bool
    def __init__(self, keep: _Optional[int] = ..., older_than_s: _Optional[int] = ..., orphaned: _Optional[bool] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class PrunedFile(_message.Message):
    __slots__ = ("name", "size", "why", "error")
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    WHY_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    name: str
    size: int
    why: str
    error: str
    def __init__(self, name: _Optional[str] = ..., size: _Optional[int] = ..., why: _Optional[str] = ..., error: _Optional[str] = ...) -> None: ...

class PruneLogsResponse(_message.Message):
    __slots__ = ("removed", "freed", "dry_run")
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    FREED_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    removed: _containers.RepeatedCompositeFieldContainer[PrunedFile]
    freed: int
    dry_run: bool
    def __init__(self, removed: _Optional[_Iterable[_Union[PrunedFile, _Mapping]]] = ..., freed: _Optional[int] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class ListCacheRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class CacheEntry(_message.Message):
    __slots__ = ("kind", "name", "path", "version", "tag", "size", "in_use", "freed", "error")
    KIND_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    IN_USE_FIELD_NUMBER: _ClassVar[int]
    FREED_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    kind: str
    name: str
    path: str
    version: str
    tag: str
    size: int
    in_use: str
    freed: int
    error: str
    def __init__(self, kind: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., version: _Optional[str] = ..., tag: _Optional[str] = ..., size: _Optional[int] = ..., in_use: _Optional[str] = ..., freed: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...

class PruneCacheRequest(_message.Message):
    __slots__ = ("version", "tag", "dry_run")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TAG_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    version: str
    tag: str
    dry_run: bool
    def __init__(self, version: _Optional[str] = ..., tag: _Optional[str] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class ClearCacheRequest(_message.Message):
    __slots__ = ("dry_run",)
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    dry_run: bool
    def __init__(self, dry_run: _Optional[bool] = ...) -> None: ...

class RemoveCacheResponse(_message.Message):
    __slots__ = ("directory", "removed", "left", "freed", "dry_run")
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    REMOVED_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    FREED_FIELD_NUMBER: _ClassVar[int]
    DRY_RUN_FIELD_NUMBER: _ClassVar[int]
    directory: str
    removed: _containers.RepeatedCompositeFieldContainer[CacheEntry]
    left: _containers.RepeatedCompositeFieldContainer[CacheEntry]
    freed: int
    dry_run: bool
    def __init__(self, directory: _Optional[str] = ..., removed: _Optional[_Iterable[_Union[CacheEntry, _Mapping]]] = ..., left: _Optional[_Iterable[_Union[CacheEntry, _Mapping]]] = ..., freed: _Optional[int] = ..., dry_run: _Optional[bool] = ...) -> None: ...

class ListCacheResponse(_message.Message):
    __slots__ = ("directory", "entries", "total")
    DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_FIELD_NUMBER: _ClassVar[int]
    directory: str
    entries: _containers.RepeatedCompositeFieldContainer[CacheEntry]
    total: int
    def __init__(self, directory: _Optional[str] = ..., entries: _Optional[_Iterable[_Union[CacheEntry, _Mapping]]] = ..., total: _Optional[int] = ...) -> None: ...

class GetMetricsRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class MetricsText(_message.Message):
    __slots__ = ("text",)
    TEXT_FIELD_NUMBER: _ClassVar[int]
    text: str
    def __init__(self, text: _Optional[str] = ...) -> None: ...

class ReloadConfigRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ReloadConfigResponse(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
