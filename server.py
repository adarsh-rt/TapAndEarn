from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import json
from typing import List, Optional
import uuid
import logging
from datetime import datetime, timedelta

app = FastAPI(
    title="Tap to Win Pro API",
    description="Professional clicker game backend with PostgreSQL integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection with connection pooling
def get_db_connection():
    try:
        return psycopg2.connect(
            host=os.getenv('PGHOST'),
            database=os.getenv('PGDATABASE'),
            user=os.getenv('PGUSER'),
            password=os.getenv('PGPASSWORD'),
            port=os.getenv('PGPORT'),
            cursor_factory=RealDictCursor
        )
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=503, detail="Database connection failed")

# Pydantic models
class PlayerData(BaseModel):
    total_money: int
    total_clicks: int
    best_streak: int
    owned_power_ups: List[str]
    achievements: List[str]

class PlayerResponse(BaseModel):
    player_id: str
    total_money: int
    total_clicks: int
    best_streak: int
    owned_power_ups: List[str]
    achievements: List[str]

# API Routes
@app.get("/api/player/{player_id}", response_model=PlayerResponse)
async def get_player(player_id: str):
    """Get player data by ID"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            SELECT player_id, total_money, total_clicks, best_streak, owned_power_ups, achievements
            FROM players WHERE player_id = %s
        """, (player_id,))
        
        result = cur.fetchone()
        if result:
            return PlayerResponse(
                player_id=result[0],
                total_money=result[1],
                total_clicks=result[2],
                best_streak=result[3],
                owned_power_ups=result[4] or [],
                achievements=result[5] or []
            )
        else:
            # Create new player
            cur.execute("""
                INSERT INTO players (player_id, total_money, total_clicks, best_streak, owned_power_ups, achievements)
                VALUES (%s, 0, 0, 0, '{}', '{}')
                RETURNING player_id, total_money, total_clicks, best_streak, owned_power_ups, achievements
            """, (player_id,))
            
            result = cur.fetchone()
            conn.commit()
            
            if result:
                return PlayerResponse(
                    player_id=result[0],
                    total_money=result[1],
                    total_clicks=result[2],
                    best_streak=result[3],
                    owned_power_ups=result[4] or [],
                    achievements=result[5] or []
                )
            else:
                raise HTTPException(status_code=500, detail="Failed to create new player")
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.post("/api/player/{player_id}/save")
async def save_player(player_id: str, data: PlayerData):
    """Save player data"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO players (player_id, total_money, total_clicks, best_streak, owned_power_ups, achievements)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (player_id) 
            DO UPDATE SET 
                total_money = EXCLUDED.total_money,
                total_clicks = EXCLUDED.total_clicks,
                best_streak = EXCLUDED.best_streak,
                owned_power_ups = EXCLUDED.owned_power_ups,
                achievements = EXCLUDED.achievements,
                updated_at = CURRENT_TIMESTAMP
        """, (
            player_id,
            data.total_money,
            data.total_clicks,
            data.best_streak,
            data.owned_power_ups,
            data.achievements
        ))
        
        conn.commit()
        return {"success": True, "message": "Data saved successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.delete("/api/player/{player_id}/reset")
async def reset_player(player_id: str):
    """Reset player data"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE players 
            SET total_money = 0, total_clicks = 0, best_streak = 0, 
                owned_power_ups = '{}', achievements = '{}', updated_at = CURRENT_TIMESTAMP
            WHERE player_id = %s
        """, (player_id,))
        
        conn.commit()
        return {"success": True, "message": "Player data reset successfully"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/leaderboard")
async def get_leaderboard(limit: int = 10):
    """Get top players leaderboard with enhanced analytics"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Get top players with additional stats
        cur.execute("""
            SELECT 
                player_id, 
                total_money, 
                total_clicks, 
                best_streak,
                array_length(achievements, 1) as achievement_count,
                array_length(owned_power_ups, 1) as power_up_count,
                created_at,
                updated_at,
                CASE 
                    WHEN updated_at > NOW() - INTERVAL '1 hour' THEN 'online'
                    WHEN updated_at > NOW() - INTERVAL '24 hours' THEN 'recent'
                    ELSE 'offline'
                END as status
            FROM players 
            WHERE total_money > 0
            ORDER BY total_money DESC, total_clicks DESC
            LIMIT %s
        """, (limit,))
        
        results = cur.fetchall()
        leaderboard = []
        
        for i, result in enumerate(results, 1):
            leaderboard.append({
                "rank": i,
                "player_id": result[0],
                "total_money": result[1],
                "total_clicks": result[2],
                "best_streak": result[3],
                "achievement_count": result[4] or 0,
                "power_up_count": result[5] or 0,
                "status": result[8],
                "last_active": result[7].isoformat() if result[7] else None
            })
        
        # Get total player count for context
        cur.execute("SELECT COUNT(*) as total_players FROM players WHERE total_money > 0")
        total_result = cur.fetchone()
        total_players = total_result[0] if total_result else 0
        
        return {
            "leaderboard": leaderboard,
            "total_players": total_players,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Leaderboard query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/stats")
async def get_global_stats():
    """Get global game statistics"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Get comprehensive global statistics
        cur.execute("""
            SELECT 
                COUNT(*) as total_players,
                SUM(total_money) as total_money_earned,
                SUM(total_clicks) as total_clicks,
                MAX(total_money) as highest_earnings,
                MAX(total_clicks) as most_clicks,
                MAX(best_streak) as best_streak_global,
                AVG(total_money) as avg_money,
                AVG(total_clicks) as avg_clicks,
                COUNT(*) FILTER (WHERE updated_at > NOW() - INTERVAL '1 hour') as active_players,
                COUNT(*) FILTER (WHERE updated_at > NOW() - INTERVAL '24 hours') as daily_active_players
            FROM players 
            WHERE total_money > 0
        """)
        
        stats = cur.fetchone()
        
        return {
            "global_stats": {
                "total_players": int(stats[0] or 0),
                "total_money_earned": int(stats[1] or 0),
                "total_clicks": int(stats[2] or 0),
                "highest_earnings": int(stats[3] or 0),
                "most_clicks": int(stats[4] or 0),
                "best_streak_global": int(stats[5] or 0),
                "average_money": int(stats[6] or 0),
                "average_clicks": int(stats[7] or 0),
                "active_players": int(stats[8] or 0),
                "daily_active_players": int(stats[9] or 0)
            },
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Global stats query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/player/{player_id}/rank")
async def get_player_rank(player_id: str):
    """Get player's current rank and percentile"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        # Get player's rank
        cur.execute("""
            WITH ranked_players AS (
                SELECT 
                    player_id,
                    total_money,
                    ROW_NUMBER() OVER (ORDER BY total_money DESC, total_clicks DESC) as rank
                FROM players 
                WHERE total_money > 0
            )
            SELECT rank, total_money
            FROM ranked_players 
            WHERE player_id = %s
        """, (player_id,))
        
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Player not found or no earnings")
        
        # Get total player count for percentile calculation
        cur.execute("SELECT COUNT(*) as total FROM players WHERE total_money > 0")
        total_result = cur.fetchone()
        total = total_result[0] if total_result else 0
        
        percentile = ((total - result[0]) / total * 100) if total > 0 else 0
        
        return {
            "player_id": player_id,
            "rank": result[0],
            "total_players": total,
            "percentile": round(percentile, 1),
            "earnings": result[1]
        }
    except Exception as e:
        logger.error(f"Player rank query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# Serve static files
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def serve_index():
    return FileResponse("index.html")

@app.get("/favicon.ico")
async def serve_favicon():
    return FileResponse("generated-icon.png")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)