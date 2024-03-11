from agentops import Client, ActionEvent, ErrorEvent
from typing import List
from opentelemetry.trace.status import Status, StatusCode
from opentelemetry import trace
from functools import wraps
import requests


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


def trace_request(func):
    """Decorator to trace HTTP requests made with the `requests` library."""

    @wraps(func)
    def wrapper_trace_request(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span("agentops-patched-request-body", kind=trace.SpanKind.CLIENT) as span:
            if 'json' in kwargs:
                span.set_attribute("http.request.body", str(kwargs['json']))
            elif 'data' in kwargs:
                span.set_attribute("http.request.body", str(kwargs['data']))

            try:
                response = func(*args, **kwargs)
                return response
            except Exception as e:
                span.set_status(Status(StatusCode.ERROR, description=str(e)))
                raise

    return wrapper_trace_request


requests.post = trace_request(requests.post)

__all__ = ['AgentOpsClient', 'ActionEvent']
