from validate_email import validate_email
from password_strength import PasswordPolicy


class Form:

    policy = PasswordPolicy.from_names(
        length=8,
        uppercase=1,
        numbers=1
    )

    @staticmethod
    def valid_email(email):
        return validate_email(email_address=email,
                              smtp_timeout=10, dns_timeout=10)

    @staticmethod
    def valid_user_name(user_name):
        return True

    @staticmethod
    def valid_password(password):
        return Form.policy.password(password=password).test()

    @staticmethod
    def evaluate_password_strength(password):
        if password is None or password.strip() == "":
            return 0
        return Form.policy.password(password=password).strength()


if __name__ == '__main__':
    print(Form.valid_email("merkava234@gmail.com"))
