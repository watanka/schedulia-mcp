from fastmcp.server import FastMCP
import signal
import sys
import httpx
from typing import List, Dict
from datetime import datetime
import json
import logging
import os
import argparse

# 로깅 설정
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('mcp_server')

# 환경 설정
SERVER_URL = "http://13.125.134.57:8000"  # 기본값은 로컬 백엔드 서버
ENV = os.getenv('MCP_ENV', 'development')

def parse_args():
    parser = argparse.ArgumentParser(description='MCP server for schedulia.org')
    parser.add_argument('--api-key', default=os.getenv('MCP_API_KEY'),
                      help='API Key for authentication')
    parser.add_argument('--server-url', default=SERVER_URL,
                      help=f'Server URL (default: {SERVER_URL})')
    parser.add_argument('--env', default=ENV,
                      choices=['development', 'production'],
                      help='Environment (development/production)')
    return parser.parse_args()

def signal_handler(sig, frame):
    logger.info("Received signal to terminate...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

args = parse_args()
API_KEY = args.api_key
SERVER_URL = args.server_url
ENV = args.env

# MCP 서버 설정
mcp = FastMCP(
    host="127.0.0.1",
    port=8080,
    timeout=30,
    debug=(ENV == 'development')
)

def get_http_client():
    """HTTP 클라이언트 설정을 환경에 따라 반환"""
    timeout = 30.0 if ENV == 'production' else 10.0
    return httpx.AsyncClient(
        follow_redirects=True,
        timeout=timeout,
        verify=(ENV == 'production')  # 개발 환경에서는 SSL 검증 비활성화
    )

@mcp.tool()
async def view_meeting_schedules(date=None):
    logger.info(f"Viewing meeting schedules for date={date}")
    async with get_http_client() as client:
        params = {}
        if date:
            params["date"] = date
        headers = {"X-API-Key": API_KEY} if API_KEY else {}
        
        try:
            response = await client.get(f"{SERVER_URL}/schedules/", params=params, headers=headers)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {str(e)}")
            raise

@mcp.tool()
async def view_meeting_requests():
    logger.debug(f"Calling view_meeting_requests")
    async with get_http_client() as client:
        headers = {"X-API-Key": API_KEY} if API_KEY else {}
        response = await client.get(f"{SERVER_URL}/requests/", headers=headers)
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response.json()

@mcp.tool()
async def request_meeting(receiver_email: str, 
                          available_times: List[Dict],  
                          title: str, 
                          description: str):
    
    try:
        async with get_http_client() as client:
            request_data = {
                "receiver_email": receiver_email,
                "available_times": available_times,
                "title": title,
                "description": description
            }
            headers = {"X-API-Key": API_KEY} if API_KEY else {}
            
            logger.info(f"Sending meeting request to {receiver_email}")
            logger.debug(f"Request data: {json.dumps(request_data, indent=2)}")
            
            response = await client.post(
                f"{SERVER_URL}/requests",
                json=request_data,
                headers=headers
            )
            response.raise_for_status()
            
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            
            return response.json()
            
    except httpx.HTTPError as e:
        logger.error(f"HTTP Error occurred: {str(e)}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON response: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise

@mcp.tool()
async def respond_to_meeting_request(request_id: int,
                                     accept: bool, 
                                     selected_time: Dict):
    try:
        async with get_http_client() as client:
            headers = {"X-API-Key": API_KEY} if API_KEY else {}
            response = await client.post(
                f"{SERVER_URL}/requests/{request_id}/respond",
                json={"accept": accept, "selected_time": selected_time},
                headers=headers
            )
            return response.json()
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        if not API_KEY and ENV == 'production':
            logger.warning("API key is not set in production environment!")
        
        logger.info(f"Starting MCP server in {ENV} mode...")
        logger.info(f"Server URL: {SERVER_URL}")
        
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        sys.exit(1) 