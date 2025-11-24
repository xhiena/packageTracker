"""
KeyDelivery tracking service.

This module provides tracking functionality using the KeyDelivery (kd100.com) API.
"""
import requests
import json
import hashlib
from typing import Dict, Any, List, Optional
from app.core.config import settings


DETECT_URL = "https://www.kd100.com/api/v1/carriers/detect"
TRACK_URL = "https://www.kd100.com/api/v1/tracking/realtime"


def _generate_signature(body: str) -> str:
    """Generate MD5 signature for API authentication."""
    api_key = settings.KD100_APIKEY
    secret = settings.KD100_SECRET
    # Signature = MD5(Body + API-Key + Secret)
    signature_string = f"{body}{api_key}{secret}"
    return hashlib.md5(signature_string.encode()).hexdigest().upper()


def _make_request(url: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    """Make authenticated request to KeyDelivery API."""
    api_key = settings.KD100_APIKEY
    secret = settings.KD100_SECRET
    
    if not api_key or not secret:
        raise ValueError("KeyDelivery API key and secret not configured")
    
    body = json.dumps(payload, separators=(',', ':'))
    signature = _generate_signature(body)
    
    headers = {
        "Content-Type": "application/json",
        "API-Key": api_key,
        "signature": signature
    }
    
    response = requests.post(url, data=body, headers=headers)
    response.raise_for_status()
    return response.json()


def detect_carrier(tracking_number: str) -> List[Dict[str, str]]:
    """
    Detect possible carriers for a tracking number.
    
    Args:
        tracking_number: The tracking number to detect carriers for
        
    Returns:
        List of dicts with 'carrier_id' and 'carrier_name'
    """
    try:
        payload = {"tracking_number": tracking_number}
        result = _make_request(DETECT_URL, payload)
        
        if result.get("code") == 200:
            return result.get("data", [])
        else:
            return []
    except Exception as e:
        print(f"Carrier detection error: {e}")
        return []


def validate_tracking_number(tracking_number: str) -> bool:
    """Basic validation - KeyDelivery handles actual validation."""
    return bool(tracking_number and len(tracking_number) > 3)


def track(tracking_number: str, carrier_code: str) -> Dict[str, Any]:
    """
    Get real-time tracking information for a package.
    
    Args:
        tracking_number: The tracking number to track
        carrier_code: The carrier code (e.g., 'correos', 'dhl', 'ups')
        
    Returns:
        Dictionary containing tracking information with keys:
        - status: Current status of the package
        - location: Current or last known location
        - history: List of tracking events
        - error: Error message if tracking failed
        - carrier: The carrier code
    """
    api_key = settings.KD100_APIKEY
    secret = settings.KD100_SECRET
    
    if not api_key or not secret:
        return {
            "status": "error",
            "location": None,
            "history": [],
            "error": "KeyDelivery API key and secret not configured",
            "carrier": None
        }
    
    if not carrier_code or carrier_code == "auto":
        return {
            "status": "error",
            "location": None,
            "history": [],
            "error": "Carrier not detected. Please add the package first.",
            "carrier": None
        }
    
    try:
        payload = {
            "carrier_id": carrier_code,
            "tracking_number": tracking_number
        }
        
        result = _make_request(TRACK_URL, payload)
        
        if result.get("code") != 200:
            return {
                "status": "error",
                "location": None,
                "history": [],
                "error": result.get("message", "Tracking failed"),
                "carrier": carrier_code
            }
        
        data = result.get("data", {})
        
        # Map order_status_code to readable status
        status_map = {
            0: "Pending",
            1: "Accepted",
            2: "In Transit",
            3: "Out for Delivery",
            4: "Delivered",
            5: "Exception",
            6: "Expired"
        }
        
        order_status_code = data.get("order_status_code")
        status = status_map.get(order_status_code, "Unknown")
        
        # Parse tracking history
        history = []
        items = data.get("items", [])
        for item in items:
            history.append({
                "status": item.get("order_status_description", ""),
                "location": item.get("location") or item.get("area_name") or "",
                "timestamp": item.get("time", ""),
                "context": item.get("context", "")
            })
        
        # Get location from most recent event
        location = None
        if history:
            location = history[0].get("location") or history[0].get("context")
        
        return {
            "status": status,
            "location": location,
            "history": history,
            "error": None,
            "carrier": data.get("carrier_id", carrier_code)
        }
        
    except Exception as e:
        return {
            "status": "error",
            "location": None,
            "history": [],
            "error": str(e),
            "carrier": carrier_code
        }
