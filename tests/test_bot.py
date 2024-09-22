from unittest.mock import AsyncMock, patch

import pytest

from actual_discord_bot.bot import bot


@pytest.mark.asyncio
async def test_on_message():
    # Arrange
    mock_message = AsyncMock()
    mock_message.author = AsyncMock()
    mock_message.author.bot = False
    mock_message.content = "Test message"

    # Act
    with patch.object(mock_message.channel, "send") as mock_send:
        await bot.on_message(mock_message)

    # Assert
    mock_send.assert_called_once_with("Echo: Test message")


@pytest.mark.asyncio
async def test_on_message_from_bot():
    # Arrange
    mock_message = AsyncMock()
    mock_message.author = bot.user

    # Act
    with patch.object(mock_message.channel, "send") as mock_send:
        await bot.on_message(mock_message)

    # Assert
    mock_send.assert_not_called()
