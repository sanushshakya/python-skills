"""
Module for implementing per-key rate limiting in the API.

This module defines a middleware to apply rate limits based on API keys,
using an in-memory dictionary to store request counts.
"""

from fastapi import Request, HTTPException, status, Depends
from datetime import datetime
import time

# Dictionary to store rate limit data (key: API key, value: (last_request_time, request_count))
rate_limit_data = {}

async def rate_limiter(request: Request):
    """
    Middleware to apply rate limiting based on API keys.
    
    Args:
        request (Request): The incoming HTTP request.
        
    Raises:
        HTTPException: If the request exceeds the rate limit.
    """
    api_key = await get_api_key_from_request(request)
    if not api_key:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="API key required")

    current_time = time.time()
    
    # Get or initialize rate limit data for this API key
    if api_key not in rate_limit_data:
        rate_limit_data[api_key] = (current_time, 1)
        return
    
    last_request_time, request_count = rate_limit_data[api_key]
    
    # If the time since the last request is less than a minute, increment the request count
    if current_time - last_request_time < 60:
        request_count += 1
    else:
        # Reset the request count and update the last request time
        request_count = 1
    
    # Check if the rate limit has been exceeded
    if request_count > 5:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
    
    # Update the rate limit data
    rate_limit_data[api_key] = (current_time, request_count)

async def get_api_key_from_request(request: Request) -> Union[str, None]:
    """
    Extracts the API key from the request headers.
    
    Args:
        request (Request): The incoming HTTP request.
        
    Returns:
        str or None: The API key if found, otherwise None.
    """
    api_key = request.headers.get("X-API-Key")
    return api_key