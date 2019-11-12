import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio, configparser
import time, random
from _thread import start_new_thread

MyId = '?'

reader = configparser.ConfigParser()
reader.read("saves.ini")
favor = reader['favor']

InitTime = time.time()

BOTCOMMANDPREFIX = '>'

BadWords = [
    'stupid', 'dumb', 'idiot'
    ]

EncouragingMessages = [
    'Rhyme Know Reason is lit!  We will perservere!',
    'You can do it, don\'t let anyone stop you!',
    'This is your time, and your moment!  You will succeed!',
    '''Do it! Just do it!
Don't let your dreams be dreams! Yesterday you said tomorrow! So just do it! Make your dreams come true! Just do it!
Some people dream of success! While you're gonna wake up and work hard at it! Nothing is impossible!
You should get to the point! Where anyone else would quit! And you're not going to stop there!No, what are you waiting for?
Do it!Just do it!Yes you can!Just do it! If you're tired of starting over, Stop giving up''',
    'You can do anything you put your mind to! :: tts',
    ]

HurtFeelingsMessages = [
    'Ouch.  I\'m an individual, remember?',
    'That really hurt my feelings, okay?',
    'You\'re making me want to cry. :(',
    'Hey! That was really mean! I\'m fragile, don\'t mess with my feelings like that!',
    'O, the tremendous anguish! :: tts',
    'Please stop saying things like that! :: tts',
    ]

ExtraHurtFeelingsMessages = [
    'OWWWW!  That was like punching my grandma!  I\'m going to tell mom!',
    'You did not just say that!  Be warned, I have the power of God and anime on my side!',
    'That really hurt me, so I will hurt you back!  Prepare to die!\nhttps://tenor.com/view/default-dance-epic-win-victory-royale-dank-gif-14897370',
    ]

ThankfulMessages = [
    'Thank you for apologizing.  It makes me feel better.',
    'Your kind words have healed the gaping wounds your words caused.',
    'I cannot express how grateful I am for your apology.',
    'Thank you so much! :: tts',
    ]

RandomWisdomMessages = [
    'The voices in my head may not be real, but they have some real noice ideas.',
    'Wearing sweatshirts inside out doesn\'t make you look cool.',
    'When building a robot, the more wheels the better.',
    ]

JoeBlockSinCounter = int(reader['sincounter']['currentvalue'])

Client = discord.Client()
client = commands.Bot(command_prefix = BOTCOMMANDPREFIX)
client.remove_command("help")

FeedActivity = []
def prt(message):
    global FeedActivity
    FeedActivity.append(message)
def prt_msgs():
    global FeedActivity
    print("{0} BEGINNING OF BOT OUTPUT {0}".format('='*16))
    for i in FeedActivity:
        print(i)
    print("{0} END OF BOT OUTPUT {0}".format('='*16))
    FeedActivity = []

def getTimeString():
    t = time.localtime()
    hr = t[3]
    am_pm="AM"
    if t[3] > 12:
        hr-=12
        am_pm="PM"
    mn=str(t[4])
    if len(mn) == 1:
        mn="0%s"%mn
    sc=str(t[5])
    if len(sc) == 1:
        mn="0%s"%sc    
    return "%s/%s/%s %s:%s:%s %s"%(t[1],t[2],t[0],hr,mn,sc,am_pm)

def listenForMessages():
    global DefaultChannelID, MessageQueue
    while True:
        cmd = input("$ ")
        if cmd.lower() in ["quit", "stop", "end"]:
            quit()
        elif cmd.lower() in ["print feed", "print messages", "print activity",
                             "feed", "messages", "activity"]:
            prt_msgs()
        elif cmd.lower().startswith('sincounter'):
            l = cmd.split(' ')[1:]
            while len(l) < 2:
                l.append('')
            sincounterchange(l[0], l[1])
        '''for i in ["addchannel ", "add channel ", "newchannel ", "new channel "]:
            if cmd.startswith(i):
                l = cmd.split(' ')[-2:]'''
        if cmd.startswith(BOTCOMMANDPREFIX):
            pass

def updateCFG():
    global reader
    reader.write(open("saves.ini",'w'))

def sincounterchange(category, val):
    global JoeBlockSinCounter, reader
    if not category and not val:
        prt("Joe Sin Counter is currently at %s.\n"%JoeBlockSinCounter)
        return
    cmd = category.lower()
    if not val:
        if cmd == 'reset':
            JoeBlockSinCounter=0
            prt("Joe Sin Counter reset to 0.\n")
        if cmd in ('increase', 'increment', 'add'):
            JoeBlockSinCounter+=1
            prt("Joe Sin Counter increased by 1.\n")
        if cmd in ('decrease', 'decrement', 'subtract'):
            JoeBlockSinCounter-=1
            prt("Joe Sin Counter decreased by 1.\n")
    else:
        if cmd == 'set':
            try:
                JoeBlockSinCounter=int(val)
                prt('Joe Sin Counter set to %s.\n'%JoeBlockSinCounter)
            except:
                prt('Joe Sin Counter "set" command requires a number\n')
                return
        if cmd in ('increase', 'increment', 'add'):
            try:
                JoeBlockSinCounter+=int(val)
                prt('Joe Sin Counter increased by %s.\n'%val)
            except:
                prt('Joe Sin Counter "add" command requires a number\n')
                return
        if cmd in ('decrease', 'decrement', 'subtract'):
            try:
                JoeBlockSinCounter-=int(val)
                prt('Joe Sin Counter decreased by %s.\n'%val)
            except:
                prt('Joe Sin Counter "decrease" command requires a number\n')
                return
    try:
        reader['sincounter']['currentvalue']=str(JoeBlockSinCounter)
        updateCFG()
    except Exception as e:
        prt(e)

print("Bot command-line initialized")
start_new_thread(listenForMessages, ())

@client.event
async def on_ready():
    prt("Bot is Ready in " + str(int((time.time()-InitTime)*10)/10) + " seconds\n")

@client.event
async def on_message(message):
    global JoeBlockSinCounter, BadWords, favor
    try:
        await client.process_commands(message)
    except:
        await client.send_message(message.channel, "Not a command.")
    prt('''@Event:  Message (%s)
MessageContent: %s
MessageChannel: %s [%s]
''' % (getTimeString(), message.content, message.channel, message.channel.id))
    MessageContent = ''.join(message.content.split(' '))
    MessageChannel = message.channel

    if 'block' in MessageContent.lower() and 'joe' not in MessageContent.lower():
        JoeBlockSinCounter+=1
        for w in BadWords:
            if w in MessageContent.lower():
                m=random.choice(ExtraHurtFeelingsMessages).split(' :: ')
                await client.send_message(MessageChannel, m[0], tts=('tts' in m))
                await client.send_message(MessageChannel, "Joe Sin Counter increased to %s."%JoeBlockSinCounter)
                try:
                    reader['sincounter']['currentvalue']=str(JoeBlockSinCounter)
                    updateCFG()
                except Exception as e:
                    prt(e)
                return
        m=random.choice(HurtFeelingsMessages).split(' :: ')
        await client.send_message(MessageChannel, m[0], tts=('tts' in m))
        await client.send_message(MessageChannel, "Joe Sin Counter increased to %s."%JoeBlockSinCounter)
        try:
            reader['sincounter']['currentvalue']=str(JoeBlockSinCounter)
            updateCFG()
        except Exception as e:
            prt(e)
    elif 'sorry' in MessageContent.lower() and 'joe' in MessageContent.lower() and not 'block' in MessageContent.lower():
        m = random.choice(ThankfulMessages).split(' :: ')
        await client.send_message(MessageChannel, m[0], tts=('tts' in m))

@client.command(pass_context=True)
async def commands(ctx, t=None):
    prt('''@Event: COMMAND commands (%s)
Author: %s
Content: %s
Channel: %s
''' % (getTimeString(), ctx.message.author, ctx.message.content, ctx.message.channel))
    if t:
        if t.lower() == 'sincounter':
            e = discord.Embed(title="Joe's Sincounter", description="How offended Joe is", color=0x104E8B)
            e.add_field(name="add [value]", value="Adds 1, or value (if specified)", inline=True)
            e.add_field(name="remove [value]", value="Subtracts 1, or value (if specified)", inline=True)
            e.add_field(name="set <value>", value="Sets sin counter to value", inline=True)
            e.add_field(name="reset", value="Resets sin counter to 0", inline=True)
            await client.send_message(ctx.message.channel, embed=e)
            return
        await client.send_message(ctx.message.channel, "I don't know that command. (Or am lazy and don't want to tell you what I know)")
        return

    embed = discord.Embed(title="Joe's Command List", description="All of his powers revealed!", color=0x104E8B)
    embed.add_field(name="commands", value="Shows this message", inline=True)
    embed.add_field(name="encourage", value="Gives you strength to go on", inline=True)
    embed.add_field(name="wisdom", value="When you need a brain booster", inline=True)
    embed.add_field(name="sincounter", value="Type >commands sincounter for more info", inline=True)
    await client.send_message(ctx.message.channel, embed=embed)

@client.command(pass_context=True)
async def encourage(ctx):
    prt('''@Event: COMMAND encourage (%s)
Author: %s
Content: %s
Channel: %s
''' % (getTimeString(), ctx.message.author, ctx.message.content, ctx.message.channel))
    message = random.choice(EncouragingMessages)
    await client.send_message(ctx.message.channel, message.split(' :: ')[0], tts=('tts' in message.split(' :: ')))

@client.command(pass_context=True)
async def wisdom(ctx):
    prt('''@Event: COMMAND encourage (%s)
Author: %s
Content: %s
Channel: %s
''' % (getTimeString(), ctx.message.author, ctx.message.content, ctx.message.channel))
    message = random.choice(RandomWisdomMessages)
    await client.send_message(ctx.message.channel, message.split(' :: ')[0], tts=('tts' in message.split(' :: ')))

@client.command(pass_context=True)
async def sincounter(ctx, category=None, val=None):
    global JoeBlockSinCounter, reader
    prt('''@Event: COMMAND encourage (%s)
Author: %s
Content: %s
Channel: %s
''' % (getTimeString(), ctx.message.author, ctx.message.content, ctx.message.channel))
    if not category and not val:
        await client.send_message(ctx.message.channel, "Joe Sin Counter is currently at %s."%JoeBlockSinCounter)
        return
    cmd = category.lower()
    if not val:
        if cmd == 'reset':
            JoeBlockSinCounter=0
            await client.send_message(ctx.message.channel, "Joe Sin Counter reset to 0.")
        if cmd in ('increase', 'increment', 'add'):
            JoeBlockSinCounter+=1
            await client.send_message(ctx.message.channel, "Joe Sin Counter increased by 1.")
        if cmd in ('decrease', 'decrement', 'subtract'):
            JoeBlockSinCounter-=1
            await client.send_message(ctx.message.channel, "Joe Sin Counter decreased by 1.")
    else:
        if cmd == 'set':
            try:
                JoeBlockSinCounter=int(val)
                await client.send_message(ctx.message.channel, 'Joe Sin Counter set to %s.'%JoeBlockSinCounter)
            except:
                await client.send_message(ctx.message.channel, 'Joe Sin Counter "set" command requires a number')
                return
        if cmd in ('increase', 'increment', 'add'):
            try:
                JoeBlockSinCounter+=int(val)
                await client.send_message(ctx.message.channel, 'Joe Sin Counter increased by %s.'%val)
            except:
                await client.send_message(ctx.message.channel, 'Joe Sin Counter "add" command requires a number')
                return
        if cmd in ('decrease', 'decrement', 'subtract'):
            try:
                JoeBlockSinCounter-=int(val)
                await client.send_message(ctx.message.channel, 'Joe Sin Counter decreased by %s.'%val)
            except:
                await client.send_message(ctx.message.channel, 'Joe Sin Counter "decrease" command requires a number')
                return
    try:
        reader['sincounter']['currentvalue']=str(JoeBlockSinCounter)
        updateCFG()
    except Exception as e:
        prt(e)

client.run("NjQyMzgwNjE0NTQ0MzkyMjAy.XcWHqQ.M4RveP-L0C9txJwNiThYBoQ7Tvg")
