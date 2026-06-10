#!/data/data/com.termux/files/usr/bin/bash
# ============================================================
# Telegram Shop Bot — Termux সেটআপ স্ক্রিপ্ট
# Bohudur Payment API সহ
# ============================================================

set -e

echo "========================================"
echo "  Telegram Shop Bot সেটআপ শুরু হচ্ছে"
echo "  Bohudur Payment Gateway"
echo "========================================"
echo ""

# ---- ধাপ ১: প্যাকেজ আপডেট ----
echo "[১/৫] প্যাকেজ আপডেট হচ্ছে..."
pkg update -y && pkg upgrade -y

# ---- ধাপ ২: পাইথন ইনস্টল ----
echo ""
echo "[২/৫] Python ইনস্টল হচ্ছে..."
pkg install -y python python-pip

# ---- ধাপ ৩: প্রজেক্ট ফোল্ডারে যান ----
echo ""
echo "[৩/৫] প্রজেক্ট ফোল্ডার তৈরি হচ্ছে..."
mkdir -p ~/telegram-shop
cd ~/telegram-shop

# ---- ধাপ ৪: ডিপেন্ডেন্সি ইনস্টল ----
echo ""
echo "[৪/৫] ডিপেন্ডেন্সি ইনস্টল হচ্ছে (এটি কিছুটা সময় নিতে পারে)..."
pip install --upgrade pip

pip install python-dotenv==1.0.1 \
  aiogram==3.22.0 \
  SQLAlchemy==2.0.43 \
  aiohttp==3.12.14 \
  aiosqlite==0.20.0 \
  pydantic==2.5.0 \
  cryptography==41.0.7 \
  python-dateutil==2.8.2

# ঐচ্ছিক: অ্যাডমিন প্যানেলের জন্য
pip install sqladmin starlette uvicorn itsdangerous markupsafe

# ---- ধাপ ৫: .env ফাইল চেক ----
echo ""
echo "[৫/৫] সেটআপ যাচাই করা হচ্ছে..."

if [ ! -f .env ]; then
    echo "⚠️  .env ফাইল পাওয়া যায়নি!"
    echo "আপনার .env.example থেকে কপি করে আপনার তথ্য দিন:"
    echo "  cp .env.example .env"
    echo "  nano .env"
else
    echo "✅ .env ফাইল পাওয়া গেছে"
fi

# data ও logs ফোল্ডার তৈরি
mkdir -p data logs

echo ""
echo "========================================"
echo "  ✅ সেটআপ সম্পন্ন!"
echo "========================================"
echo ""
echo "বট চালু করতে নিচের কমান্ড চালান:"
echo ""
echo "  cd ~/telegram-shop"
echo "  python run.py"
echo ""
echo "বট বন্ধ করতে: Ctrl + C"
echo ""