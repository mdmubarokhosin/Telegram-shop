# Telegram Shop Bot — Bohudur Payment Integration
## সম্পূর্ণ সেটআপ গাইড (বাংলা)

এই গাইডে আপনি জানতে পারবেন কিভাবে Termux এ ডেভেলপ করবেন এবং Cloudflare + GitHub দিয়ে ডিপ্লয় করবেন।

---

## পূর্বে যা যা প্রয়োজন

| প্রয়োজনীয়তা | জিনিস |
|---|---|
| প্রয়োজন | Android ফোন (Termux এর জন্য) |
| প্রয়োজন | Telegram অ্যাকাউন্ট |
| প্রয়োজন | GitHub অ্যাকাউন্ট |
| প্রয়োজন | Cloudflare অ্যাকাউন্ট (ফ্রি প্ল্যান) |
| প্রয়োজন | Bohudur অ্যাকাউন্ট (Google লগইন) |
| প্রয়োজন নেই | ট্রেড লাইসেন্স |
| প্রয়োজন নেই | VPS/সার্ভার |
| প্রয়োজন নেই | PostgreSQL (SQLite ব্যবহৃত হয়) |

---

## ধাপ ১: Telegram Bot তৈরি করুন

1. Telegram খুলুন
2. **@BotFather** সার্চ করুন
3. `/newbot` কমান্ড দিন
4. বটের নাম দিন (যেমন: `MyDigitalShopBot`)
5. ইউজারনেম দিন (যেমন: `mydigitalshop_bot`)
6. BotFather আপনাকে একটি **BOT_TOKEN** দেবে (যেমন: `7483272074:AAEy...`)
7. এই টোকেন `.env` ফাইলে `TOKEN=` এর পরে বসান

### আপনার Telegram User ID বের করুন:
1. Telegram এ **@userinfobot** সার্চ করুন
2. পাঠান (Send) বাটন চাপুন
3. একটি নম্বর পাবেন (যেমন: `1779607726`)
4. এটি `.env` ফাইলে `OWNER_ID=` এর পরে বসান

---

## ধাপ ২: Bohudur API Key নিন

1. ব্রাউজারে **https://console.bohudur.one** যান
2. **Google দিয়ে লগইন** করুন
3. ড্যাশবোর্ড থেকে আপনার **API Key** কপি করুন
4. এই API Key `.env` ফাইলে `BOHUDUR_API_KEY=` এর পরে বসান

**টিপস**: Bohudur সম্পূর্ণ ফ্রি! কোনো মাসিক চার্জ, মাসিক ফি, বা ট্রেড লাইসেন্স লাগে না। শুধু ট্রানজেকশন ফি দিতে হয় (1%+VAT)।

### সাপোর্টেড পেমেন্ট মেথড:
- bKash (সেন্ড মানি)
- Nagad (সেন্ড মানি)
- Rocket (সেন্ড মানি)
- Upay
- SSLCommerz
- Stripe
- PayPal

### Bohudur API এর ৩টি এন্ডপয়েন্ট:

| এন্ডপয়েন্ট | কাজ |
|---|---|
| `POST /create/v2/` | পেমেন্ট সেশন তৈরি করে, payment_url দেয় |
| `POST /query/v2/` | পেমেন্টের স্ট্যাটাস চেক করে |
| `POST /execute/v2/` | পেমেন্ট নিশ্চিত করে (একবারই) |

---

## ধাপ ৩: Termux এ সেটআপ

### ৩.১ Termux ইনস্টল করুন

**F-Droid থেকে** Termux ইনস্টল করুন। গুগল প্লে স্টোর থেকে নয়! Play Store এর Termux আপডেট পায় না।

F-Droid লিংক: https://f-droid.org/en/packages/com.termux/

### ৩.২ দ্রুত সেটআপ (স্বয়ংক্রিয়)

নিচের কমান্ডগুলো একটি একটি করে কপি করে Termux এ পেস্ট করুন:

```bash
# প্যাকেজ আপডেট
pkg update -y && pkg upgrade -y

# Python ও Git ইনস্টল
pkg install python git -y

# প্রজেক্ট ক্লোন করুন
cd ~
git clone https://github.com/mdmubarokhosin/Telegram-shop.git
cd Telegram-shop

# ডিপেন্ডেন্সি ইনস্টল (কিছুটা সময় নিতে পারে)
pip install --upgrade pip
pip install -r requirements.txt

# ফোল্ডার তৈরি
mkdir -p data logs
```

### ৩.৩ .env ফাইল কনফিগার করুন

`.env` ফাইলটি ইতিমধ্যে আপনার তথ্য দিয়ে সেট করা আছে। তবে আপনি চাইলে পরিবর্তন করতে পারেন:

```bash
nano .env
```

নিশ্চিত করুন এই তিনটি সঠিক আছে:
- `TOKEN=` — আপনার BotFather টোকেন
- `OWNER_ID=` — আপনার Telegram User ID
- `BOHUDUR_API_KEY=` — আপনার Bohudur API Key

সেভ করতে: `Ctrl + X`, তারপর `Y`, তারপর `Enter`

### ৩.৪ বট চালু করুন

```bash
python run.py
```

বট চালু হলে নিচের মতো দেখাবে:
```
Starting bot: @YourBotUsername (ID: 123456789)
ডাটাবেস শুরু হয়েছে: SQLite (WAL মোড)
Recovery and admin panel initialized on localhost:9090
```

Telegram এ গিয়ে আপনার বটকে `/start` দিন। আপনি অটোমেটিক্যালি অ্যাডমিন হিসেবে সেট হবেন।

### ৩.৫ বট বন্ধ করুন

`Ctrl + C` চাপুন।

### ৩.৬ ব্যাকগ্রাউন্ডে চালু করুন (ফোন বন্ধ করলেও চলবে)

```bash
# প্রথমবার
nohup python run.py > bot_output.log 2>&1 &

# লগ দেখুন
tail -f bot_output.log

# বট বন্ধ করুন
pkill -f "python run.py"
```

**গুরুত্বপূর্ণ**: Termux ব্যাকগ্রাউন্ডে চালানোর সময় ফোনের ব্যাটারি সেভিং মোড বন্ধ রাখুন। Termux অ্যাপের ব্যাটারি অপশন থেকে "Unrestricted" সিলেক্ট করুন।

---

## ধাপ ৪: পণ্য যোগ করুন (অ্যাডমিন হিসেবে)

বটে `/start` দেলে যেহেতু আপনি OWNER_ID দিয়েছেন, আপনি অটোমেটিক পূর্ণ অ্যাডমিন অধিকার পাবেন।

1. বটে যান
2. মেনুতে **কনসোল** বাটন দেখতে পাবেন (শুধু অ্যাডমিনরা দেখে)
3. **ক্যাটাগরি ম্যানেজমেন্ট** → নতুন ক্যাটাগরি তৈরি করুন (যেমন: "ডিজিটাল পণ্য")
4. **পণ্য ম্যানেজমেন্ট** → নতুন পণ্য যোগ করুন
5. পণ্যের নাম, দাম, বিবরণ দিন
6. পণ্যের ভ্যালু (ডিজিটাল কন্টেন্ট) যোগ করুন — লিংক, অ্যাকাউন্ট, কোড ইত্যাদি

---

## ধাপ ৫: পেমেন্ট ফ্লো টেস্ট করুন

1. বট চালু করুন
2. বটে `/start` দিন
3. **প্রোফাইল** → **ব্যালেন্স রিচার্জ** ক্লিক করুন
4. পরিমাণ লিখুন (যেমন: `10`)
5. **Bohudur পেমেন্ট** বাটন চাপুন — Bohudur পেমেন্ট পেজ খুলবে
6. bKash/Nagad/Rocket দিয়ে পেমেন্ট সম্পন্ন করুন
7. ফিরে এসে **পেমেন্ট চেক করুন** বাটন চাপুন
8. ব্যালেন্স স্বয়ংক্রিয়ভাবে বাড়বে!

### পেমেন্ট কিভাবে কাজ করে:
```
ইউজার পরিমাণ লেখে
  → বট Bohudur Create API কল করে
  → payment_url পায়
  → ইউজার পেমেন্ট পেজে যায়
  → bKash/Nagad/Rocket দিয়ে পরিশোধ করে
  → "পেমেন্ট চেক" চাপে
  → বট Query API কল করে স্ট্যাটাস দেখে
  → Execute API কল করে পেমেন্ট নিশ্চিত করে
  → ব্যালেন্স বাড়ায়
```

---

## ধাপ ৬: অ্যাডমিন প্যানেল (ওয়েব)

বট চালালে অ্যাডমিন প্যানেল পাওয়া যাবে:
```
http://localhost:9090/admin
```
- **ইউজারনেম**: `.env` এ `ADMIN_USERNAME` এর মান (ডিফল্ট: `admin`)
- **পাসওয়ার্ড**: `.env` এ `ADMIN_PASSWORD` এর মান (ডিফল্ট: `admin123`)

**প্রোডাকশনে অবশ্যই পাসওয়ার্ড পরিবর্তন করুন!**

অ্যাডমিন প্যানেল থেকে:
- ইউজার ম্যানেজমেন্ট
- পণ্য/ক্যাটাগরি ম্যানেজমেন্ট
- পেমেন্ট হিস্ট্রি দেখুন
- রোল ও পারমিশন ম্যানেজমেন্ট
- অডিট লগ দেখুন

---

## ধাপ ৭: Cloudflare তে ডিপ্লয় (ঐচ্ছিক)

### ৭.১ GitHub তে কোড পুশ করুন

```bash
cd ~/Telegram-shop
git add .
git commit -m "Bohudur payment integrated"
git push origin main
```

### ৭.২ ডাটাবেস পরিবর্তন করুন

Cloudflare এ SQLite কাজ করবে না, তাই PostgreSQL লাগবে:

1. **https://supabase.com** যান (ফ্রি প্ল্যান)
2. নতুন প্রজেক্ট তৈরি করুন
3. **Project Settings** → **Database** থেকে তথ্য নিন
4. `.env` ফাইলে আপডেট করুন:

```
DB_DRIVER=postgresql+asyncpg
POSTGRES_HOST=db.xxxxx.supabase.co
POSTGRES_PORT=5432
POSTGRES_DB=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=আপনার_পাসওয়ার্ড
```

5. আবার পুশ করুন

### ৭.৩ Cloudflare Pages সেটআপ

> **গুরুত্বপূর্ণ নোট**: এই বট একটি Python ব্যাকগ্রাউন্ড অ্যাপ, তাই Cloudflare Pages এ সরাসরি চলবে না। আপনাকে একটি VPS বা Cloudflare Workers (Python support সহ) লাগবে। Termux থেকে ২৪/৭ চালানোর জন্য:

**বিকল্প ১**: Termux + `nohup` (ফোন চালু রাখলে কাজ করবে)

**বিকল্প ২**: একটি সস্তা VPS নিন (DigitalOcean/Hetzner — মাসে $4-5 থেকে শুরু)

---

## ধাপ ৮: ডাটাবেস ব্যাকআপ

SQLite ডাটাবেস ফাইলটি হলো `data/shop.db`। ব্যাকআপ নিতে:

```bash
# ব্যাকআপ তৈরি
cp data/shop.db data/shop_backup_$(date +%Y%m%d).db

# ব্যাকআপ রিস্টোর
cp data/shop_backup_20250610.db data/shop.db
```

---

## সমস্যা সমাধান

### বট চালু হচ্ছে না:
- `.env` ফাইলে সব ভ্যালু সঠিক আছে কিনা চেক করুন
- `TOKEN` সঠিক আছে কিনা যাচাই করুন
- `data/` ও `logs/` ফোল্ডার আছে কিনা চেক করুন
- ইন্টারনেট কানেকশন আছে কিনা নিশ্চিত করুন

### পেমেন্ট তৈরি হচ্ছে না:
- `BOHUDUR_API_KEY` সঠিক আছে কিনা চেক করুন
- https://console.bohudur.one এ লগইন করে API key নিশ্চিত করুন
- ন্যূনতম পরিমাণ `MIN_AMOUNT=10` টাকা

### "ModuleNotFoundError" এরর:
- সব ডিপেন্ডেন্সি ইনস্টল হয়েছে কিনা চেক করুন: `pip install -r requirements.txt`
- ভার্চুয়াল এনভায়রনমেন্ট ব্যবহার করলে অ্যাক্টিভেট করেছেন কিনা

### ডাটাবেস এরর:
- `data/shop.db` ফাইল ডিলিট করুন ও বট আবার চালু করুন — টেবিল অটোমেটিক তৈরি হবে
- `rm data/shop.db && python run.py`

### অ্যাডমিন প্যানেল খুলছে না:
- বট চালু আছে কিনা নিশ্চিত করুন
- পোর্ট 9090 ব্যস্ত আছে কিনা: `ADMIN_PORT=9091` দিয়ে পরিবর্তন করুন

---

## প্রজেক্ট স্ট্রাকচার

```
Telegram-shop/
├── .env                          # আপনার কনফিগারেশন (গোপনীয়)
├── .env.example                  # কনফিগারেশন টেমপ্লেট
├── bot/
│   ├── handlers/
│   │   ├── user/
│   │   │   ├── balance_and_payment.py  # Bohudur পেমেন্ট হ্যান্ডলার
│   │   │   ├── shop_and_goods.py       # দোকান ও পণ্য
│   │   │   ├── cart.py                 # কার্ট সিস্টেম
│   │   │   ├── referral_system.py      # রেফারেল সিস্টেম
│   │   │   └── main.py                 # /start ও প্রোফাইল
│   │   └── admin/                 # অ্যাডমিন হ্যান্ডলার
│   ├── misc/
│   │   ├── env.py                 # এনভায়রমেন্ট কনফিগ
│   │   ├── validators.py          # ইনপুট ভ্যালিডেশন
│   │   └── services/
│   │       ├── payment.py         # Bohudur API ক্লায়েন্ট
│   │       ├── recovery.py        # পেমেন্ট রিকভারি
│   │       └── cleanup.py         # অটো ক্লিনআপ
│   ├── i18n/
│   │   └── strings.py             # বাংলা/English/Русский অনুবাদ
│   ├── keyboards/
│   │   └── inline.py              # ইনলাইন কীবোর্ড
│   ├── database/
│   │   ├── main.py                # SQLite/PostgreSQL সাপোর্ট
│   │   ├── dsn.py                 # ডাটাবেস URL
│   │   ├── models/main.py         # ডাটাবেস মডেল
│   │   └── methods/               # CRUD অপারেশন
│   ├── web/
│   │   └── admin.py               # ওয়েব অ্যাডমিন প্যানেল
│   └── main.py                    # বট মূল ফাইল
├── run.py                         # বট শুরু করার ফাইল
├── requirements.txt               # Python ডিপেন্ডেন্সি
├── setup_termux.sh                # Termux সেটআপ স্ক্রিপ্ট
├── SETUP_GUIDE.md                 # এই গাইড
└── data/
    └── shop.db                    # SQLite ডাটাবেস (অটো তৈরি)
```

---

## সাহায্য

- **Bohudur Telegram**: https://t.me/bohudur
- **Bohudur Docs**: https://docs.bohudur.one
- **Bohudur Console**: https://console.bohudur.one