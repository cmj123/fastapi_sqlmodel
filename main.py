from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from sqlmodel import SQLModel, Session, select
from models import Category, CategoryBase, Video, VideoBase
from database import engine 
import uvicorn
from typing import List
from datetime import datetime

# Define main app name and database session name
app = FastAPI()
session = Session(bind=engine)

# Routes
# Root folder (home page)
@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
    <h1>Home Page</h1>
    <a href='http://127.0.0.1:8000/docs'>http://127.0.0.1:8000/docs</a>
    '''

# region  video_routes
@app.post('/video', status_code=status.HTTP_201_CREATED)
async def post_a_video(video:VideoBase):
    # Create a new video object from data passed in 
    new_video = Video.from_orm(video)
    # make sure new video has a valid category id
    if not await is_category_id(new_video.category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such category")
    # Post the video
    with Session(engine) as session:
        session.add(new_video)
        session.commit()
        session.refresh(new_video)
    return new_video

# Delete one video by changing is_active to False
@app.delete('/Video/{video_id}')
async def delete_a_video(video_id: int):
    if not await is_active_video(video_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No such video")
    with Session(engine) as session:
        # Get the video to delete
        video = session.get(Video, video_id)
        # Set is_active to False, and update date last changed 
        video.is_active = False
        video.date_last_changed = datetime.utcnow()
        session.commit()
    return {'Deleted': video_id}


# endregion
# region categories_routes

# Get all categories
@app.get('/category', response_model=List[Category])
async def get_all_categories():
    with Session(engine) as session:
        statement = select(Category).order_by(Category.id.desc())
        result = session.exec(statement)
        all_categories = result.all()
    return all_categories

# Post a new category 
@app.post('/category', status_code=status.HTTP_201_CREATED)
async def post_a_category(category:CategoryBase):
    if await is_category_name(category.name):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Category name already in use")
    new_category = Category(name=category.name)
    with Session(engine) as session:
        session.add(new_category)
        session.commit()
        session.refresh(new_category)
    return new_category

# Get a specific category
@app.get('/category/{category_id}',response_model=Category)
async def get_a_category(category_id:int):
    with Session(engine) as session:
        # Alternative syntax when getting one row by id
        category = session.get(Category, category_id)
        # Return error if no such category
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such category")
    return category

# Update a specific category
@app.put('/category/{category_id}', response_model=Category)
async def update_a_category(category_id:int, category:CategoryBase):
    if not await is_category_id(category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such category")

    with Session(engine) as session:
        # Get current category object from table
        current_category = session.get(Category, category_id)
        # Replace current category name with the one just passed in
        current_category.name = category.name
        # Put back in table with new name
        session.add(current_category)
        session.commit()
        session.refresh(current_category)
    return current_category


# Delete a specific category
@app.delete('/category/{category_id}',)
async def delete_a_category(category_id:int):
    if not await is_category_id(category_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such category")
    with Session(engine) as session:
        # Get the category to delete
        category = session.get(Category, category_id)
        # Delete the category
        session.delete(category)
        session.commit()
    return {'Deleted':category_id}

# endregion

# region validators
async def is_category_id(category_id:int):
    if not session.get(Category, category_id):
        return False
    return True 

async def is_category_name(category_name:str):
    if session.exec(
        select(Category).where(Category.name == category_name)
    ).one_or_none():
        return True
    return False

# returns True if video id exists and is_active is True, otherwise return False
async def is_active_video(video_id: int):
    if session.exec(
        # Select where video id is valid and is_active is True
        select(Video).where(Video.id == video_id, Video.is_active)
        ).one_or_none():
        return True
    return False

# endregion

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)