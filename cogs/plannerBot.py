import disnake
from disnake.ext import commands, tasks
from datetime import datetime, timedelta
from cogs import func


class CodPlannerPro(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mode = {}
        self.content = {}
        self.sent_reminders = {}

    @commands.Cog.listener()
    async def on_ready(self):
        print("BOT STARTED")
        self.delete_msg.start()


    @tasks.loop(minutes=5)
    async def delete_msg(self):
        messages_to_delete = []

        for msg_id, data in self.mode.items():
            time_data = data['time']
            date_data = data['data']
            data_msg_id = data['msg_id']
            if data_msg_id is None:
                return
            if date_data and time_data is not None:
                if date_data.lower() in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота','воскресенье']:
                    today = datetime.now().date()
                    weekday = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'].index(date_data.lower())
                    days_until_next_weekday = (weekday - today.weekday() + 7) % 7
                    event_date = today + timedelta(days=days_until_next_weekday)
                elif date_data.lower() == 'завтра':
                    tomorrow = datetime.now() + timedelta(days=1)
                    event_date = tomorrow.date()
                else:
                    today_n = datetime.now()
                    event_date = today_n.date()

                current_time = datetime.now() - timedelta(minutes=5)
                current_data = datetime.now().date().strftime("%d %B")
                formatted_time = current_time.strftime('%H:%M')
                formatted_date = event_date.strftime("%d %B")

                if formatted_date == current_data:
                    if formatted_time >= time_data:
                        messages_to_delete.append(data_msg_id)

        for data_msg_id in messages_to_delete:
            id_channel = self.bot.get_channel(1181709365938487296)
            message = await id_channel.fetch_message(data_msg_id)
            try:
                self.sent_reminders.pop(data_msg_id)
                self.content.pop(msg_id)
                self.mode.pop(msg_id)
                await message.delete()
            except Exception as error:
                print(f"An error occurred [on_message]: >>> {error}")

    @tasks.loop(minutes=5)
    async def reminder(self):
        reminders_to_send = []

        for user_id, data in self.mode.items():
            time_data = data['time']
            data_mode = data['data']
            data_map = data['map']
            data_vs = data['vs']
            data_mod = data['mode']
            data_user_id = data['id_owner']
            data_message_id = data['msg_jump']
            data_msg_id = data['msg_id']
            if data_mode and time_data is not None:
                if data_mode.lower() in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота','воскресенье']:
                    today = datetime.now().date()
                    weekday = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'].index(data_mode.lower())
                    days_until_next_weekday = (weekday - today.weekday() + 7) % 7
                    event_date = today + timedelta(days=days_until_next_weekday)
                elif data_mode.lower() == 'завтра':
                    tomorrow = datetime.now() + timedelta(days=1)
                    event_date = tomorrow.date()
                else:
                    today_n = datetime.now()
                    event_date = today_n.date()

                current_time = datetime.now() + timedelta(minutes=20)
                current_data = datetime.now().date().strftime("%d %B")
                formatted_time = current_time.strftime('%H:%M')
                formatted_date = event_date.strftime("%d %B")

                if formatted_date == current_data:
                    if formatted_time >= time_data:
                        user_red = data['red']
                        user_blue = data['blue']
                        reminders_to_send.append((data_msg_id, user_red + user_blue, time_data, data_mode, data_map, data_vs, data_mod, data_user_id, data_message_id))

        for data_msg_id, users_to_message, time_data, data_mode, data_map, data_vs, data_mod, data_user_id, data_message_id in reminders_to_send:
            if data_msg_id in self.sent_reminders:
                pass
            else:
                self.sent_reminders[data_msg_id] = set()
                self.sent_reminders[data_msg_id].update(users_to_message)

                for user_id_to_message in users_to_message:
                    try:
                        user = self.bot.get_user(user_id_to_message)
                        if user:
                            embed = disnake.Embed(
                                title="Lucky Squad Community",
                                description=f"<:gru:1181591929817931796>/<:kortac:1181591895357542421>[**{data_mod}** - нажми, чтобы перейти к сообщению!]({data_message_id})\n"
                                            f"`Режим:` {data_vs}\n"
                                            f"`Карта:` {data_map}\n"
                                            f"`Время:` {time_data}\n"
                                            f"<:emoji_109:1142156603710255144> Создатель: <@{data_user_id}>\n\n"
                                            f"Привет, **{user.name}**! Ты присоединился к событию в дискорд канале Lucky Squad. Скоро начнем, готовься!",
                                color=disnake.Color(int("0b5e54", 16)))
                            embed.set_footer(
                                text="COD Planner - Lucky Squad Team",
                                icon_url="https://i.ibb.co/LkvHvRd/Adobe-Express-20230814-2227330-1.png",
                            )
                            embed.set_thumbnail(url="https://i.ibb.co/LkvHvRd/Adobe-Express-20230814-2227330-1.png")
                            await user.send(embed=embed)
                    except Exception as error:
                        print(f"An error occurred [reminder]: {error}")


    @commands.Cog.listener()
    async def on_button_click(self, interaction: disnake.MessageInteraction):
        for vs_value in ['1vs1', '2vs2', '3vs3', '4vs4', '5vs5', '6vs6']:
            if interaction.component.custom_id.startswith(vs_value):
                if interaction.user.id in self.mode:
                    embed = disnake.Embed(
                        title="",
                        description="⚠️ Ты уже создал событие, прежде чем создать новое, удали старое событие!",
                        color=disnake.Color(int("ff3737", 16)))
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    self.mode[interaction.user.id] = {'blue': [], 'red': [], 'vs': vs_value, 'name_img': "", 'map': "", 'mode': "", 'data': "", 'time': "", 'id_owner': interaction.author.id, 'msg_id': None, 'msg_jump': None}
                    view = func.MapView(self.bot, self.mode, self.content)
                    await interaction.response.send_message(view=view, ephemeral=True, delete_after=120)
        if interaction.component.custom_id.startswith("del_mode"):
            if interaction.user.id in self.mode:
                if interaction.user.id in self.content:
                    if self.content[interaction.user.id] is None:
                        pass
                    else:
                        self.content.pop(interaction.user.id)
                        msg_id = self.mode[interaction.user.id].get("msg_id")
                        message = await interaction.channel.fetch_message(int(msg_id))
                        self.sent_reminders.pop(message.id)
                        await message.delete()
                self.mode.pop(interaction.user.id)
                embed = disnake.Embed(
                    title="",
                    description="⚠️ Событие удалено!",
                    color=disnake.Color(int("179455", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=12)
            else:
                embed = disnake.Embed(
                    title="",
                    description="⚠️ Событие не найдено!",
                    color=disnake.Color(int("ff3737", 16)))
                await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=12)
        if interaction.component.custom_id.startswith("red:"):
            split_msg_id = int(interaction.component.custom_id.split(":")[1])
            if interaction.user.id in self.mode[int(split_msg_id)]['red']:
                member_group = self.mode[int(split_msg_id)]['red']

                vs_options = {
                    "1vs1": 1,
                    "2vs2": 2,
                    "3vs3": 3,
                    "4vs4": 4,
                    "5vs5": 5,
                    "6vs6": 6
                }

                vs = self.mode[split_msg_id]['vs']
                self.mode[int(split_msg_id)]['red'].remove(interaction.user.id)
                count_current_group_member_new = len(member_group)
                member_group_blue = self.mode[int(split_msg_id)]['blue']
                count_current_group_member_blue = len(member_group_blue)
                if count_current_group_member_new == 0 and count_current_group_member_blue == 0:
                    msg_id = self.mode[int(split_msg_id)].get("msg_id")
                    message = await interaction.channel.fetch_message(int(msg_id))
                    await message.delete()
                    self.content.pop(int(split_msg_id))
                    self.mode.pop(int(split_msg_id))
                    return

                free_slots_new = vs_options[vs] - count_current_group_member_new
                group_output = [f'\n <a:busyslot:1142143554836250664> <@{item}>' for item in member_group]
                kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(free_slots_new)])
                kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** {count_current_group_member_new} из {vs_options[vs]} участников:" + ''.join(group_output) + ''.join(kortac)
                self.content[int(split_msg_id)]["content_kortac"] = kortac_output

                await interaction.response.edit_message(
                    self.content[int(split_msg_id)]['content_header'] +
                    self.content[int(split_msg_id)]['content_body'] +
                    self.content[int(split_msg_id)]['content_kortac'] +
                    self.content[int(split_msg_id)]['content_gry'])
            else:
                if interaction.user.id in self.mode[int(split_msg_id)]['blue']:
                    embed = disnake.Embed(
                        title="",
                        description="⚠️ Ты уже присоединился к СпецГРУ!",
                        color=disnake.Color(int("ff3737", 16)))
                    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=12)
                    return

                member_group = self.mode[int(split_msg_id)]['red']
                count_current_group_member = len(member_group)

                vs_options = {
                    "1vs1": 1,
                    "2vs2": 2,
                    "3vs3": 3,
                    "4vs4": 4,
                    "5vs5": 5,
                    "6vs6": 6
                }

                vs = self.mode[split_msg_id]['vs']
                free_slots = vs_options[vs] - count_current_group_member

                if free_slots < 1:
                    embed = disnake.Embed(
                        title="",
                        description="⚠️ Команда заполнена, присоединиться не удалось!",
                        color=disnake.Color(int("ff3737", 16)))
                    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=12)
                    return
                else:
                    self.mode[int(split_msg_id)]['red'].append(interaction.user.id)
                    count_current_group_member_new = len(member_group)
                    free_slots_new = vs_options[vs] - count_current_group_member_new

                    group_output = [f'\n <a:busyslot:1142143554836250664> <@{item}>' for item in member_group]
                    kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(free_slots_new)])
                    kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** {count_current_group_member_new} из {vs_options[vs]} участников:" + ''.join(group_output) + ''.join(kortac)
                    self.content[int(split_msg_id)]["content_kortac"] = kortac_output

                await interaction.response.edit_message(
                    self.content[int(split_msg_id)]['content_header'] +
                    self.content[int(split_msg_id)]['content_body'] +
                    self.content[int(split_msg_id)]['content_kortac'] +
                    self.content[int(split_msg_id)]['content_gry'])
        if interaction.component.custom_id.startswith("blue:"):
            split_msg_id = int(interaction.component.custom_id.split(":")[1])
            if interaction.user.id in self.mode[int(split_msg_id)]['blue']:
                member_group = self.mode[int(split_msg_id)]['blue']

                vs_options = {
                    "1vs1": 1,
                    "2vs2": 2,
                    "3vs3": 3,
                    "4vs4": 4,
                    "5vs5": 5,
                    "6vs6": 6
                }

                vs = self.mode[split_msg_id]['vs']
                self.mode[int(split_msg_id)]['blue'].remove(interaction.user.id)
                count_current_group_member_new = len(member_group)
                member_group_red = self.mode[int(split_msg_id)]['red']
                count_current_group_member_red = len(member_group_red)
                if count_current_group_member_new == 0 and count_current_group_member_red == 0:
                    msg_id = self.mode[int(split_msg_id)].get("msg_id")
                    message = await interaction.channel.fetch_message(int(msg_id))
                    await message.delete()
                    self.content.pop(int(split_msg_id))
                    self.mode.pop(int(split_msg_id))
                    return

                free_slots_new = vs_options[vs] - count_current_group_member_new
                group_output = [f'\n <a:busyslot:1142143554836250664> <@{item}>' for item in member_group]
                gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(free_slots_new)])
                gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** {count_current_group_member_new} из {vs_options[vs]} участников:" + ''.join(group_output) + ''.join(
                    gry)
                self.content[int(split_msg_id)]["content_gry"] = gry_output

                await interaction.response.edit_message(
                    self.content[int(split_msg_id)]['content_header'] +
                    self.content[int(split_msg_id)]['content_body'] +
                    self.content[int(split_msg_id)]['content_kortac'] +
                    self.content[int(split_msg_id)]['content_gry'])
            else:
                if interaction.user.id in self.mode[int(split_msg_id)]['red']:
                    embed = disnake.Embed(
                        title="",
                        description="⚠️ Ты уже присоединился к Кортак!",
                        color=disnake.Color(int("ff3737", 16)))
                    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=12)
                    return

                member_group = self.mode[int(split_msg_id)]['blue']
                count_current_group_member = len(member_group)

                vs_options = {
                    "1vs1": 1,
                    "2vs2": 2,
                    "3vs3": 3,
                    "4vs4": 4,
                    "5vs5": 5,
                    "6vs6": 6
                }

                vs = self.mode[split_msg_id]['vs']
                free_slots = vs_options[vs] - count_current_group_member

                if free_slots < 1:
                    embed = disnake.Embed(
                        title="",
                        description="⚠️ Команда заполнена, присоединиться не удалось!",
                        color=disnake.Color(int("ff3737", 16)))
                    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=12)
                    return
                else:
                    self.mode[int(split_msg_id)]['blue'].append(interaction.user.id)
                    count_current_group_member_new = len(member_group)
                    free_slots_new = vs_options[vs] - count_current_group_member_new

                    group_output = [f'\n <a:busyslot:1142143554836250664> <@{item}>' for item in member_group]
                    gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(free_slots_new)])
                    gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** {count_current_group_member_new} из {vs_options[vs]} участников:" + ''.join(group_output) + ''.join(
                        gry)
                    self.content[int(split_msg_id)]["content_gry"] = gry_output

                await interaction.response.edit_message(
                    self.content[int(split_msg_id)]['content_header'] +
                    self.content[int(split_msg_id)]['content_body'] +
                    self.content[int(split_msg_id)]['content_kortac'] +
                    self.content[int(split_msg_id)]['content_gry'])


def setup(bot):
    bot.add_cog(CodPlannerPro(bot))
