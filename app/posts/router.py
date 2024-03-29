from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import parse_obj_as

from app.posts.dao import PostsDAO
from app.posts.models import Posts
from app.tasks.tasks import send_post_confimation_email
from app.users.dependecies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth
from app.posts.dependecies import get_response, change_rating, create_vote

router = APIRouter(
    prefix="/posts",
    tags=["Посты"],
)


@router.post("/create_post")
async def create_post(post_text: str, current_user=Depends(get_current_user)):# -> dict:
    """
    Create a new post.

    Args:
        post_text (str): The text content of the post.
        current_user: The current authenticated user.

    Returns:
        str: A success message if the post is created successfully, or an error message if the user is not logged in.
    """
    await PostsDAO.add(
        text=post_text, date=datetime.utcnow(), author_id=int(current_user.id)
    )
    post = {"post_text": post_text}
    send_post_confimation_email.delay(post,current_user.email )
    return {"message": "Post created successfully"}


@router.get("/")
async def read_top_posts():
    """
    Read the top posts.

    Returns:
        List[Post]: A list of top posts.
    """
    return await PostsDAO.find_all()


@router.put("plus_vote")
async def plus_vote(id_post, current_user=Depends(get_current_user)) -> dict:
    """
    Increase the rating of a post by 1.

    Args:
        id_post: The ID of the post.
        current_user: The current authenticated user.
    Logic:
        1. If the user has already voted to like, then raise an error.
        2. If the user has already voted to dislike, then delete the dislike vote and increase the rating by 2.
        (because if post was disliked, then it's rating was decreased by 1, so we need to increase it by 2)
        3. If the user has not voted yet, then increase the rating by 1.
    """
    response_true = await get_response(id_post, current_user.id, True)
    if response_true:
        raise HTTPException(status_code=404, detail="You already voted to like")
    response_false = await get_response(id_post, current_user.id, False)
    if response_false:
        await change_rating(id_post, 2, current_user.id, True)
    else:
        await create_vote(id_post, 1, current_user.id, True)

    return {"message": "Post rating increased by 1"}


@router.put("minus_vote")
async def minus_vote(id_post, current_user=Depends(get_current_user)) -> dict:
    """
    Decrease the rating of a post by 1.

    Args:
        id_post: The ID of the post.
        current_user: The current authenticated user.
    Logic:
        1. If the user has already voted to dislike, then raise an error.
        2. If the user has already voted to like, then delete the like vote and decrease the rating by 2.
        (because if post was liked, then it's rating was increased by 1, so we need to decrease it by 2)
    """
    response_false = await get_response(id_post, current_user.id, False)
    if response_false:
        raise HTTPException(status_code=404, detail="You already voted to dislike")
    response_true = await get_response(id_post, current_user.id, True)
    if response_true:
        await change_rating(id_post, 2, current_user.id, False)
    else:
        await create_vote(id_post, 1, current_user.id, False)

    return {"message": "Post rating decreased by 1"}
