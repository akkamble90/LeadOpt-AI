from typing import Any, Dict, List
import psycopg2


class HybridVectorStore:
    """Manages hybrid BM25 + dense vector storage using PostgreSQL and pgvector."""

    def __init__(self, db_config: Dict[str, str]):
        self.db_config = db_config
        self._init_db()

    def _get_connection(self):
        return psycopg2.connect(**self.db_config)

    def _init_db(self):
        """Initializes database schema and pgvector extension."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_chunks (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                compound_id VARCHAR(50),
                target_name VARCHAR(50),
                text_vector vector(384),
                chem_vector vector(384),
                clearance_level INT DEFAULT 1
            );
        """)
        conn.commit()
        cursor.close()
        conn.close()

    def add_chunk(
        self,
        content: str,
        compound_id: str,
        target_name: str,
        text_vector: List[float],
        chem_vector: List[float],
        clearance_level: int = 1,
    ):
        """Inserts document chunk into vector store."""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO document_chunks 
            (content, compound_id, target_name, text_vector, chem_vector, clearance_level)
            VALUES (%s, %s, %s, %s::vector, %s::vector, %s)
            """,
            (
                content,
                compound_id,
                target_name,
                text_vector,
                chem_vector,
                clearance_level,
            ),
        )
        conn.commit()
        cursor.close()
        conn.close()

    def hybrid_search(
        self,
        query_text_vector: List[float],
        target_filter: str = None,
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """Executes cosine similarity search on text vector embeddings."""
        conn = self._get_connection()
        cursor = conn.cursor()

        sql = """
            SELECT content, compound_id, target_name, 
                   1 - (text_vector <=> %s::vector) AS similarity
            FROM document_chunks
        """
        params = [query_text_vector]

        if target_filter:
            sql += " WHERE target_name = %s"
            params.append(target_filter)

        sql += " ORDER BY similarity DESC LIMIT %s;"
        params.append(top_k)

        cursor.execute(sql, params)
        rows = cursor.fetchall()

        results = []
        for row in rows:
            results.append({
                "content": row[0],
                "compound_id": row[1],
                "target_name": row[2],
                "similarity_score": round(float(row[3]), 4),
            })

        cursor.close()
        conn.close()
        return results