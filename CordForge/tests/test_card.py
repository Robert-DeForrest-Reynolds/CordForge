import pytest
import pytest_asyncio
from unittest.mock import Mock, patch
from CordForge.card import Card
from CordForge.colors import GRAY, WHITE

@pytest.fixture
def mock_user():
    return Mock()


@pytest_asyncio.fixture
async def card(mock_user):
    c = Card(mock_user)
    await c.new_image()
    return c


@pytest.mark.asyncio
async def test_card_methods(card, tmp_path):
    card
    with patch("CordForge.card.Panel", autospec=True), \
         patch("CordForge.card.Line", autospec=True), \
         patch("CordForge.card.Board", autospec=True), \
         patch("CordForge.card.Text", autospec=True), \
         patch("CordForge.card.Sprite", autospec=True), \
         patch("CordForge.card.DiscordFile", autospec=True):

        await card._construct()
        await card._buffer_image()
        await card.save_image(str(tmp_path / "test"))
        await card.add_button("btn", lambda *_: None, [])
        await card.panel()
        await card.line()
        await card.board()
        await card.text("Hello")
        await card.sprite()
        await card.debug(vertical_center=True, horizontal_center=True)
