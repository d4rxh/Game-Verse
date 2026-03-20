#!/usr/bin/env python3
"""
GameVerse - Ultimate Telegram Game Bot
Complete interactive game bot for Telegram groups
"""

import os
import random
import logging
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from database import Database

# Logging setup
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize database
db = Database()

# ⚙️ WELCOME IMAGE CONFIGURATION
WELCOME_IMAGE_URL = os.getenv('WELCOME_IMAGE_URL', 'https://i.ibb.co/gZYYY5H1/1739872830412.jpg')
# Set WELCOME_IMAGE_URL in Railway/Render environment variables

# ---------------- WEB SERVER (Render fix) ---------------- #
def run_web_server():
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"GameVerse Bot Running!")

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# Game data
COUNTRIES = {
    "🇮🇳": "India", "🇺🇸": "USA", "🇬🇧": "UK", "🇨🇦": "Canada", "🇦🇺": "Australia",
    "🇯🇵": "Japan", "🇨🇳": "China", "🇫🇷": "France", "🇩🇪": "Germany", "🇮🇹": "Italy",
    "🇧🇷": "Brazil", "🇲🇽": "Mexico", "🇪🇸": "Spain", "🇷🇺": "Russia", "🇰🇷": "South Korea",
    "🇸🇦": "Saudi Arabia", "🇦🇪": "UAE", "🇹🇷": "Turkey", "🇿🇦": "South Africa", "🇳🇬": "Nigeria",
    "🇦🇷": "Argentina", "🇵🇹": "Portugal", "🇳🇱": "Netherlands", "🇸🇪": "Sweden", "🇳🇴": "Norway",
    "🇵🇱": "Poland", "🇬🇷": "Greece", "🇪🇬": "Egypt", "🇹🇭": "Thailand", "🇻🇳": "Vietnam"
}

RIDDLES = [
    {"q": "What has keys but no locks, space but no room, and you can enter but can't go inside?", "a": "keyboard", "hint": "You're using it to type right now!"},
    {"q": "I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I?", "a": "echo", "hint": "You might hear it in mountains or caves"},
    {"q": "The more you take, the more you leave behind. What am I?", "a": "footsteps", "hint": "Think about walking"},
    {"q": "What can travel around the world while staying in a corner?", "a": "stamp", "hint": "Found on envelopes"},
    {"q": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "a": "map", "hint": "Helps with navigation"},
    {"q": "What gets wet while drying?", "a": "towel", "hint": "Used after a shower"},
    {"q": "What can you break, even if you never pick it up or touch it?", "a": "promise", "hint": "It's not a physical object"},
    {"q": "What goes up but never comes down?", "a": "age", "hint": "Gets bigger every year"},
    {"q": "I'm tall when I'm young, and short when I'm old. What am I?", "a": "candle", "hint": "Gives light and melts"},
    {"q": "What has hands but cannot clap?", "a": "clock", "hint": "Tells time"},
    {"q": "What has a head and tail but no body?", "a": "coin", "hint": "Used as currency"},
    {"q": "What can run but never walks, has a mouth but never talks?", "a": "river", "hint": "Flows with water"},
    {"q": "What has one eye but cannot see?", "a": "needle", "hint": "Used for sewing"},
    {"q": "What gets bigger the more you take away?", "a": "hole", "hint": "You dig it"},
    {"q": "What belongs to you but others use it more?", "a": "name", "hint": "People call you by it"}
]

QUIZ_QUESTIONS = [
    {"q": "What is the capital of India?", "options": ["Mumbai", "Delhi", "Kolkata", "Chennai"], "a": 1},
    {"q": "How many continents are there?", "options": ["5", "6", "7", "8"], "a": 2},
    {"q": "Which planet is known as the Red Planet?", "options": ["Venus", "Mars", "Jupiter", "Saturn"], "a": 1},
    {"q": "Who painted the Mona Lisa?", "options": ["Picasso", "Van Gogh", "Leonardo da Vinci", "Michelangelo"], "a": 2},
    {"q": "What is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "a": 3},
    {"q": "Which year did World War II end?", "options": ["1943", "1944", "1945", "1946"], "a": 2},
    {"q": "What is the smallest prime number?", "options": ["0", "1", "2", "3"], "a": 2},
    {"q": "How many sides does a hexagon have?", "options": ["5", "6", "7", "8"], "a": 1},
    {"q": "What is the hardest natural substance?", "options": ["Gold", "Iron", "Diamond", "Platinum"], "a": 2},
    {"q": "Which programming language is known as the 'language of the web'?", "options": ["Python", "Java", "JavaScript", "C++"], "a": 2},
    {"q": "Who wrote 'Romeo and Juliet'?", "options": ["Charles Dickens", "William Shakespeare", "Mark Twain", "Jane Austen"], "a": 1},
    {"q": "What is the speed of light?", "options": ["300,000 km/s", "150,000 km/s", "450,000 km/s", "200,000 km/s"], "a": 0},
    {"q": "How many bones are in the human body?", "options": ["196", "206", "216", "226"], "a": 1},
    {"q": "What is the chemical symbol for gold?", "options": ["Go", "Gd", "Au", "Ag"], "a": 2},
    {"q": "Which is the longest river in the world?", "options": ["Amazon", "Nile", "Yangtze", "Mississippi"], "a": 1},
    {"q": "What year did the Titanic sink?", "options": ["1910", "1911", "1912", "1913"], "a": 2},
    {"q": "How many hearts does an octopus have?", "options": ["1", "2", "3", "4"], "a": 2},
    {"q": "What is the largest mammal?", "options": ["Elephant", "Blue Whale", "Giraffe", "Polar Bear"], "a": 1},
    {"q": "Who invented the telephone?", "options": ["Thomas Edison", "Nikola Tesla", "Alexander Graham Bell", "Benjamin Franklin"], "a": 2},
    {"q": "What is the square root of 144?", "options": ["10", "11", "12", "13"], "a": 2}
]

EMOJI_MEANINGS = {
    "🔥": "Fire", "💧": "Water", "🌍": "Earth", "💨": "Wind", "⚡": "Lightning",
    "🌙": "Moon", "☀️": "Sun", "⭐": "Star", "🌈": "Rainbow", "❄️": "Snow",
    "🌸": "Flower", "🌳": "Tree", "🍕": "Pizza", "🍔": "Burger", "🍰": "Cake",
    "☕": "Coffee", "🎮": "Gaming", "🎵": "Music", "📱": "Phone", "💻": "Computer",
    "🚗": "Car", "✈️": "Airplane", "🏠": "Home", "⚽": "Football", "🎨": "Art"
}

LINGOGRID_WORDS = ["PYTHON", "CODING", "GAMES", "ROBOT", "CLOUD", "BRAIN", "MUSIC", "DANCE", "HAPPY", "WORLD",
                   "DREAM", "LIGHT", "SPACE", "OCEAN", "MAGIC", "POWER", "THINK", "SMART", "BRAVE", "PEACE",
                   "TRUST", "SMILE", "HEART", "FRIEND", "LOVE", "HOPE", "FAITH", "COURAGE", "WISDOM", "TRUTH"]

# Game states
active_games = {}

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with welcome IMAGE and message"""
    user = update.effective_user
    db.add_user(user.id, user.first_name)
    
    welcome_text = f"""
🎮 **Welcome to GAME VERSE!!**

⭕ Tic Tac Toe  •  ✊ Rock Paper Scissors
🌍 Country Guess  •  ❓ Quiz & Emoji Game
✍️ LingoGrid  •  🧠 Riddles

🏆 Leaderboard /leaderboard  •  📊 Stats /stats

🏅 **Win games · Earn points · Climb the leaderboard!**

Type /help to see all features!
Type /games to start playing!
    """
    
    # Send custom logo with caption
    try:
        await update.message.reply_photo(
            photo=WELCOME_IMAGE_URL,
            caption=welcome_text,
            parse_mode='Markdown'
        )
    except Exception as e:
        logger.error(f"Error sending welcome image: {e}")
        # Fallback to text if image fails
        await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """COMPLETE help command with all features"""
    help_text = """
🎮 **GAMEVERSE - Complete Guide** 🎮

━━━━━━━━━━━━━━━━━━━━━━
**🎯 AVAILABLE GAMES**
━━━━━━━━━━━━━━━━━━━━━━

⭕ **Tic Tac Toe** - /tictactoe
   • VS Bot mode (single player)
   • Multiplayer mode (2 players)
   • Strategic 3x3 grid gameplay
   • Win: 10 points 🏆

✊ **Rock Paper Scissors** - /rps
   • VS Bot mode (quick battles)
   • Multiplayer mode (challenge friends)
   • Classic hand game
   • Win: 5 points 🏆

🌍 **Country Guess** - /countryguess
   • Identify countries from emoji flags
   • 30 different countries
   • Multiple choice questions
   • Correct answer: 8 points 🏆

❓ **Quiz Game** - /quiz
   • 20+ general knowledge questions
   • Science, History, Geography
   • 4 options per question
   • Correct answer: 5 points 🏆

🔤 **Emoji Game** - /emojigame
   • Guess emoji meanings
   • 25+ different emojis
   • Fun and educational
   • Correct answer: 6 points 🏆

✍️ **LingoGrid** - /lingogrid
   • Unscramble word puzzles
   • 30+ different words
   • Type your answer
   • Correct answer: 15 points 🏆

🧠 **Riddles** - /riddle
   • Brain-teasing riddles
   • 15+ challenging questions
   • Hint button available 💡
   • Correct answer: 12 points 🏆

━━━━━━━━━━━━━━━━━━━━━━
**📊 STATS & LEADERBOARD**
━━━━━━━━━━━━━━━━━━━━━━

🏆 **/leaderboard** - Top 10 players
📈 **/stats** - Your game statistics
🎯 **/profile** - Your gaming profile

━━━━━━━━━━━━━━━━━━━━━━
**🎮 HOW TO PLAY**
━━━━━━━━━━━━━━━━━━━━━━

1️⃣ Choose a game from /games menu
2️⃣ Select mode (VS Bot or Multiplayer)
3️⃣ Follow game instructions
4️⃣ Earn points for wins
5️⃣ Climb the leaderboard!

━━━━━━━━━━━━━━━━━━━━━━
**🏅 POINT SYSTEM**
━━━━━━━━━━━━━━━━━━━━━━

• Tic Tac Toe: 10 points
• Rock Paper Scissors: 5 points
• Country Guess: 8 points
• Quiz: 5 points
• Emoji Game: 6 points
• LingoGrid: 15 points
• Riddle: 12 points (8 with hint)

**Level Up:** Every 100 points = 1 Level! ⭐

━━━━━━━━━━━━━━━━━━━━━━
**💡 SPECIAL FEATURES**
━━━━━━━━━━━━━━━━━━━━━━

✅ VS Bot Mode - Play against AI
✅ Multiplayer - Challenge friends
✅ Hints - Available in riddles
✅ Auto-save - Progress never lost
✅ Daily play - Build your streak
✅ Group play - Compete together

━━━━━━━━━━━━━━━━━━━━━━

**Ready to play?** Type /games to start! 🚀

**Need support?** Contact admin
**Enjoying the bot?** Share with friends! 💙
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def games_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all available games"""
    keyboard = [
        [InlineKeyboardButton("⭕ Tic Tac Toe", callback_data="game_ttt_menu")],
        [InlineKeyboardButton("✊ Rock Paper Scissors", callback_data="game_rps_menu")],
        [InlineKeyboardButton("🌍 Country Guess (Emoji)", callback_data="game_country")],
        [InlineKeyboardButton("🗺️ Map Guess", callback_data="game_map")],
        [InlineKeyboardButton("❓ Quiz", callback_data="game_quiz")],
        [InlineKeyboardButton("🔤 Emoji Game", callback_data="game_emoji")],
        [InlineKeyboardButton("✍️ LingoGrid", callback_data="game_lingo")],
        [InlineKeyboardButton("🧠 Riddle", callback_data="game_riddle")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎮 **Choose Your Game:**", reply_markup=reply_markup, parse_mode='Markdown')

# ========== TIC TAC TOE - VS BOT + MULTIPLAYER ========== #

async def tictactoe_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show Tic Tac Toe mode selection"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🤖 VS Bot (Single Player)", callback_data="ttt_vsbot")],
        [InlineKeyboardButton("👥 Multiplayer (2 Players)", callback_data="ttt_multi")],
        [InlineKeyboardButton("⬅️ Back to Games", callback_data="back_to_games")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "⭕ **Tic Tac Toe - Choose Mode:**\n\n"
        "🤖 **VS Bot:** Play against AI\n"
        "👥 **Multiplayer:** Play with a friend",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def tictactoe_vsbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Tic Tac Toe VS Bot"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    # Initialize game board
    board = [["⬜" for _ in range(3)] for _ in range(3)]
    active_games[chat_id] = {
        'type': 'ttt_bot',
        'board': board,
        'current_player': user_id,
        'players': [user_id, 'bot'],
        'symbols': {user_id: '❌', 'bot': '⭕'},
        'turn': 0,
        'mode': 'vsbot'
    }
    
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(InlineKeyboardButton(board[i][j], callback_data=f"ttt_{i}_{j}"))
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "⭕ **Tic Tac Toe - VS Bot** ⭕\n\n"
        "You: ❌\nBot: ⭕\n\n"
        "**Your turn!** Click any cell to make your move!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def tictactoe_multi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Tic Tac Toe Multiplayer"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    # Initialize game board
    board = [["⬜" for _ in range(3)] for _ in range(3)]
    active_games[chat_id] = {
        'type': 'ttt',
        'board': board,
        'current_player': user_id,
        'players': [user_id],
        'symbols': {user_id: '❌'},
        'turn': 0,
        'mode': 'multiplayer'
    }
    
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(InlineKeyboardButton(board[i][j], callback_data=f"ttt_{i}_{j}"))
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "⭕ **Tic Tac Toe - Multiplayer** ⭕\n\n"
        "Player 1: ❌\nPlayer 2: ⭕\n\n"
        "**Waiting for Player 2 to join...**\n"
        "Click any cell to make your move!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

def get_bot_ttt_move(board):
    """Simple AI for Tic Tac Toe"""
    # Try to win
    for i in range(3):
        for j in range(3):
            if board[i][j] == '⬜':
                board[i][j] = '⭕'
                if check_ttt_winner(board):
                    board[i][j] = '⬜'
                    return (i, j)
                board[i][j] = '⬜'
    
    # Block player from winning
    for i in range(3):
        for j in range(3):
            if board[i][j] == '⬜':
                board[i][j] = '❌'
                if check_ttt_winner(board):
                    board[i][j] = '⬜'
                    return (i, j)
                board[i][j] = '⬜'
    
    # Take center if available
    if board[1][1] == '⬜':
        return (1, 1)
    
    # Take corners
    corners = [(0,0), (0,2), (2,0), (2,2)]
    random.shuffle(corners)
    for corner in corners:
        if board[corner[0]][corner[1]] == '⬜':
            return corner
    
    # Take any available spot
    for i in range(3):
        for j in range(3):
            if board[i][j] == '⬜':
                return (i, j)
    
    return None

# Tic Tac Toe Game
async def tictactoe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Tic Tac Toe game"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    # Initialize game board
    board = [["⬜" for _ in range(3)] for _ in range(3)]
    active_games[chat_id] = {
        'type': 'ttt',
        'board': board,
        'current_player': user_id,
        'players': [user_id],
        'symbols': {user_id: '❌'},
        'turn': 0
    }
    
    keyboard = []
    for i in range(3):
        row = []
        for j in range(3):
            row.append(InlineKeyboardButton(board[i][j], callback_data=f"ttt_{i}_{j}"))
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "⭕ **Tic Tac Toe Started!** ⭕\n\n"
        "❌ - Player 1\n⭕ - Player 2\n\n"
        "Waiting for Player 2 to join...\n"
        "Click any cell to make your move!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def ttt_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle Tic Tac Toe moves with bot AI"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    if chat_id not in active_games or 'ttt' not in active_games[chat_id]['type']:
        await query.edit_message_text("❌ No active game. Start with /tictactoe")
        return
    
    game = active_games[chat_id]
    
    # Add second player in multiplayer
    if game.get('mode') == 'multiplayer' and len(game['players']) == 1 and user_id != game['players'][0]:
        game['players'].append(user_id)
        game['symbols'][user_id] = '⭕'
    
    # Check if it's player's turn
    if user_id != game['current_player']:
        await query.answer("❌ Not your turn!", show_alert=True)
        return
    
    # Parse move
    _, row, col = query.data.split('_')
    row, col = int(row), int(col)
    
    # Check if cell is empty
    if game['board'][row][col] != '⬜':
        await query.answer("❌ Cell already taken!", show_alert=True)
        return
    
    # Make move
    symbol = game['symbols'][user_id]
    game['board'][row][col] = symbol
    game['turn'] += 1
    
    # Check winner
    winner = check_ttt_winner(game['board'])
    
    # Update board
    keyboard = []
    for i in range(3):
        row_buttons = []
        for j in range(3):
            row_buttons.append(InlineKeyboardButton(game['board'][i][j], callback_data=f"ttt_{i}_{j}"))
        keyboard.append(row_buttons)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if winner:
        db.add_points(user_id, 10)
        db.record_game(user_id, 'tictactoe', 'win')
        await query.edit_message_text(
            f"🎉 **Game Over!** 🎉\n\n{symbol} **Winner: {query.from_user.first_name}**\n+10 points! 🏆",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        del active_games[chat_id]
        return
    elif game['turn'] >= 9:
        await query.edit_message_text(
            "🤝 **Game Over - Draw!** 🤝\n\nNo winner this time!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        del active_games[chat_id]
        return
    
    # Bot move in VS Bot mode
    if game.get('mode') == 'vsbot':
        bot_move = get_bot_ttt_move(game['board'])
        if bot_move:
            game['board'][bot_move[0]][bot_move[1]] = '⭕'
            game['turn'] += 1
            
            # Check winner after bot move
            winner = check_ttt_winner(game['board'])
            
            keyboard = []
            for i in range(3):
                row_buttons = []
                for j in range(3):
                    row_buttons.append(InlineKeyboardButton(game['board'][i][j], callback_data=f"ttt_{i}_{j}"))
                keyboard.append(row_buttons)
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if winner:
                db.record_game(user_id, 'tictactoe', 'loss')
                await query.edit_message_text(
                    "🤖 **Game Over!** 🤖\n\n⭕ **Bot Wins!**\n\nBetter luck next time!",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                del active_games[chat_id]
            elif game['turn'] >= 9:
                await query.edit_message_text(
                    "🤝 **Game Over - Draw!** 🤝\n\nNo winner this time!",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
                del active_games[chat_id]
            else:
                await query.edit_message_text(
                    "⭕ **Tic Tac Toe - VS Bot** ⭕\n\n**Your turn!** Make your move!",
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
    else:
        # Multiplayer mode - switch player
        current_idx = game['players'].index(game['current_player'])
        game['current_player'] = game['players'][(current_idx + 1) % len(game['players'])]
        next_symbol = game['symbols'][game['current_player']]
        
        await query.edit_message_text(
            f"⭕ **Tic Tac Toe - Multiplayer** ⭕\n\nCurrent turn: {next_symbol}",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

def check_ttt_winner(board):
    """Check Tic Tac Toe winner"""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != '⬜':
            return True
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != '⬜':
            return True
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != '⬜':
        return True
    if board[0][2] == board[1][1] == board[2][0] != '⬜':
        return True
    
    return False

# ========== ROCK PAPER SCISSORS - VS BOT + MULTIPLAYER ========== #

async def rps_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show RPS mode selection"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [InlineKeyboardButton("🤖 VS Bot", callback_data="rps_vsbot")],
        [InlineKeyboardButton("👥 Multiplayer", callback_data="rps_multi")],
        [InlineKeyboardButton("⬅️ Back to Games", callback_data="back_to_games")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "✊ **Rock Paper Scissors - Choose Mode:**\n\n"
        "🤖 **VS Bot:** Play against AI\n"
        "👥 **Multiplayer:** Challenge a friend",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def rps_vsbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start RPS VS Bot"""
    query = update.callback_query
    await query.answer()
    
    keyboard = [
        [
            InlineKeyboardButton("🪨 Rock", callback_data="rps_bot_rock"),
            InlineKeyboardButton("📄 Paper", callback_data="rps_bot_paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="rps_bot_scissors")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        "✊ **Rock Paper Scissors - VS Bot!** ✊\n\nChoose your move:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def rps_multi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start RPS Multiplayer"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    active_games[chat_id] = {
        'type': 'rps_multi',
        'players': {user_id: None},
        'starter': user_id
    }
    
    keyboard = [
        [
            InlineKeyboardButton("🪨 Rock", callback_data="rps_multi_rock"),
            InlineKeyboardButton("📄 Paper", callback_data="rps_multi_paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="rps_multi_scissors")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        f"✊ **Rock Paper Scissors - Multiplayer!** ✊\n\n"
        f"**Player 1:** {query.from_user.first_name}\n"
        f"**Waiting for Player 2...**\n\n"
        f"Both players: Choose your move!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Rock Paper Scissors (old command for backwards compatibility)
async def rps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Rock Paper Scissors - redirects to menu"""
    keyboard = [
        [InlineKeyboardButton("🤖 VS Bot", callback_data="rps_vsbot")],
        [InlineKeyboardButton("👥 Multiplayer", callback_data="rps_multi")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✊ **Rock Paper Scissors - Choose Mode:**\n\n"
        "🤖 **VS Bot:** Play against AI\n"
        "👥 **Multiplayer:** Challenge a friend",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def rps_bot_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle RPS VS Bot moves"""
    query = update.callback_query
    await query.answer()
    
    user_choice = query.data.split('_')[2]
    bot_choice = random.choice(['rock', 'paper', 'scissors'])
    
    choices_emoji = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
    
    # Determine winner
    if user_choice == bot_choice:
        result = "🤝 **It's a Draw!**"
        points = 0
    elif (user_choice == 'rock' and bot_choice == 'scissors') or \
         (user_choice == 'paper' and bot_choice == 'rock') or \
         (user_choice == 'scissors' and bot_choice == 'paper'):
        result = "🎉 **You Win!** 🎉"
        points = 5
        db.add_points(query.from_user.id, points)
        db.record_game(query.from_user.id, 'rps', 'win')
    else:
        result = "🤖 **Bot Wins!**"
        points = 0
        db.record_game(query.from_user.id, 'rps', 'loss')
    
    await query.edit_message_text(
        f"✊ **Rock Paper Scissors - VS Bot** ✊\n\n"
        f"You: {choices_emoji[user_choice]}\n"
        f"Bot: {choices_emoji[bot_choice]}\n\n"
        f"{result}\n"
        f"{f'+{points} points! 🏆' if points > 0 else ''}",
        parse_mode='Markdown'
    )

async def rps_multi_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle RPS Multiplayer moves"""
    query = update.callback_query
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    if chat_id not in active_games or active_games[chat_id]['type'] != 'rps_multi':
        await query.answer("❌ No active game!", show_alert=True)
        return
    
    game = active_games[chat_id]
    user_choice = query.data.split('_')[2]
    
    # Add player choice
    game['players'][user_id] = user_choice
    
    # Wait for both players
    if len(game['players']) < 2:
        await query.answer("✅ Choice locked! Waiting for opponent...")
        return
    
    if None in game['players'].values():
        await query.answer("✅ Choice locked! Waiting for opponent...")
        return
    
    await query.answer()
    
    # Both players have chosen
    players = list(game['players'].keys())
    choices = list(game['players'].values())
    
    choices_emoji = {'rock': '🪨', 'paper': '📄', 'scissors': '✂️'}
    
    # Determine winner
    if choices[0] == choices[1]:
        result = "🤝 **It's a Draw!**"
    elif (choices[0] == 'rock' and choices[1] == 'scissors') or \
         (choices[0] == 'paper' and choices[1] == 'rock') or \
         (choices[0] == 'scissors' and choices[1] == 'paper'):
        result = f"🎉 **Player 1 Wins!** 🎉"
        db.add_points(players[0], 5)
        db.record_game(players[0], 'rps', 'win')
        db.record_game(players[1], 'rps', 'loss')
    else:
        result = f"🎉 **Player 2 Wins!** 🎉"
        db.add_points(players[1], 5)
        db.record_game(players[1], 'rps', 'win')
        db.record_game(players[0], 'rps', 'loss')
    
    await query.edit_message_text(
        f"✊ **Rock Paper Scissors - Multiplayer** ✊\n\n"
        f"Player 1: {choices_emoji[choices[0]]}\n"
        f"Player 2: {choices_emoji[choices[1]]}\n\n"
        f"{result}",
        parse_mode='Markdown'
    )
    
    del active_games[chat_id]

async def rps_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle old RPS callback (backwards compatibility)"""
    # Redirect to bot move
    await rps_bot_move(update, context)

# Country Guess (Emoji)
async def country_guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Country Guess game"""
    chat_id = update.effective_chat.id
    emoji, country = random.choice(list(COUNTRIES.items()))
    
    # Create wrong options
    all_countries = list(COUNTRIES.values())
    all_countries.remove(country)
    wrong_options = random.sample(all_countries, 3)
    options = wrong_options + [country]
    random.shuffle(options)
    
    active_games[chat_id] = {
        'type': 'country',
        'answer': country,
        'emoji': emoji
    }
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"country_{opt}")] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🌍 **Guess the Country!** 🌍\n\n{emoji}\n\nWhich country is this?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def country_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle country guess answer"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    if chat_id not in active_games or active_games[chat_id]['type'] != 'country':
        await query.edit_message_text("❌ No active game. Start with /countryguess")
        return
    
    game = active_games[chat_id]
    user_answer = query.data.split('_', 1)[1]
    
    if user_answer == game['answer']:
        db.add_points(user_id, 8)
        db.record_game(user_id, 'countryguess', 'win')
        await query.edit_message_text(
            f"🎉 **Correct!** 🎉\n\n{game['emoji']} = {game['answer']}\n+8 points! 🏆",
            parse_mode='Markdown'
        )
    else:
        db.record_game(user_id, 'countryguess', 'loss')
        await query.edit_message_text(
            f"❌ **Wrong!**\n\nCorrect answer: {game['emoji']} = {game['answer']}",
            parse_mode='Markdown'
        )
    
    del active_games[chat_id]

# Quiz Game
async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Quiz game"""
    chat_id = update.effective_chat.id
    question_data = random.choice(QUIZ_QUESTIONS)
    
    active_games[chat_id] = {
        'type': 'quiz',
        'answer': question_data['a'],
        'question': question_data['q']
    }
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"quiz_{i}")] 
                for i, opt in enumerate(question_data['options'])]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"❓ **Quiz Time!** ❓\n\n{question_data['q']}",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle quiz answer"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    if chat_id not in active_games or active_games[chat_id]['type'] != 'quiz':
        await query.edit_message_text("❌ No active game. Start with /quiz")
        return
    
    game = active_games[chat_id]
    user_answer = int(query.data.split('_')[1])
    
    if user_answer == game['answer']:
        db.add_points(user_id, 5)
        db.record_game(user_id, 'quiz', 'win')
        await query.edit_message_text(
            f"🎉 **Correct!** 🎉\n\n+5 points! 🏆",
            parse_mode='Markdown'
        )
    else:
        db.record_game(user_id, 'quiz', 'loss')
        await query.edit_message_text(
            f"❌ **Wrong!**\n\nBetter luck next time!",
            parse_mode='Markdown'
        )
    
    del active_games[chat_id]

# Emoji Game
async def emoji_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Emoji Game"""
    chat_id = update.effective_chat.id
    emoji, meaning = random.choice(list(EMOJI_MEANINGS.items()))
    
    all_meanings = list(EMOJI_MEANINGS.values())
    all_meanings.remove(meaning)
    wrong_options = random.sample(all_meanings, 3)
    options = wrong_options + [meaning]
    random.shuffle(options)
    
    active_games[chat_id] = {
        'type': 'emoji',
        'answer': meaning,
        'emoji': emoji
    }
    
    keyboard = [[InlineKeyboardButton(opt, callback_data=f"emoji_{opt}")] for opt in options]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🔤 **Emoji Game!** 🔤\n\n{emoji}\n\nWhat does this emoji mean?",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def emoji_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle emoji game answer"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    if chat_id not in active_games or active_games[chat_id]['type'] != 'emoji':
        await query.edit_message_text("❌ No active game. Start with /emojigame")
        return
    
    game = active_games[chat_id]
    user_answer = query.data.split('_', 1)[1]
    
    if user_answer == game['answer']:
        db.add_points(user_id, 6)
        db.record_game(user_id, 'emojigame', 'win')
        await query.edit_message_text(
            f"🎉 **Correct!** 🎉\n\n{game['emoji']} = {game['answer']}\n+6 points! 🏆",
            parse_mode='Markdown'
        )
    else:
        db.record_game(user_id, 'emojigame', 'loss')
        await query.edit_message_text(
            f"❌ **Wrong!**\n\nCorrect answer: {game['emoji']} = {game['answer']}",
            parse_mode='Markdown'
        )
    
    del active_games[chat_id]

# LingoGrid Game
async def lingogrid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start LingoGrid game"""
    chat_id = update.effective_chat.id
    word = random.choice(LINGOGRID_WORDS)
    
    # Scramble the word
    scrambled = ''.join(random.sample(word, len(word)))
    
    active_games[chat_id] = {
        'type': 'lingo',
        'answer': word.lower(),
        'scrambled': scrambled,
        'user_id': update.effective_user.id
    }
    
    await update.message.reply_text(
        f"✍️ **LingoGrid!** ✍️\n\n"
        f"Unscramble this word:\n\n**{scrambled}**\n\n"
        f"Type your answer!",
        parse_mode='Markdown'
    )

# ========== RIDDLE GAME WITH HINT BUTTON ========== #

async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Riddle game with HINT button"""
    chat_id = update.effective_chat.id
    riddle_data = random.choice(RIDDLES)
    
    active_games[chat_id] = {
        'type': 'riddle',
        'answer': riddle_data['a'].lower(),
        'question': riddle_data['q'],
        'hint': riddle_data['hint'],
        'user_id': update.effective_user.id,
        'hint_used': False
    }
    
    keyboard = [[InlineKeyboardButton("💡 Get Hint", callback_data="riddle_hint")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"🧠 **Riddle Time!** 🧠\n\n{riddle_data['q']}\n\nType your answer!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def riddle_hint(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show hint for riddle"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    
    if chat_id not in active_games or active_games[chat_id]['type'] != 'riddle':
        await query.answer("❌ No active riddle!", show_alert=True)
        return
    
    game = active_games[chat_id]
    
    if game['hint_used']:
        await query.answer("💡 Hint already shown!", show_alert=True)
        return
    
    game['hint_used'] = True
    
    keyboard = [[InlineKeyboardButton("💡 Hint Used", callback_data="riddle_hint_used")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"🧠 **Riddle Time!** 🧠\n\n"
        f"{game['question']}\n\n"
        f"💡 **Hint:** {game['hint']}\n\n"
        f"Type your answer!",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

# Text answer handler
async def handle_text_answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text-based game answers"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    if chat_id not in active_games:
        return
    
    game = active_games[chat_id]
    
    if game['type'] in ['lingo', 'riddle'] and game.get('user_id') == user_id:
        user_answer = update.message.text.lower().strip()
        
        if user_answer == game['answer']:
            if game['type'] == 'lingo':
                points = 15
                game_name = 'lingo'
            else:
                # Riddle - check if hint was used
                points = 12 if not game.get('hint_used') else 8
                game_name = 'riddle'
            
            db.add_points(user_id, points)
            db.record_game(user_id, game_name, 'win')
            
            hint_msg = "\n💡 (Hint was used: -4 points)" if game.get('hint_used') else ""
            
            await update.message.reply_text(
                f"🎉 **Correct!** 🎉\n\n"
                f"Answer: **{game['answer'].upper()}**\n"
                f"+{points} points! 🏆{hint_msg}",
                parse_mode='Markdown'
            )
            del active_games[chat_id]
        else:
            await update.message.reply_text("❌ Wrong! Try again!")

# Leaderboard
async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show leaderboard"""
    top_users = db.get_leaderboard(10)
    
    if not top_users:
        await update.message.reply_text("🏆 No players yet! Be the first to play!")
        return
    
    leaderboard_text = "🏆 **TOP 10 PLAYERS** 🏆\n\n"
    medals = ["🥇", "🥈", "🥉"]
    
    for i, (user_id, username, points) in enumerate(top_users, 1):
        medal = medals[i-1] if i <= 3 else f"{i}."
        leaderboard_text += f"{medal} **{username}** - {points} points\n"
    
    await update.message.reply_text(leaderboard_text, parse_mode='Markdown')

# Stats
async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user statistics"""
    user_id = update.effective_user.id
    user_stats = db.get_user_stats(user_id)
    
    if not user_stats:
        await update.message.reply_text("📊 No statistics yet! Play some games first!")
        return
    
    total_games = user_stats['wins'] + user_stats['losses']
    win_rate = (user_stats['wins'] / total_games * 100) if total_games > 0 else 0
    
    stats_text = f"""
📊 **Your Statistics** 📊

👤 Player: {update.effective_user.first_name}
🏆 Total Points: {user_stats['points']}
🎮 Games Played: {total_games}
✅ Wins: {user_stats['wins']}
❌ Losses: {user_stats['losses']}
📈 Win Rate: {win_rate:.1f}%

Keep playing to climb the leaderboard! 🚀
    """
    
    await update.message.reply_text(stats_text, parse_mode='Markdown')

# Profile
async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user profile"""
    user_id = update.effective_user.id
    user_stats = db.get_user_stats(user_id)
    
    if not user_stats:
        await update.message.reply_text("👤 No profile yet! Play some games first!")
        return
    
    rank = db.get_user_rank(user_id)
    total_games = user_stats['wins'] + user_stats['losses']
    
    # Calculate level based on points
    level = user_stats['points'] // 100 + 1
    next_level_points = level * 100
    
    profile_text = f"""
👤 **Gaming Profile** 👤

**{update.effective_user.first_name}**

🏅 Rank: #{rank}
⭐ Level: {level}
🏆 Points: {user_stats['points']}/{next_level_points}
🎮 Total Games: {total_games}

**Game Breakdown:**
✅ Wins: {user_stats['wins']}
❌ Losses: {user_stats['losses']}

Keep grinding! 💪
    """
    
    await update.message.reply_text(profile_text, parse_mode='Markdown')

# Callback query router
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route callback queries to appropriate handlers"""
    query = update.callback_query
    data = query.data
    
    # Back to games menu
    if data == 'back_to_games':
        await query.answer()
        keyboard = [
            [InlineKeyboardButton("⭕ Tic Tac Toe", callback_data="game_ttt_menu")],
            [InlineKeyboardButton("✊ Rock Paper Scissors", callback_data="game_rps_menu")],
            [InlineKeyboardButton("🌍 Country Guess (Emoji)", callback_data="game_country")],
            [InlineKeyboardButton("🗺️ Map Guess", callback_data="game_map")],
            [InlineKeyboardButton("❓ Quiz", callback_data="game_quiz")],
            [InlineKeyboardButton("🔤 Emoji Game", callback_data="game_emoji")],
            [InlineKeyboardButton("✍️ LingoGrid", callback_data="game_lingo")],
            [InlineKeyboardButton("🧠 Riddle", callback_data="game_riddle")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            "🎮 **Choose Your Game:**",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    # Tic Tac Toe handlers
    elif data == 'ttt_vsbot':
        await tictactoe_vsbot(update, context)
    elif data == 'ttt_multi':
        await tictactoe_multi(update, context)
    elif data.startswith('ttt_'):
        await ttt_move(update, context)
    # RPS handlers
    elif data == 'rps_vsbot':
        await rps_vsbot(update, context)
    elif data == 'rps_multi':
        await rps_multi(update, context)
    elif data.startswith('rps_bot_'):
        await rps_bot_move(update, context)
    elif data.startswith('rps_multi_'):
        await rps_multi_move(update, context)
    elif data.startswith('rps_'):
        await rps_move(update, context)
    # Riddle hint
    elif data == 'riddle_hint':
        await riddle_hint(update, context)
    elif data == 'riddle_hint_used':
        await query.answer("💡 Hint already shown!")
    # Other games
    elif data.startswith('country_'):
        await country_answer(update, context)
    elif data.startswith('quiz_'):
        await quiz_answer(update, context)
    elif data.startswith('emoji_'):
        await emoji_answer(update, context)
    # Game menu selections
    elif data.startswith('game_'):
        game_type = data.split('_')[1]
        if game_type == 'ttt':
            await tictactoe_menu(update, context)
        elif game_type == 'rps':
            await rps_menu(update, context)
        elif game_type == 'country':
            await country_guess(update, context)
        elif game_type == 'quiz':
            await quiz(update, context)
        elif game_type == 'emoji':
            await emoji_game(update, context)
        elif game_type == 'lingo':
            await lingogrid(update, context)
        elif game_type == 'riddle':
            await riddle(update, context)

def main():
    """Start the bot"""
    # Get token from environment
    TOKEN = os.getenv('BOT_TOKEN')
    
    if not TOKEN:
        logger.error("BOT_TOKEN not found in environment variables!")
        return
    
    # Create application
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("games", games_list))
    application.add_handler(CommandHandler("tictactoe", tictactoe))
    application.add_handler(CommandHandler("rps", rps))
    application.add_handler(CommandHandler("countryguess", country_guess))
    application.add_handler(CommandHandler("mapguess", country_guess))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(CommandHandler("emojigame", emoji_game))
    application.add_handler(CommandHandler("lingogrid", lingogrid))
    application.add_handler(CommandHandler("riddle", riddle))
    application.add_handler(CommandHandler("leaderboard", leaderboard))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("profile", profile))

    application.add_handler(CallbackQueryHandler(button_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_answer))

    # 🚀 Start dummy web server (Render fix)
    threading.Thread(target=run_web_server, daemon=True).start()

    logger.warning("🎮 GameVerse Bot Started!")

    application.run_polling(allowed_updates=Update.ALL_TYPES)

# ---------------- RUN ---------------- #

if __name__ == '__main__':
    main()
