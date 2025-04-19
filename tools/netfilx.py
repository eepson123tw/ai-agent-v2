from lib import QdrantDB
from typing import List, Dict, Union, Any

# Netflix tools configuration
netflixToolsConfig = [
    {
        "type": "function",
        "function": {
            "name": "get_netflix",
            "description": "取得使用者需求的影集資訊",
            "parameters": {
                "type": "object",
                "properties": {
                    "drama": {
                        "type": "string",
                        "description": "影集名稱",
                    }
                },
                "additionalProperties": False,
                "required": ["drama"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_pdf",
            "description": "取得使用者需求的pdf資訓",
            "parameters": {
                "type": "object",
                "properties": {
                    "pdf": {
                        "type": "string",
                        "description": "pdf資訊",
                    }
                },
                "additionalProperties": False,
                "required": ["pdf"],
            },
        },
    },
]

def get_netflix(drama: str) -> Union[List[Dict[str, Any]], str]:
    """
    Search for Netflix content based on user query.
    
    Args:
        drama: Search query for Netflix content
        
    Returns:
        List of formatted Netflix content information or error message
    """
    try:
        # Initialize vector database
        vector_db = QdrantDB(collection_name="netflix")
        
        # Search for content matching the query
        search_results = vector_db.search(query=drama)
        
        # Check if we got any results
        if not search_results:
            return f"❌ 找不到與 '{drama}' 相關的影集資訊"
        
        # Format the results
        formatted_results = []
        for item in search_results:
            formatted_item = {
                "title": item.get("title", "未知標題"),
                "type": item.get("type", "未知類型"),
                "year": item.get("release_year", "未知年份"),
                "rating": item.get("rating", "未知分級"),
                "duration": item.get("duration", "未知時長"),
                "description": item.get("description", "無簡介"),
            }
            
            # Add director and cast if available
            if item.get("director"):
                formatted_item["director"] = item.get("director")
            
            if item.get("cast"):
                formatted_item["cast"] = item.get("cast").split(", ") if isinstance(item.get("cast"), str) else item.get("cast")
            
            formatted_results.append(formatted_item)
        
        return formatted_results
        
    except Exception as e:
        return f"❌ 搜尋影集資訊時發生錯誤: {str(e)}"


# Example usage
def search_netflix_content(query: str) -> Dict[str, Any]:
    """
    Search for Netflix content and format the response for API return.
    
    Args:
        query: User's search query
        
    Returns:
        Formatted API response
    """
    results = get_netflix(query)
    
    if isinstance(results, str) and results.startswith("❌"):
        # Error occurred
        return {
            "success": False,
            "message": results,
            "data": None
        }
    
    return {
        "success": True,
        "message": f"找到 {len(results)} 筆與 '{query}' 相關的影集資訊",
        "data": results
    }


def get_pdf(pdf: str) -> Union[List[Dict[str, Any]], str]:
    """
    Search for pdf content based on user query.
    
    Args:
        drama: Search query for pdf content
        
    Returns:
        List of formatted pdf content information or error message
    """
    try:
        # Initialize vector database
        vector_db = QdrantDB(collection_name="pythonbook")
        
        # Search for content matching the query
        search_results = vector_db.search(query=pdf)
        
        # Check if we got any results
        if not search_results:
            return f"❌ 找不到與 '{pdf}' 相關的資訊"
        
        # Format the results
        formatted_results = []
        for item in search_results:
            formatted_item = {
                "page": item.get("page", "未知頁面"),
                "text": item.get("text", "未知描述"),
            }
            
            formatted_results.append(formatted_item)
        
        return formatted_results
        
    except Exception as e:
        return f"❌ 搜尋pdf資訊時發生錯誤: {str(e)}"


# # Example usage
def search_pdf_content(query: str) -> Dict[str, Any]:
    """
    Search for pdf content and format the response for API return.
    
    Args:
        query: User's search query
        
    Returns:
        Formatted API response
    """
    results = get_pdf(query)
    
    if isinstance(results, str) and results.startswith("❌"):
        # Error occurred
        return {
            "success": False,
            "message": results,
            "data": None
        }
    
    return {
        "success": True,
        "message": f"找到 {len(results)} 筆與 '{query}' 相關的pdf資訊",
        "data": results
    }
