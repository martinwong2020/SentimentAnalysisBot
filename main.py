import discord
from textblob import TextBlob
import os
import random
import copy
client = discord.Client()

Greetings = ["hello", "welcome", "hi", "ello", "greeting"]
ResponseGif = [
    'https://tenor.com/view/muri-muri-muri-muri-muri-muri-gif-20679784',
    'https://c.tenor.com/OpI0JjvBNMUAAAAC/barf-ewww.gif',
    'https://i.pinimg.com/originals/33/2a/1a/332a1a4d8c0f6b40fe74abb235b2250e.gif',
]
SummonGif = [
    'https://c.tenor.com/63FqaZrXRKUAAAAC/86anime-fido.gif',
    'https://tenor.com/view/fido-86-pop-gif-21842021',
    'https://c.tenor.com/wLAO4CCJ96QAAAAd/86anime-eighty-six.gif',
    'https://c.tenor.com/2OitdQYUwJ8AAAAC/86anime-eighty-six.gif'
]
Chat = ["Chat with Fido"]
ChatQueue = []
ChatState = False
BanList = ["jackie", "joshua", "buyan", "ryan", "victor", "josh"]

Subject = ["Math", "Science", "Coding", "School", "Games", "Anime", "86"]
CopySubject=copy.deepcopy(Subject)
CurrentSubject=""
def Question(Subject):
  QuestionFormat = [
      "What are your thoughts on " + Subject + "?",
      "Where do you stand on " + Subject + "?",
      "Do you like " + Subject + "?",
      "Does " + Subject + " interest you per chance?",
      "How much do you like " + Subject + "?",
  ]
  return random.choice(QuestionFormat)
Counter = 0
SetLimitQuestion = random.randint(2, 3)


def ChangeStatus(state):
    global ChatState
    if (state == True):
        ChatState = False
    elif (state == False):
        ChatState = True


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    global Counter
    global Subject
    global CurrentSubject
    if message.author == client.user:
        return
    msg = message.content.lower()
    author = str(message.author)
    if msg.startswith('fido'):
        await message.channel.send(random.choice(SummonGif))

    if any(word in msg for word in Greetings):
        await message.channel.send(random.choice(ResponseGif))
    if any(word in msg for word in BanList):
        await message.channel.send(random.choice(ResponseGif))

    if ChatState == True and author == ChatQueue[0] and Counter==0:
      
        print(type(msg))
        response = TextBlob(msg)
        if (response.polarity > 0):
            await message.channel.send("Glad you are doing well")
        elif (response.polarity < 0):
            await message.channel.send("Hope you will do better.")
        else:
            await message.channel.send("Hope you start enjoying yourself.")
        # ChangeStatus(ChatState)
        # ChatQueue.remove(author)
        
        SubjectSelected=random.choice(Subject)
        Subject.remove(SubjectSelected)
        global CurrentSubject
        CurrentSubject=SubjectSelected
        # await message.channel.send(random.choice(QuestionFormat))
        
        Counter=Counter+1
        # await message.channel.send(SubjectSelected)
        # print(Question(SubjectSelected))
        await message.channel.send((Question(SubjectSelected)))
        return
    # if ChatState ==True and author ==ChatQueue[0] and Counter>0:
    if ChatState==True and author==ChatQueue[0] and Counter>0:
        response=TextBlob(msg)
        if(response.polarity>0.5):
            await message.channel.send("You really like "+CurrentSubject+" huh.")
        elif(response.polarity>0.1):
            await message.channel.send("You like "+CurrentSubject+".")
        elif(response.polarity<-0.5):
            await message.channel.send("Strong hate for "+CurrentSubject+".")
        elif(response.polarity<-0.1):
            await message.channel.send("You don't like "+CurrentSubject+".")
        else:
            await message.channel.send("I see your thoughts on "+CurrentSubject+".")
        
        if(Counter==SetLimitQuestion):
          ChatQueue.remove(author)
          ChangeStatus(ChatState)
          CurrentSubject=""
          await message.channel.send("Thank you for conversing with Fido.")
          Counter=0
          Subject=copy.deepcopy(CopySubject)
          return
        else:
          Counter=Counter+1
          
          SubjectSelected=random.choice(Subject)
          Subject.remove(SubjectSelected)
          CurrentSubject=SubjectSelected
          await message.channel.send((Question(SubjectSelected)))
    if msg == Chat[0].lower() and len(ChatQueue) == 0:
        await message.channel.send("Starting Chat with " + author)
        ChangeStatus(ChatState)
        ChatQueue.append(author)
        # await message.channel.send(ChatState)
        await message.channel.send("How are you doing?")
    elif msg == Chat[0].lower() and len(ChatQueue) != 0:
        await message.channel.send("Chatting with " + ChatQueue[0] +
                                   " already. Please wait.")


my_secret = os.environ['Key']

client.run(my_secret)
