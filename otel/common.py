import logging
import os
from trace import Trace

# from opentelemetry import metrics, trace
from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

# from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

# from opentelemetry.sdk.metrics import Meter, MeterProvider
# from opentelemetry.sdk.metrics.export import (
#     ConsoleMetricExporter,
#     PeriodicExportingMetricReader,
# )
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")


# logging.basicConfig(level=logging.DEBUG)


def create_resource(name: str, version: str) -> Resource:
    return Resource.create(
        {
            "service.name": name,
            "service.version": version,
        }
    )


def configure_logger(name: str, version: str) -> logging.Logger:
    logger_provider = LoggerProvider(resource=create_resource(name, version))
    set_logger_provider(logger_provider)
    logger_provider.add_log_record_processor(
        BatchLogRecordProcessor(OTLPLogExporter(endpoint=ENDPOINT, insecure=True))
    )
    logging.getLogger().addHandler(LoggingHandler(logger_provider=logger_provider))

    return logging.getLogger(name)


# def configure_meter(name: str, version: str) -> Meter:
#     reader = PeriodicExportingMetricReader(
#         OTLPMetricExporter(endpoint=ENDPOINT, insecure=True)
#     )

#     metrics.set_meter_provider(
#         MeterProvider(
#             metric_readers=[reader],
#             resource=create_resource(name, version),
#         )
#     )

#     return metrics.get_meter_provider().get_meter(
#         name=name,
#         version=version,
#     )


def configure_tracer(name: str, version: str) -> Trace:
    trace.set_tracer_provider(TracerProvider(resource=create_resource(name, version)))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(OTLPSpanExporter(endpoint=ENDPOINT, insecure=True))
    )

    return trace.get_tracer(name)
