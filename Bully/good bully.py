# https://www.geeksforgeeks.org/dsa/bully-algorithm-in-distributed-system/

from typing import List, Optional


class Node:
    counter = 0
    def __init__(self, node_id: int, largest_id: int):
        self.id = node_id
        self.is_coordinator = False
        self.has_announced = False
        self.has_elected = False
        self.largest_id = largest_id
        self.cluster: Optional[List["Node"]] = None

    def set_cluster(self, nodes: List["Node"]) -> None:
        self.cluster = nodes
    
    def get_id(self) -> int:
        return self.id

    def initiate_election(self) -> None:
        print(f"Node {self.id} initiates election.")
        assert self.cluster is not None, "Cluster not set"

        got_response = False
        # Ask all higher-ID nodes
        for node in self.cluster:
            if node.id > self.id and not self.has_elected:
                if node.receive_election_message(self):
                    got_response = True
                    break
                if node.get_id() == self.largest_id:
                    self.has_elected = True

        # If nobody higher responded, I win
        if not got_response and not self.has_announced and not self.has_elected:
            self.become_coordinator()
            self.announce_coordinator()
            self.has_announced = True
        # Else: do nothing; a higher node will continue and eventually announce

    def receive_election_message(self, sender: "Node") -> bool:
        print(f"Node {self.id} receives election message from Node {sender.id}")
        Node.counter += 1
        print(f"Counter: {Node.counter}")
        if self.id > sender.id:
            print(f"Node {self.id} responds to Node {sender.id}")
            sender.receive_response(self)
            # Per bully: a higher node that responded now runs its own election
            self.initiate_election()
            return True
        return False

    def receive_response(self, sender: "Node") -> None:
        print(f"Node {self.id} receives response from Node {sender.id}")
        Node.counter += 1
        print(f"Counter: {Node.counter}")

    def become_coordinator(self) -> None:
        print(f"Node {self.id} becomes the coordinator.")
        self.is_coordinator = True

    def set_coordinator(self, coordinator: "Node") -> None:
        print(f"Node {self.id} acknowledges Node {coordinator.id} as coordinator.")
        Node.counter += 1
        print(f"Counter: {Node.counter}")

    def announce_coordinator(self) -> None:
        assert self.cluster is not None
        for node in self.cluster:
            node.is_coordinator = False
        self.is_coordinator = True
        # (Optional) notify others
        for node in self.cluster:
            if node.id != self.id:
                node.set_coordinator(self)

# --- Demo ---
if __name__ == "__main__":
    largest_id = 100  # Assuming IDs are 1 to 5
    nodes = [Node(i, largest_id) for i in range(1, largest_id + 1)]
    for n in nodes:
        n.set_cluster(nodes)

    # Simulate: Node 3 detects failure and starts election
    nodes[0].initiate_election()  # Node with id=3
    print(Node.counter)
