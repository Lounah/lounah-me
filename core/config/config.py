from dataclasses import dataclass


class SocialLink:
    def __init__(self, social_network: str, username: str):
        self.social_network = social_network
        self.username = username


@dataclass
class Config:
    secret_key: str
    socialLinks: list[SocialLink]
