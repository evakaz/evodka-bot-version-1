import discord
from discord.ext import commands
from discord.ext.commands import Bot
import datetime

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix = '!', intents = intents)


IDSERVER = ''
IDCHANNEL = ''
INVITELINK = ''

@bot.event
async def on_ready():
    print('The bot is ready.')
    return await bot.change_presence(activity=discord.Streaming(name="evodka", url='https://www.twitch.tv/ev0dka'))


async def onMemberJoinAction(myBot, myMember):
    print('here')
    guild = myBot.get_guild(IDSERVER)
    channel = guild.get_channel(IDCHANNEL)
    await channel.send(f'Welcome to the server {myMember.mention}! :crown:') #welcome the myMember to the server
    await myMember.send(f'Welcome to {guild.name} server, {myMember.name}!')  # welcome thru dms
    embed = discord.Embed(title=f"{myMember.name} just joined!", colour=(0xff001f),
                          description=f"Welcome to [{guild.name}]({INVITELINK}) server! You are the {len(list(myMember.guild.members))} member! ```\nHave fun!```")
    embed.set_thumbnail(url=f"{myMember.avatar_url}")
    embed.set_author(name=f"{myMember.name}", icon_url=f"{myMember.avatar_url}")
    embed.set_footer(text="evodka", icon_url=f"{myMember.guild.icon_url}")
    embed.timestamp = datetime.datetime.utcnow()

    await channel.send(embed=embed)


@bot.event
async def on_member_join(member):
    return await onMemberJoinAction(bot, member)


async def onMemberRemoveAction(myBot, myMember):
    guild = myBot.get_guild(IDSERVER)
    channel = guild.get_channel(IDCHANNEL)
    await channel.send(f'{myMember.mention} left the server')


@bot.event
async def on_member_remove(member):
    return await onMemberRemoveAction(bot, member)


async def onRoleAddAction(myBot, myPayload):
    RRMESSAGEID =''
    message_id = myPayload.message_id
    if message_id == RRMESSAGEID:
        guild = myBot.get_guild(IDSERVER)
        ROLENAME = myPayload.emoji.name
        roleid = discord.utils.get(guild.roles, name = ROLENAME)
        role = guild.get_role(roleid.id)

        if role is not None:
            member = guild.get_member(myPayload.user_id)
            member = myPayload.member
            if member is not None:
                await member.add_roles(role)
                print('The role is added')
            else:
                print('Member not found')
        else:
                print('Role not found')


@bot.event
async def on_raw_reaction_add(payload):
    print('emoji')
    return await onRoleAddAction(bot, payload)
    
            
async def onRoleRemoveAction(myBot, myPayload):
    RRMESSAGEID = 819582773547106304
    message_id = myPayload.message_id
    if message_id == RRMESSAGEID:
        guild = myBot.get_guild(IDSERVER)
        ROLENAME = myPayload.emoji.name
        roleid = discord.utils.get(guild.roles, name = ROLENAME)
        role = guild.get_role(roleid.id)

        if role is not None:
            member = guild.get_member(myPayload.user_id)
            if member is not None:
                await member.remove_roles(role)
                print('The role is removed')
            else:
                print('Member not found')
        else:
                print('Role not found')

@bot.event
async def on_raw_reaction_remove(payload):
   return await onRoleRemoveAction(bot, payload)


async def onClearAction(myCtx, myNumber:int = None):
    if myCtx.message.author.guild_permissions.manage_messages:
        try:
            if myNumber == None:
               await myCtx.send('Please enter an amount of messages you want to delete.')
            else:
                await myCtx.channel.purge(limit=myNumber)
                print('purge')
                await myCtx.send(f'Messages cleared by {myCtx.message.author.mention} {myNumber}.')
                print('purge 2')
        except Exception as e:
            traceback.print_exc() 
            await myCtx.send("I can't delete messages here.")
    else:
        await myCtx.send("You don't have the permission to use this command.")


@bot.command(name='clear', description='clears a certain amount of messages')
async def clear(ctx, number:int = None):
    return await onClearAction(ctx, number)


@bot.command(name='kick')
async def kick(ctx, user: discord.Member, *, reason=None):
    print('kick')
    if user.guild_permissions.manage_messages:
        await ctx.send("You can't kick this user!")
    elif ctx.message.author.guild_permissions.kick_members:
        if reason == None:
            await ctx.guild.kick(user=user, reason='Unknown')
            await ctx.send(f'{user} has been kicked')
        else:
            await ctx.guild.kick(user=user, reason=reason)
            await ctx.send(f'{user} has been kicked for {reason}')
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command(name='ban')
async def ban(ctx, user: discord.Member, *, reason=None):
    print('ban')
    if user.guild_permissions.manage_messages:
        await ctx.send("You can't ban this user!")
    elif ctx.message.author.guild_permissions.ban_members:
        if reason == None:
            await ctx.guild.ban(user=user, reason='Unknown')
            await ctx.send(f'{user} has been banned')
        else:
            await ctx.guild.ban(user=user, reason=reason)
    else:
        await ctx.send("You don't have permission to use this command.")


@bot.command(name='unban')
async def unban(ctx, *, member):
    print('unban')
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            if ctx.message.author.guild_permissions.ban_members:
                await ctx.guild.unban(user)
                await ctx.send(f'{user} has been unbanned')
                await member.send(f'You have been unbanned from {guild.name}')
            else:
                await ctx.send("You don't have permission to use this command.")
        else:
            await ctx.send(f'{user} is not banned.')
            return

bot.run('TOKEN')



