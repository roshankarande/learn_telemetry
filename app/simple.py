from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import (
    OTLPMetricExporter,
)
from opentelemetry.metrics import (
    get_meter_provider,
    set_meter_provider,
)
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

exporter = OTLPMetricExporter(endpoint="http://host.docker.internal:4366",insecure=True)
reader = PeriodicExportingMetricReader(exporter)
provider = MeterProvider(metric_readers=[reader])
set_meter_provider(provider)


meter = get_meter_provider().get_meter("getting-started", "0.1.2")

# Counter
counter = meter.create_counter("counter", description="----------This is a simple counter--------------")
counter.add(1)


# UpDownCounter
updown_counter = meter.create_up_down_counter("updown_counter", description="----------This is an updown counter-----------")
updown_counter.add(1)
updown_counter.add(-5)
