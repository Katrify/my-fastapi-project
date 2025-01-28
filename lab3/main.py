##########################################################################################################
#   In this activity, we are going to try to use an external API to manipulate and play with.
#   Our end goal here is to
#   1. Understand how to get values from an API
#   2. Use the values from the API and manipulate it accordingly using Python
#   3. Create another API that utilizes multiple APIs
#   4. Return data from Python into a valid JSON string.
#

# requests is a module that enables users to perform API calls
# You can download this by doing pip install requests (or just install the requirements.txt file that comes with this code.)
import requests

# json is native module in Python that enables users to parse JSON strings into Python data types (list, dictionary, tuples, etc.)
# and vice versa. This is a native module so there is no need to install this as this comes with the installation of Python
import json 

# FastAPI imports
from fastapi import FastAPI
from typing import Optional

# Instantiates the FastAPI class
app = FastAPI()

# Example # 1: We are trying to get the values from an external API. We used a query parameter to make the API scalable to different API calls
# to the external API
@app.get("/posts/")
def get_posts(postId: Optional[int] = None):
    if postId is None:
        posts = requests.get('https://jsonplaceholder.typicode.com/posts')
        response = json.loads(posts.text)
    else:
        posts = requests.get(f'https://jsonplaceholder.typicode.com/posts/{postId}')
        response = json.loads(posts.text)
    
    return response

@app.get("/comments/")
def get_comments(postId: Optional[int] = None):
    if postId is None:
        comments = requests.get('https://jsonplaceholder.typicode.com/comments')
        response = json.loads(comments.text)
    else:
        comments = requests.get(f'https://jsonplaceholder.typicode.com/comments/?postId={postId}')
        response = json.loads(comments.text)
    
    return response

# Example #2: : We are trying to get the values from an external API. We used a path parameter to ensure that we are requiring the parameter.
# After calling the API, we format the data according to our preference by accessing the values of the JSON string.
@app.get("/formatted_posts/{userID}")
def get_post_then_format_according_to_user(userID: Optional[int] = None):
    # We get the data from the get_post function above. In this case, we are calling it as a function.
    posts = get_posts()

    # Create the new format of data that we want to present
    data = {"userID": userID, "posts": []}

    # Enumerate the posts, then filter the user ID based on the parameter
    # Then add it to the posts value
    for idx, u in enumerate(posts):

        # Take note here that in Python, to get the value of a key in a dictionary, we use the [] notation
        # where in the string inside the [] is the key of the value in the dictionary.
        if u['userId'] == userID:
            data["posts"].append({
                "post_title": u["title"],
                "post_body": u["body"],
            })
    return data

@app.get("/formatted_comment/{postID}")
def get_post_then_format_according_to_user(postID: int):
    # We get the data from the get_comments function above. In this case, we are calling it as an API
    req = requests.get(f'http://127.0.0.1:8000/comments/?postId={postID}')
    comments = json.loads(req.text)

    # Create the new format of data that we want to present
    data = {"post_id": postID, "comments": []}

    # Enumerate the comments, then filter the post ID based on the parameter
    # Then add it to the comments value
    for idx, c in enumerate(comments):
        # Take note here that in Python, to get the value of a key in a dictionary, we use the [] notation
        # where in the string inside the [] is the key of the value in the dictionary.
        if c['postId'] == postID:
            data["comments"].append({
                "commenter_email": c["email"],
                "commenter_name": c["name"],
                "comment": c["body"],
            })
    return data

############################################################################################################
##      PUT YOUR LAB ACTIVITY 4 ANSWER BELOW
##      - Create a new API that has the following specs:
##              Endpoint: /detailed_post/{userID}
##              Method: GET
##      - Given the userID, you should show all the post of that specific user and all comments per each post.
##      - Use necessary key names based on the value to be outputted.
############################################################################################################
@app.get("/detailed_post/{userID}")
def get_detailed_post(userID: int):

    #Ife-fetch yung mga Post para sa mga binigay na User ID
    posts = get_posts()
    # Create the new format of data that we want to present
    #Eto din yung part ng Output kung saan makikita natin yung User ID pati yung post na naglalaman nung mga TITLE/BODY/COMMENTS/ETC.
    detailed_data = {"userID": userID, "posts": []}

    # Ifi-filter ang user id based sa parameter 
    # Then i-a-add ito sa post value
    for p in posts:
        if p['userId'] == userID:
            # Ife-fetch yung mga comments para sa bawat post
            req = requests.get(f'http://127.0.0.1:8000/comments/?postId={p["id"]}')
            comments = json.loads(req.text)
            #Eto na yung part ng JSON format na makikita natin sa output, lahat ng TITLE/BODY/COMMENTS/NAME/EMAIL/
            #Ay nanggaling doon sa http link.(EXTERNAL API) na ige-get dipende sa given na User ID so specific lang
            #Ang mga users na lalabas.
            post_data = {
                "post_title": p["title"],
                "post_body": p["body"],
                "comments": []
            }

            #I-a-add(append) yung mga comments doon sa post
            #Comments na nagko-contain nung mga info na makikita din sa output
            for c in comments:
                post_data["comments"].append(
                    {
                    "post_id": p["id"],
                    "id": c["id"],
                    "name": c["name"],
                    "email": c["email"],
                    "comment": c["body"],
                }
                )

  
            #Lahat ng process na nasa taas na pag-combine ang comments sa post is mapupunta or ma-a-add(append) sa detailed_data
            #na syang itatawag by user ID
            detailed_data["posts"].append(post_data)

    # I-re-return yung final detailed_data bilang isang JSON format once na ni-run yung code.
    return detailed_data