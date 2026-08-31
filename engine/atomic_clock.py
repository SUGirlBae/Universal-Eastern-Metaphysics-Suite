"""
High-Precision Atomic & Quantum Clock Synchronization Module
Queries international atomic time servers (NIST, Google, Cloudflare) with RTT latency compensation.
"""
import socket
import struct
import time
from datetime import datetime, timezone, timedelta

LOCAL_TZ = timezone(timedelta(hours=7))

ATOMIC_SERVERS = [
    "time.cloudflare.com",
    "time.google.com",
    "time.nist.gov",
    "pool.ntp.org",
    "time.windows.com"
]

def query_ntp_server(server: str, timeout: float = 2.0):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.settimeout(timeout)
    data = b"\x1b" + 47 * b"\0"
    try:
        t_send = time.time()
        client.sendto(data, (server, 123))
        recv_data, address = client.recvfrom(1024)
        t_recv = time.time()
        if recv_data:
            unpacked = struct.unpack("!12I", recv_data[0:48])
            # NTP epoch (1900-01-01) to Unix epoch (1970-01-01) diff: 2,208,988,800s
            ntp_time = unpacked[10] + float(unpacked[11]) / (2**32) - 2208988800
            # Network Round-Trip Time compensation (half-trip latency offset)
            rtt = t_recv - t_send
            exact_time = ntp_time + (rtt / 2.0)
            dt_utc = datetime.fromtimestamp(exact_time, tz=timezone.utc)
            dt_local = dt_utc.astimezone(LOCAL_TZ)
            return dt_local, rtt * 1000, server
    except Exception:
        return None, None, server
    finally:
        client.close()
    return None, None, server

def get_precise_atomic_now():
    """
    Attempts to get the precise time from atomic/quantum time servers.
    Falls back to high-resolution local clock if network is unreachable.
    """
    for server in ATOMIC_SERVERS:
        dt, rtt, srv = query_ntp_server(server)
        if dt is not None:
            return {
                "datetime": dt,
                "source": "ATOMIC_QUANTUM_CLOCK",
                "server": srv,
                "latency_ms": round(rtt, 2),
                "timestamp_str": dt.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
            }
            
    # Fallback to local clock
    dt_local = datetime.now(LOCAL_TZ)
    return {
        "datetime": dt_local,
        "source": "LOCAL_SYSTEM_CLOCK",
        "server": "localhost",
        "latency_ms": 0.0,
        "timestamp_str": dt_local.strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
    }
