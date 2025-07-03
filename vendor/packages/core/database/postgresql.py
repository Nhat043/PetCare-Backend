import os
import psycopg2
import asyncpg
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import logging

logger = logging.getLogger(__name__)


class PostgreSQLConnection:
    """
    PostgreSQL connection class that provides both synchronous and asynchronous connections.
    Uses environment variable DATABASE_URL for connection string.
    """

    def __init__(self, connection_string: Optional[str] = None):
        """
        Initialize the PostgreSQL connection.

        Args:
            connection_string: Optional connection string. If not provided,
                             will use DATABASE_URL environment variable.
        """
        self.connection_string = connection_string or os.getenv("DATABASE_URL")
        if not self.connection_string:
            raise ValueError(
                "Database connection string is required. Set DATABASE_URL environment variable or pass connection_string parameter."
            )

        self._sync_conn = None
        self._async_conn = None

    def get_sync_connection(self):
        """
        Get a synchronous PostgreSQL connection.

        Returns:
            psycopg2 connection object
        """
        try:
            if self._sync_conn is None or self._sync_conn.closed:
                self._sync_conn = psycopg2.connect(self.connection_string)
                logger.info("Synchronous PostgreSQL connection established")
            return self._sync_conn
        except Exception as e:
            logger.error(f"Failed to establish synchronous connection: {e}")
            raise

    async def get_async_connection(self):
        """
        Get an asynchronous PostgreSQL connection.

        Returns:
            asyncpg connection object
        """
        try:
            if self._async_conn is None or self._async_conn.is_closed():
                self._async_conn = await asyncpg.connect(self.connection_string)
                logger.info("Asynchronous PostgreSQL connection established")
            return self._async_conn
        except Exception as e:
            logger.error(f"Failed to establish asynchronous connection: {e}")
            raise

    @contextmanager
    def get_sync_cursor(self):
        """
        Context manager for synchronous database operations.

        Yields:
            psycopg2 cursor object
        """
        conn = self.get_sync_connection()
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(f"Database operation failed: {e}")
            raise
        finally:
            cursor.close()

    async def get_async_cursor(self):
        """
        Get an asynchronous cursor for database operations.

        Returns:
            asyncpg connection object (can be used as cursor)
        """
        return await self.get_async_connection()

    def execute_query(self, query: str, params: Optional[tuple] = None) -> list:
        """
        Execute a synchronous query and return results.

        Args:
            query: SQL query string
            params: Optional parameters for the query

        Returns:
            List of results
        """
        with self.get_sync_cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                return cursor.fetchall()
            return []

    def execute_query_dict(
        self, query: str, params: Optional[tuple] = None
    ) -> List[Dict[str, Any]]:
        """
        Execute a synchronous query and return results as dictionaries.

        Args:
            query: SQL query string
            params: Optional parameters for the query

        Returns:
            List of dictionaries with column names as keys
        """
        with self.get_sync_cursor() as cursor:
            cursor.execute(query, params)
            if query.strip().upper().startswith("SELECT"):
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
            return []

    async def execute_async_query(
        self, query: str, params: Optional[tuple] = None
    ) -> list:
        """
        Execute an asynchronous query and return results.

        Args:
            query: SQL query string
            params: Optional parameters for the query

        Returns:
            List of results
        """
        conn = await self.get_async_connection()
        try:
            if query.strip().upper().startswith("SELECT"):
                return (
                    await conn.fetch(query, *params)
                    if params
                    else await conn.fetch(query)
                )
            else:
                (
                    await conn.execute(query, *params)
                    if params
                    else await conn.execute(query)
                )
                return []
        except Exception as e:
            logger.error(f"Async query execution failed: {e}")
            raise

    def test_connection(self) -> bool:
        """
        Test the database connection.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            with self.get_sync_cursor() as cursor:
                cursor.execute("SELECT 1")
                result = cursor.fetchone()
                return result[0] == 1
        except Exception as e:
            logger.error(f"Connection test failed: {e}")
            return False

    async def test_async_connection(self) -> bool:
        """
        Test the asynchronous database connection.

        Returns:
            True if connection is successful, False otherwise
        """
        try:
            conn = await self.get_async_connection()
            result = await conn.fetchval("SELECT 1")
            return result == 1
        except Exception as e:
            logger.error(f"Async connection test failed: {e}")
            return False

    def close_sync_connection(self):
        """Close the synchronous connection."""
        if self._sync_conn and not self._sync_conn.closed:
            self._sync_conn.close()
            logger.info("Synchronous PostgreSQL connection closed")

    async def close_async_connection(self):
        """Close the asynchronous connection."""
        if self._async_conn and not self._async_conn.is_closed():
            await self._async_conn.close()
            logger.info("Asynchronous PostgreSQL connection closed")

    def close_all_connections(self):
        """Close all connections."""
        self.close_sync_connection()
        # Note: This will need to be called in an async context
        # or you can use asyncio.create_task(self.close_async_connection())


# Global instance for easy access
postgres_db = PostgreSQLConnection()


# Convenience functions for easy usage
def get_db_connection() -> PostgreSQLConnection:
    """
    Get the global database connection instance.

    Returns:
        PostgreSQLConnection instance
    """
    return postgres_db


def execute_query(query: str, params: Optional[tuple] = None) -> list:
    """
    Execute a synchronous query using the global connection.

    Args:
        query: SQL query string
        params: Optional parameters for the query

    Returns:
        List of results
    """
    return postgres_db.execute_query(query, params)


def execute_query_dict(
    query: str, params: Optional[tuple] = None
) -> List[Dict[str, Any]]:
    """
    Execute a synchronous query and return results as dictionaries.

    Args:
        query: SQL query string
        params: Optional parameters for the query

    Returns:
        List of dictionaries with column names as keys
    """
    return postgres_db.execute_query_dict(query, params)


async def execute_async_query(query: str, params: Optional[tuple] = None) -> list:
    """
    Execute an asynchronous query using the global connection.

    Args:
        query: SQL query string
        params: Optional parameters for the query

    Returns:
        List of results
    """
    return await postgres_db.execute_async_query(query, params)
