class httpError401Exception(Exception):
    def __init__(self):
        Exception.__init__(self, "The call to the FamilySearch API returned a 401 error")

class httpError403Exception(Exception):
    def __init__(self):
        Exception.__init__(self, "The call to the FamilySearch API returned a 403 error")

class httpErrorUnhandledException(Exception):
    def __init__(self, errorCode):
        Exception.__init__(self, "The call to the FamilySearch API returned a " + str(errorCode) + " error")
