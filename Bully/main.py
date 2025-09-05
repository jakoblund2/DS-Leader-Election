
class state(str)



class Node:
    def __init__(self, id):
        self.id = id
        self.sstate = state
    
    def send_message(self, message, destination):
        pass

class Network:
    def __init__(self,nodes,leader):
        self.nodes = nodes
        self.leader = leader
    def update_leader(self,leaderId):
        sel


def main():
    pass

if __name__ == "__main__":
    main()