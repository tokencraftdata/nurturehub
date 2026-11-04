import os

import boto3
from fastapi import HTTPException

from .schemas import ChildContext


class ChildRepository:
    def __init__(self) -> None:
        self.table = boto3.resource("dynamodb").Table(os.environ["CHILD_CONTEXT_TABLE"])

    def load_for_parent(self, parent_id: str, child_id: str) -> ChildContext:
        # The authenticated parent is part of the key. A client-supplied household
        # or user ID is never accepted, preventing cross-family reads (IDOR).
        result = self.table.get_item(Key={"parentId": parent_id, "childId": child_id})
        item = result.get("Item")
        if not item:
            raise HTTPException(404, "Child profile not found")
        return ChildContext.model_validate(item["agentContext"])
