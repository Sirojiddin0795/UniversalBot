import os
import aiohttp
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

load_dotenv()

bot = Bot(
    token=os.getenv("BOT_TOKEN"),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: Message):
    text = (
        "<b>👋 Salom! Men Sirojiddin tomonidan tayyorlangan UniversalBotman!</b>\n\n"
        "Quyidagi komandalarni ishlatib, turli xizmatlardan foydalanishingiz mumkin:\n\n"
        "🌤 /weather — Ob-havo ma’lumoti\n"
        "🧠 /fact — Random fakt\n"
        "🌍 /country &lt;davlat&gt; — Davlatlar haqida malumot\n"
        "🌐 /ip &lt;ip&gt; — IP manzildan joylashuv\n"
        "😂 /joke — Inglizcha hazil\n"
        "⏰ /time &lt;zona&gt; — Vaqt zonasi (masalan: Asia/Tashkent)\n"
        "💸 /crypto — Kripto valyutalar kursi\n"
        "📸 /photo &lt;kategoriya&gt; — Random rasm\n"
        "🐙 /github &lt;username&gt; — GitHub profili\n"
        "🔳 /qr &lt;matn&gt; — QR-kod yaratish\n"
        "👨‍👧 /dadjoke — Dad-joke hazili\n"
        "📖 /book &lt;kitob nomi&gt; — Kitob qidirish\n"
        "🧑 /name — Random ism va familiya\n"
    )
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/weather"), KeyboardButton(text="/fact")],
            [KeyboardButton(text="/country Uzbekistan"), KeyboardButton(text="/ip 8.8.8.8")],
            [KeyboardButton(text="/joke"), KeyboardButton(text="/time Asia/Tashkent")],
            [KeyboardButton(text="/crypto"), KeyboardButton(text="/photo nature")],
            [KeyboardButton(text="/github sirojiddin0795"), KeyboardButton(text="/qr Hello")],
            [KeyboardButton(text="/dadjoke"), KeyboardButton(text="/book Python")],
            [KeyboardButton(text="/name")],
        ],
        resize_keyboard=True
    )
    await message.answer(text, reply_markup=keyboard)

@dp.message(Command("weather"))
async def weather(message: Message):
    city = "Tashkent"
    key = os.getenv("OPENWEATHERMAP_API_KEY")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={key}&units=metric"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            if resp.status == 200:
                await message.answer(
                    f"🌤 <b>{city.title()}</b>\n"
                    f"🌡 Temp: {data['main']['temp']}°C\n"
                    f"💧 Namlik: {data['main']['humidity']}%\n"
                    f"📈 Bosim: {data['main']['pressure']} hPa"
                )
            else:
                await message.answer("❌ Shahar topilmadi.")

@dp.message(Command("fact"))
async def fact(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://uselessfacts.jsph.pl/random.json?language=en") as resp:
            data = await resp.json()
            await message.answer(f"🧠 {data['text']}")

@dp.message(Command("country"))
async def country(message: Message):
    parts = message.text.split(maxsplit=1)
    country_name = parts[1] if len(parts) > 1 else "Uzbekistan"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://restcountries.com/v3.1/name/{country_name}") as resp:
            data = await resp.json()
            if resp.status == 200:
                country_data = data[0]
                capital = country_data.get("capital", ["Noma'lum"])[0]
                population = country_data.get("population", 0)
                currency = list(country_data['currencies'].keys())[0]
                await message.answer(
                    f"🏳️ {country_name.title()}\n"
                    f"🏙 Poytaxt: {capital}\n"
                    f"👥 Aholi: {population:,}\n"
                    f"💰 Valyuta: {currency}"
                )
            else:
                await message.answer("❌ Davlat topilmadi.")

@dp.message(Command("ip"))
async def ip_lookup(message: Message):
    parts = message.text.split(maxsplit=1)
    ip = parts[1] if len(parts) > 1 else "8.8.8.8"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://ip-api.com/json/{ip}") as resp:
            data = await resp.json()
            if data['status'] == "success":
                await message.answer(
                    f"📍 Joylashuv: {data['city']}, {data['country']}\n"
                    f"🌐 ISP: {data['isp']}"
                )
            else:
                await message.answer("❌ IP manzil topilmadi.")

@dp.message(Command("joke"))
async def joke(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://v2.jokeapi.dev/joke/Any") as resp:
            data = await resp.json()
            if data["type"] == "single":
                await message.answer(f"😂 {data['joke']}")
            else:
                await message.answer(f"😂 {data['setup']}\n{data['delivery']}")

@dp.message(Command("time"))
async def get_time(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) == 1:
        return await message.answer("⏳ Format: /time Asia/Tashkent")

    zone = parts[1]
    key = os.getenv("TIMEZONEDB_API_KEY")
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={key}&format=json&by=zone&zone={zone}"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data["status"] == "OK":
                        await message.answer(
                            f"🕰 Zona: <b>{data['zoneName']}</b>\n"
                            f"📅 Sana: {data['formatted'].split()[0]}\n"
                            f"⏰ Vaqt: {data['formatted'].split()[1]}"
                        )
                    else:
                        await message.answer(f"❌ Xatolik: {data['message']}")
                else:
                    await message.answer("❌ API javob bermadi.")
    except Exception as e:
        await message.answer(f"⚠️ Xatolik: {str(e)}")

@dp.message(Command("crypto"))
async def crypto(message: Message):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            await message.answer(
                f"💸 BTC: ${data['bitcoin']['usd']}\n"
                f"💰 ETH: ${data['ethereum']['usd']}"
            )

@dp.message(Command("photo"))
async def photo(message: Message):
    parts = message.text.split(maxsplit=1)
    category = parts[1] if len(parts) > 1 else "nature"
    key = os.getenv("UNSPLASH_ACCESS_KEY")
    url = f"https://api.unsplash.com/photos/random?query={category}&client_id={key}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            await message.answer_photo(photo=data['urls']['regular'], caption=data.get('alt_description') or "📸")

@dp.message(Command("github"))
async def github(message: Message):
    parts = message.text.split(maxsplit=1)
    username = parts[1] if len(parts) > 1 else "sirojiddin0795"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.github.com/users/{username}") as resp:
            if resp.status == 200:
                data = await resp.json()
                await message.answer(
                    f"👤 {data['login']}\n"
                    f"📦 Repos: {data['public_repos']}\n"
                    f"👥 Followers: {data['followers']}\n"
                    f"📝 Bio: {data['bio'] or 'Yo‘q'}"
                )
            else:
                await message.answer("❌ Profil topilmadi.")

@dp.message(Command("qr"))
async def qr(message: Message):
    parts = message.text.split(maxsplit=1)
    text = parts[1] if len(parts) > 1 else "Hello"
    url = f"https://api.qrserver.com/v1/create-qr-code/?data={text}&size=200x200"
    await message.answer_photo(url)

@dp.message(Command("dadjoke"))
async def dadjoke(message: Message):
    headers = {"Accept": "application/json"}
    async with aiohttp.ClientSession() as session:
        async with session.get("https://icanhazdadjoke.com/", headers=headers) as resp:
            data = await resp.json()
            await message.answer(f"👨‍👧 {data['joke']}")

@dp.message(Command("book"))
async def book(message: Message):
    parts = message.text.split(maxsplit=1)
    query = parts[1] if len(parts) > 1 else "Python"
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://www.googleapis.com/books/v1/volumes?q={query}") as resp:
            data = await resp.json()
            if "items" in data:
                book_info = data["items"][0]["volumeInfo"]
                await message.answer(
                    f"📚 {book_info['title']}\n"
                    f"✍️ Muallif: {', '.join(book_info.get('authors', ['No info']))}\n"
                    f"📅 Yil: {book_info.get('publishedDate', 'No info')}\n"
                    f"📝 Tavsif: {book_info.get('description', 'No info')[:500]}"
                )
            else:
                await message.answer("❌ Kitob topilmadi.")

@dp.message(Command("name"))
async def name(message: Message):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://randomuser.me/api/") as resp:
            data = await resp.json()
            person = data["results"][0]["name"]
            await message.answer(f"🧑 {person['first']} {person['last']}")

async def main():
    print("✅ Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
