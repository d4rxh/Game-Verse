# 🎮 GameVerse - Ultimate Telegram Game Bot

**Transform your Telegram group chats into an interactive game zone!** 🚀

[English](#english) | [हिंदी](#hindi)

---

## English

### 🌟 Features

#### 🎯 Games Available:
1. **⭕ Tic Tac Toe** - Classic 2-player strategy game
2. **✊ Rock Paper Scissors** - Quick battle against the bot
3. **🌍 Country Guess** - Identify countries from emoji flags
4. **🗺️ Map Guess** - Guess countries from map shapes
5. **❓ Quiz** - Test your general knowledge
6. **🔤 Emoji Game** - Guess emoji meanings
7. **✍️ LingoGrid** - Unscramble word puzzles
8. **🧠 Riddles** - Solve brain teasers

#### 🏆 Additional Features:
- **Points System** - Earn points for every win
- **Live Leaderboard** - Compete with friends
- **User Statistics** - Track your gaming progress
- **Profile System** - Level up based on points
- **Multiplayer Support** - Play with group members
- **Auto-save Progress** - Never lose your data

---

### 📋 Prerequisites

Before starting, make sure you have:
- A Telegram account
- Basic computer knowledge
- Internet connection

**No coding experience needed!** We'll guide you through everything.

---

### 🚀 Complete Setup Guide

#### Step 1: Create Your Bot on Telegram

1. **Open Telegram** and search for `@BotFather`
2. **Start a chat** with BotFather by clicking "Start"
3. **Create your bot:**
   - Type `/newbot`
   - Enter a **name** for your bot (Example: "GameVerse Bot")
   - Enter a **username** ending in "bot" (Example: "MyGameVerseBot")
   
4. **Save your token:**
   - BotFather will give you a token like: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **⚠️ KEEP THIS SECRET!** Don't share it with anyone
   - Copy and save it somewhere safe

5. **Optional: Set bot commands** (makes it easier for users):
   - Type `/setcommands` to BotFather
   - Select your bot
   - Copy and paste this:
   ```
   start - Start the bot
   help - Show help message
   games - List all games
   tictactoe - Play Tic Tac Toe
   rps - Rock Paper Scissors
   countryguess - Guess the country
   quiz - Take a quiz
   emojigame - Emoji guessing game
   lingogrid - Word puzzle
   riddle - Solve riddles
   leaderboard - Top players
   stats - Your statistics
   profile - Your gaming profile
   ```

#### Step 2: Download the Bot Code

**Option A: Using Git (Recommended)**
1. Install Git:
   - Windows: Download from [git-scm.com](https://git-scm.com/)
   - Mac: `brew install git`
   - Linux: `sudo apt install git`

2. Clone the repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gameverse-bot.git
   cd gameverse-bot
   ```

**Option B: Download ZIP**
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract the ZIP file
4. Open terminal/command prompt in that folder

#### Step 3: Install Python

1. **Download Python:**
   - Go to [python.org](https://www.python.org/downloads/)
   - Download Python 3.8 or higher
   - **⚠️ Important:** Check "Add Python to PATH" during installation

2. **Verify installation:**
   ```bash
   python --version
   ```
   Should show: `Python 3.x.x`

#### Step 4: Install Dependencies

1. **Open terminal/command prompt** in the bot folder

2. **Install required packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Wait for installation** to complete (may take 1-2 minutes)

#### Step 5: Configure Your Bot

1. **Create `.env` file:**
   - Copy `.env.example` to `.env`
   - Windows: `copy .env.example .env`
   - Mac/Linux: `cp .env.example .env`

2. **Edit `.env` file:**
   - Open `.env` in any text editor (Notepad, VSCode, etc.)
   - Replace `your_bot_token_here` with your actual bot token
   - Save the file

   Example:
   ```
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

#### Step 6: Test Your Bot Locally

1. **Run the bot:**
   ```bash
   python bot.py
   ```

2. **You should see:**
   ```
   🎮 GameVerse Bot Started! 🎮
   ```

3. **Test on Telegram:**
   - Open your bot on Telegram
   - Type `/start`
   - Try playing a game!

4. **Stop the bot:** Press `Ctrl+C`

---

### ☁️ Deploy to Free Hosting

#### Option 1: Render (Recommended - Easiest)

1. **Create Render Account:**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create New Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name:** gameverse-bot
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python bot.py`

3. **Add Environment Variables:**
   - Go to "Environment" tab
   - Add: `BOT_TOKEN` = `your_bot_token`

4. **Deploy:**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Your bot is now live 24/7! 🎉

#### Option 2: Railway

1. **Create Railway Account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Deploy from GitHub:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add Environment Variables:**
   - Go to "Variables" tab
   - Add: `BOT_TOKEN` = `your_bot_token`

4. **Deploy:**
   - Railway will auto-deploy
   - Your bot is live! 🚀

#### Option 3: PythonAnywhere

1. **Create Account:**
   - Go to [pythonanywhere.com](https://www.pythonanywhere.com)
   - Sign up for free account

2. **Upload Code:**
   - Go to "Files" tab
   - Upload all bot files

3. **Install Dependencies:**
   - Go to "Consoles" → "Bash"
   - Run: `pip3 install --user -r requirements.txt`

4. **Set Environment Variable:**
   - Add to `.bashrc`: `export BOT_TOKEN='your_token'`

5. **Create Always-On Task:**
   - Go to "Tasks" tab
   - Add: `python3 /home/yourusername/bot.py`

---

### 📱 Add Bot to Group

1. **Add bot to your group:**
   - Open your Telegram group
   - Click "Add Members"
   - Search for your bot
   - Add it

2. **Make bot admin (optional but recommended):**
   - Group Settings → Administrators
   - Add your bot as admin

3. **Start playing:**
   - Type `/start` in the group
   - Type `/games` to see all games
   - Enjoy! 🎮

---

### 🎮 How to Play

#### Starting Games:
- `/tictactoe` - Start Tic Tac Toe
- `/rps` - Play Rock Paper Scissors
- `/countryguess` - Guess countries
- `/quiz` - Take a quiz
- `/emojigame` - Emoji game
- `/lingogrid` - Word puzzle
- `/riddle` - Solve riddles

#### Tracking Progress:
- `/leaderboard` - See top players
- `/stats` - Your statistics
- `/profile` - Your gaming profile

---

### 🎯 Point System

| Game | Points per Win |
|------|---------------|
| Tic Tac Toe | 10 points |
| Rock Paper Scissors | 5 points |
| Country Guess | 8 points |
| Quiz | 5 points |
| Emoji Game | 6 points |
| LingoGrid | 15 points |
| Riddle | 12 points |

**Level Up:** Every 100 points = 1 level! 🌟

---

### 🔧 Troubleshooting

#### Bot not responding?
- Check if bot is running
- Verify BOT_TOKEN is correct
- Check internet connection

#### Commands not working?
- Make sure bot is admin in group
- Restart the bot
- Check for typos in commands

#### Deploy failing?
- Check all files are uploaded
- Verify requirements.txt exists
- Check Python version (must be 3.8+)

#### Database errors?
- Delete `gameverse.db` file
- Restart bot (will create new database)

---

### 📞 Support

Having issues? 
- Check [Issues](https://github.com/YOUR_USERNAME/gameverse-bot/issues)
- Create new issue with details
- Join our [Telegram Group](https://t.me/YOUR_GROUP)

---

### 🤝 Contributing

Want to add features?
1. Fork the repository
2. Create your feature branch
3. Make changes
4. Submit pull request

---

### 📄 License

MIT License - Feel free to use and modify!

---

## Hindi

### 🌟 फीचर्स

#### 🎯 उपलब्ध गेम्स:
1. **⭕ टिक टैक टो** - क्लासिक 2-प्लेयर गेम
2. **✊ रॉक पेपर सीज़र्स** - बॉट के साथ तेज़ लड़ाई
3. **🌍 कंट्री गेस** - इमोजी फ्लैग से देश पहचानो
4. **🗺️ मैप गेस** - नक्शे से देश पहचानो
5. **❓ क्विज़** - अपना ज्ञान टेस्ट करो
6. **🔤 इमोजी गेम** - इमोजी का मतलब बताओ
7. **✍️ लिंगोग्रिड** - शब्द पहेली सुलझाओ
8. **🧠 पहेलियाँ** - दिमागी सवाल हल करो

#### 🏆 अतिरिक्त फीचर्स:
- **पॉइंट सिस्टम** - हर जीत पर पॉइंट्स कमाओ
- **लाइव लीडरबोर्ड** - दोस्तों से प्रतिस्पर्धा करो
- **यूज़र स्टैटिस्टिक्स** - अपनी प्रगति ट्रैक करो
- **प्रोफाइल सिस्टम** - पॉइंट्स पर लेवल अप करो
- **मल्टीप्लेयर सपोर्ट** - ग्रुप मेंबर्स के साथ खेलो
- **ऑटो-सेव** - डेटा कभी नहीं खोएगा

---

### 📋 आवश्यकताएं

शुरू करने से पहले ज़रूरी चीज़ें:
- टेलीग्राम अकाउंट
- बेसिक कंप्यूटर नॉलेज
- इंटरनेट कनेक्शन

**कोडिंग का अनुभव ज़रूरी नहीं!** हम सब कुछ सिखाएंगे।

---

### 🚀 पूरी सेटअप गाइड

#### स्टेप 1: टेलीग्राम पर बॉट बनाएं

1. **टेलीग्राम खोलें** और `@BotFather` सर्च करें
2. BotFather के साथ **चैट शुरू करें** ("Start" पर क्लिक करें)
3. **अपना बॉट बनाएं:**
   - टाइप करें `/newbot`
   - बॉट का **नाम** डालें (उदाहरण: "GameVerse Bot")
   - **यूज़रनेम** डालें जो "bot" से खत्म हो (उदाहरण: "MyGameVerseBot")
   
4. **टोकन सेव करें:**
   - BotFather आपको टोकन देगा जैसे: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **⚠️ इसे गुप्त रखें!** किसी से शेयर ना करें
   - कॉपी करके कहीं सुरक्षित जगह सेव करें

5. **ऑप्शनल: बॉट कमांड्स सेट करें:**
   - BotFather को `/setcommands` टाइप करें
   - अपना बॉट सेलेक्ट करें
   - यह कॉपी-पेस्ट करें:
   ```
   start - बॉट शुरू करें
   help - हेल्प मैसेज दिखाएं
   games - सभी गेम्स की लिस्ट
   tictactoe - टिक टैक टो खेलें
   rps - रॉक पेपर सीज़र्स
   countryguess - देश पहचानो
   quiz - क्विज़ लें
   emojigame - इमोजी गेम
   lingogrid - शब्द पहेली
   riddle - पहेलियाँ हल करें
   leaderboard - टॉप प्लेयर्स
   stats - आपकी स्टैटिस्टिक्स
   profile - आपकी गेमिंग प्रोफाइल
   ```

#### स्टेप 2: बॉट कोड डाउनलोड करें

**ऑप्शन A: Git का उपयोग (अनुशंसित)**
1. Git इंस्टॉल करें:
   - Windows: [git-scm.com](https://git-scm.com/) से डाउनलोड करें
   - Mac: `brew install git`
   - Linux: `sudo apt install git`

2. Repository clone करें:
   ```bash
   git clone https://github.com/YOUR_USERNAME/gameverse-bot.git
   cd gameverse-bot
   ```

**ऑप्शन B: ZIP डाउनलोड करें**
1. GitHub repository पर जाएं
2. "Code" → "Download ZIP" पर क्लिक करें
3. ZIP फाइल extract करें
4. उस फोल्डर में terminal/command prompt खोलें

#### स्टेप 3: Python इंस्टॉल करें

1. **Python डाउनलोड करें:**
   - [python.org](https://www.python.org/downloads/) पर जाएं
   - Python 3.8 या higher डाउनलोड करें
   - **⚠️ ज़रूरी:** इंस्टॉलेशन के दौरान "Add Python to PATH" चेक करें

2. **इंस्टॉलेशन वेरिफाई करें:**
   ```bash
   python --version
   ```
   दिखना चाहिए: `Python 3.x.x`

#### स्टेप 4: Dependencies इंस्टॉल करें

1. **Terminal/command prompt खोलें** बॉट फोल्डर में

2. **ज़रूरी पैकेज इंस्टॉल करें:**
   ```bash
   pip install -r requirements.txt
   ```

3. **इंस्टॉलेशन पूरा होने का इंतज़ार करें** (1-2 मिनट लग सकते हैं)

#### स्टेप 5: अपना बॉट कॉन्फ़िगर करें

1. **`.env` फाइल बनाएं:**
   - `.env.example` को `.env` में कॉपी करें
   - Windows: `copy .env.example .env`
   - Mac/Linux: `cp .env.example .env`

2. **`.env` फाइल एडिट करें:**
   - `.env` को किसी टेक्स्ट एडिटर में खोलें (Notepad, VSCode, आदि)
   - `your_bot_token_here` को अपने असली बॉट टोकन से रिप्लेस करें
   - फाइल सेव करें

   उदाहरण:
   ```
   BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
   ```

#### स्टेप 6: अपना बॉट लोकली टेस्ट करें

1. **बॉट चलाएं:**
   ```bash
   python bot.py
   ```

2. **आपको दिखना चाहिए:**
   ```
   🎮 GameVerse Bot Started! 🎮
   ```

3. **टेलीग्राम पर टेस्ट करें:**
   - टेलीग्राम पर अपना बॉट खोलें
   - `/start` टाइप करें
   - कोई गेम खेलकर देखें!

4. **बॉट बंद करें:** `Ctrl+C` दबाएं

---

### ☁️ फ्री होस्टिंग पर डिप्लॉय करें

#### ऑप्शन 1: Render (अनुशंसित - सबसे आसान)

1. **Render अकाउंट बनाएं:**
   - [render.com](https://render.com) पर जाएं
   - GitHub से साइन अप करें

2. **नई Web Service बनाएं:**
   - "New +" → "Web Service" पर क्लिक करें
   - अपनी GitHub repository कनेक्ट करें
   - कॉन्फ़िगर करें:
     - **Name:** gameverse-bot
     - **Environment:** Python 3
     - **Build Command:** `pip install -r requirements.txt`
     - **Start Command:** `python bot.py`

3. **Environment Variables जोड़ें:**
   - "Environment" टैब पर जाएं
   - जोड़ें: `BOT_TOKEN` = `your_bot_token`

4. **Deploy करें:**
   - "Create Web Service" पर क्लिक करें
   - 2-3 मिनट deployment का इंतज़ार करें
   - आपका बॉट अब 24/7 लाइव है! 🎉

#### ऑप्शन 2: Railway

1. **Railway अकाउंट बनाएं:**
   - [railway.app](https://railway.app) पर जाएं
   - GitHub से साइन अप करें

2. **GitHub से Deploy करें:**
   - "New Project" पर क्लिक करें
   - "Deploy from GitHub repo" सेलेक्ट करें
   - अपनी repository चुनें

3. **Environment Variables जोड़ें:**
   - "Variables" टैब पर जाएं
   - जोड़ें: `BOT_TOKEN` = `your_bot_token`

4. **Deploy:**
   - Railway ऑटो-deploy करेगा
   - आपका बॉट लाइव है! 🚀

---

### 📱 बॉट को ग्रुप में जोड़ें

1. **बॉट को अपने ग्रुप में जोड़ें:**
   - अपना टेलीग्राम ग्रुप खोलें
   - "Add Members" पर क्लिक करें
   - अपना बॉट सर्च करें
   - इसे ऐड करें

2. **बॉट को एडमिन बनाएं (optional पर recommended):**
   - Group Settings → Administrators
   - अपने बॉट को एडमिन के रूप में जोड़ें

3. **खेलना शुरू करें:**
   - ग्रुप में `/start` टाइप करें
   - सभी गेम्स देखने के लिए `/games` टाइप करें
   - एंजॉय करें! 🎮

---

### 🎮 कैसे खेलें

#### गेम्स शुरू करना:
- `/tictactoe` - टिक टैक टो शुरू करें
- `/rps` - रॉक पेपर सीज़र्स खेलें
- `/countryguess` - देश पहचानो
- `/quiz` - क्विज़ लें
- `/emojigame` - इमोजी गेम
- `/lingogrid` - शब्द पहेली
- `/riddle` - पहेलियाँ हल करें

#### प्रगति ट्रैक करना:
- `/leaderboard` - टॉप प्लेयर्स देखें
- `/stats` - आपकी स्टैटिस्टिक्स
- `/profile` - आपकी गेमिंग प्रोफाइल

---

### 🎯 पॉइंट सिस्टम

| गेम | जीत पर पॉइंट्स |
|------|---------------|
| टिक टैक टो | 10 पॉइंट्स |
| रॉक पेपर सीज़र्स | 5 पॉइंट्स |
| कंट्री गेस | 8 पॉइंट्स |
| क्विज़ | 5 पॉइंट्स |
| इमोजी गेम | 6 पॉइंट्स |
| लिंगोग्रिड | 15 पॉइंट्स |
| पहेली | 12 पॉइंट्स |

**लेवल अप:** हर 100 पॉइंट्स = 1 लेवल! 🌟

---

### 🔧 समस्या निवारण

#### बॉट रिस्पॉन्ड नहीं कर रहा?
- चेक करें कि बॉट चल रहा है
- वेरिफाई करें कि BOT_TOKEN सही है
- इंटरनेट कनेक्शन चेक करें

#### Commands काम नहीं कर रहे?
- सुनिश्चित करें कि बॉट ग्रुप में एडमिन है
- बॉट रीस्टार्ट करें
- Commands में टाइपो चेक करें

#### Deploy फेल हो रहा है?
- चेक करें कि सभी फाइलें अपलोड हैं
- वेरिफाई करें कि requirements.txt मौजूद है
- Python version चेक करें (3.8+ होना चाहिए)

#### Database errors?
- `gameverse.db` फाइल डिलीट करें
- बॉट रीस्टार्ट करें (नया database बनाएगा)

---

### 📞 सपोर्ट

समस्या आ रही है?
- [Issues](https://github.com/YOUR_USERNAME/gameverse-bot/issues) चेक करें
- डिटेल्स के साथ नया issue बनाएं
- हमारे [Telegram Group](https://t.me/YOUR_GROUP) से जुड़ें

---

### 🤝 योगदान

फीचर्स जोड़ना चाहते हैं?
1. Repository fork करें
2. अपनी feature branch बनाएं
3. Changes करें
4. Pull request सबमिट करें

---

### 📄 लाइसेंस

MIT License - इस्तेमाल और modify करने के लिए स्वतंत्र!

---

## 🎉 Made with ❤️ for Telegram Gamers

**Happy Gaming! 🎮**
