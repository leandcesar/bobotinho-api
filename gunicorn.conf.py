# Gunicorn configuration file.

"""
Server Socket

    bind
        The socket to bind. A string of the form: HOST, HOST:PORT,
        unix:PATH, fd://FD. An IP is a valid HOST.
"""

def get_port() -> str:
    from os import environ

    return environ.get("PORT", "8000")


bind = f"0.0.0.0:{get_port()}"


"""
Worker Processes

    workers
        The number of worker processes for handling requests. A positive integer
        generally in the 2-4 x $(NUM_CORES) range.

    worker_class
        The type of workers to use.

    worker_connections
        The maximum number of simultaneous clients. This setting only affects
        the Eventlet and Gevent worker types.

    timeout
        Workers silent for more than this many seconds are killed and restarted.
        Value is a positive number or 0. Setting it to 0 has the effect of infinite
        timeouts by disabling timeouts for all workers entirely.

    graceful_timeout
        Timeout for graceful workers restart. After receiving a restart signal,
        workers have this much time to finish serving requests. Workers still alive
        after the timeout (starting from the receipt of the restart signal) are
        force killed.

    keepalive
        The number of seconds to wait for requests on a Keep-Alive connection.
        Generally set in the 1-5 seconds range for servers with direct connection to
        the client.
"""

import gevent.monkey

gevent.monkey.patch_all()


def max_workers() -> int:
    # from multiprocessing import cpu_count
    # from os import environ

    # env = environ.get("ENV", "dev")
    # if env == "prod":
    #     return cpu_count() * 2 + 1
    return 1


workers = max_workers()
worker_class = "gevent"
worker_connections = 1000
timeout = 30
graceful_timeout = 30
keepalive = 2


"""
Debugging

    spew
        Install a trace function that spews every line executed by the server. This is
        the nuclear option.

    reload
        Restart workers when code changes.
"""

def is_development() -> bool:
    from os import environ

    env = environ.get("ENV", "dev")
    return env == "dev"


spew = False
reload = is_development()


"""
Server Mechanics

    daemon
        Daemonize the Gunicorn process. Detaches the server from the controlling
        terminal and enters the background.
"""

daemon = False


"""
Logging

    loglevel
        The granularity of Error log outputs.
"""

loglevel = "info"


"""
Server Hooks

    on_starting
        Called just before the master process is initialized.

    on_reload
        Called to recycle workers during a reload via SIGHUP.

    when_ready
        Called just after the server is started.

    pre_fork
        Called just before a worker is forked.

    post_fork
        Called just after a worker has been forked.

    post_worker_init
        Called just after a worker has initialized the application.

    worker_int
        Called just after a worker exited on SIGINT or SIGQUIT.

    worker_abort
        Called when a worker received the SIGABRT signal.

    pre_exec
        Called just before a new master process is forked.

    pre_request
        Called just before a worker processes the request.

    post_request
        Called after a worker processes the request.

    child_exit
        Called just after a worker has been exited, in the master process.

    worker_exit
        Called just after a worker has been exited, in the worker process.

    on_exit
        Called just before exiting Gunicorn.
"""

def on_starting(server) -> None:
    pass


def on_reload(server) -> None:
    pass


def when_ready(server) -> None:
    server.log.info("Server is ready. Spawning workers")


def pre_fork(server, worker) -> None:
    pass


def post_fork(server, worker) -> None:
    server.log.info(f"Worker spawned (pid: {worker.pid})")


def post_worker_init(worker) -> None:
    pass


def worker_int(worker) -> None:
    worker.log.info("Worker received INT or QUIT signal")


def worker_abort(worker) -> None:
    worker.log.info("Worker received SIGABRT signal")


def pre_exec(server) -> None:
    server.log.info("Forked child, re-executing.")


def pre_request(worker, req) -> None:
    worker.log.info(f"{req.method} {req.path}")


def post_request(worker, req, environ, resp) -> None:
    pass


def child_exit(server, worker) -> None:
    pass


def worker_exit(server, worker) -> None:
    pass


def on_exit(server) -> None:
    pass
