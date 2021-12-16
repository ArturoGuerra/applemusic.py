
from applemusic import Client, client
from applemusic.errors import AuthError, APIError

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6Iks2Q0tROVk4MlMifQ.eyJpc3MiOiI5UjJVUEpWNkozIiwiZXhwIjoxNjQ3OTM0MjQyLCJpYXQiOjE2MzQ5NzA2NDJ9.UM4VtBNbRb-LlMxrkPMUQRSuU-tgVNqaSrStSxwWsHn0Is8cX6MNo4MC4SGYG03zTh95HpZYJVabUtl0VlG5OQ"
client = Client(token)
# m.authorize("AvzLdxFZPFbSZ9XwwJsnIvrWWiBLjQl9ULJ4tXcfqPuxcPF0cBgTKjzuR15Xk5idgolkgQRaeB9vwKtrpjW++/nJFDql0r6S0jnzvLD6UkeT5HnUyklnyphnL1yhM8LoPKkCsWHM39auqwk9FOt2ewYolAVU68k5XNiC3voL6Ks5mnpMdwN0t9HirKCLmqkfOMtAnlfS08a+WrF5m+ZnODlnvDeFxqOEFeBtuRUUBhE2e9ZNAQ==")
try:
    album = client.album("310730204")
    print(album.relationships.artists.data)
except APIError as e:
    print(e.code, e.message)
