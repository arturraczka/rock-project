import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.game_id = 'test'  # możemy dynamicznie pobrać to z linku, albo dynamicznie użytkownik nadaje temu nazwę
        async_to_sync(self.channel_layer.group_add)(
            self.game_id,
            self.channel_name  # to chyba bedzie nazwa/id uzytkownika, channel do polaczenie z danym uzytkownikiem
        )

        self.accept()

        # self.send(text_data = json.dumps({
        #     'type': 'connected',
        #     'message': 'you are connected',
        # }))  # to już nie jest potrzebne

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        player_choice = text_data_json['playerChoice']

        async_to_sync(self.channel_layer.group_send)(
            self.game_id,
            {
                'type': 'choice_message',  # nazwa metody
                'playerChoice': player_choice
            }
        )

    def choice_message(self, event):
        player_choice = event['playerChoice']

        self.send(text_data = json.dumps({
            'type': 'choice',
            'playerChoice': player_choice
        }))



        # print('Players choice:', player_choice)  # to się wyświetla w terminalu
        #
        # self.send(text_data=json.dumps({
        #     'type': 'choice',
        #     'playerChoice': player_choice
        # }))  # to już nie jest potrzebne, ponieważ tym komunikowaliśmy się jedynie z użytkownikiem, który wysłał
        # wiadomość (wciskał button), powyższy kod wysyła wiadomości do wszystkich w grupie (do wszystkich kanałów)
