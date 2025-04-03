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

from models import Time

SERVER_URL = "http://localhost:8000"

def parse_args():
    parser = argparse.ArgumentParser(description='MCP 서버')
    parser.add_argument('--api-key', default=os.getenv('MCP_API_KEY'),
                      help='API 키 (환경변수 MCP_API_KEY로도 설정 가능)')
    return parser.parse_args()

def signal_handler(sig, frame):
    logger.info("Received signal to terminate...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

args = parse_args()
API_KEY = args.api_key

mcp = FastMCP(
    host="127.0.0.1",
    port=8080,
    timeout=30,
    debug=True
)

@mcp.tool()
async def view_meeting_schedules(date=None):
    print(f"Calling view_meeting_schedules with date={date}")
    async with httpx.AsyncClient() as client:
        params = {}
        if date:
            params["date"] = date
        headers = {"X-API-Key": API_KEY} if API_KEY else {}
        logger.debug(f"Sending GET request to {SERVER_URL}/schedules/ with params={params}")
        response = await client.get(f"{SERVER_URL}/schedules/", params=params, headers=headers)
        logger.debug(f"Response status: {response.status_code}")
        logger.debug(f"Response body: {response.text}")
        return response.json()

@mcp.tool()
async def view_meeting_requests():
    logger.debug(f"Calling view_meeting_requests")
    async with httpx.AsyncClient() as client:
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
        async with httpx.AsyncClient() as client:
            request_data = {
                "receiver_email": receiver_email,
                "available_times": available_times,
                "title": title,
                "description": description
            }
            headers = {"X-API-Key": API_KEY} if API_KEY else {}
            logger.debug(f"Sending POST request to {SERVER_URL}/requests/ with data={json.dumps(request_data, indent=2)}")
            response = await client.post(
                f"{SERVER_URL}/requests/", 
                json=request_data,
                headers=headers
            )
            logger.debug(f"Response status: {response.status_code}")
            logger.debug(f"Response body: {response.text}")
            return response.json()
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        raise

@mcp.tool()
async def respond_to_meeting_request(request_id: int,
                                     accept: bool, 
                                     selected_time: Dict):
    try:
        async with httpx.AsyncClient() as client:
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
        if not API_KEY:
            logger.warning("API 키가 설정되지 않았습니다. --api-key 옵션이나 MCP_API_KEY 환경변수를 사용하세요.")
        logger.info("Starting MCP server...")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Shutting down gracefully...")
    except Exception as e:
        logger.error(f"Error occurred: {e}", exc_info=True)
        sys.exit(1) 