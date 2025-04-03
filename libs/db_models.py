import datetime
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func, Text, Float, \
    Boolean, ARRAY, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_mixin, registry, relationship

mapper_registry = registry()
Base = mapper_registry.generate_base()


@declarative_mixin
@dataclass
class IdBaseMixin:
    __sa_dataclass_metadata_key__ = "sa"

    id: int = field(init=False, metadata={"sa": Column(Integer, primary_key=True)})


@declarative_mixin
@dataclass
class TimestampBaseMixin:
    __sa_dataclass_metadata_key__ = "sa"

    created_at: datetime.datetime = field(
        init=False,
        metadata={
            "sa": Column(
                DateTime,
                default=datetime.datetime.utcnow,
                nullable=False,
                server_default=func.now(),
            )
        },
    )
    last_update: datetime.datetime = field(
        init=False,
        metadata={
            "sa": Column(
                DateTime,
                default=datetime.datetime.utcnow,
                onupdate=datetime.datetime.utcnow,
                nullable=False,
                server_default=func.now(),
            )
        },
    )

@mapper_registry.mapped
@dataclass
class Extract(IdBaseMixin, TimestampBaseMixin):
    __tablename__ = "extract"
    __sa_dataclass_metadata_key__ = "sa"

    name: str = field(metadata={"sa": Column(String, nullable=False)})
    extractor_type: str = field(metadata={"sa": Column(String, nullable=False)})
    config: dict = field(metadata={"sa": Column(JSONB, nullable=False)})
    content: dict = field(metadata={"sa": Column(JSONB, nullable=False)})
    content_date: datetime.datetime = field(metadata={"sa": Column(DateTime, nullable=False)})
    content_id: str = field(metadata={"sa": Column(String, nullable=False)})

    __table_args__ = (
        UniqueConstraint('name', 'content_id', name='uq_extract_name_content_id'),
    )

@mapper_registry.mapped
@dataclass
class Newsletter(IdBaseMixin, TimestampBaseMixin):
    __tablename__ = "newsletter"
    __sa_dataclass_metadata_key__ = "sa"

    base_url: str = field(metadata={"sa": Column(String, nullable=False)})
    model_name: str = field(metadata={"sa": Column(String, nullable=False)})
    params: dict = field(metadata={"sa": Column(JSONB, nullable=False)})
    system_prompt: str = field(metadata={"sa": Column(Text, nullable=False)})
    input_text: str = field(metadata={"sa": Column(Text, nullable=False)})
    output_text: str = field(metadata={"sa": Column(Text, nullable=False)})