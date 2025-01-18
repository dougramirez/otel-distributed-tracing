from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


# See the Python Acquire Tracer docs for more details
# https://opentelemetry.io/docs/languages/python/instrumentation/#acquire-tracer
def configure_tracer(name: str, version: str) -> trace:
    resource = Resource.create(
        {
            "service.name": name,
            "service.version": version,
        }
    )
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )

    return trace.get_tracer(name)
