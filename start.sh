docker run --rm --name jaeger \
  -e COLLECTOR_OTLP_ENABLED=true \
  -p 16686:16686 \
  -p 4317:4317 \
  -p 4318:4318 \
  jaegertracing/all-in-one:latest &
uvicorn bands.main:app --reload --port 8000 & 
uvicorn reviews.main:app --reload --port 8080 &