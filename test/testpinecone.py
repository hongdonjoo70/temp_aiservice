import os
from dotenv import load_dotenv
from pinecone import Pinecone
load_dotenv()  # Load environment variables from .env file
# 1. Pinecone 클라이언트 초기화 (환경 변수 사용)
# export PINECONE_API_KEY="your-pinecone-key"
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))

index_name = "chatbot-memory"  # 조회할 인덱스 이름

try:
    # 2. 인덱스 기본 설정 정보 조회 (Dimension, Metric, Host 등)
    index_info = pc.describe_index(index_name)
    print("--- [인덱스 기본 설정 정보] ---")
    print(f"인덱스 이름: {index_info.name}")
    print(f"차원 수 (Dimension): {index_info.dimension}")
    print(f"유사도 측정 방식 (Metric): {index_info.metric}")
    print(f"호스트 주소 (Host): {index_info.host}")
    print(f"상태 (Status): {index_info.status.get('state', 'N/A')}")

    # 3. 인덱스 연결 및 내부 통계 정보 조회 (저장된 벡터 수 등)
    index = pc.Index(index_name)
    stats = index.describe_index_stats()

    print("\n--- [인덱스 내부 통계 정보] ---")
    print(f"총 벡터 개수 (Total Vectors): {stats.total_vector_count}")

    # 네임스페이스가 있는 경우 상세 통계 출력
    if stats.namespaces:
        print("네임스페이스별 통계:")
        for ns, ns_data in stats.namespaces.items():
            print(f"  - 네임스페이스 '{ns}': 벡터 {ns_data.vector_count}개")
    else:
        print("네임스페이스: 기본(Default) 네임스페이스 사용 중")

except Exception as e:
    print(f"인덱스 정보를 가져오는 중 오류가 발생했습니다: {e}")

index.documents.upsert(
    namespace="chatbot-memory",
    documents=[
        {"_id": "1", "metadata": "Refund requests must be submitted within 30 days of purchase.", "values": "aaaaa"},
        {"_id": "2", "metadata": "eRefund requests must be submitted within 30 days of purchase.","values": "bbbb"},
    ],
)    

