from CordForge import *


# Initial send of dashboard, all other functions are replys/edits of the sent message
async def entry(user_card:Card) -> Card:
    await user_card.new_image()
    panel = await user_card.panel(border=True)
    await user_card.text("Hello", Vector2(5, 5), parent=panel)
    await user_card.add_button("Scavenge", scavenge_report, [])


async def scavenge_report(user_card:Card, interaction) -> None:
    await user_card.new_image()
    await user_card.add_button("Home", roc.home, [])
    await roc.reply(user_card, interaction)


roc = Cord("roc", entry)
# any necessary setup
roc.launch()