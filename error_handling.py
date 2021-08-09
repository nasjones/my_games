def integrityhandling(err):
    if 'email' in err._message():
        return "Email already registered to an account."
    return "Username already taken."
