from fastapi import HTTPException, status

ThreadNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Тред не найден!",
)

CommentNotFount = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Комментайри не найден!"
)