-- LangGraph Checkpointer Tables for Supabase
-- Run this in Supabase SQL Editor to create required tables
-- This only needs to be done ONCE

-- Table 1: Main checkpoints storage
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

-- Table 2: Checkpoint writes/operations
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

-- Table 3: Migration tracking
CREATE TABLE IF NOT EXISTS checkpoint_migrations (
    v INTEGER NOT NULL PRIMARY KEY,
    ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert migration version
INSERT INTO checkpoint_migrations (v) 
VALUES (1) 
ON CONFLICT (v) DO NOTHING;

-- Verify tables created
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_name IN ('checkpoints', 'checkpoint_writes', 'checkpoint_migrations')
ORDER BY table_name;
