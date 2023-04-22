import time


class Server:
    def __init__(self):
        self.start_time = time.time()
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def receive_message(self, message, receiver, sender, send_time):
        receive_time = time.time()
        for client in self.clients:
            if client.id == receiver:
                client.inbox.append((message, receive_time, sender, send_time))
                break

    def process_messages(self):
        for client in self.clients:
            if client.state == "RECEIVING":
                continue
            if client.inbox:
                message, receive_time, sender, send_time = client.inbox.pop(0)
                client.process_message(message, receive_time)
                client.last_sender = sender
                client.last_sender_index = client.neighbors.index(sender)
        for client in self.clients:
            if client.state == "SENT":
                client.state = "RECEIVING"
    
    def run_simulation(self):
        clients = [
            Client(1, [2], self),
            Client(2, [1, 4, 3], self),
            Client(3, [2, 5], self),
            Client(4, [2, 5], self),
            Client(5, [3, 4], self)
        ]
        for client in clients:
            self.add_client(client)
        initiator = int(input("Choisissez l'initiateur (1-5) : "))
        clients[initiator-1].send_message(self, clients[initiator-1].neighbors[0])
        while not all(client.state == "DONE" for client in clients):
            self.process_messages()
        print("Simulation terminée")
        total_messages = sum(client.message_counter for client in clients)
        print(f"Nombre total de messages envoyés : {total_messages}")