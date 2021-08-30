# musicfy 004_views

## routes

Artists

```py
GET Retrieve Artist http://127.0.0.1:8000/api/artists/1

GET List Artists http://127.0.0.1:8000/api/artists

POST Create Artist http://127.0.0.1:8000/api/artists/
{
	"name": name,
	"formed_in": formed_in,
	"status": status,
	"musics": [
		{
			"title": title
		},
		{
			"title": title
		}
	]
}

PATCH http://127.0.0.1:8000/api/artists/1
{
	"name": name,
	"formed_in": fomed_in,
	"status": status
}

DELETE http://127.0.0.1:8000/api/artists/1
```

Playlists

```py
POST http://127.0.0.1:8000/api/playlists/
{
	"title": title,
	"songs": [
		{
			"title": title,
			"artist": {
				"name": name,
				"fomed_in": fomed_in,
				"status": status
			}
		},
		{
			"title": title,
			"artist": {
				"name": name,
				"fomed_in": fomed_in,
				"status": status
			}
		},
        ...
	]
}

GET http://127.0.0.1:8000/api/playlists/
```
