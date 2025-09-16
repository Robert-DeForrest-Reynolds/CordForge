from CordForge import *


bot = Cord(entry_command="cmd")

bot.user_traits = [
    # [trait name, trait value]
    ["wallet", 0.00],
]


# Initial send of dashboard, all other functions are replys/edits of the sent message
async def entry(user_card:Card) -> Card:
    await user_card.add_button(f"Money: {user_card.user.wallet}", give_money, [])


async def give_money(user_card:Card, interaction) -> None:
    user_card.user.wallet += 1
    await bot.home(user_card, interaction)


bot.launch(entry)