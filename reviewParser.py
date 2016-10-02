import re
import string
import json
import sys

def main():
    filepath = ''

    for arg in sys.argv[1:]:
        filepath=arg

    def clean(instring):
        badchars = ['(',')','!','@','#','$','%','^','&','”','’','<','>','/','?', '*',':',';','\t']
        cleaned = instring;
        for badchar in badchars:
            cleaned =cleaned.replace(badchar,'')
        return cleaned


    with open(filepath, 'r') as reviewCopy:

        reviewsData=reviewCopy.read()
        reviewCollection=[]

        rx_name = re.compile(r'Product name:.*')
        rx_review = re.compile(r'\[t\]((?:.(?!\[t\]))*)')
        rx_positive = re.compile(r'\[\+[123]\]##((?:.(?!\[))*.)')
        rx_negative = re.compile(r'\[\-[123]\]##((?:.(?!\[))*.)')

        name = rx_name.findall(reviewsData)
        titles = rx_review.findall(reviewsData)
        reviews = rx_review.findall(reviewsData.replace('\n', ''))

        for index, review in enumerate(reviews):
            reviewObject = {}
            positiveReviews = rx_positive.findall(review)
            negativeReviews = rx_negative.findall(review)
            goodblock = ''
            badblock=''
            for goodone in positiveReviews :
                goodone = goodone + clean(goodone)
                goodblock = goodblock + goodone

            for badone in negativeReviews :
                badone = clean(badone)
                badblock = badblock + badone

            reviewObject ={'id':index, 'title':titles[index],'positive':goodblock,'negative':badblock}
            reviewCollection.append(reviewObject)
        jsonOut = json.dumps(reviewCollection, sort_keys=True, indent=4)

        outbound = filepath.replace('.txt','.json')
        with open(outbound, 'w') as outfile:
            #print(outbound)
            json.dump(reviewCollection, outfile)

if __name__ == "__main__":
    main()


