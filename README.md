# Verifier
Easily keep trolls outside with custom verifications. Welcome users with a customizable message.

## How it works:
The bot will ask users specific questions you set before. Based on their answers you can tell if they fit your server or not.

## Commands
`--setup`
>Run the initial setup. You will be asked for a mod-channel and verification-channel; the mod-channel is where the applications will be send to, the verification-channel is where users can run the `--verify` command.

`--questions`
>Set the questions the bot asks.

`--verify`
>Starts the verification with the set questions in dms of the user.

`--welcomemsg`
>Set/activate the welcome message. This message will be send after users have been approved. It requires you to have setup a role the bot can assign to users after verification.

`--approve`
>Approve users (e.g. give them the set role) and send them a welcomemessage. Users will also be notified in dms about it.

- the next update will bring a function to disapprove users

`--invite`
>Sends the invite link


## Hosting your own bot:
- fill in the file [config.json](https://github.com/Tarikazana/Verifier/blob/main/config.json) with your token.
- Make sure you have python installed (developed in V3.9.6) and [discord.py](https://discordpy.readthedocs.io/en/stable/intro.html)
- Make sure to create following directories in the same Folder as the [main.py](https://github.com/Tarikazana/Verifier/blob/main/main.py)
`/data/server`
- Have "Privileged Gateway Intents" enabled
- you may need to change directory names based on where you'll run the bot
- start the bot by running the [main.py](https://github.com/Tarikazana/Verifier/blob/main/main.py) file
