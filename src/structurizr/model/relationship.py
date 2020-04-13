# Copyright (c) 2020, Moritz E. Beber.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Provide the relationship model."""


from typing import Optional

from pydantic import Field

from .element import Element
from .interaction_style import InteractionStyle
from .model_item import ModelItem


__all__ = ("Relationship",)


class Relationship(ModelItem):
    """
    Represent a relationship between two elements.

    Attributes:
        id: The ID of this relationship in the model.
        description: A short description of this relationship.
        tags: A comma separated list of tags associated with this relationship.
        source_id: The ID of the source element.
        destination_id: The ID of the destination element.
        technology: The technology associated with this relationship
                    (e.g. HTTPS, JDBC, etc.).
        interaction_style: The interaction style (synchronous or asynchronous).

    """

    source: Optional[Element] = None
    source_id: Optional[str] = Field("", alias="sourceId")
    destination: Optional[Element] = None
    destination_id: Optional[str] = Field("", alias="destinationId")
    description: Optional[str] = ""
    technology: Optional[str] = ""
    interaction_style: Optional[InteractionStyle] = Field(
        InteractionStyle.Synchronous, alias="interactionStyle"
    )
    linked_relationship_id: Optional[str] = Field("", alias="linkedRelationshipId")
