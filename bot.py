from os import getenv
import discord
from discord.ext import commands
from sqlalchemy import engine, create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from tabulate import tabulate

from models import Base, Event, Member, Attendance, Record, Tags

engine = create_engine('sqlite:///librarian-bot.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


# If table doesn't exist, Create the database
if not engine.dialect.has_table(engine, 'record'):
    Base.metadata.create_all(engine)

description = 'A nice little event bot'
bot = commands.Bot(command_prefix='+', description=description)
token = 'GoSuckALemon'


@bot.event
async def on_ready():
    print(bot.user.id)
    print(bot.user.name)
    print('---------------')
    print('This bot is ready for action!')


@bot.command(pass_context=True)
async def ping(ctx):
    '''Returns pong when called'''
    author = ctx.message.author.name
    server = ctx.message.server.name
    await bot.say('Pong for {} from {}!'.format(author, server))

@bot.command(pass_context=True)
async def add(ctx, content: str):
    try:
        content = ctx.message.content
        content = content.lstrip('+add')
        contentArray = content.split('|')
        for s in contentArray:
            s = s.strip()
        
        title = contentArray[0]
        content = contentArray[1]
        tags = contentArray[2]

        rows = [[content], [tags]]
        header = [title]
        info = tabulate(rows, header)

        record = Record(title=title, content=content)

        session.add(record)
        session.commit()

        await bot.say('New Record Added:\n```\n' + info + '```')
    
    except Exception as e:
        await bot.say('Could not complete your command')
        print(e)

@bot.command()
async def list():
    '''Displays the list of current events
        example: ?list
    '''
    try:
        records = session.query(Record).order_by(Record.title).all()
        headers = ['Title', 'Content']
        rows = [[e.title, e.content] for e in records]
        table = tabulate(rows, headers)
        await bot.say('```\n' + table + '```')
    except Exception as e:
        await bot.say('Could not complete your command')
        print(e)

@bot.command(pass_context=True)
async def view(ctx, name: str):
    '''Displays information about a specific event
        example: ?view party
    '''
    try:
        search = ctx.message.content

        search = search.lstrip('+view')
        search = search.strip()
        record = session.query(Record).filter(Record.title.like(search)).first()
        # Verify This record exists
        if not record:
            await bot.say('This record does not exist')

            return

        await bot.say('Title:\n' + record.title + '\nContent:\n' + record.content)

    except Exception as e:
        await bot.say('Could not complete your command')
        print(e)

@bot.command(pass_context=True)
async def delete(ctx, name: str):
    '''Deletes provided event
        example: +delete party
    '''

    try:

        search = ctx.message.content

        search = search.lstrip('+delete')
        search = search.strip()

        delEvent = session.query(Record).filter(Record.title.like(search)).first()
        # Verifies the event exists
        if not delEvent:
            await bot.say('Event not found.')
            return

        session.delete(delEvent)
        session.commit()

        await bot.say('Record {} deleted.'.format(delEvent.title))
        return
    except Exception as e:
        await bot.say('Could not complete command.')
        print(e)

@bot.command(pass_context=True)
async def edit(ctx, name: str, date: str, time: str='0:00am'):
    '''Edits an event with specified name and date
        example: +create party 12/22/2017 1:40pm
    '''
    server = ctx.message.server.name
    date_time = '{} {}'.format(date, time)
    try:
        oldEvent = session.query(Event).filter(Event.name == name).first()

        if not oldEvent:
                await bot.say('Could not find event to edit.')

        event_date = datetime.strptime(date_time, '%d/%m/%Y %I:%M%p')
        event = Event(name=name, server=server, date=event_date)

        oldEvent.name = event.name
        oldEvent.server = event.server
        oldEvent.date = event.date

        session.commit()

        await bot.say('Event {} created updated for {}'.format(name, event.date))
    except Exception as e:
        await bot.say('Could not complete your command')
        print(e)

if __name__ == '__main__':
    try:
        bot.run(token)
    except Exception as e:
        print('Could Not Start Bot')
        print(e)
    finally:
        print('Closing Session')
        session.close()