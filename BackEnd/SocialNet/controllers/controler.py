from controllers.validation import Validator
from controllers.data_base_handler import DataBaseHandler
from controllers.token_controller import TokenController
from controllers.post_controller import PostController
from datetime import date

def token_validation(function):

    def wrapper(self, data):

        token = data.pop('token')
        email = data.pop('email')

        output = self.validate_token(token, email)

        return function(self, data, output)

    return wrapper

def input_validation(function):

    def wrapper2(self, data, val_output=None):

        if self.validate_input(data, function.__name__):
            return function(self, data, val_output)

        else:
            return {"result": 'Failed', "error":'not all required data is present'}

    return wrapper2


class Controler():
    """Level of abstraction which functions as a overall controller.
    It will call appropriate functions and models based of view and user input """

    def __init__(self):
            """ Initialize function, creates instances on needed classes"""

            # creates data base orm class
            self._db = DataBaseHandler()

            # creates class that handle user validation
            self._validator = Validator(self._db)

            # imports secret key from config file and creates token controller class instance
            from SocialNet.settings import SECRET_KEY
            self._jwt_token_creator = TokenController(SECRET_KEY)

            # create Projects and Task handler instance
            self._post_handler = PostController(self._db)

            self._input_validation_dict = {"sign_up": ['username', 'email', 'password', 'repeat_password'],
                                           "sign_in": ['email', 'password'],
                                           "create_post": ["title", "content", "token", "email"],
                                           "delete_post": ["id", "token", "email"],
                                           "edit_post": ['id', "token", "email"],
                                           "update_like": ['id', "token", "email"]
                                           }

    def validate_token(self, token, email):
        """ Validates JWR token and returns ID of the user if validation is successful

            Params:
                    token - JWT encoded token
                    username - name of the user

            Returns:
                    ID of the user if validation is successful
                    False if validation is failed

            Important note:
                    This should be realized as a decorator function, so all functions would not have to copy-paste
                    basic function with validation. This will be implemented in future version
        """

        token_dict = self._jwt_token_creator.decode_token(bytes(token, "UTF-8"))
        entry = self._db.get_entry('user', {"email": email}, True)

        if entry.email == token_dict["email"] and entry.id == token_dict["id"]:
            # is provided user name and user id is same as in decoded token that verification is successful
            return entry

        else:
            return False

    def validate_input(self, data, name):

        for required_key in self._input_validation_dict[name]:
            if required_key not in data.keys():
                return False
            return True


    # User Authentication functions

    @input_validation
    def sign_up(self, data):
        """Calls validation function of validator class and returns response

            Params:
                    display_name - username entered by user
                    email - email address entered by user
                    password - password entered by user
                    repeted_password - repeat of the password entered by user

            Returns:
                    response item returned by validator sign_up function

        """

        response = self._validator.sign_up(data)
        return response

    @input_validation
    def sign_in(self, data):
        """Calls sign_in function of validator class, and on success adds jwt token to the response object

            Params:
                    email - email address entered by user
                    password - password entered by user
            Returns:
                    response item dict containing status, error, token and username keys

        """

        response = self._validator.sign_in(data)
        if response["result"] == "Ok":
            id = response.pop('id')
            response["token"] = self._jwt_token_creator.create_token(response["email"], id)

        return response

    # Posts handler functions - functions to create, update and get and like posts

    @token_validation
    @input_validation
    def create_post(self, data, val_output):
        if not val_output:
            return {"result": "Fail", "error": "User is not authorized to perform this action", "error_code": 401}

        else:
            data['owner'] = val_output
            return self._post_handler.create_post(data)

    def get_posts(self, data=None):
        return self._post_handler.get_posts(data)

    @token_validation
    @input_validation
    def delete_post(self, data, val_output):
        if not val_output:
            return {"result": "Fail", "error": "User is not authorized to perform this action", "error_code": 401}

        else:
            return self._post_handler.delete_post(data)

    @token_validation
    @input_validation
    def edit_post(self, data, val_output):
        if not val_output:
            return {"result": "Fail", "error": "User is not authorized to perform this action", "error_code": 401}

        else:
            data['owner'] = val_output
            return self._post_handler.edit_post(data)

    @token_validation
    @input_validation
    def update_like(self, data, val_output):
        if not val_output:
            return {"result": "Fail", "error": "User is not authorized to perform this action", "error_code": 401}

        else:
            data['user id'] = val_output.id
            return self._post_handler.update_like(data)