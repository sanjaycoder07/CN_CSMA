import random
class Node:
    def __init__(self, id, num_packets=10):
        self.id = id
        self.queue = num_packets          # Packets remaining to send
        self.backoff = 0
        self.collision_count = 0
        self.successful_transmissions = 0

class Channel:
    def __init__(self):
        self.busy = False
        self.current_transmitter = None
        self.transmission_time_left = 0

def simulate_csma(num_nodes=5, max_time=1000, slot_time=1, transmission_duration=5):
    Simple CSMA/CD simulation using discrete time steps.
    nodes = [Node(i, num_packets=10) for i in range(num_nodes)]
    channel = Channel()
    current_time = 0
    total_collisions = 0
    total_success = 0

    print(f"Starting CSMA/CD Simulation with {num_nodes} nodes\n")

    while current_time < max_time and any(node.queue > 0 for node in nodes):
        # Progress ongoing transmission
        if channel.transmission_time_left > 0:
            channel.transmission_time_left -= 1
            if channel.transmission_time_left == 0:
                channel.busy = False
                channel.current_transmitter = None

        # Collect nodes ready to transmit (carrier idle + no backoff)
        ready_nodes = []
        for node in nodes:
            if node.queue > 0 and node.backoff == 0 and not channel.busy:
                ready_nodes.append(node)

        # Handle transmission or collision
        if ready_nodes:
            if len(ready_nodes) == 1:
                # Successful transmission
                node = ready_nodes[0]
                node.queue -= 1
                node.successful_transmissions += 1
                node.collision_count = 0  # Reset collision counter

                channel.busy = True
                channel.current_transmitter = node
                channel.transmission_time_left = transmission_duration

                total_success += 1
                print(f"Time {current_time:4d} | Node {node.id} → SUCCESS (queue left: {node.queue})")
            else:
                # Collision occurred
                total_collisions += 1
                for node in ready_nodes:
                    node.collision_count += 1
                    # Binary Exponential Backoff (simplified)
                    max_backoff_slots = min(2 ** node.collision_count, 16)
                    node.backoff = random.randint(1, max_backoff_slots) * slot_time

                # Simulate jam signal (channel busy for short time)
                channel.busy = True
                channel.transmission_time_left = 2
                print(f"Time {current_time:4d} | COLLISION involving nodes {[n.id for n in ready_nodes]}")

        # Decrement backoff timers
        for node in nodes:
            if node.backoff > 0:
                node.backoff -= 1

        current_time += 1

    # Final statistics
    print("\n" + "="*60)
    print("SIMULATION COMPLETE")
    print("="*60)
    print(f"Total successful transmissions : {total_success}")
    print(f"Total collisions              : {total_collisions}")
    print(f"Channel utilization           : {total_success * transmission_duration / current_time:.2%}")
    print("\nPer Node Statistics:")
    for node in nodes:
        print(f"  Node {node.id}: {node.successful_transmissions:2d} successes, "
              f"final backoff collisions: {node.collision_count}")
