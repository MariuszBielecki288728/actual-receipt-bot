from unittest.mock import AsyncMock, patch

import discord
import pytest

from actual_discord_bot import ActualDiscordBot
from actual_discord_bot.config import DiscordConfig


@pytest.fixture
def bot():
    config = DiscordConfig(
        token="token",
        bank_notification_channel="bank-notifications",
    )
    return ActualDiscordBot(config)


@pytest.fixture
def mock_channel():
    channel = AsyncMock(spec=discord.TextChannel)
    channel.name = "bank-notifications"
    return channel


class AsyncContextManagerMock:
    async def __aenter__(self):
        return None

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return None


@pytest.fixture
def ctx():
    context = AsyncMock(spec=discord.ext.commands.Context)
    context.typing.return_value = AsyncContextManagerMock()
    return context


@pytest.mark.asyncio
async def test_catch_up_processes_unreacted_messages(bot, mock_channel, ctx):
    bot.target_channel = mock_channel

    unreacted_message = AsyncMock(spec=discord.Message)
    unreacted_message.reactions = []

    reacted_message = AsyncMock(spec=discord.Message)
    reaction = AsyncMock(spec=discord.Reaction)
    reaction.emoji = "✅"
    reaction.me = True
    reacted_message.reactions = [reaction]

    mock_channel.history.return_value.__aiter__.return_value = [
        unreacted_message,
        reacted_message,
    ]

    with patch.object(bot, "handle_message") as mock_handle:
        await bot.catch_up.callback(bot, ctx)

        mock_handle.assert_called_once_with(unreacted_message)
        ctx.send.assert_called_once_with("Catch-up complete. Processed 1 messages.")


@pytest.mark.asyncio
async def test_catch_up_handles_missing_channel(bot, ctx):
    bot.target_channel = None

    await bot.catch_up.callback(bot, ctx)

    ctx.send.assert_called_once_with("Error: Channel 'bank-notifications' not found.")


@pytest.mark.asyncio
async def test_catch_up_handles_empty_channel(bot, mock_channel, ctx):
    bot.target_channel = mock_channel
    mock_channel.history.return_value.__aiter__.return_value = []

    await bot.catch_up.callback(bot, ctx)

    ctx.send.assert_called_once_with("Catch-up complete. Processed 0 messages.")


@pytest.mark.asyncio
async def test_catch_up_ignores_already_reacted_messages(bot, mock_channel, ctx):
    bot.target_channel = mock_channel

    # Create a message that already has our reaction
    reacted_message = AsyncMock(spec=discord.Message)
    reaction = AsyncMock(spec=discord.Reaction)
    reaction.emoji = "✅"
    reaction.me = True
    reacted_message.reactions = [reaction]

    mock_channel.history.return_value.__aiter__.return_value = [reacted_message]

    with patch.object(bot, "handle_message") as mock_handle:
        await bot.catch_up.callback(bot, ctx)

        mock_handle.assert_not_called()
        ctx.send.assert_called_once_with("Catch-up complete. Processed 0 messages.")


@pytest.mark.asyncio
async def test_catch_up_processes_message_with_different_reaction(
    bot,
    mock_channel,
    ctx,
):
    # Arrange
    bot.target_channel = mock_channel

    # Create a message that has a different reaction
    message_with_different_reaction = AsyncMock(spec=discord.Message)
    different_reaction = AsyncMock(spec=discord.Reaction)
    different_reaction.emoji = "👍"  # Different emoji
    different_reaction.me = True
    message_with_different_reaction.reactions = [different_reaction]

    # Set up the history to return the message
    mock_channel.history.return_value.__aiter__.return_value = [
        message_with_different_reaction,
    ]

    # Act
    with patch.object(bot, "handle_message") as mock_handle:
        await bot.catch_up.callback(bot, ctx)

        # Assert
        mock_handle.assert_called_once_with(message_with_different_reaction)
        ctx.send.assert_called_once_with("Catch-up complete. Processed 1 messages.")
