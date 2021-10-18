# ---- Worker application --------------------------------

import json
import os
import argparse

import pika

from CaptureThread import CaptureThread
from PortscanThread import PortscanThread
from TracerouteThread import TracerouteThread

CAPTURE = "capture"
PORTSCAN = "portscan"
TRACEROUTE = "traceroute"


def start_receiving():

    print(f"Worker: starting rabbitmq, listening for work requests")

    credentials = pika.PlainCredentials("hazzleUser", "hazzlePass")
    connection = pika.BlockingConnection(pika.ConnectionParameters(broker, credentials=credentials))
    channel = connection.channel()
    worker_queue = worker_name
    channel.queue_declare(queue=worker_queue, durable=True)
    print(f"\n\n [*] Worker: waiting for messages on queue: {worker_queue}.")

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        on_message_callback=receive_work_request, queue=worker_queue
    )

    try:
        channel.start_consuming()

    except KeyboardInterrupt:
        print(f"\n\n\n---> Worker: shutting down")
        channel.close()
        connection.close()
        exit()


def receive_work_request(capture_channel, method, _, body):

    capture_channel.basic_ack(delivery_tag=method.delivery_tag)

    work_info = json.loads(body)
    if "work_type" not in work_info:
        print(f" !!! Received work request with no work_type: {work_info}")
        return
    if work_info["work_type"] not in [CAPTURE, PORTSCAN, TRACEROUTE]:
        print(f" !!! Received work request for unknown work_type: {work_info['work_type']}")
        return

    print(f"Received work: {work_info['work_type']} full work info: {work_info}")

    process_work_request(work_info["work_type"], work_info)
    print("\n\n [*] Worker: waiting for messages.")


def process_work_request(work_type, work_info):

    if "hazzle" not in work_info:
        print(f"!!! 'hazzle' not present in work_info, cannot continue")
        return
    else:
        hazzle = work_info["hazzle"]
        print(f"---> work request received, will send results to {hazzle}")

    if work_type == CAPTURE:
        work_thread = CaptureThread(hazzle, work_info)
    elif work_type == PORTSCAN:
        work_thread = PortscanThread(hazzle, work_info)
    elif work_type == TRACEROUTE:
        work_thread = TracerouteThread(hazzle, work_info)
    else:
        print(f" !!! Invalid work_type: {work_type}, should have been caught earlier")
        return

    work_thread.start()


if __name__ == "__main__":

    if os.geteuid() != 0:
        exit("You must have root privileges to run this script, try using 'sudo'.")

    parser = argparse.ArgumentParser(description="Remote worker for hazzle")
    parser.add_argument(
        "-N",
        "--name",
        default="hazzle-worker",
        help="Name of this worker; must match what is configured on hazzle server",
    )
    parser.add_argument(
        "-B",
        "--broker",
        default="localhost",
        help="Hostname or IP address of the message broker for receiving work requests",
    )
    parser.add_argument(
        "-S", "--serialno", default="111-111-111", help="A preferably unique id of worker"
    )
    parser.add_argument(
        "-H",
        "--heartbeat",
        default="30",
        help="Frequency of heartbeats sent to hazzle server, in seconds",
    )

    args = parser.parse_args()

    worker_name = args.name
    broker = args.broker
    serial_no = args.serialno
    heartbeat = args.heartbeat

    start_receiving()
