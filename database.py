"""
Database handler for GameVerse Bot
Manages user data, points, and game statistics
"""

import sqlite3
from datetime import datetime
import threading

class Database:
    def __init__(self, db_name='gameverse.db'):
        self.db_name = db_name
        self.local = threading.local()
        self.init_db()
    
    def get_connection(self):
        """Get thread-local database connection"""
        if not hasattr(self.local, 'conn'):
            self.local.conn = sqlite3.connect(self.db_name, check_same_thread=False)
            self.local.conn.row_factory = sqlite3.Row
        return self.local.conn
    
    def init_db(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                points INTEGER DEFAULT 0,
                games_played INTEGER DEFAULT 0,
                wins INTEGER DEFAULT 0,
                losses INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_played TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Game history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS game_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                game_type TEXT,
                result TEXT,
                points_earned INTEGER DEFAULT 0,
                played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (user_id)
            )
        ''')
        
        # Create indexes for better performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_user_points ON users(points DESC)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_game_user ON game_history(user_id)')
        
        conn.commit()
    
    def add_user(self, user_id, username):
        """Add or update user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO users (user_id, username) 
            VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET 
                username = excluded.username,
                last_played = CURRENT_TIMESTAMP
        ''', (user_id, username))
        
        conn.commit()
    
    def add_points(self, user_id, points):
        """Add points to user"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users 
            SET points = points + ?,
                last_played = CURRENT_TIMESTAMP
            WHERE user_id = ?
        ''', (points, user_id))
        
        conn.commit()
    
    def record_game(self, user_id, game_type, result):
        """Record a game result"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Points mapping
        points_map = {
            'tictactoe': 10,
            'rps': 5,
            'countryguess': 8,
            'quiz': 5,
            'emojigame': 6,
            'lingo': 15,
            'riddle': 12
        }
        
        points = points_map.get(game_type, 0) if result == 'win' else 0
        
        # Update user stats
        if result == 'win':
            cursor.execute('''
                UPDATE users 
                SET wins = wins + 1,
                    games_played = games_played + 1
                WHERE user_id = ?
            ''', (user_id,))
        else:
            cursor.execute('''
                UPDATE users 
                SET losses = losses + 1,
                    games_played = games_played + 1
                WHERE user_id = ?
            ''', (user_id,))
        
        # Record in game history
        cursor.execute('''
            INSERT INTO game_history (user_id, game_type, result, points_earned)
            VALUES (?, ?, ?, ?)
        ''', (user_id, game_type, result, points))
        
        conn.commit()
    
    def get_leaderboard(self, limit=10):
        """Get top players"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, username, points
            FROM users
            ORDER BY points DESC
            LIMIT ?
        ''', (limit,))
        
        return cursor.fetchall()
    
    def get_user_stats(self, user_id):
        """Get user statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT points, games_played, wins, losses
            FROM users
            WHERE user_id = ?
        ''', (user_id,))
        
        row = cursor.fetchone()
        
        if row:
            return {
                'points': row['points'],
                'games_played': row['games_played'],
                'wins': row['wins'],
                'losses': row['losses']
            }
        return None
    
    def get_user_rank(self, user_id):
        """Get user's rank on leaderboard"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT COUNT(*) + 1 as rank
            FROM users
            WHERE points > (SELECT points FROM users WHERE user_id = ?)
        ''', (user_id,))
        
        result = cursor.fetchone()
        return result['rank'] if result else 0
    
    def get_game_stats(self, user_id, game_type):
        """Get statistics for a specific game type"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT 
                COUNT(*) as total_played,
                SUM(CASE WHEN result = 'win' THEN 1 ELSE 0 END) as wins,
                SUM(CASE WHEN result = 'loss' THEN 1 ELSE 0 END) as losses,
                SUM(points_earned) as total_points
            FROM game_history
            WHERE user_id = ? AND game_type = ?
        ''', (user_id, game_type))
        
        row = cursor.fetchone()
        
        if row:
            return {
                'total_played': row['total_played'],
                'wins': row['wins'],
                'losses': row['losses'],
                'total_points': row['total_points']
            }
        return None
    
    def get_recent_games(self, user_id, limit=10):
        """Get recent game history"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT game_type, result, points_earned, played_at
            FROM game_history
            WHERE user_id = ?
            ORDER BY played_at DESC
            LIMIT ?
        ''', (user_id, limit))
        
        return cursor.fetchall()
    
    def close(self):
        """Close database connection"""
        if hasattr(self.local, 'conn'):
            self.local.conn.close()
