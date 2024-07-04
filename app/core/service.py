from app import services


class Service:
    def __init__(self):
        self.jwt = services.JWTService()
