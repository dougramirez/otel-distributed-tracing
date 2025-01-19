import logging

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry._logs import set_logger_provider


def configure_logger(name: str, version: str) -> logging.Logger:
    resource = Resource.create(
        {
            "service.name": name,
            "service.version": version,
        }
    )
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    logging.getLogger().addHandler(LoggingHandler(logger_provider=logger_provider))

    return logging.getLogger(name)


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
