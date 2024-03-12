import disnake
from disnake import TextInputStyle
from datetime import datetime, timedelta
import locale
import os


class Application(disnake.ui.Modal):
    def __init__(self, bot, mode, content):
        self.bot = bot
        self.mode = mode
        self.content = content
        components = [
            disnake.ui.TextInput(
                label="Время:",
                placeholder="Укажжите время: [Пример: 17:00/18:30]",
                custom_id="time",
                style=TextInputStyle.short,
                max_length=5,
            ),
        ]
        super().__init__(
            title="Lucky Squad",
            custom_id="create_tag",
            components=components,
            timeout=120,
        )

    async def callback(self, interaction: disnake.ModalInteraction):
        self.mode[interaction.user.id]['time'] = dict(interaction.text_values.items()).get('time')
        if self.mode[interaction.user.id]['data'].lower() in ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота','воскресенье']:
            today = datetime.now().date()
            weekday = ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'].index(self.mode[interaction.user.id]['data'].lower())
            days_until_next_weekday = (weekday - today.weekday() + 7) % 7
            event_date = today + timedelta(days=days_until_next_weekday)
        elif self.mode[interaction.user.id]['data'].lower() == 'завтра':
            tomorrow = datetime.now() + timedelta(days=1)
            event_date = tomorrow.date()
        else:
            today_n = datetime.now()
            event_date = today_n.date()

        event_time = datetime.strptime(self.mode[interaction.user.id]['time'], '%H:%M').time()
        datetime_obj = datetime.combine(event_date, event_time)
        timestamp = disnake.utils.format_dt(datetime_obj, style='R')
        timestamp_1 = disnake.utils.format_dt(datetime_obj, style='t')
        locale.setlocale(locale.LC_ALL, 'ru_RU.utf8')
        formatted_date = event_date.strftime("%d %B")

        if self.mode[interaction.user.id]['vs'] == "1vs1":
            group_output = f'\n <a:busyslot:1142143554836250664> <@{interaction.user.id}>'
            gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(1)])
            kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** 1 из 1 участника:" + ''.join(group_output)
            gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** 0 из 1 участника:" + ''.join(gry)
        elif self.mode[interaction.user.id]['vs'] == "2vs2":
            group_output = f'\n <a:busyslot:1142143554836250664> <@{interaction.user.id}>'
            kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(1)])
            kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** 1 из 2 участников:" + ''.join(group_output) + ''.join(kortac)
            gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(2)])
            gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** 0 из 2 участников:" + ''.join(gry)
        elif self.mode[interaction.user.id]['vs'] == "3vs3":
            group_output = f'\n <a:busyslot:1142143554836250664> <@{interaction.user.id}>'
            kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(2)])
            kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** 1 из 3 участников:" + ''.join(group_output) + ''.join(kortac)
            gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(3)])
            gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** 0 из 3 участников:" + ''.join(gry)
        elif self.mode[interaction.user.id]['vs'] == "4vs4":
            group_output = f'\n <a:busyslot:1142143554836250664> <@{interaction.user.id}>'
            kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(3)])
            kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** 1 из 4 участников:" + ''.join(group_output) + ''.join(kortac)
            gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(4)])
            gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** 0 из 4 участников:" + ''.join(gry)
        elif self.mode[interaction.user.id]['vs'] == "5vs5":
            group_output = f'\n <a:busyslot:1142143554836250664> <@{interaction.user.id}>'
            kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(4)])
            kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** 1 из 5 участников:" + ''.join(group_output) + ''.join(kortac)
            gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(5)])
            gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** 0 из 5 участников:" + ''.join(gry)
        else:
            group_output = f'\n <a:busyslot:1142143554836250664> <@{interaction.user.id}>'
            kortac = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(5)])
            kortac_output = f"\n<:kortac:1181591895357542421> **Кортак:** 1 из 6 участников:" + ''.join(group_output) + ''.join(kortac)
            gry = "".join([f"\n <a:freeslot:1142143566634811495> Свободное место." for _ in range(6)])
            gry_output = f"\n<:gru:1181591929817931796> **СпецГРУ:** 0 из 6 участников:" + ''.join(gry)

        file_name = self.mode[interaction.user.id]['name_img']
        file_path_img = os.path.join("img", f"{file_name}.png")
        file = disnake.File(file_path_img)

        content_header = f"```⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀COD Fight: {self.mode[interaction.user.id]['vs']}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀```"

        content_body = (f"\n<:cod:1194212299427287070> **VS Противостояние** {timestamp}"
                        f"\n⠀<:map:1194211132966182973> `Карта` ➔ {self.mode[interaction.user.id]['map']}"
                        f"\n⠀<:mode:1194210872256630784> `Режим` ➔ {self.mode[interaction.user.id]['mode']}"
                        f"\n⠀<:time:1194212537068163152> `Время` ➔ {timestamp_1}"
                        f"\n⠀<:date:1194212573650886656> `Дата⠀` ➔ {formatted_date}\n")

        content_kortac = kortac_output
        content_gry = gry_output

        content_output = {
            "content_header": content_header,
            "content_body": content_body,
            "content_kortac": content_kortac,
            "content_gry": content_gry
        }

        id_channel = self.bot.get_channel(1181709365938487296)
        msg = await id_channel.send(f"{content_output['content_header'] + content_output['content_body'] + content_output['content_kortac'] + content_output['content_gry']}", file=file)
        self.mode[interaction.user.id]['msg_id'] = msg.id
        self.mode[interaction.user.id]['msg_jump'] = msg.jump_url
        self.content[interaction.user.id] = content_output
        self.mode[interaction.user.id]['red'].append(interaction.user.id)

        join_red = disnake.ui.Button(style=disnake.ButtonStyle.danger, label="⠀⠀⠀⠀⠀⠀⠀Кортак⠀⠀⠀⠀⠀⠀⠀", custom_id=f"red:{interaction.user.id}")
        join_blue = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="⠀⠀⠀⠀⠀⠀⠀СпецГРУ⠀⠀⠀⠀⠀⠀⠀", custom_id=f"blue:{interaction.user.id}")

        await msg.edit(components=[join_red, join_blue])
        await interaction.response.defer()
        await interaction.delete_original_message()


class SelectData(disnake.ui.StringSelect):
    def __init__(self, bot, mode, content):
        self.bot = bot
        self.mode = mode
        self.content = content
        options = [
            disnake.SelectOption(label="Сегодня", value="1"),
            disnake.SelectOption(label="Завтра", value="2"),
            disnake.SelectOption(label="Понедельник", value="3"),
            disnake.SelectOption(label="Вторник", value="4"),
            disnake.SelectOption(label="Среда", value="5"),
            disnake.SelectOption(label="Четверг", value="6"),
            disnake.SelectOption(label="Пятница", value="7"),
            disnake.SelectOption(label="Суббота", value="8"),
            disnake.SelectOption(label="Воскресенье", value="9"),
        ]
        super().__init__(
            placeholder="Выберите день:",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            map_options = ["Сегодня", "Завтра", "Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
            self.mode[interaction.user.id]['data'] = map_options[int(self.values[0]) - 1]
            await interaction.response.send_modal(modal=Application(self.bot, self.mode, self.content))
        except Exception as e:
            print(f"An error occurred: {e}")


class DataView(disnake.ui.View):
    def __init__(self, bot, mode, content):
        super().__init__(timeout=120.0)
        self.add_item(SelectData(bot, mode, content))


class SelectMode(disnake.ui.StringSelect):
    def __init__(self, bot, mode, content):
        self.bot = bot
        self.mode = mode
        self.content = content
        options = [
            disnake.SelectOption(label="Командный бой", value="1"),
            disnake.SelectOption(label="Превосходство", value="2"),
            disnake.SelectOption(label="Найти и уничтожить", value="3"),
            disnake.SelectOption(label="Убийство подтверждено", value="4"),
            disnake.SelectOption(label="Опорный пункт", value="5"),
            disnake.SelectOption(label="Контроль", value="6"),
        ]
        super().__init__(
            placeholder="Выберите режим:",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            map_options = ["Командный бой", "Превосходство", "Найти и уничтожить", "Убийство подтверждено", "Опорный пункт", "Контроль"]
            self.mode[interaction.user.id]['mode'] = map_options[int(self.values[0]) - 1]
            views = DataView(self.bot, self.mode, self.content)
            await interaction.response.send_message(view=views, ephemeral=True, delete_after=120)
        except Exception as e:
            print(f"An error occurred: {e}")


class ModeView(disnake.ui.View):
    def __init__(self, bot, mode, content):
        super().__init__(timeout=120.0)
        self.add_item(SelectMode(bot, mode, content))


class SelectMap(disnake.ui.StringSelect):
    def __init__(self, bot, mode, content):
        self.bot = bot
        self.mode = mode
        self.content = content
        options = [
            disnake.SelectOption(label="Shipment", value="0"),
            disnake.SelectOption(label="Afghan", value="1"),
            disnake.SelectOption(label="Derail", value="2"),
            disnake.SelectOption(label="Estate", value="3"),
            disnake.SelectOption(label="Favela", value="4"),
            disnake.SelectOption(label="Karachi", value="5"),
            disnake.SelectOption(label="Highrise", value="6"),
            disnake.SelectOption(label="Invasion", value="7"),
            disnake.SelectOption(label="Quarry", value="8"),
            disnake.SelectOption(label="Rundown", value="9"),
            disnake.SelectOption(label="Rust", value="10"),
            disnake.SelectOption(label="Scrapyard", value="11"),
            disnake.SelectOption(label="Skidrow", value="12"),
            disnake.SelectOption(label="Sub Base", value="13"),
            disnake.SelectOption(label="Terminal", value="14"),
            disnake.SelectOption(label="Underpass", value="15"),
            disnake.SelectOption(label="Wasteland", value="16"),
        ]
        super().__init__(
            placeholder="Выберите карту:",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: disnake.MessageInteraction):
        try:
            map_options = ["Shipment", "Afghan", "Derail", "Estate", "Favela", "Karachi", "Highrise", "Invasion", "Quarry", "Rundown", "Rust", "Scrapyard", "Skidrow", "Sub Base", "Terminal", "Underpass", "Wasteland"]
            self.mode[interaction.user.id]['map'] = map_options[int(self.values[0])]
            self.mode[interaction.user.id]['name_img'] = map_options[int(self.values[0])]
            views = ModeView(self.bot, self.mode, self.content)
            await interaction.response.send_message(view=views, ephemeral=True, delete_after=120)
        except Exception as e:
            print(f"An error occurred: {e}")


class MapView(disnake.ui.View):
    def __init__(self, bot, mode, content):
        super().__init__(timeout=120.0)
        self.add_item(SelectMap(bot, mode, content))
