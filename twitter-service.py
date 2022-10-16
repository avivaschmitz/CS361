# Lily Zhou
# CS361 Microservice: Returns a url address to post a tweet on twitter.com

while True:
    pass

    file = open("signal.txt", "r")  # Checks to see if a request was made.
    request = file.read()

    request = request.split("|")  # splits the request into two items: ["tweet", "the contents of the tweet"]
    if request[0] == "tweet":
        content = request[1]
        url = f"https://twitter.com/intent/tweet?text={content}"  # the content part will autofill in the tweet box using the user's request
        file = open("url.txt", "w")
        file.write("")  # clears the txt file first
        file.write(url)  # writes url link in the url.txt file

    file.close()