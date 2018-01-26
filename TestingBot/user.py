import requests
import random

ADJECTIVES = ["Ancient", 'Imaginary', 'Hissing', 'Magnificent', 'Jolly', 'Last', 'Happy', 'Little', 'Crazy', 'Secret']
NOUNS = ['City', 'Bicycle', 'Yacht', 'Tree', 'Coffin', 'Crow', 'Rose', 'Wine', 'Holiday', 'Necklace']

class User:

    def __init__(self):
        self._base_address= 'http://127.0.0.1:8000'
        self._name = 'Cinty'
        self._email = "aasdf@qwer.com"
        self._password = "@Guerrilla@12"
        self._token = None

    def _return_logger_string(self, result ,succsess, fail):
        if result == 'Ok':
            return succsess
        else:
            return fail

    def _make_post_request(self, url, data):
        resp = requests.post(self._base_address + url, data)
        h = resp.json()
        return h

    def _get_content(self):
        with open("/alice_in_wounderland.txt", "r") as file:
            file.seek(random.choice(range(139574)))
            return file.read(random.choice(range(9000)))

    def create_account(self):
        data = {'email': self._email,
                'username': self._name,
                'password': self._password,
                'repeat_password': self._password}

        responce = self._make_post_request('/sign_up/', data)

        succsess = "user with name = %s and email = %s is successfully logged in" % (self._name, self._email)
        fail = "user with name = %s and email = %s is not created - check input data" % (self._name, self._email)

        return self._return_logger_string(responce['result'], succsess, fail)

    def log_in(self):
        data = {'email': self._email,
                'password': self._password}

        responce = self._make_post_request('/sign_in/', data)

        succsess = "user with name = %s and email = %s is successfully logged in" % (self._name, self._email)

        fail = "user with name = %s and email = %s has encountered error %s" % (self._name,
                                                                                self._email,
                                                                                responce['password_error'])

        return self._return_logger_string(responce['result'], succsess, fail)

    def create_post(self):

        title = "The %s %s" % (random.choice(ADJECTIVES), random.choice(NOUNS))

        data = {'email': self._email,
                'token': self._token,
                'title': title,
                'content': self._get_content()}

        responce = self._make_post_request("/create_post/", data)

        succsess = "user with email = %s has created post with title = %s" % (self._email, title)
        fail = "user with email = %s has encountered next error = %s" % (self._email, responce['error'])

        return self._return_logger_string(responce['result'], succsess, fail)

    def like_post(self):

        post = requests.get(self._base_address + "/get_posts/").json()

        post = random.choice(post)

        data = {'email': self._email,
                'token': self._token,
                'id': post['id']}

        responce = self._make_post_request("/update_like/", data)

        succsess = "user with email = %s has update his like for post with title = %s and id = %s" % (self._email,
                                                                                                      post['title'],
                                                                                                      post['id'])
        fail = "user with email = %s has encountered next error = %s" % (self._email, responce['error'])

        return self._return_logger_string(responce['result'], succsess, fail)

if __name__ == "__main__":

    Cindy = User()

    print(Cindy.create_account())
    print(Cindy.create_post())
    print(Cindy.log_in())
    print(Cindy.create_post())
    print(Cindy.like_post())
