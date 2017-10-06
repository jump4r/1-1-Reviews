from pprint import pprint

class Review:
    def __init__(self, user, date, name, link, review, size="N/A"):
        # Useful for matching post with review
        self.user = user 
        self.date = date

        self.name = name
        self.link = link
        self.review = review
        self.size = size

        self.postId = "" # Set by parent

    def print(self):
        pprint((self.name, self.link, self.review, self.user, self.size))
