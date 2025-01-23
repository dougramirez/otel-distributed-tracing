import logging

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import Meter, MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def create_resource(name: str, version: str) -> Resource:
    resource = Resource.create(
        {
            "service.name": name,
            "service.version": version,
        }
    )

    return resource


def configure_logger(name: str, version: str) -> logging.Logger:
    resource = create_resource(name, version)
    logger_provider = LoggerProvider(resource=resource)
    set_logger_provider(logger_provider)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter()))
    logging.getLogger().addHandler(LoggingHandler(logger_provider=logger_provider))

    return logging.getLogger(name)


def configure_meter(name: str, version: str) -> Meter:
    resource = create_resource(name, version)
    reader = PeriodicExportingMetricReader(OTLPMetricExporter())
    metrics.set_meter_provider(
        MeterProvider(metric_readers=[reader], resource=resource)
    )

    return metrics.get_meter_provider().get_meter(name)


# See the Python Acquire Tracer docs for more details
# https://opentelemetry.io/docs/languages/python/instrumentation/#acquire-tracer
def configure_tracer(name: str, version: str) -> trace:
    resource = create_resource(name, version)
    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter())
    )

    return trace.get_tracer(name)
