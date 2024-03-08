from agentops import Client, ActionEvent, ErrorEvent
from typing import List


class AgentOpsClient:
    def __init__(self, api_key: str = None, org_key: str = None, tags: List[str] = ["prod"]):
        # TODO: need some way to track the calling function e.g. browse
        self.client = Client(api_key=api_key,
                             tags=tags,  # TODO: Add ORG_KEY back to Client?
                             auto_start_session=False)

    def start_session(self):
        if self.client:
            self.client.start_session()

    def record(self, event):
        if self.client:
            self.client.record(event)

    def end_session(self, video_url: None, end_state="Success"):
        if self.client:
            self.client.end_session(end_state=end_state, video=video_url)


__all__ = ['AgentOpsClient', 'ActionEvent']
