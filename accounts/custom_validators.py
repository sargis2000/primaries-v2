import re
from django.core.exceptions import ValidationError


class NumberValidator:
    """ It's a class that validates numbers """

    def validate(self, password, user=None):
        """
        If the password doesn't contain a number, raise a ValidationError

        :param password: The password to validate
        :param user: The user model instance
        """
        if not re.findall('\d', password):
            raise ValidationError(
                "Գաղտնաբառը պետք է պարունակի առնվազն 1 թվանշան՝ 0-9:",
                code='password_no_number',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 digit, 0-9."


class UppercaseValidator:
    """ It's a validator that checks if a string is all uppercase """

    def validate(self, password, user=None):
        """
        If the password is valid, return `None`. Otherwise, return a string that describes the error

        :param password: The password that was provided by the user
        :param user: The user object that is being authenticated
        """
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                "Գաղտնաբառը պետք է պարունակի առնվազն 1 մեծատառ՝ A-Z:",
                code='password_no_upper',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 uppercase letter, A-Z."


class LowercaseValidator:
    def validate(self, password, user=None):
        """
        If the password is valid, return `None`. Otherwise, return a string that describes the error

        :param password: The password that was provided by the user
        :param user: The user object that is being authenticated
        """
        if not re.findall('[a-z]', password):
            raise ValidationError(
                "Գաղտնաբառը պետք է պարունակի առնվազն 1 փոքրատառ՝ a-z:",
                code='password_no_lower',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 lowercase letter, a-z."


class SymbolValidator:
    """ It takes a string and returns a boolean indicating whether or not the string is a valid symbol"""

    def validate(self, password, user=None):
        """
        If the password is valid, return `None`. Otherwise, return a string that describes the error

        :param password: The password that was provided by the user
        :param user: The user object that is being validated
        """
        if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                "Գաղտնաբառը պետք է պարունակի առնվազն 1 նիշ." +
                "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?",
                code='password_no_symbol',
            )

    def get_help_text(self):
        return "Your password must contain at least 1 symbol: " + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"
