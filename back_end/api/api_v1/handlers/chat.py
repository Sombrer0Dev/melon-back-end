from uuid import UUID

import pymongo.errors
from fastapi import APIRouter, HTTPException, status, Depends

from back_end.api.deps.user_deps import get_current_user
from back_end.schemas.chat_schema import CreateChat, ChatInvitation, CreateDM, GenericChatScheme
from back_end.schemas.generic_response_schema import GenericDelete
from back_end.services.chat_service import ChatService

chat_router = APIRouter()


@chat_router.post("/create", summary="Create new chat", response_model=GenericChatScheme)
async def create_chat(data: CreateChat, user=Depends(get_current_user)):
    return await ChatService.create_chat(data, user)


@chat_router.post("/dm", summary="Create direct message", response_model=GenericChatScheme)
async def create_dm(data: CreateDM, user=Depends(get_current_user)):
    return await ChatService.create_dm(data, user)


@chat_router.post("/invite", summary="Invite to chat", response_model=GenericChatScheme)
async def invite_to_chat(chat_inv: ChatInvitation, user=Depends(get_current_user)):
    try:
        return await ChatService.invite_to_chat(chat_inv, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/delete", summary="Delete message", response_model=GenericDelete)
async def delete_chat(chat_id: UUID, user=Depends(get_current_user)):
    try:
        return await ChatService.delete_chat(chat_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/remove", summary="Delete message", response_model=GenericDelete)
async def remove_from_chat(chat_id: UUID, user=Depends(get_current_user)):
    try:
        return await ChatService.remove_from_chat(chat_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )


@chat_router.post("/remove/me", summary="Delete message", response_model=GenericDelete)
async def remove_me_from_chat(chat_id: UUID, user=Depends(get_current_user)):
    try:
        return await ChatService.remove_me_from_chat(chat_id, user)
    except pymongo.errors.OperationFailure:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Message does not exist"
        )