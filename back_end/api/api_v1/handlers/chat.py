from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status, Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.schemas.chat_schema import CreateChat, ChatInvitation, CreateDM, GenericChatScheme, CreatedChat
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.services.chat_service import ChatService

chat_router = APIRouter()


@chat_router.post("/create/", summary="Create new chat", response_model=CreatedChat)
async def create_chat(data: CreateChat, user=Depends(get_current_user)):
    """ Пост для создания чата

    Args:
        data: Схема создания чата
        user: DI юзера для jwt токена

    Returns: Универсальная схема юзера

    """
    return await ChatService.create_chat(data, user)


@chat_router.post("/dm/", summary="Create direct message", response_model=CreatedChat)
async def create_dm(data: CreateDM, user=Depends(get_current_user)):
    """ Пост для создания личных сообщений

    Args:
        data: Схема создания ЛС
        user: DI юзера для jwt токена

    Returns: Универсальная схема юзера

    """
    return await ChatService.create_dm(data, user)


@chat_router.post("/invite/", summary="Invite to chat", response_model=GenericChatScheme)
async def invite_to_chat(chat_inv: ChatInvitation, user=Depends(get_current_user)):
    """ Пост для приглашения в чат

    Args:
        chat_inv: Схема приглашения в чат
        user: DI юзера для jwt токена

    Returns: Универсальная схема юзера

    """
    try:
        return await ChatService.invite_to_chat(chat_inv, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/delete/", summary="Delete message", response_model=GenericDelete)
async def delete_chat(chat_id: UUID, user=Depends(get_current_user)):
    """ Пост для удаления чата

    Args:
        chat_id: UUID чата
        user: DI юзера для jwt токена

    Returns: Универсальная схема удаления

    """
    try:
        return await ChatService.delete_chat(chat_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/remove/", summary="Delete message", response_model=GenericDelete)
async def remove_from_chat(chat: GenericChatScheme, user=Depends(get_current_user)):
    """ Пост для удаления из чата

    Args:
        chat: Универсальная схема чата
        user: DI юзера для jwt токена

    Returns: Универсальная схема удаления

    """
    try:
        return await ChatService.remove_from_chat(chat, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/remove/me/", summary="Delete message", response_model=GenericDelete)
async def remove_me_from_chat(chat_id: UUID, user=Depends(get_current_user)):
    """ Пост для удаления текущего юзера из чата

    Args:
        chat_id: UUID чата
        user: DI юзера для jwt токена

    Returns: Универсальная схема удаления

    """
    try:
        return await ChatService.remove_me_from_chat(chat_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


# @chat_router.get("/me", summary="Find all user chats")
# async def get_my_chats(user: Depends(get_current_user)):
#     """Пост для удаления текущего юзера из чата
#
#     Args:
#         user: DI юзера для jwt токена
#
#     Returns: Универсальная схема удаления
#
#     """
#     try:
#         return await ChatService.get_chats_by_user_id(user.user_id)
#     except pymongo.errors.OperationFailure:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail="User does not exist"
#         )
