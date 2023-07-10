import discord
import os
import json
from keep_alive import keep_alive

from dotenv import load_dotenv
from discord.ext import commands

from collections import Counter # for tier requirements per level

Token = os.environ['W1_TOKEN']

intents = discord.Intents.all()
load_dotenv()
bot = commands.Bot(command_prefix="$", intents=intents)

# GLOBAL VARIABLES
LVLexponent = 2.5
LVLoffset = 30
tierLVLexponent = 1.7
tierLVLoffset = 10
MaxLevel = 20
GameMasters = ["n3ith4n", "t4nj3nt"]
AcceptEmojis = ["☕", "👍"]
RejectEmojis = ["❌"]
TierLevels = ["🪵 Woodcutter", "🛖 Carpenter", "🪨 Stonemason", "🧱 Bricklayer", "🏠 Architect", "🏛 Philosopher", "🔩 Engineer", "🚀 Astronaut", "🪐 Stargazer"]
TierLevelsEmojiOnly = ["🪵", "🛖", "🪨", "🧱", "🏠", "🏛", "🔩", "🚀", "🪐"]
TierReqsPerLevel = [
  [], #level 1
  [], #level 2
  [], #level 3
  [], #level 4
  [], #level 5
  [], #level 6
  ["🪵","🪵","🪵"], #level 7
  ["🪵","🪵","🪵",
   "🛖","🛖","🛖"], #level 8
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖",
   "🪨"], #level 9
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨"], #level 10
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱"], #level 11
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱",
   "🏠"], #level 12
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠"], #level 13
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛"], #level 14
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛",
   "🔩"], #level 15
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛","🏛","🏛",
   "🔩","🔩","🔩"], #level 16
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛","🏛","🏛",
   "🔩","🔩","🔩","🔩","🔩",
   "🚀"], #level 17
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛","🏛","🏛",
   "🔩","🔩","🔩","🔩","🔩",
   "🚀","🚀","🚀",
   "🪐"], #level 18
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛","🏛","🏛",
   "🔩","🔩","🔩","🔩","🔩",
   "🚀","🚀","🚀","🚀","🚀",
   "🪐","🪐","🪐"], #level 19
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛","🏛","🏛",
   "🔩","🔩","🔩","🔩","🔩",
   "🚀","🚀","🚀","🚀","🚀",
   "🪐","🪐","🪐","🪐","🪐"], #level 20
  ["🪵","🪵","🪵","🪵","🪵",
   "🛖","🛖","🛖","🛖","🛖",
   "🪨","🪨","🪨","🪨","🪨",
   "🧱","🧱","🧱","🧱","🧱",
   "🏠","🏠","🏠","🏠","🏠",
   "🏛","🏛","🏛","🏛","🏛",
   "🔩","🔩","🔩","🔩","🔩",
   "🚀","🚀","🚀","🚀","🚀",
   "🪐","🪐","🪐","🪐","🪐"] #level 21 <- same as level 20 but needed so I can display unlocked tiers at maxxed level
]


@bot.event
async def on_reaction_add(reaction, user):
  # get message where the reaction was given
  message = reaction.message
  # await message.channel.send(f"message: {message.content}")
  # await message.channel.send(f"user who reacted: {user}")
  # await message.channel.send(f"owner of message: {message.author}")
  # await message.channel.send(f"emoji: {reaction}")

  if str(user) in GameMasters and str(reaction) in AcceptEmojis:
    # await message.channel.send(f"{user} in GameMasters and {reaction} in AcceptEmojis")
    # open file for writing xp etc
    with open("levels.json", "r") as f:
        data = json.load(f)
      
    if str(message.author.id) in data:

      # add general XP
      data[str(message.author.id)]["XP"] += 3

      # add points to channel/skill; create if not yet found in record of player
      '''
      try:
        data[str(message.author.id)][message.channel.name] += 3
      except:
        data[str(message.author.id)][message.channel.name] = 3
      '''
      try:
        data[str(message.author.id)][message.channel.name]["tierXP"] += 3

        #check for level up in skill/channel tiers
        # tier requirements ok?

        # register the level up in data
        if int(data[str(message.author.id)][message.channel.name]["tierXP"]) >= int(data[str(message.author.id)][message.channel.name]["tierLVL"])**tierLVLexponent+tierLVLoffset:
          data[str(message.author.id)][message.channel.name]["tierXP"] = 0
          data[str(message.author.id)][message.channel.name]["tierLVL"] += 1

        # print nice message saying a skill channel leveled up
          embed = discord.Embed(title="Skill Level Up! ⭐", description=f"{message.author.name}\'s {message.channel.name} proficiency has reached the [{TierLevels[int(data[str(message.author.id)][message.channel.name]['tierLVL'])-1]}] Tier",
                                color=0xFFA500)

          await message.channel.send(embed=embed)
      except:
        data[str(message.author.id)][message.channel.name] = {
          "tierLVL": 1,
          "tierXP": 3
        }

      # in case player levels up after checking
      # level up after reaching certain threshold

      channelnames = []
      for i in message.guild.channels:
        channelnames.append(i.name)

      collectedTiers = []
      for i in data[str(message.author.id)]:
        if i in channelnames:
          await message.channel.send(f"{i} {data[str(message.author.id)][i]['tierLVL']}")
          j = int(data[str(message.author.id)][i]['tierLVL'])
          for k in range(0,j):
            collectedTiers += TierLevelsEmojiOnly[k]
      
      
      curr_LVL = data[str(message.author.id)]["LVL"]
      await message.channel.send(curr_LVL)

      RequirementsSatisfied = False
      # RequirementsSatisfied = all(item in collectedTiers for item in TierReqsPerLevel[int(curr_LVL)])
      # await message.channel.send(RequirementsSatisfied)

      await message.channel.send(f"req to unlock next tier is: {TierReqsPerLevel[int(curr_LVL)]}\n" +
                                 f"collected tiers: {collectedTiers}")

      # get missing tiers if any
      collected_counts = Counter(collectedTiers)
      req_counts = Counter(TierReqsPerLevel[int(curr_LVL)])

      missing_emojis = []

      for emoji, count in req_counts.items():
          if collected_counts[emoji] < count:
              missing_emojis.extend([emoji] * (count - collected_counts[emoji]))

      if missing_emojis:
          await message.channel.send(f"You are missing the following: {missing_emojis}")
          RequirementsSatisfied = False
      else:
          await message.channel.send("Tier requirements for level up sufficient.")
          RequirementsSatisfied = True

      # register level up only if not yet in max level
      if int(data[str(message.author.id)]["XP"]) >= int(data[str(
        message.author.id)]["LVL"])**LVLexponent + LVLoffset:
          if curr_LVL < MaxLevel and RequirementsSatisfied:
            data[str(message.author.id)]["LVL"] += 1
            data[str(message.author.id)]["XP"] = 0


        
            # embeds for prettier message
            embed = discord.Embed(title="Level Up! 🏆",
                                  description=message.author.name +
                                  " has levelled up to LVL: " +
                                  str(data[str(message.author.id)]["LVL"]),
                                  color=0xFFD700)

            target_msg = await message.channel.fetch_message(message.id)
            await message.channel.send(embed=embed, reference=target_msg)

      # inform chat that XP has been registered
      acceptEmbed = discord.Embed(title=f"Solution/Proof Accepted! ✅",
                            description=f"🔨 XP increased by 3\n" +
                            f"{message.channel.name} increased by 3\n" +
                            f"👤: <@{message.author.id}>\n" +
                            f"📁: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
                            color=0x228B22)
      
      target_msg = await message.channel.fetch_message(message.id)
      await message.channel.send(embed=acceptEmbed, reference=target_msg)

      # write changes
      with open("levels.json", "w") as f:
        json.dump(data, f)
        
    else:
      await message.channel.send(f"can't find: {message.author.id} in player database\nPlease contact Game Masters")

    with open("levels.json", "w") as f:
      json.dump(data, f)
  elif str(user) in GameMasters and str(reaction) in RejectEmojis:
    rejectEmbed = discord.Embed(title=f"Solution/Proof not Accepted! ❌",
                        description=f"No XP awarded\n" +
                        f"you will receive feedback on how to fix your submission\n"
                        f"👤: <@{message.author.id}>\n" +
                        f"📁: https://discord.com/channels/{message.guild.id}/{message.channel.id}/{message.id}",
                        color=0x8B0000)
    target_msg_id = message.id
    target_msg = await message.channel.fetch_message(target_msg_id)

    await message.channel.send(embed=rejectEmbed,reference=target_msg)
    # await message.channel.send(f"{user} not in {GameMasters} and {reaction} in {AcceptEmojis}")
    # await message.channel.send(f"{user} not in {GameMasters} and {reaction} in {AcceptEmojis}")
    
    

@bot.event
async def on_message(message):

  if message.content.startswith("$"):

    #tierlevel management
    if message.content.startswith("$tiercheck"):
      await message.channel.send(f"{TierLevelsEmojiOnly}")
      await message.channel.send(f"{sorted(TierLevelsEmojiOnly)}")

      with open("levels.json", "r") as f:
          data = json.load(f)
                
      channelnames = []
      for i in message.guild.channels:
        channelnames.append(i.name)

      collectedTiers = []
      for i in data[str(message.author.id)]:
        if i in channelnames:
          await message.channel.send(f"{i} {data[str(message.author.id)][i]['tierLVL']}")
          j = int(data[str(message.author.id)][i]['tierLVL'])
          for k in range(0,j):
            collectedTiers += TierLevelsEmojiOnly[k]

      await message.channel.send(f"{sorted(collectedTiers)}")
      
    if message.content.startswith("$getLVLexponent"):
      global LVLexponent
      await message.channel.send(f"Current LVLExponent: {LVLexponent}")

    if message.content.startswith('$setLVLexponent'):
      message_parts = message.content.split()
      if len(message_parts) >= 2:
        # global LVLexponent
        LVLexponent = float(message_parts[1])
        await message.channel.send(f"LVLexponent changed to: {LVLexponent}")
      else:
        await message.channel.send(f"No new LVLexponent value provided")

    # simple ping, W1 replies with "pong!"
    if message.content.startswith("$ping"):
      await message.channel.send("pong!")

    # simple hello message, W1 responds with Hello
    if message.content.startswith("$hello"):
      await message.channel.send('Hello! I am Widget-One.')

    # retrieve channel from where the message was sent
    if message.content.startswith("$from"):
      await message.channel.send(f'message sent in {message.channel.mention}')

    if message.content.startswith("$getchannels"):
      channels = message.guild.channels
      for i in channels:
        await message.channel.send(i.name)

    if message.content.startswith("$stats"):

      try:
        with open("levels.json", "r") as f:
          data = json.load(f)
          
        self_name = message.author.name
        self_level = data[str(message.author.id)]["LVL"]
        self_xpn = data[str(message.author.id)]["XP"]
        self_xpd = round(
          int(data[str(message.author.id)]["LVL"])**LVLexponent + LVLoffset)
        self_xpuntilnextlevel = round(
          int(data[str(message.author.id)]["LVL"])**LVLexponent + LVLoffset) - data[str(
            message.author.id)]["XP"]
  
        # generate description to be passed to embed
        g_desc = ""
        # prepare channels filter (para si mga channels lang kang current server maiba sa print)
  
        channelnames = []
        for i in message.guild.channels:
          channelnames.append(i.name)
          
        # await message.channel.send(channelnames)

        # get missing emojis
        # channelnames = []
        # for i in message.guild.channels:
          # channelnames.append(i.name)
  
        collectedTiers = []
        for i in data[str(message.author.id)]:
          if i in channelnames:
            await message.channel.send(f"{i} {data[str(message.author.id)][i]['tierLVL']}")
            j = int(data[str(message.author.id)][i]['tierLVL'])
            for k in range(0,j):
              collectedTiers += TierLevelsEmojiOnly[k]
        
        
        curr_LVL = data[str(message.author.id)]["LVL"]
        await message.channel.send(curr_LVL)
  
        RequirementsSatisfied = False
        # RequirementsSatisfied = all(item in collectedTiers for item in TierReqsPerLevel[int(curr_LVL)])
        # await message.channel.send(RequirementsSatisfied)

        if curr_LVL < MaxLevel:
          await message.channel.send(f"req to unlock next tier is: {TierReqsPerLevel[int(curr_LVL)]}\n" +
                                   f"collected tiers: {collectedTiers}")
        else:
          await message.channel.send(f"Max level reached no next tier to unlock")
  
        # get missing tiers if any only if LVL is 19 or lower

        collected_counts = Counter(collectedTiers)
        req_counts = Counter(TierReqsPerLevel[int(curr_LVL)])
        req_emojis = TierReqsPerLevel[int(curr_LVL)]
  
        missing_emojis = []
  
        for emoji, count in req_counts.items():
            if collected_counts[emoji] < count:
                missing_emojis.extend([emoji] * (count - collected_counts[emoji]))
  
        if missing_emojis:
            await message.channel.send(f"You are missing the following: {missing_emojis}")
            RequirementsSatisfied = False
        else:
            await message.channel.send("Tier requirements for level up sufficient.")
            RequirementsSatisfied = True

        LVLupReqs = ""
        newlinectr = 0
        for emoji in TierLevelsEmojiOnly:
          if emoji in req_emojis:

            # attempt to build a string that has three tiers per line
            if newlinectr % 3 == 0:
              if newlinectr != 0:
                LVLupReqs += f"\n╰✧"
              else:
                LVLupReqs += f"╰✧"

            if curr_LVL < 20:
              LVLupReqs += f"{emoji}: {collectedTiers.count(emoji)} / {req_emojis.count(emoji)} • "
            else:
              LVLupReqs += f"{emoji}: {req_emojis.count(emoji)} / {req_emojis.count(emoji)} • "
            
            newlinectr += 1

        
        for i in data[str(message.author.id)]:
          if i == "LVL":
            g_desc += f"🏆 LVL: {self_level}\n"
          elif i == "XP":
            # g_desc += i + ": " + str(data[str(message.author.id)][i]) + "\n"
            if self_xpuntilnextlevel > 0:
              g_desc += f"🔨 XP: {self_xpn} / {self_xpd} ({self_xpuntilnextlevel} until next level)\n"
            else:
              g_desc += f"🔨 XP: {self_xpn} / {self_xpd} (XP requirement reached)\n╰✧ complete NEXT LVL REQs to level up\n\n"
  
            if curr_LVL < 20:
              if missing_emojis:
                g_desc += f"🔒 NEXT LVL REQS (to unlock LVL {curr_LVL+1}):\n{LVLupReqs}\n\n"
              else:
                if LVLupReqs:
                  g_desc += f"🔓 NEXT LVL REQS satisfied\n{LVLupReqs}\n╰✧complete XP requirement to level up\n\n"
                else:
                  g_desc += f"🔓 NEXT LVL REQS satisfied\n╰✧complete XP requirement to level up\n\n"
            else:
              g_desc += f"✨🔓✨ ALL TIERS UNLOCKED:\n{LVLupReqs}\n\n"
          else:
            
            tLVL = str(data[str(message.author.id)][i]['tierLVL'])
            tXP = str(data[str(message.author.id)][i]['tierXP'])
            tXPd = round(int(data[str(message.author.id)][i]["tierLVL"]) ** tierLVLexponent+tierLVLoffset)
            
            if i in channelnames:
              g_desc += f"**{i}**\n╰✧{TierLevels[int(tLVL)-1]} Tier: {tXP} / {tXPd} ({tXPd - int(tXP)} tierXP til next tier)\n\n" 
            
              # g_desc += i + ": Lvl " + str(data[str(message.author.id)][i]['tierLVL']) + ", xp " + str(data[str(message.author.id)][i]['tierXP'])

        # calculate number of swords based on level
        swords = ""
        for i in range(0,curr_LVL):
          if i % 4 == 0:
            swords += "⚔️"
        if curr_LVL == 20:
          swords += "🏁"
            
        embed = discord.Embed(title=self_name + f" {swords}",
                              description=g_desc,
                              color=0xFFD700)
        '''
        embed = discord.Embed(
          title=self_name + " ⚔️",
          description=
          f"LVL: {self_level} \n XP: {self_xpn} / {self_xpd} ({self_xpuntilnextlevel} until next level)",
          color=0xFFD700)
        '''
        target_msg = await message.channel.fetch_message(message.id)
        await message.channel.send(embed=embed,reference=target_msg)
      except:
        noStats = discord.Embed(title=message.author.name + " ⚔️", 
                              description=f"No stats yet for <@{message.author.id}>. \n" +
                              f"Try submitting solutions/proofs to gain XP",
                              color=0x808080)
        target_msg = await message.channel.fetch_message(message.id)
        await message.channel.send(embed=noStats, reference=target_msg)
  else:
    if message.author != bot.user:
      # await message.channel.send("normal text")

      with open("levels.json", "r") as f:
        try:
          data = json.load(f)
          # check if already exists, if yes update xp
          if str(message.author.id) in data:
            # add 3 to XP of existing person

            '''
            data[str(message.author.id)]["XP"] += 3
            # await message.channel.send("found!")

            # add the channel name to record of person and add XP to it also
            try:
              data[str(message.author.id)][message.channel.name] += 3
            except:
              data[str(message.author.id)][message.channel.name] = 3

            # level up after reaching certain threshold
            if int(data[str(message.author.id)]["XP"]) >= int(data[str(
                message.author.id)]["LVL"])**LVLexponent + 30:
              data[str(message.author.id)]["LVL"] += 1
              data[str(message.author.id)]["XP"] = 0

              # embeds for prettier message

              embed = discord.Embed(title="Level Up! 🏆",
                                    description=message.author.name +
                                    " has levelled up to LVL: " +
                                    str(data[str(message.author.id)]["LVL"]),
                                    color=0xFFD700)
              await message.channel.send(embed=embed)
            '''
            # write changes
            with open("levels.json", "w") as f:
              json.dump(data, f)
          else:
            data[str(message.author.id)] = {}
            data[str(message.author.id)]["LVL"] = 1
            data[str(message.author.id)]["XP"] = 0

            # welcome message and instructions for first message

            # write changes
            with open("levels.json", "w") as f:
              json.dump(data, f)
        except json.JSONDecodeError:
          data = {}

      if not data:
        data[str(message.author.id)] = {}
        data[str(message.author.id)]["LVL"] = 1
        data[str(message.author.id)]["XP"] = 0

        with open("levels.json", "w") as f:
          json.dump(data, f)
    '''
    with open("levels.json", "r") as f:
      data = json.load(f)
    if str(message.author.id) in data:
      data[str(message.author.id)]["XP"] += 3
    else:
      data[str(message.author.id)] = {}
      data[str(message.author.id)]["LVL"] = 1
      data[str(message.author.id)]["XP"] = 0
    '''

  # write back to the json file
  '''
  with open("levels.json", "w") as f:
    json.dump(data, f)
  '''


keep_alive()
bot.run(Token)
'''
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print('Widget One (W1) has arrived as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return
    
  if message.content == "$hello":
    await message.channel.send('Hello! I am Widget-One.')

#client.run(os.getenv('W1_TOKEN'))
my_secret = os.environ['W1_TOKEN']
client.run(my_secret)
'''
