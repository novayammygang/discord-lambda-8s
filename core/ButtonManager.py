import datetime

from core import QueueManager
from discord_lambda import Interaction
from dao.QueueDao import QueueDao

queue_dao = QueueDao()
def button_flow_tree(interaction: Interaction):
  if interaction.custom_id == QueueManager.join_queue_custom_id:
    join_queue_button(interaction.guild_id, interaction)
  elif interaction.custom_id == QueueManager.leave_queue_custom_id:
    leave_queue_button(interaction.guild_id, interaction)

def join_queue_button(guild_id: str, inter: Interaction):
  print("Join queue button clicked")
  resp = QueueManager.add_player(inter)

  if resp is None:
    return

  (embed, component) = resp
  record = queue_dao.get_queue(guild_id=guild_id, queue_id="1")
  queue_dao.put_queue(record)

  inter.edit_response(channel_id=record.channel_id, message_id=record.message_id, content=str(datetime.datetime.now()), embeds=[embed], components=[component])


def leave_queue_button(guild_id: str, inter: Interaction):
  print("Leave queue button clicked")
  resp = QueueManager.remove_player(inter)

  if resp is None:
    return

  (embed, component) = resp

  record = queue_dao.get_queue(guild_id=guild_id, queue_id="1")
  queue_dao.put_queue(record)

  inter.edit_response(channel_id=record.channel_id, message_id=record.message_id, content=str(datetime.datetime.now()), embeds=[embed], components=[component])