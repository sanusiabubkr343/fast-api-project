from math import ceil
from pydantic import BaseModel
from sqlalchemy.orm import Query
from sqlalchemy.ext.asyncio import AsyncSession


def paginate(query: Query, page_number: int, page_size: int):
    """
    Paginates a SQLAlchemy query.
    """
    # Calculate total count
    total_result = query.count()

    # Offset and Limit for pagination
    offset = (page_number - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)

    # Execute paginated query
    paginated_data = paginated_query.all()

    # Total pages
    total_page_number = ceil(total_result / page_size)

    # Return pagination response
    return {
        "data": paginated_data,
        "current_result": len(paginated_data),
        "total_result": total_result,
        "current_page_number": page_number,
        "total_page_number": total_page_number,
    }


class PaginationMeta(BaseModel):
    current_page: int
    total_pages: int
    total_results: int
