from yandex_music import Client

token = "AgAAAAABRBLiAAG8Xvn5-G9dMEHEibceZEj11-w"
client = Client.from_token(token)
search = client.search("moby")

print(search)