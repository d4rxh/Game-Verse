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
    "🇸🇦": "Saudi Arabia", "🇦🇪": "UAE", "🇹🇷": "Turkey", "🇿🇦": "South Africa", "🇳🇬": "Nigeria"
}

RIDDLES = [
    {"q": "What has keys but no locks, space but no room, and you can enter but can't go inside?", "a": "keyboard"},
    {"q": "I speak without a mouth and hear without ears. I have no body, but come alive with wind. What am I?", "a": "echo"},
    {"q": "The more you take, the more you leave behind. What am I?", "a": "footsteps"},
    {"q": "What can travel around the world while staying in a corner?", "a": "stamp"},
    {"q": "I have cities, but no houses. I have mountains, but no trees. I have water, but no fish. What am I?", "a": "map"},
    {"q": "What gets wet while drying?", "a": "towel"},
    {"q": "What can you break, even if you never pick it up or touch it?", "a": "promise"},
    {"q": "What goes up but never comes down?", "a": "age"},
    {"q": "I'm tall when I'm young, and short when I'm old. What am I?", "a": "candle"},
    {"q": "What has hands but cannot clap?", "a": "clock"}
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
    {"q": "Which programming language is known as the 'language of the web'?", "options": ["Python", "Java", "JavaScript", "C++"], "a": 2}
]

EMOJI_MEANINGS = {
    "🔥": "Fire", "💧": "Water", "🌍": "Earth", "💨": "Wind", "⚡": "Lightning",
    "🌙": "Moon", "☀️": "Sun", "⭐": "Star", "🌈": "Rainbow", "❄️": "Snow",
    "🌸": "Flower", "🌳": "Tree", "🍕": "Pizza", "🍔": "Burger", "🍰": "Cake"
}

LINGOGRID_WORDS = ["PYTHON", "CODING", "GAMES", "ROBOT", "CLOUD", "BRAIN", "MUSIC", "DANCE", "HAPPY", "WORLD"]

# Game states
active_games = {}

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command with welcome message"""
    user = update.effective_user
    db.add_user(user.id, user.first_name)
    
    welcome_text = f"""
🎮 **Welcome to GameVerse, {user.first_name}!** 🎮

Transform your chat into an interactive game zone! 🚀

🎯 **Available Games:**
⭕ /tictactoe - Play Tic Tac Toe with friends
✊ /rps - Rock Paper Scissors battle
🌍 /countryguess - Guess the country (Emoji mode)
🗺️ /mapguess - Guess the country (Map mode)
❓ /quiz - Test your knowledge
🔤 /emojigame - Guess the emoji meaning
✍️ /lingogrid - Word guessing game
🧠 /riddle - Solve brain teasers

📊 **Leaderboard & Stats:**
🏆 /leaderboard - Top players
📈 /stats - Your game statistics
🎯 /profile - Your gaming profile

💡 **Group Features:**
• Multiplayer games
• Point system
• Real-time leaderboards
• Fun challenges

Let's play! Choose a game and start earning points! 🎊
    """
    await update.message.reply_text(welcome_text, parse_mode='Markdown')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    help_text = """
🎮 **GameVerse Help** 🎮

**How to Play:**
1️⃣ Choose a game from the menu
2️⃣ Follow the game instructions
3️⃣ Earn points for wins
4️⃣ Climb the leaderboard

**Point System:**
• Tic Tac Toe Win: 10 points
• RPS Win: 5 points
• Country Guess: 8 points
• Quiz Correct: 5 points
• Emoji Game: 6 points
• LingoGrid: 15 points
• Riddle Solved: 12 points

**Commands:**
/start - Start the bot
/help - Show this message
/games - List all games
/leaderboard - Top 10 players
/stats - Your statistics
/profile - Your gaming profile

**Tips:**
💡 Play daily to maintain streaks
💡 Challenge friends in groups
💡 Complete all games for bonus points

Need support? Contact @YourUsername
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def games_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """List all available games"""
    keyboard = [
        [InlineKeyboardButton("⭕ Tic Tac Toe", callback_data="game_ttt")],
        [InlineKeyboardButton("✊ Rock Paper Scissors", callback_data="game_rps")],
        [InlineKeyboardButton("🌍 Country Guess (Emoji)", callback_data="game_country")],
        [InlineKeyboardButton("🗺️ Map Guess", callback_data="game_map")],
        [InlineKeyboardButton("❓ Quiz", callback_data="game_quiz")],
        [InlineKeyboardButton("🔤 Emoji Game", callback_data="game_emoji")],
        [InlineKeyboardButton("✍️ LingoGrid", callback_data="game_lingo")],
        [InlineKeyboardButton("🧠 Riddle", callback_data="game_riddle")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🎮 **Choose Your Game:**", reply_markup=reply_markup, parse_mode='Markdown')

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
    """Handle Tic Tac Toe moves"""
    query = update.callback_query
    await query.answer()
    
    chat_id = query.message.chat_id
    user_id = query.from_user.id
    
    if chat_id not in active_games or active_games[chat_id]['type'] != 'ttt':
        await query.edit_message_text("❌ No active game. Start with /tictactoe")
        return
    
    game = active_games[chat_id]
    
    # Add second player
    if len(game['players']) == 1 and user_id != game['players'][0]:
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
    elif game['turn'] >= 9:
        await query.edit_message_text(
            "🤝 **Game Over - Draw!** 🤝\n\nNo winner this time!",
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        del active_games[chat_id]
    else:
        # Switch player
        current_idx = game['players'].index(game['current_player'])
        game['current_player'] = game['players'][(current_idx + 1) % len(game['players'])]
        next_symbol = game['symbols'][game['current_player']]
        
        await query.edit_message_text(
            f"⭕ **Tic Tac Toe** ⭕\n\nCurrent turn: {next_symbol}",
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

# Rock Paper Scissors
async def rps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Rock Paper Scissors"""
    keyboard = [
        [
            InlineKeyboardButton("🪨 Rock", callback_data="rps_rock"),
            InlineKeyboardButton("📄 Paper", callback_data="rps_paper"),
            InlineKeyboardButton("✂️ Scissors", callback_data="rps_scissors")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "✊ **Rock Paper Scissors!** ✊\n\nChoose your move:",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def rps_move(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle RPS moves"""
    query = update.callback_query
    await query.answer()
    
    user_choice = query.data.split('_')[1]
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
        result = "😔 **You Lose!**"
        points = 0
        db.record_game(query.from_user.id, 'rps', 'loss')
    
    await query.edit_message_text(
        f"✊ **Rock Paper Scissors** ✊\n\n"
        f"You: {choices_emoji[user_choice]}\n"
        f"Bot: {choices_emoji[bot_choice]}\n\n"
        f"{result}\n"
        f"{f'+{points} points! 🏆' if points > 0 else ''}",
        parse_mode='Markdown'
    )

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

# Riddle Game
async def riddle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start Riddle game"""
    chat_id = update.effective_chat.id
    riddle_data = random.choice(RIDDLES)
    
    active_games[chat_id] = {
        'type': 'riddle',
        'answer': riddle_data['a'].lower(),
        'question': riddle_data['q'],
        'user_id': update.effective_user.id
    }
    
    await update.message.reply_text(
        f"🧠 **Riddle Time!** 🧠\n\n{riddle_data['q']}\n\nType your answer!",
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
            points = 15 if game['type'] == 'lingo' else 12
            db.add_points(user_id, points)
            db.record_game(user_id, game['type'], 'win')
            
            await update.message.reply_text(
                f"🎉 **Correct!** 🎉\n\n"
                f"Answer: **{game['answer'].upper()}**\n"
                f"+{points} points! 🏆",
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
    
    if data.startswith('ttt_'):
        await ttt_move(update, context)
    elif data.startswith('rps_'):
        await rps_move(update, context)
    elif data.startswith('country_'):
        await country_answer(update, context)
    elif data.startswith('quiz_'):
        await quiz_answer(update, context)
    elif data.startswith('emoji_'):
        await emoji_answer(update, context)
    elif data.startswith('game_'):
        game_type = data.split('_')[1]
        if game_type == 'ttt':
            await tictactoe(update, context)
        elif game_type == 'rps':
            await rps(update, context)
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
