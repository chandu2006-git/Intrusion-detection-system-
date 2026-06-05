import numpy as np

def extract_features(flow):

    duration = flow["last_seen"] - flow["start_time"]
    total_bytes = flow["byte_count"]
    packet_count = flow["packet_count"]

    avg_packet_size = total_bytes / (packet_count + 1)

    tcp_count = flow["tcp_count"] / (packet_count + 1)
    udp_count = flow["udp_count"] / (packet_count + 1)

    packets_per_second = packet_count / (duration + 1)
    bytes_per_second = total_bytes / (duration + 1)

    same_srv_rate = tcp_count
    diff_srv_rate = udp_count

    srv_diff_host_rate = 0.0
    serror_rate = 0.0

    features = np.array([
        duration,
        total_bytes,
        avg_packet_size,
        tcp_count,
        udp_count,
        packet_count / 100,
        packets_per_second,
        bytes_per_second,
        same_srv_rate,
        diff_srv_rate,
        srv_diff_host_rate,
        serror_rate
    ])

    return features