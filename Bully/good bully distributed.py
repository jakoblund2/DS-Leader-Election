import requests
import http.server
import socketserver
from typing import List

class Node:
    def __init__(self, node_id: int):
        self.handler = MyRequestHandler()
        self.id = node_id
        self.is_coordinator = False
        self.has_coordinator = False
        self.cluster_ids = list(range(0, 6))
        self.leader_id = None

    def initiate_election(self) -> None:
        got_response = False
        # Ask all higher-ID nodes
        for node_id in self.cluster_ids:
            if not self.has_coordinator and node_id > self.id:
                try:
                    r = requests.get(f"http://localhost:500{node_id}/election/{self.id}")
                    got_response = True
                except requests.exceptions.ConnectionError:
                    continue

        # If nobody higher responded, I win
        if not got_response:
            self.become_coordinator()
            self.announce_coordinator()
        # Else: do nothing; a higher node will continue and eventually announce

    def receive_election_message(self, sender: "Node") -> bool:
        if self.id > sender.id:
            # Per bully: a higher node that responded now runs its own election
            self.initiate_election()
            return True
        return False

    def become_coordinator(self) -> None:
        self.is_coordinator = True

    def set_coordinator(self, coordinator: "Node") -> None:
        self.has_coordinator = True

    def announce_coordinator(self) -> None:
        assert self.cluster is not None
        for node in self.cluster:
            node.is_coordinator = False
        self.is_coordinator = True
        # (Optional) notify others
        for node in self.cluster:
            if node.id != self.id:
                node.set_coordinator(self)
    
    def check_leader(self):
        try:
            r = requests.get(f"http://localhost:500{self.leader_id}/heartbeat")
        except requests.exceptions.ConnectionError:
            self.has_coordinator = False
            self.initiate_election()
    
    # somehow respond alive as leader
    def heartbeat(self):
        pass

    # som sorta runtime loop thingy
    def update(self):
        pass
        
    def election_server(self):
        with socketserver.TCPServer(("", 80), self.handler) as httpd:
            httpd.serve_forever()
            
class MyRequestHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, node_id):
        self.node_id = node_id

    # Recieve election message
    def do_GET(self):
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(self.node_id)

        