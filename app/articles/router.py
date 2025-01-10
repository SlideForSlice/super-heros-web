import logging
from typing import Dict, List

from fastapi import APIRouter, Depends, UploadFile
from fastapi_versioning import version

from app.articles.dao import ArticleDAO

from app.articles.schema import SArticles
from app.exceptions import *
from app.users.dependencies import get_current_user
from app.users.model import User
from app.users.schemas import SAuthor

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/article",
    tags=["articles"]
)

@router.get("/all")
@version(1)
async def get_all_articles() -> List[SArticles]:
    articles = [article async for article in ArticleDAO.find_all_without_filter()]
    return articles

@router.get("/{hero_name}")
@version(1)
async def get_article_by_name(hero_name: str) -> SArticles:
    result = await ArticleDAO.find_one_or_none(name_of_hero=hero_name)

    if not result:
        raise ArticleIsNotFound

    return result

@router.get("/share/{article_id}")
@version(1)
async def share_article_by_id(article_id: int) -> str:
    result = await ArticleDAO.share_link(article_id=article_id)

    if not result:
        raise ArticleIsNotFound

    return result

@router.get("/author/{article_id}")
@version(1)
async def get_author_by_id(article_id: int) -> SAuthor:
    return await ArticleDAO.get_author(article_id=article_id)

@router.post("/")
@version(1)
async def create_article(
        name_of_hero: str,
        description: str,
        powers: str,
        solo: bool,
        current_user: User = Depends(get_current_user)
) -> SArticles:
    return await ArticleDAO.add(name_of_hero, description, powers, solo, current_user.id)

@router.patch("/edit_article/{article_id}")
@version(1)
async def edit_article_desc_by_id(article_id: int, new_description: str) -> SArticles:
    updated_article = await ArticleDAO.update(id=article_id, description=new_description)
    if not updated_article:
        raise ArticleIsAlreadyExistsException
    else:
        return updated_article

@router.patch("/{article_id}/upload_file")
@version(1)
async def add_image_by_id(article_id: int, file: UploadFile) -> SArticles:
    return await ArticleDAO.upload_file(article_id=article_id, file=file)

@router.delete("/{article_id}")
@version(1)
async def delete_article_by_id(article_id: int) -> Dict[str, str]:
    await ArticleDAO.delete(article_id)
    return {"message":"The Article was deleted"}

