from .errors import APIError

def auth_check(func):
    def inner(self, *args, **kwargs):
        # TODO: Adds jwt validation and prompt to renter if expired or invalid
        if self.usertoken != None:
            return func(self, *args, **kwargs)
        # TODO: If JWT is invalid we should either throw a more specific error or kill the program as a whole
        raise APIError(401, "Unauthorized")
    return inner