import requests

def main():
    ALBUMS_URI = 'localhost:5000/albums'

    # Gets list of albums
    list_response = requests.get(ALBUMS_URI).json()
    print(list_response['data'])

    # Creates a new album
    new_album_response = requests.post(
        url=ALBUMS_URI,
        data=dict(
            name='Surrenda',
            author='Manu',
            year=2008)
    ).json()
    print(f"new album: {new_album_response['message']}")

    # Gets a new list of albums
    list_response = requests.get(ALBUMS_URI).json()
    print(list_response['data'])


if __name__ == '__main__':
    main()