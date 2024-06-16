class PasswordWithSpacesError(ValueError):
    def __init__(self):
        super().__init__("A senha não pode conter espaços.")


class PasswordWithoutNumberError(ValueError):
    def __init__(self):
        super().__init__("A senha deve conter pelo menos um número.")


class PasswordWithoutUppercaseError(ValueError):
    def __init__(self):
        super().__init__("A senha deve conter pelo menos uma letra maiúscula.")


class PasswordWithoutLowercaseError(ValueError):
    def __init__(self):
        super().__init__("A senha deve conter pelo menos uma letra minúscula.")


class PasswordWithoutSpecialCharacterError(ValueError):
    def __init__(self):
        super().__init__("A senha deve conter pelo menos um caractere especial.")
