
class State(str):
    pass


class Node:
    def __init__(self, id, state):
        self.id = id
        self.state = state

    def set_state(self, state):
        self.state = state
    
    def get_state(self):
        return self.state

    def send_message(self, message, destination):
        if(message = "ping"):
            

class Network:
    def __init__(self, nodes, leader):
        self.nodes = nodes
        self.leader = leader

    def update_leader(self, leaderId):
        self.leader = leaderId


def main():
    pass

if __name__ == "__main__":
    main()
