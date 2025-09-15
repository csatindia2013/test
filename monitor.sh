#!/bin/bash
# Production Monitoring Script for EasyBill Admin Dashboard

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
APP_URL="http://localhost:5000"
LOG_FILE="logs/app.log"
ERROR_LOG="logs/error.log"
HEALTH_ENDPOINT="/health"

echo -e "${BLUE}🔍 EasyBill Admin Dashboard - Production Monitoring${NC}"
echo "=================================================="

# Function to check if service is running
check_service() {
    echo -e "\n${YELLOW}📊 Service Status${NC}"
    if pgrep -f "gunicorn.*wsgi:application" > /dev/null; then
        echo -e "${GREEN}✅ Application is running${NC}"
        return 0
    else
        echo -e "${RED}❌ Application is not running${NC}"
        return 1
    fi
}

# Function to check health endpoint
check_health() {
    echo -e "\n${YELLOW}🏥 Health Check${NC}"
    if curl -s -f "${APP_URL}${HEALTH_ENDPOINT}" > /dev/null; then
        echo -e "${GREEN}✅ Health endpoint responding${NC}"
        # Get detailed health info
        HEALTH_INFO=$(curl -s "${APP_URL}${HEALTH_ENDPOINT}")
        echo "Health Info: $HEALTH_INFO"
        return 0
    else
        echo -e "${RED}❌ Health endpoint not responding${NC}"
        return 1
    fi
}

# Function to check logs
check_logs() {
    echo -e "\n${YELLOW}📋 Log Analysis${NC}"
    
    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}Application Logs (last 10 lines):${NC}"
        tail -10 "$LOG_FILE"
        
        # Count errors in last hour
        ERROR_COUNT=$(find "$LOG_FILE" -mmin -60 -exec grep -c "ERROR" {} \; 2>/dev/null || echo "0")
        echo -e "\n${BLUE}Errors in last hour: ${RED}$ERROR_COUNT${NC}"
    else
        echo -e "${RED}❌ Log file not found: $LOG_FILE${NC}"
    fi
    
    if [ -f "$ERROR_LOG" ]; then
        echo -e "\n${BLUE}Error Logs (last 5 lines):${NC}"
        tail -5 "$ERROR_LOG"
    else
        echo -e "${YELLOW}⚠️ Error log file not found: $ERROR_LOG${NC}"
    fi
}

# Function to check disk space
check_disk_space() {
    echo -e "\n${YELLOW}💾 Disk Space${NC}"
    df -h | grep -E "(Filesystem|/dev/)"
    
    # Check log directory size
    if [ -d "logs" ]; then
        LOG_SIZE=$(du -sh logs 2>/dev/null | cut -f1)
        echo -e "${BLUE}Log directory size: $LOG_SIZE${NC}"
    fi
}

# Function to check memory usage
check_memory() {
    echo -e "\n${YELLOW}🧠 Memory Usage${NC}"
    free -h
    
    # Check application memory usage
    APP_PID=$(pgrep -f "gunicorn.*wsgi:application" | head -1)
    if [ ! -z "$APP_PID" ]; then
        APP_MEM=$(ps -p $APP_PID -o rss= | awk '{print $1/1024 " MB"}')
        echo -e "${BLUE}Application memory usage: $APP_MEM${NC}"
    fi
}

# Function to check network connections
check_network() {
    echo -e "\n${YELLOW}🌐 Network Connections${NC}"
    netstat -tlnp | grep :5000 || echo -e "${RED}❌ No process listening on port 5000${NC}"
}

# Function to check background processor
check_background_processor() {
    echo -e "\n${YELLOW}⚙️ Background Processor${NC}"
    if curl -s "${APP_URL}/api/background-processor/status" > /dev/null; then
        STATUS=$(curl -s "${APP_URL}/api/background-processor/status")
        echo -e "${GREEN}✅ Background processor status: $STATUS${NC}"
    else
        echo -e "${RED}❌ Cannot get background processor status${NC}"
    fi
}

# Function to generate report
generate_report() {
    echo -e "\n${YELLOW}📊 System Report${NC}"
    echo "Generated at: $(date)"
    echo "Uptime: $(uptime)"
    echo "Load average: $(cat /proc/loadavg 2>/dev/null || echo 'N/A')"
}

# Main monitoring function
main() {
    local exit_code=0
    
    check_service || exit_code=1
    check_health || exit_code=1
    check_logs
    check_disk_space
    check_memory
    check_network
    check_background_processor
    generate_report
    
    echo -e "\n${BLUE}=================================================="
    if [ $exit_code -eq 0 ]; then
        echo -e "${GREEN}✅ All checks passed - System is healthy${NC}"
    else
        echo -e "${RED}❌ Some checks failed - Please investigate${NC}"
    fi
    echo -e "${BLUE}==================================================${NC}"
    
    exit $exit_code
}

# Run main function
main "$@"
