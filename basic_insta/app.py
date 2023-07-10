from flask import Flask, request

app = Flask(__name__)

posts = [
    {"username": "Chetan", "caption": "Hello from Chetan", "id": 1, "like": 0, "comment": []},
    {"username": "Gagan", "caption": "Hello from Gagan", "id": 2, "like": 0, "comment": []}
]

id = 3

@app.route("/post", methods=["POST"])
def post():
    global id
    data = request.get_json()
    data["id"] = id
    data["like"] = 0
    data["id"] = []
    posts.append(data)
    id += 1
    return "Posted", 200

@app.route("/view", methods=["GET"])
def view():
    return posts

@app.route("/delete/<id>", methods=["DELETE"])
def delete(id):
    global posts
    temp = []
    count = 0
    for post in posts:
        if post["id"] != int(id):
            temp.append(post)
            count += 1
    posts = temp
    if count == len(posts):
        return "post not found", 400
    return "post deleted with id: {}".format(id)

@app.route("/like/<id>", methods=["PATCH"])
def like(id):
    global posts
    count = 0
    for post in posts:
        if post["id"] == int(id):
            post["like"] += 1
            count += 1
    if count == 0:
        return "post not found", 400
    return "post like incrase by 1 with id: {}".format(id)

@app.route("/comment/<id>", methods=["PATCH"])
def comment(id):
    global posts
    count = 0
    data = request.get_json()
    for post in posts:
        if post["id"] == int(id):
            post["comment"].append(data["comment"])
            count += 1
    if count == 0:
        return "post not found", 400
    return "commented on post with id: {}".format(id)

if __name__ == "__main__":
    app.run()