import time
from server import Server
class client.Client:
    def __init__(self, id, neighbors, server):
        self.id = id
        self.neighbors = neighbors
        self.server = server
        self.state = "IDLE"
        self.inbox = []
        self.last_message = None
        self.last_sender = None
        self.last_sender_index = 0
        self.message_counter = 0

    def send_message(self, server, receiver):
        self.message_counter += 1
        message = f"Hello, neighbor! ({self.message_counter})"
        send_time = time.time()
        server.receive_message(message, receiver, self.id, send_time)

    def process_message(self, message, receive_time):
        self.state = "RECEIVING"
        print(f"{self} received '{message}' from client.Client {self.last_sender} at time {int((receive_time - self.server.start_time) * 1000)}ms")
        self.last_message = message
        sender = self.last_sender
        self.last_sender = self.neighbors[self.last_sender_index]
        self.last_sender_index = (self.last_sender_index + 1) % len(self.neighbors)
        for neighbor in self.neighbors:
            if neighbor != sender:
                self.send_message(self.server, neighbor)
        if self.last_sender_index == 0:
            self.state = "DONE"
            done_time = time.time()
            print(f"{self} changed state to 'DONE' at time {int((done_time - self.server.start_time) * 1000)}ms")
        else:
            self.state = "IDLE"
            idle_time = time.time()
            print(f"{self} changed state to 'IDLE' at time {int((idle_time - self.server.start_time) * 1000)}ms")
        
        # Check if there are multiple messages received at the same time
        same_time_messages = [m for m in self.inbox if m[1] == receive_time]
        if len(same_time_messages) > 1:
            same_time_messages.sort(key=lambda m: m[2])
            chosen_message = same_time_messages[0]
            self.inbox = [chosen_message]
            print(f"{self} chose message '{chosen_message[0]}' from client.Client {chosen_message[3]} and rejected message '{same_time_messages[1][0]}' from client.Client {same_time_messages[1][3]} at time {int((receive_time - self.server.start_time) * 1000)}ms")

    def __str__(self):
        return f"client.Client {self.id}"

server = Server()
server.run_simulation()