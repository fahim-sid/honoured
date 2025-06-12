import discord
from discord.ext import tasks, commands
from datetime import datetime, timedelta
import json

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True

bot = commands.Bot(command_prefix='!', intents=intents)

join_log = []

@bot.event
async def on_ready():
    print(f"✅ Bot logged in as {bot.user}")
    await update_now()  # প্রথমে একবার চালায়
    track_members.start()

@bot.event
async def on_member_join(member):
    now = datetime.utcnow()
    join_log.append({'id': member.id, 'time': now.isoformat()})

@tasks.loop(seconds=60)
async def track_members():
    await update_now()

async def update_now():
    now = datetime.utcnow()
    join_log[:] = [entry for entry in join_log if datetime.fromisoformat(entry['time']) > now - timedelta(hours=24)]

    total_members = 0
    for guild in bot.guilds:
        total_members += guild.member_count

    data = {
        'total_members': total_members,
        'last_24h_joins': len(join_log),
        'updated_at': now.strftime("%Y-%m-%d %H:%M:%S UTC")
    }

    with open('data.json', 'w') as f:
        json.dump(data, f, indent=4)

    print("✅ data.json updated!")

bot.run('MTM4MjM0NDI2MDUzNTMyNDc0NQ.GOP6HD.-XGr8MTKX2bmXyUk02WjCFEMYn2RP0geIZKwNM')  # ⬅️ এখানে তোমার bot টোকেন বসাও
