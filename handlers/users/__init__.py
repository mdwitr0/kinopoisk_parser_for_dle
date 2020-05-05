"""
Импортирует хндлеры в логическом порядке.
Если нарушить порядок, то некотоыре хендлеры перестанут работать.
"""

from .start import dp
from .find_movie_id import dp
from .find_movie_title import dp
from .change_description import dp
from .finish import dp

__all__ = ["dp"]
