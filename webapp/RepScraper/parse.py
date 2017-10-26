from pprint import pprint
import datetime, re
import keywords
import urllib.request

def parse_reddit_link(reddit_link):
    rtn = "#"
    try:
        rtn = re.search(r'\]\((.*?)\)', reddit_link).group(1)
        # rtn = re.search(r'\((.*?)\)', reddit_link).group(1)
    except:
        return rtn

    return rtn
"""
    try:
        text = urllib.request.urlopen(rtn).read()
        print(text)
        return rtn
    except urllib.error.HTTPError:
        print("Link dead asf lmao")
        return reddit_link
"""


def parse_date(timestamp):
    months = ['Janurary', 'Februrary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    date = datetime.datetime.fromtimestamp(timestamp)
    return '%s %d, %d' % (months[date.month-1], date.day, date.year)

def parse_review(split_review, post):
    from webapp.models import Review

    # Parse Header
    ordered_header = {"item": -1, "size": -1, "w2c": -1, "review": -1, "pic": -1 }
    review_start_index = -1
    total_columns = 0

    for row_num, raw_post_row in enumerate(split_review):
        split_post_row = raw_post_row.lower().split('|')
        if (len(split_post_row) < 2):
            continue

        row_start_index = row_num
        total_columns = len(split_post_row) # Because people are gonna separate their shit weird
        for index, label in enumerate   (split_post_row):
            for keyword_set in keywords.header_keywords:
                # pprint ((label, " - ", keyword_set))
                if (label.lower().strip() in keyword_set):
                    ordered_header[keyword_set[0]] = index
                    print('Match ' + label + ' with ' + keyword_set[0])
        break

    #Parse Body
    if (len(split_review) < 2):
        return False # No Values

    
    body = split_review[row_start_index+2:len(split_review)]
    print('Amount of Reviews In Total: ' + str(len(body)))

    # pprint(body)
    item_reviews = []
    for review in body:

        split_review = review.split('|')

        print("This sections column length" + str(len(split_review)))
        
        if (total_columns != len(split_review)):
            continue

        item_name, item_size, item_link, item_review, item_pic = "None Given", "None Given", "#", "None Given", "http://via.placeholder.com/250x250"

        if ordered_header["item"] != -1:
            item_name = split_review[ordered_header["item"]]
        if ordered_header["size"] != -1:
            item_size = split_review[ordered_header["size"]]
        if ordered_header["w2c"] != -1:
            item_link = split_review[ordered_header["w2c"]]
        if ordered_header["review"] != -1:
            item_review = split_review[ordered_header["review"]]
        if ordered_header["pic"] != -1:
            item_pic = split_review[ordered_header["pic"]]

        item_link = parse_reddit_link(item_link)
        item_pic = parse_reddit_link(item_pic)

        print (item_name + " + " +  item_link + "Number of sections on this specific Review: " + str(len(split_review)))
        r = Review(post=post, user=post.user, date=post.date, itemName=item_name, itemLink=item_link, itemReview=item_review, itemSize=item_size, itemPic=item_pic)
        item_reviews.append(r)

    return item_reviews