from review import Review
import uuid

class Post:
    def __init__(self, user, reviews, date, link, id):
        self.reviews = reviews
        self.user = user
        self.date = date
        self.link = link
        self.id = id 

        for review in self.reviews:
            review.postId = self.id
