from yandex_music import Client

token = ""
client = Client.from_token(token)
search = client.search("moby")

print(search)