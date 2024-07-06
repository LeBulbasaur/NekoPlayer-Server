# Api Documentation

## Running the Server

To run the backend server for the Neko Player application, follow these steps:

1. **Navigate to the server directory:**

   ```sh
   cd server
   ```

2. **Set up a virtual environment (optional but recommended):**

   ```sh
   python -m venv .env
   source .env/bin/activate  # On Windows use `.env\Scripts\activate`
   ```

3. **Install server dependencies:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Start the server:**

   ```sh
   flask run
   ```

   The server should now be running on `http://127.0.0.1:5000`.

## Handling authentication

1. POST /register: Adds user with given `username` and `password` to the database. Example json:

```json
{
  "username": "user",
  "password": "testpassword"
}
```

2. POST /login: Logs user to the website, returns `access_token` using JWT. Example json:

```json
{
  "username": "user",
  "password": "testpassword"
}
```

## Handling users

Each endpoint from this point requires user to be logged. Server verifies it via Authorization header which looks like:

```json
{
  "Authorization": "Bearer example_encrypted_access_token"
}
```

1. GET /user: Returns JSON with an array of all user accounts:

- id: The ID of the user.
- username: The name of user.
- picture_path: The path to the profile picture file.

2. GET /user/id: Returns id of the currently logged user based on the given token.

3. GET /user/\<int:id>: Returns JSON with certain user data:

- id: The ID of the user.
- username: The name of user.
- picture_path: The path to the profile picture file.

4. GET /user/\<int:id>/photo: Returns user profile picture.

5. POST /user/\<int:id>/photo: Adds new profile picture for a given user. Example JSON:

```json
{
    "photo": jpg_file.jpg
}

```

6. PUT /user/\<int:id>/username: Updates username for a given user.

```json
{
  "username": "new_username"
}
```

7. PUT /user/\<int:id>/password: Updates password for a given user.

```json
{
  "new_password": "new_password"
}
```

## Handling songs

1. GET /songs: Returns a list of all songs. Each song is represented as a JSON object with the following fields:

- title: The title of the song.
- artist: The artist who performed the song.
- release_date: The release date of the song (stored as milliseconds).
- user_id: The ID of the user who added the song.
- cover_path: The path to the song's cover image.
- song_path: The path to the song file.

2. POST /songs: Used for creating new songs. It expects a multipart form with song data in JSON format, a song file, and a cover image. Example input:

```json
{
  "song_data": {
    "artist": "John",
    "release_date": "1717175079830",
    "title": "Imagine",
  },
  "cover_image": jpg_file.jpg,
  "song_file": mp3_file.mp3
}
```

3. GET /songs/cover/<cover_path>: Returns the cover image of a song. <cover_path> is the path to the cover image that you get from the cover_path field of the song object from the GET /songs endpoint.

4. GET /songs/file/<song_path>: Returns the song file. <song_path> is the path to the song file that you get from the song_path field of the song object from the GET /songs endpoint.

## Handling playlists

1. GET /playlist: Returns JSON with an array of all playlists:

   - id: The ID of the playlist.
   - title: The title of the playlist.
   - description: The description of the playlist.
   - cover_path: The path to the playlist's cover image.
   - user_id: The ID of the user who created the playlist.

2. GET /playlist/\<int:id\>: Returns JSON with the details of the specified playlist, including the songs in the playlist.

3. GET /playlist/cover/\<string:cover_path\>: Returns the cover image of a song.

4. POST /playlist: Creates a new playlist. Example JSON:

```json
{
  "title": "My Playlist",
  "cover_image": jpg_file.jpg
}
```

5. POST /playlist/song/\<int:id\>: Creates a new playlist with a song in it. Example JSON:

```json
{
  "title": "My Playlist",
  "cover_image": jpg_file.jpg
}
```

6. DELETE /playlist/\<int:id\>: Deletes the specified playlist.

7. PUT /playlist/\<int:id\>/song/\<int:song_id\>: Adds a song with given id to the specified playlist.

8. DELETE /playlist/\<int:id\>/song/\<int:song_id\>: Removes a song with given id from the specified playlist.
