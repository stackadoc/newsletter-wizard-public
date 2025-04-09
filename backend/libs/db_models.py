import datetime
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Union

import sqlalchemy
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String, func, Text, Float, \
    Boolean, ARRAY, UniqueConstraint, Table
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

# Association table for Source <-> NewsletterConfig many-to-many relationship
source_newsletter_config_association = Table(
    'source_newsletter_config_association',
    Base.metadata,
    Column('source_id', Integer, ForeignKey('source.id', ondelete="CASCADE"), primary_key=True),
    Column('newsletter_config_id', Integer, ForeignKey('newsletter_config.id', ondelete="CASCADE"), primary_key=True)
)


@mapper_registry.mapped
@dataclass
class Source(IdBaseMixin, TimestampBaseMixin):
    __tablename__ = "source"
    __sa_dataclass_metadata_key__ = "sa"

    name: str = field(metadata={"sa": Column(String, nullable=False)})
    type: str = field(metadata={"sa": Column(String, nullable=False)})
    config: dict = field(metadata={"sa": Column(JSONB, nullable=False)})

    # One-to-many relationship with Extract
    extracts: List["Extract"] = field(default_factory=list, metadata={"sa": relationship("Extract", back_populates="source")})

    # Many-to-many relationship with NewsletterConfig
    newsletter_configs: List["NewsletterConfig"] = field(
        default_factory=list,
        metadata={"sa": relationship("NewsletterConfig", secondary=source_newsletter_config_association, back_populates="sources")}
    )

    def __repr__(self):
        attrs = ["id", "name"]
        dict_repr = []
        for attr in attrs:
            value = getattr(self, attr, None)

            # Truncate long strings for better readability
            if isinstance(value, str) and len(value) > 100:
                value = f"{value[:100]}..."

            dict_repr.append(f"{attr}={value!r}")
        dict_repr = ", ".join(dict_repr)

        return f"{self.__class__.__name__}({dict_repr})"

@mapper_registry.mapped
@dataclass
class LLMConfig(IdBaseMixin, TimestampBaseMixin):
    __tablename__ = "llm_config"
    __sa_dataclass_metadata_key__ = "sa"

    name: str = field(metadata={"sa": Column(String, nullable=False)})
    base_url: str = field(metadata={"sa": Column(String, nullable=False)})
    api_key_name: str = field(metadata={"sa": Column(String, nullable=False)})
    model_name: str = field(metadata={"sa": Column(String, nullable=False)})
    system_prompt: str = field(metadata={"sa": Column(String, nullable=False)})
    params: dict = field(metadata={"sa": Column(JSONB, nullable=False)})

    # One-to-many relationship with NewsletterConfig
    newsletter_configs: List["NewsletterConfig"] = field(default_factory=list, metadata={"sa": relationship("NewsletterConfig", back_populates="llm_config")})

@mapper_registry.mapped
@dataclass
class NewsletterConfig(IdBaseMixin, TimestampBaseMixin):
    __tablename__ = "newsletter_config"
    __sa_dataclass_metadata_key__ = "sa"

    name: str = field(metadata={"sa": Column(String, nullable=False)})
    slug: str = field(metadata={"sa": Column(String, nullable=False)})
    image_url: str = field(metadata={"sa": Column(String, nullable=False)})

    # Foreign key for one-to-many relationship with LLMConfig
    llm_config_id: int = field(metadata={"sa": Column(Integer, ForeignKey("llm_config.id"), nullable=False)})
    llm_config: "NewsletterConfig" = field(init=False, metadata={"sa": relationship("LLMConfig", back_populates="newsletter_configs")})

    # Many-to-many relationship with Source
    sources: List["Source"] = field(
        default_factory=list,
        metadata={"sa": relationship("Source", secondary=source_newsletter_config_association, back_populates="newsletter_configs")}
    )

    # One-to-many relationship with Newsletter
    newsletters: List["Newsletter"] = field(default_factory=list, metadata={"sa": relationship("Newsletter", back_populates="newsletter_config")})

    def __repr__(self):
        attrs = ["id", "name"]
        dict_repr = []
        for attr in attrs:
            value = getattr(self, attr, None)

            # Truncate long strings for better readability
            if isinstance(value, str) and len(value) > 100:
                value = f"{value[:100]}..."

            dict_repr.append(f"{attr}={value!r}")
        dict_repr = ", ".join(dict_repr)

        return f"{self.__class__.__name__}({dict_repr})"


@mapper_registry.mapped
@dataclass
class Extract(IdBaseMixin, TimestampBaseMixin):
    __tablename__ = "extract"
    __sa_dataclass_metadata_key__ = "sa"

    extractor_type: str = field(metadata={"sa": Column(String, nullable=False)})
    config: dict = field(metadata={"sa": Column(JSONB, nullable=False)})
    content: dict = field(metadata={"sa": Column(JSONB, nullable=False)})
    content_date: datetime.datetime = field(metadata={"sa": Column(DateTime, nullable=False)})
    content_id: str = field(metadata={"sa": Column(String, nullable=False)})

    # Foreign key for one-to-many relationship with Source
    source_id: int = field(metadata={"sa": Column(Integer, ForeignKey("source.id"), nullable=False)})
    source: "Source" = field(init=False, metadata={"sa": relationship("Source", back_populates="extracts")})


    __table_args__ = (
        UniqueConstraint('source_id', 'content_id', name='uq_extract_source_id_content_id'),
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
    output_markdown: str = field(metadata={"sa": Column(Text, nullable=False)})
    output_html: str = field(metadata={"sa": Column(Text, nullable=False)})
    published_at: datetime.datetime = field(metadata={"sa": Column(DateTime, nullable=False)})

    title: str = field(metadata={"sa": Column(String, nullable=False)})
    slug: str = field(metadata={"sa": Column(String, nullable=False)})
    image_url: str = field(metadata={"sa": Column(String, nullable=False)})

    # Foreign key for one-to-many relationship with NewsletterConfig
    newsletter_config_id: int = field(metadata={"sa": Column(Integer, ForeignKey("newsletter_config.id"), nullable=False)})
    newsletter_config: "NewsletterConfig" = field(init=False, metadata={"sa": relationship("NewsletterConfig", back_populates="newsletters")})