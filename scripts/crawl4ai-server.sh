#!/bin/bash
# crawl4ai-server.sh - Manage crawl4ai Docker container for distributor-inspector

set -e

CONTAINER_NAME="crawl4ai"
IMAGE_NAME="unclecode/crawl4ai:latest"
PORT=11235

# Check Docker availability
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed. Please install Docker first."
    exit 1
fi

if ! docker info &> /dev/null 2>&1; then
    echo "Error: Cannot connect to Docker daemon. Is Docker running? Do you have permission?"
    exit 1
fi

start() {
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "✓ crawl4ai server already running on port ${PORT}"
        exit 0
    fi

    echo "Starting crawl4ai server..."
    docker run -d \
        --name "${CONTAINER_NAME}" \
        -p "${PORT}:${PORT}" \
        "${IMAGE_NAME}"

    # Wait and verify container started successfully
    sleep 2
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "Error: Container failed to start. Check logs: docker logs ${CONTAINER_NAME}"
        exit 1
    fi

    echo "✓ crawl4ai server started on port ${PORT}"
    echo "  API endpoint: http://localhost:${PORT}/crawl"
}

stop() {
    if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "✓ crawl4ai server not running"
        exit 0
    fi

    echo "Stopping crawl4ai server..."
    docker stop "${CONTAINER_NAME}" && docker rm "${CONTAINER_NAME}"
    echo "✓ crawl4ai server stopped"
}

status() {
    if docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
        echo "✓ crawl4ai server running on port ${PORT}"
        echo "  Container: ${CONTAINER_NAME}"
        echo "  API endpoint: http://localhost:${PORT}/crawl"
    else
        echo "✗ crawl4ai server not running"
        echo "  Run: $0 start"
        exit 1
    fi
}

case "${1:-status}" in
    start)  start ;;
    stop)   stop ;;
    status) status ;;
    restart) stop; start ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        exit 1
        ;;
esac