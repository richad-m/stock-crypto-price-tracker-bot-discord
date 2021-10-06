import discord
import os
import methods

my_secret = os.environ['TOKEN']

client = discord.Client()


@client.event
async def on_ready():
    # As soon as the bot is ready
    print('Logged as {}'.format(client.user))


@client.event
# Each time a message is received
async def on_message(message):
    # Ignoring messages from the bot
    if message.author == client.user:
        return

    if message.content.startswith('!yo'):
        # Greets the author of the message
        autor = message.author.display_name
        await message.channel.send("Yo to you {}. Feel free to ask for help by typing the command !help".format(autor))

    if message.content.startswith('!price'):
        symbol = message.content.split()[1]
        try:
            response = methods.get_stock_price(symbol)
        except:
            response = "I couldn't find any price for {}, are you sure it speels like that ?".format(
                symbol)
        await message.channel.send(response)

    if message.content.startswith('!stocks delete'):
        # Removes a stock from the stock Watchlist
        try:
            symbol = message.content.split()[2]
            try:
                response = methods.remove_stock_to_follow(symbol, 'stocks')
            except:
                response = "Oops ! {} not in your followed stocks".format(
                    symbol, 'stocks')
        except:
            response = "Oops ! I couldn't delete your stock. Try using this format '!stocks delete AAPL'"
        await message.channel.send(response)

    if message.content.startswith('!stocks'):
        # Adds a stock to stock Watchlist
        try:
            symbol = message.content.split()[1]
            if symbol == "delete":
                return
            try:
                response = methods.add_stock_to_follow(symbol, 'stocks')
            except:
                response = "Oops, I didn't get that !"
        except IndexError:
            # If no symbol is provided, display watchlist
            response = methods.stock_to_follow('stocks')
        await message.channel.send(response)

    if message.content.startswith('!cryptoprice'):
        # Gets price for a crypto
        try:
            symbol = message.content.split()[1]
            try:
                response = methods.get_crypto_price(symbol)
            except:
                response = "I couldn't find any price for {}, are you sure it speels like that ?".format(
                    symbol)
        except:
            response = "Oops, I didn't get that !"
        await message.channel.send(response)

    if message.content.startswith('!cryptolist'):
        # Adds crypto to crypto Watchlist
        if message.content == '!cryptolist':
            response = methods.stock_to_follow('crypto')
        else:
            method = message.content.split()[1]
            symbol = message.content.split()[2]
            if method == "delete":
                return
            try:
                response = methods.add_stock_to_follow(symbol, 'crypto')
            except:
                response = "Oops, I didn't get that !"
        await message.channel.send(response)

    if message.content.startswith('!cryptolist delete'):
        # Deletes crypto from cryptolist Watchlist
        try:
            # Try if a crypto is specified
            symbol = message.content.split()[2]
            try:
                # Try to remove if crypto is currently in watchlist
                response = methods.remove_stock_to_follow(symbol, 'crypto')
            except:
                # Display message if crypto not followed yet
                response = "Oops ! {} not in your followed crypto".format(
                    symbol, 'crypto')
        except:
            response = "Oops ! I couldn't delete your crypto. Try using this format '!cryptolist delete BTC'"
        await message.channel.send(response)

client.run(my_secret)
