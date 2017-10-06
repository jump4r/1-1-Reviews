from pprint import pprint
from review import Review
import keywords

def parse_reddit_link(reddit_link):
    rtn = reddit_link[reddit_link.find('(')+1:reddit_link.find(')')]
    if (reddit_link == rtn):
        return null
    else:
        return rtn

def parse_review(split_review, user, date):
    # Parse Header
    ordered_header = {"item": 0, "size": 0, "w2c": 0, "review": 0}
    header = split_review[0].lower().split('|')
    for index, label in enumerate(header):
        for keyword_set in keywords.header_keywords:
            if (label in keyword_set):
                ordered_header[keyword_set[0]] = index

    #Parse Body
    if (len(split_review) < 2):
        return False # No Values

    body = split_review[2:len(split_review)]
    item_reviews = []
    for review in body:
        split_review = review.split('|')
        item_name = split_review[ordered_header["item"]]
        item_size = split_review[ordered_header["size"]]
        item_link = split_review[ordered_header["w2c"]]
        item_review = split_review[ordered_header["review"]]

        item_reviews.append(Review(user, date, item_name, item_link, item_review, item_size))

    return item_reviews