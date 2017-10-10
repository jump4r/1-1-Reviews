from pprint import pprint

import keywords
import re

def parse_reddit_link(reddit_link):
    try:
        rtn = re.search(r'\[link\]\((.*?)\)', reddit_link).group(1)
        print(rtn)
        return rtn
    except:
        return reddit_link

def parse_review(split_review, post):
    from webapp.models import Review

    # Parse Header
    ordered_header = {"item": -1, "size": -1, "w2c": -1, "review": -1}
    review_start_index = -1

    for row_num, raw_post_row in enumerate(split_review):
        split_post_row = raw_post_row.lower().split('|')
        if (len(split_post_row) < 2):
            continue

        row_start_index = row_num
        for index, label in enumerate(split_post_row):
            for keyword_set in keywords.header_keywords:
                if (label.lower().strip() in keyword_set):
                    ordered_header[keyword_set[0]] = index
                    print('Match ' + label + ' with ' + keyword_set[0])
        break

    #Parse Body
    if (len(split_review) < 2):
        return False # No Values

    body = split_review[row_start_index+2:len(split_review)]
    item_reviews = []
    for review in body:
        split_review = review.split('|')
        item_name = split_review[ordered_header["item"]] if ((ordered_header["item"]) != -1) else 'None Given'
        item_size = split_review[ordered_header["size"]] if ((ordered_header["size"]) != -1) else 'N/A'
        item_link = split_review[ordered_header["w2c"]] if ((ordered_header["w2c"]) != -1) else 'None Given' 
        item_review = split_review[ordered_header["review"]] if ((ordered_header["review"]) != -1) else 'None Given'

        item_link = parse_reddit_link(item_link)

        r = Review(post=post, user=post.user, date=post.date, itemName=item_name, itemLink=item_link, itemReview=item_review, itemSize=item_size)
        item_reviews.append(r)

    return item_reviews