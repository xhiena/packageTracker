#!/usr/bin/env python
"""
Demo script to showcase the tracking service functionality.
"""
from app.tracking.service import TrackingService


def main():
    """Demonstrate the tracking service."""
    print("=== Package Tracker Demo ===\n")
    
    # Show available carriers
    print("Available carriers:")
    carriers = TrackingService.get_available_carriers()
    for carrier in carriers:
        print(f"  - {carrier}")
    print()
    
    # Test each carrier
    test_cases = [
        ("correos", "PK123456789ES"),
        ("gls", "GLS987654321"),
        ("seur", "SEUR456789123"),
    ]
    
    for carrier_code, tracking_number in test_cases:
        print(f"\n--- Tracking with {carrier_code.upper()} ---")
        print(f"Tracking Number: {tracking_number}")
        
        result = TrackingService.get_status(carrier_code, tracking_number)
        
        if "error" in result:
            print(f"Error: {result['error']}")
        else:
            print(f"Carrier: {result['carrier']}")
            print(f"Status: {result['status']}")
            print(f"Last Update: {result['last_update']}")
            print(f"Location: {result['location']}")
            print(f"Estimated Delivery: {result.get('estimated_delivery', 'N/A')}")
            
            if "delivered_at" in result:
                print(f"Delivered At: {result['delivered_at']}")
                print(f"Signed By: {result.get('signed_by', 'N/A')}")
            
            print(f"\nTracking Events ({len(result['events'])} events):")
            for event in result['events']:
                print(f"  [{event['timestamp']}] {event['status']}")
                print(f"    Location: {event['location']}")
                print(f"    {event['description']}")
    
    # Test unknown carrier
    print("\n\n--- Testing Unknown Carrier ---")
    result = TrackingService.get_status("unknown", "TEST123")
    print(f"Result: {result}")


if __name__ == "__main__":
    main()
