"""Module which checks client info used in different process"""

from re import compile
from passlib.hash import pbkdf2_sha256 as hash

# RegEx constants for validating different inputs
EMAIL_REGEX = compile(r"[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\..[a-zA-Z0-9]+")
USERNAME_REGEX = compile(r"[a-zA-Z0-9-_ ]+")
PASSWORD_REGEX = compile(r".*[A-Z]+.*[!@#$%^&*()_+-=]+.*\d+.*")


class Validator:
    """Class that validates all user data used durin log in and sign up process"""

    def __init__(self, data_base):
        """Initilizes Validator class, in which DataBase object is created"""
        self._DB = data_base

    def sign_up(self, data):
        """Function to validate user data from Sign Up page

            Args:
                username -- entered login
                email -- entered email
                password -- entered password
                repeated_password -- repeated password



            Returns:
                True, None - if validation is successful. True is status of operation, None is error message
                False, Tuple - if validation is failed, returns Status False, and error messages

         """

        username, email, password, repeated_password = \
            data["username"], data["email"].lower(), data["password"], data["repeat_password"]

        # Validates email, and receives status and error message
        if not self._DB.contains("user", {"email":email}):
            email_result, email_message = self._validate_field(email, EMAIL_REGEX)
        else:
            email_result, email_message = False, "Specified email is already registered"

        # Validates login, and receives status and error message
        username_result, username_message = self._validate_field(username.lstrip().rstrip(), USERNAME_REGEX)

        # Validates password, and receives status and error message
        password_result, password_message = self._validate_field(password, PASSWORD_REGEX)

        # Validates that repeated password is same as first password
        if password == repeated_password:
            repeat_password_result, repeat_password_message = True, "Ok"
        else:
            repeat_password_result, repeat_password_message = False, "Passwords do not match"

        # if every validation is successful - adds entry in DB and returns JSON with result OK
        if email_result and username_result and password_result and repeat_password_result:
            self._DB.add_entry('user', {"email": email,
                                         "username": username.lstrip().rstrip(),
                                         "password": hash.hash(password)})
            return {"result": "Ok"}

        # if at least one validation is not successful - then returns error messages and result Fail
        else:
            return {"result": "Fail", "email_error": email_message, "displayNameError": username_message,
                    "password_error": password_message, "repeatedPasswordError": repeat_password_message}

    def sign_in(self, data):
        """Method to validate data submitted by user during sign in process

            Args:
                email -- email submitted by user
                password -- passwordsubmittedd by user

            Returns:
                Dictionary with "result" and "password_error":
                False, Message - If validation of data is not successful - then returns status fail and error message
                True, None - If validation is successful - returns status True and None as error message

         """

        data["email"].lower(), data["password"]

        entry = self._DB.get_entry('user', {"email": data["email"].lower()})
        if not entry['email'] or not hash.verify(data["password"], entry['password']):
            return {"result": "Fail", "password_error": "Username or password are not correct"}
        else:
            return {"result": "Ok", "email": entry["email"], "id": entry['id']}

    def update_user(self, data):
        pass

    def _validate_field(self, field, reg_ex):
        """Private function to validate any value against provided regular expression"""

        fullmatch = reg_ex.fullmatch(field)

        if fullmatch:
            return True, "Ok"
        else:
            return False, "%s is not correct value" % field
