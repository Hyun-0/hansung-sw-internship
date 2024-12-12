from llama_index.core import VectorStoreIndex
from llama_index.core import StorageContext
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

# local 환경에서 docker 사용하여 port 6333으로 qdrant 접속 가능
# docker run -p 6333:6333 -p 6334:6334 -v $(pwd)/qdrant_storage:/qdrant/storage:z qdrant/qdrant

class Db:
    def __init__(self, documents):
        self.client = QdrantClient(host="52.78.92.110", port=6333)
        # # colab
        # self.client = QdrantClient(location=":memory:")
        # self.client.recreate_collection(
        #     collection_name="qdrant",
        #     vectors_config=VectorParams(
        #         size=384,    # 벡터 크기 설정
        #         distance=Distance.COSINE  # 거리 계산 방식 설정 (Cosine Similarity)
        #     )
        # )
            
        self.vector_store = QdrantVectorStore(client=self.client,collection_name="qdrant")
        self.storage_context = StorageContext.from_defaults(vector_store=self.vector_store)
        self.documents = documents

        
    def get_index(self):
        return VectorStoreIndex.from_vector_store(vector_store=self.vector_store)
        # return VectorStoreIndex.from_documents(self.documents,storage_context=self.storage_context)
