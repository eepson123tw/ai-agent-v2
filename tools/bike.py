import requests
from typing import List, Dict, Union, Optional


bikeToolsConfig = [
    {
        "type": "function",
        "function": {
            "name": "get_bike",
            "description": "取得隨機的動畫訊息",
            "parameters": {
                "type": "object",
                "properties": {
                    "area": {
                        "type": "string",
                        "description": "詢問者的位置",
                    }
				},
                "additionalProperties": False,
                "required": ["area"],
            },
        },
    }
]


def get_bike(area: Optional[str] = None) -> Union[List[Dict], str]:
    """
    Fetch YouBike station information, optionally filtered by area.
    
    Args:
        area: Optional area name filter (e.g., "大安區")
        
    Returns:
        List of bike station information or error message
    """
    BASE_URL = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"
    
    try:
        response = requests.get(BASE_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Filter by area if specified
            if area:
                filtered_data = [station for station in data if station.get("sarea") == area]
            else:
                filtered_data = data
            
            # Format the response
            result = []
            for station in filtered_data:
                result.append({
                    "id": station.get("sno"),
                    "name": station.get("sna"),
                    "area": station.get("sarea"),
                    "address": station.get("ar"),
                    "last_updated": station.get("mday"),
                    "available_bikes": station.get("available_rent_bikes"),
                    "available_spaces": station.get("available_return_bikes"),
                    "total": station.get("total"),
                    "coordinates": {
                        "lat": station.get("latitude"),
                        "lng": station.get("longitude")
                    }
                })
            
            return result
        else:
            return f"❌ 無法取得YouBike資料: HTTP {response.status_code}"
    
    except requests.exceptions.RequestException as e:
        return f"❌ 連線錯誤: {str(e)}"
    except ValueError:
        return "❌ 解析JSON資料失敗"
    except Exception as e:
        return f"❌ 未知錯誤: {str(e)}"


# Example usage:
def get_nearby_bikes(lat: float, lng: float, radius: float = 0.5) -> List[Dict]:
    """
    Get bike stations within a specific radius of coordinates.
    
    Args:
        lat: latitude
        lng: longitude
        radius: search radius in kilometers
        
    Returns:
        List of nearby bike stations
    """
    all_bikes = get_bike()
    if isinstance(all_bikes, str):  # Error occurred
        return []
    
    nearby = []
    for station in all_bikes:
        # Calculate rough distance (simplified)
        station_lat = station["coordinates"]["lat"]
        station_lng = station["coordinates"]["lng"]
        
        # Simple Euclidean distance (not perfect for geo, but works for small distances)
        distance = ((lat - station_lat) ** 2 + (lng - station_lng) ** 2) ** 0.5 * 111  # rough km conversion
        
        if distance <= radius:
            station["distance"] = round(distance, 2)  # Add distance to the result
            nearby.append(station)
    
    # Sort by distance
    nearby.sort(key=lambda x: x["distance"])
    return nearby
