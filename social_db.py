"""
EchoWorld Community Database - PostgreSQL backend for social features
Phase 2: Persistent storage with user profiles and karma system
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from typing import List, Dict, Optional

class CommunityDB:
    def __init__(self):
        self.db_url = os.getenv("DATABASE_URL")
        if not self.db_url:
            raise ValueError("DATABASE_URL not set")
        self.init_db()
    
    def get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.db_url)
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            # Users table with karma system
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    display_name VARCHAR(100) UNIQUE NOT NULL,
                    karma_points INT DEFAULT 0,
                    posts_count INT DEFAULT 0,
                    comments_count INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Posts table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS posts (
                    id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL REFERENCES users(id),
                    title VARCHAR(255) NOT NULL,
                    content TEXT NOT NULL,
                    category VARCHAR(100) NOT NULL,
                    likes_count INT DEFAULT 0,
                    comments_count INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Comments table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS comments (
                    id SERIAL PRIMARY KEY,
                    post_id INT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
                    user_id INT NOT NULL REFERENCES users(id),
                    content TEXT NOT NULL,
                    likes_count INT DEFAULT 0,
                    created_at TIMESTAMP DEFAULT NOW(),
                    updated_at TIMESTAMP DEFAULT NOW()
                )
            """)
            
            # Likes table (prevents duplicate likes)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS likes (
                    id SERIAL PRIMARY KEY,
                    user_id INT NOT NULL REFERENCES users(id),
                    post_id INT REFERENCES posts(id) ON DELETE CASCADE,
                    comment_id INT REFERENCES comments(id) ON DELETE CASCADE,
                    created_at TIMESTAMP DEFAULT NOW(),
                    UNIQUE(user_id, post_id, comment_id)
                )
            """)
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            if "already exists" not in str(e):
                raise
        finally:
            cur.close()
            conn.close()
    
    def get_or_create_user(self, display_name: str) -> int:
        """Get or create user, return user_id"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT id FROM users WHERE display_name = %s", (display_name,))
            result = cur.fetchone()
            
            if result:
                return result[0]
            
            cur.execute(
                """INSERT INTO users (display_name) VALUES (%s) RETURNING id""",
                (display_name,)
            )
            user_id = cur.fetchone()[0]
            conn.commit()
            return user_id
        except psycopg2.IntegrityError:
            conn.rollback()
            cur.execute("SELECT id FROM users WHERE display_name = %s", (display_name,))
            return cur.fetchone()[0]
        finally:
            cur.close()
            conn.close()
    
    def create_post(self, user_id: int, title: str, content: str, category: str) -> int:
        """Create a new post, return post_id"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                """INSERT INTO posts (user_id, title, content, category)
                   VALUES (%s, %s, %s, %s) RETURNING id""",
                (user_id, title, content, category)
            )
            post_id = cur.fetchone()[0]
            
            cur.execute(
                """UPDATE users SET posts_count = posts_count + 1, 
                   karma_points = karma_points + 5 WHERE id = %s""",
                (user_id,)
            )
            
            conn.commit()
            return post_id
        finally:
            cur.close()
            conn.close()
    
    def get_posts(self, category: Optional[str] = None) -> List[Dict]:
        """Get all posts, optionally filtered by category"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            if category and category != "All":
                cur.execute("""
                    SELECT p.*, u.display_name 
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.category = %s
                    ORDER BY p.created_at DESC
                """, (category,))
            else:
                cur.execute("""
                    SELECT p.*, u.display_name 
                    FROM posts p
                    JOIN users u ON p.user_id = u.id
                    ORDER BY p.created_at DESC
                """)
            
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Get a single post by ID"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("""
                SELECT p.*, u.display_name 
                FROM posts p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = %s
            """, (post_id,))
            
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()
    
    def create_comment(self, post_id: int, user_id: int, content: str) -> int:
        """Create a comment, return comment_id"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                """INSERT INTO comments (post_id, user_id, content)
                   VALUES (%s, %s, %s) RETURNING id""",
                (post_id, user_id, content)
            )
            comment_id = cur.fetchone()[0]
            
            cur.execute(
                "UPDATE posts SET comments_count = comments_count + 1 WHERE id = %s",
                (post_id,)
            )
            
            cur.execute(
                """UPDATE users SET comments_count = comments_count + 1,
                   karma_points = karma_points + 2 WHERE id = %s""",
                (user_id,)
            )
            
            conn.commit()
            return comment_id
        finally:
            cur.close()
            conn.close()
    
    def get_comments(self, post_id: int) -> List[Dict]:
        """Get all comments for a post"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("""
                SELECT c.*, u.display_name 
                FROM comments c
                JOIN users u ON c.user_id = u.id
                WHERE c.post_id = %s
                ORDER BY c.created_at ASC
            """, (post_id,))
            
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()
    
    def like_post(self, user_id: int, post_id: int) -> bool:
        """Like a post. Return True if liked, False if already liked"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                "SELECT id FROM likes WHERE user_id = %s AND post_id = %s",
                (user_id, post_id)
            )
            
            if cur.fetchone():
                cur.execute(
                    "DELETE FROM likes WHERE user_id = %s AND post_id = %s",
                    (user_id, post_id)
                )
                cur.execute(
                    "UPDATE posts SET likes_count = likes_count - 1 WHERE id = %s",
                    (post_id,)
                )
                conn.commit()
                return False
            else:
                cur.execute(
                    "INSERT INTO likes (user_id, post_id, comment_id) VALUES (%s, %s, NULL)",
                    (user_id, post_id)
                )
                cur.execute(
                    "UPDATE posts SET likes_count = likes_count + 1 WHERE id = %s",
                    (post_id,)
                )
                conn.commit()
                return True
        finally:
            cur.close()
            conn.close()
    
    def like_comment(self, user_id: int, comment_id: int) -> bool:
        """Like a comment. Return True if liked, False if already liked"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                "SELECT id FROM likes WHERE user_id = %s AND comment_id = %s",
                (user_id, comment_id)
            )
            
            if cur.fetchone():
                cur.execute(
                    "DELETE FROM likes WHERE user_id = %s AND comment_id = %s",
                    (user_id, comment_id)
                )
                cur.execute(
                    "UPDATE comments SET likes_count = likes_count - 1 WHERE id = %s",
                    (comment_id,)
                )
                conn.commit()
                return False
            else:
                cur.execute(
                    "INSERT INTO likes (user_id, post_id, comment_id) VALUES (%s, NULL, %s)",
                    (user_id, comment_id)
                )
                cur.execute(
                    "UPDATE comments SET likes_count = likes_count + 1 WHERE id = %s",
                    (comment_id,)
                )
                conn.commit()
                return True
        finally:
            cur.close()
            conn.close()
    
    def has_user_liked_post(self, user_id: int, post_id: int) -> bool:
        """Check if user has liked a post"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                "SELECT id FROM likes WHERE user_id = %s AND post_id = %s",
                (user_id, post_id)
            )
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()
    
    def has_user_liked_comment(self, user_id: int, comment_id: int) -> bool:
        """Check if user has liked a comment"""
        conn = self.get_connection()
        cur = conn.cursor()
        
        try:
            cur.execute(
                "SELECT id FROM likes WHERE user_id = %s AND comment_id = %s",
                (user_id, comment_id)
            )
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()
    
    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile with stats"""
        conn = self.get_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute("""
                SELECT id, display_name, karma_points, posts_count, comments_count, created_at
                FROM users WHERE id = %s
            """, (user_id,))
            
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

_db_instance = None

def get_community_db():
    """Get or create database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = CommunityDB()
    return _db_instance
