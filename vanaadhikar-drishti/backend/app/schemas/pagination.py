from __future__ import annotations

from pydantic import BaseModel, Field


class PaginationParams(BaseModel):
    """Pagination parameters."""
    page: int = Field(default=1, ge=1, description="Page number (1-indexed)")
    limit: int = Field(default=20, ge=1, le=100, description="Items per page")

    @property
    def offset(self) -> int:
        """Calculate offset from page number."""
        return (self.page - 1) * self.limit


class PaginatedResponse(BaseModel):
    """Generic paginated response wrapper."""
    data: list
    total: int = Field(description="Total number of items")
    page: int = Field(description="Current page number")
    limit: int = Field(description="Items per page")
    pages: int = Field(description="Total number of pages")

    @classmethod
    def create(cls, data: list, total: int, page: int, limit: int):
        """Create paginated response."""
        pages = (total + limit - 1) // limit  # Ceiling division
        return cls(data=data, total=total, page=page, limit=limit, pages=pages)


class ClaimsPaginatedResponse(BaseModel):
    """Paginated claims response."""
    data: list
    total: int
    page: int
    limit: int
    pages: int
    filters: dict = Field(description="Applied filters")


class VillagesPaginatedResponse(BaseModel):
    """Paginated villages response."""
    data: list
    total: int
    page: int
    limit: int
    pages: int
    filters: dict = Field(description="Applied filters")


class OfficersPaginatedResponse(BaseModel):
    """Paginated officers response."""
    data: list
    total: int
    page: int
    limit: int
    pages: int
    filters: dict = Field(description="Applied filters")


class GrievancesPaginatedResponse(BaseModel):
    """Paginated grievances response."""
    data: list
    total: int
    page: int
    limit: int
    pages: int
    filters: dict = Field(description="Applied filters")
