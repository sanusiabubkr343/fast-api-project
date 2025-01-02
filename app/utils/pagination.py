from math import ceil
from sqlalchemy.future import select
from sqlalchemy.orm import Session


async def paginate(db: Session, model, page_number: int, page_size: int, filters=None):

    filters = filters or []
    query = select(model).where(*filters)

    # Calculate total count
    total_result = (await db.execute(select(model).where(*filters))).scalar().count()

    # Offset and Limit for pagination
    offset = (page_number - 1) * page_size
    paginated_query = query.offset(offset).limit(page_size)

    # Execute paginated query
    result = await db.execute(paginated_query)
    paginated_data = result.scalars().all()

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
