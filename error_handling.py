def integrityhandling(err):
    """Handles the errors thrown when attempting to add to the db"""
    if 'email' in err._message():
        return "Email already registered to an account."
    return "Username already taken."
