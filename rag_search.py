
from lib import QdrantDB

vector_db = QdrantDB(collection_name="pythonbook") #netfilx or 
search_result = vector_db.search(query="what is the key point")  # 搜尋恐龍電影

print(search_result)
