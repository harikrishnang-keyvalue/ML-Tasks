from crewai_tools import BaseTool
from slackUtils import SlackClient
from typing import Type, Any
from pydantic.v1 import BaseModel, Field


class SlackToolSchema(BaseModel):
    """Input for SlackTool."""

    message: str = Field(
        ..., description="Mandatory message that needs to be sent to slack channel."
    )


class SlackTool(BaseTool):
    name: str = "Send slack message"
    description: str = "A tool that can be used to send slack message to a channel"
    args_schema: Type[BaseModel] = SlackToolSchema
    message: str = "Hello from CrewAI"

    def _run(self, **kwargs: Any) -> Any:
        message = kwargs.get("message", self.message)
        slackClient = SlackClient()
        return slackClient.post_message("C0761L2JX6U", message)
