class AuthValidation:
    @staticmethod
    def validate_register(data):
        errors = {}
        if not data.get("username") or len(data.get("username", "").strip()) < 3:
            errors["username"] = "Username must be at least 3 characters long."
        if not data.get("email") or "@" not in data.get("email", ""):
            errors["email"] = "Valid email address is required."
        if not data.get("password") or len(data.get("password", "")) < 6:
            errors["password"] = "Password must be at least 6 characters long."
        return errors

    @staticmethod
    def validate_login(data):
        errors = {}
        if not data.get("email"):
            errors["email"] = "Email is required."
        if not data.get("password"):
            errors["password"] = "Password is required."
        return errors
