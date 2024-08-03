from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = [
    {"title": "Hello", "content": "World!! ", "published": True, "id": 222},
    {"title": "Fast", "content": "API", "published": False, "id": 999},
]

# Get all posts
@app.get("/posts")
def get_all_posts():
    return {"data": my_posts}

# Post a new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict["id"] = len(my_posts) + 1
    my_posts.append(post_dict)
    return {"data": post_dict}

#get lastest post
@app.get("/posts/latest")
def get_latest_post():
    return {"data": my_posts[-1]}

# Get a post by id
@app.get("/posts/{post_id}")
def get_post_by_id(post_id: int):
    post = find_post(post_id)
    if post is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with ID {post_id} not found")
    return {"data": post}


# Delete a post by id
@app.delete("/posts/{post_id}")
def delete_post_by_id(post_id: int):
    post_index = find_index_post(post_id)
    if post_index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with ID {post_id} not found")
    deleted_post = my_posts.pop(post_index)
    return {"message": f"Post with ID {post_id} has been deleted"}

# Update a post by id
@app.put("/posts/{post_id}")
def update_post_by_id(post_id: int, post: Post):
    post_index = find_index_post(post_id)
    if post_index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Post with ID {post_id} not found")
    post_dict = post.dict()
    post_dict["id"] = post_id
    my_posts[post_index] = post_dict
    return {"message": f"Post with ID {post_id} has been updated"}


def find_index_post(id):
    for index, post in enumerate(my_posts):
        if post["id"] == id:
            return index
    return None


def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post
    return None


