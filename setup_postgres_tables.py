#!/usr/bin/env python3
"""
Setup Postgres tables for LangGraph checkpointer.
This script runs ONCE to create tables, then the main app can use them.
Use this with Transaction Mode (port 6543) in Docker.
"""
import os
import sys
import time
import psycopg

def setup_tables_with_retry(max_retries=5, retry_delay=3):
    """Setup tables with retry logic for Docker startup"""
    
    postgres_url = os.getenv('POSTGRES_DATABASE_URL')
    if not postgres_url:
        print("[ERROR] POSTGRES_DATABASE_URL not set!")
        return False
    
    print("\n" + "="*60)
    print("LangGraph Postgres Table Setup")
    print("="*60)
    print(f"[INFO] Database URL: {postgres_url.split('@')[1] if '@' in postgres_url else 'N/A'}")
    
    # LangGraph checkpointer table creation SQL
    # Copied from langgraph.checkpoint.postgres
    CREATE_TABLES_SQL = """
    CREATE TABLE IF NOT EXISTS checkpoints (
        thread_id TEXT NOT NULL,
        checkpoint_ns TEXT NOT NULL DEFAULT '',
        checkpoint_id TEXT NOT NULL,
        parent_checkpoint_id TEXT,
        type TEXT,
        checkpoint JSONB NOT NULL,
        metadata JSONB NOT NULL DEFAULT '{}',
        PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
    );

    CREATE TABLE IF NOT EXISTS checkpoint_writes (
        thread_id TEXT NOT NULL,
        checkpoint_ns TEXT NOT NULL DEFAULT '',
        checkpoint_id TEXT NOT NULL,
        task_id TEXT NOT NULL,
        idx INTEGER NOT NULL,
        channel TEXT NOT NULL,
        type TEXT,
        value JSONB,
        PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
    );

    CREATE TABLE IF NOT EXISTS checkpoint_migrations (
        v INTEGER NOT NULL PRIMARY KEY,
        ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    INSERT INTO checkpoint_migrations (v) 
    VALUES (1) 
    ON CONFLICT (v) DO NOTHING;
    """
    
    for attempt in range(1, max_retries + 1):
        try:
            print(f"\n[ATTEMPT {attempt}/{max_retries}] Connecting to database...")
            
            # Use autocommit=True for DDL operations
            conn = psycopg.connect(
                postgres_url,
                autocommit=True,
                prepare_threshold=None,  # Required for Transaction Mode
                connect_timeout=15
            )
            
            print("[SUCCESS] Connected!")
            print("[INFO] Creating tables...")
            
            with conn.cursor() as cur:
                # Execute all DDL statements
                cur.execute(CREATE_TABLES_SQL)
            
            print("[SUCCESS] Tables created/verified!")
            
            # Verify tables exist
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_name IN ('checkpoints', 'checkpoint_writes', 'checkpoint_migrations')
                    ORDER BY table_name;
                """)
                tables = cur.fetchall()
                print(f"[VERIFY] Found {len(tables)} tables: {[t[0] for t in tables]}")
            
            conn.close()
            print("\n[SUCCESS] Setup complete!")
            print("="*60)
            return True
            
        except psycopg.OperationalError as e:
            print(f"[FAILED] Connection error: {e}")
            if attempt < max_retries:
                print(f"[RETRY] Waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
            else:
                print(f"\n[ERROR] Failed after {max_retries} attempts")
                return False
                
        except Exception as e:
            print(f"[FAILED] Unexpected error: {type(e).__name__}: {e}")
            if attempt < max_retries:
                print(f"[RETRY] Waiting {retry_delay}s before retry...")
                time.sleep(retry_delay)
            else:
                print(f"\n[ERROR] Failed after {max_retries} attempts")
                import traceback
                traceback.print_exc()
                return False
    
    return False

if __name__ == "__main__":
    try:
        success = setup_tables_with_retry()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Setup cancelled")
        sys.exit(1)
