from fastapi import HTTPException, status


class Exceptions(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(detail=self.detail, status_code=self.status_code)

class UserAlreadyExistsException(Exceptions):
    status_code=status.HTTP_409_CONFLICT
    detail="User already exists"

class IncorrectEmailOrPasswordException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail="Incorrect email or password"


class TokenExpiredException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Token expired or not exist'


class TokenAbsentException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail='Token is missing'


class IncorrectTokenFormatException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Incorrect token format'


class UserIsNotPresentException(Exceptions):
    status_code=status.HTTP_401_UNAUTHORIZED
    detail = "User is unauthorized"

class ArticleIsAlreadyExistsException(Exceptions):
    status_code=status.HTTP_409_CONFLICT
    detail="Article already exists"

class UploadFileError(Exceptions):
    status_code=status.HTTP_409_CONFLICT
    detail = "Invalid file format. Only JPEG or PNG allowed."

class UserDontFound(Exceptions):
    status_code=status.HTTP_404_NOT_FOUND
    detail="User not found"

class ArticleIsNotFound(Exceptions):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Article not found"

class ChatNotFound(Exceptions):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Chat not found"

class MessagesNotFound(Exceptions):
    status_code=status.HTTP_404_NOT_FOUND
    detail="Messages not found"


