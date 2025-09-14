#!/bin/bash

# Production Startup Script for Management System
# This script handles production deployment with proper error handling and logging

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="Management System"
LOG_FILE="logs/startup.log"
PID_FILE="app.pid"

# Functions
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR:${NC} $1" | tee -a "$LOG_FILE"
}

warning() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING:${NC} $1" | tee -a "$LOG_FILE"
}

# Check if running as root
check_root() {
    if [[ $EUID -eq 0 ]]; then
        error "This script should not be run as root for security reasons"
        exit 1
    fi
}

# Check Python version
check_python() {
    log "Checking Python version..."
    if ! python3 --version | grep -q "Python 3.11"; then
        error "Python 3.11+ is required"
        exit 1
    fi
    log "Python version check passed"
}

# Check dependencies
check_dependencies() {
    log "Checking dependencies..."
    if ! pip3 list | grep -q "Flask"; then
        error "Flask not found. Please run: pip install -r requirements.txt"
        exit 1
    fi
    log "Dependencies check passed"
}

# Create necessary directories
create_directories() {
    log "Creating necessary directories..."
    mkdir -p logs uploads
    chmod 755 logs uploads
    log "Directories created successfully"
}

# Check environment variables
check_env() {
    log "Checking environment variables..."
    
    required_vars=(
        "SECRET_KEY"
        "ADMIN_USERNAME"
        "ADMIN_PASSWORD_HASH"
        "FIREBASE_PROJECT_ID"
    )
    
    missing_vars=()
    for var in "${required_vars[@]}"; do
        if [[ -z "${!var}" ]]; then
            missing_vars+=("$var")
        fi
    done
    
    if [[ ${#missing_vars[@]} -gt 0 ]]; then
        error "Missing required environment variables: ${missing_vars[*]}"
        error "Please check your .env file or environment configuration"
        exit 1
    fi
    
    log "Environment variables check passed"
}

# Check if already running
check_running() {
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            warning "Application is already running with PID $PID"
            read -p "Do you want to stop it and restart? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                log "Stopping existing application..."
                kill "$PID" || true
                sleep 2
                rm -f "$PID_FILE"
            else
                log "Exiting without changes"
                exit 0
            fi
        else
            log "Removing stale PID file"
            rm -f "$PID_FILE"
        fi
    fi
}

# Start the application
start_app() {
    log "Starting $APP_NAME..."
    
    # Determine startup method
    if command -v gunicorn &> /dev/null; then
        log "Starting with Gunicorn (production mode)"
        nohup gunicorn \
            --bind 0.0.0.0:5000 \
            --workers 4 \
            --timeout 120 \
            --keep-alive 2 \
            --max-requests 1000 \
            --max-requests-jitter 100 \
            --access-logfile logs/access.log \
            --error-logfile logs/error.log \
            --log-level info \
            app:app > logs/app.log 2>&1 &
    else
        log "Starting with Flask development server"
        warning "Gunicorn not found. Using Flask development server (not recommended for production)"
        nohup python3 app.py > logs/app.log 2>&1 &
    fi
    
    # Save PID
    echo $! > "$PID_FILE"
    log "Application started with PID $!"
}

# Health check
health_check() {
    log "Performing health check..."
    
    # Wait for application to start
    sleep 5
    
    # Check if process is running
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE")
        if ! ps -p "$PID" > /dev/null 2>&1; then
            error "Application process not running"
            return 1
        fi
    fi
    
    # Check HTTP endpoint
    for i in {1..10}; do
        if curl -f -s http://localhost:5000/health > /dev/null 2>&1; then
            log "Health check passed"
            return 0
        fi
        log "Health check attempt $i/10 failed, retrying in 2 seconds..."
        sleep 2
    done
    
    error "Health check failed after 10 attempts"
    return 1
}

# Show status
show_status() {
    log "Application Status:"
    echo "=================="
    
    if [[ -f "$PID_FILE" ]]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            echo "Status: Running (PID: $PID)"
            echo "Health: $(curl -s http://localhost:5000/health | jq -r '.status' 2>/dev/null || echo 'Unknown')"
            echo "Logs: tail -f logs/app.log"
            echo "Stop: kill $PID"
        else
            echo "Status: Not running (stale PID file)"
        fi
    else
        echo "Status: Not running"
    fi
}

# Main execution
main() {
    log "Starting $APP_NAME deployment script..."
    
    # Parse command line arguments
    case "${1:-start}" in
        "start")
            check_root
            check_python
            check_dependencies
            create_directories
            check_env
            check_running
            start_app
            if health_check; then
                log "$APP_NAME started successfully!"
                show_status
            else
                error "Failed to start $APP_NAME"
                exit 1
            fi
            ;;
        "stop")
            log "Stopping $APP_NAME..."
            if [[ -f "$PID_FILE" ]]; then
                PID=$(cat "$PID_FILE")
                kill "$PID" || true
                rm -f "$PID_FILE"
                log "Application stopped"
            else
                warning "No PID file found"
            fi
            ;;
        "restart")
            log "Restarting $APP_NAME..."
            $0 stop
            sleep 2
            $0 start
            ;;
        "status")
            show_status
            ;;
        "health")
            health_check
            ;;
        *)
            echo "Usage: $0 {start|stop|restart|status|health}"
            echo ""
            echo "Commands:"
            echo "  start   - Start the application (default)"
            echo "  stop    - Stop the application"
            echo "  restart - Restart the application"
            echo "  status  - Show application status"
            echo "  health  - Perform health check"
            exit 1
            ;;
    esac
}

# Run main function
main "$@"
