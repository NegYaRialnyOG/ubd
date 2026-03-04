




## WARNING! ALL YOU DO WITH THIS USERBOT ITS ON YOU OWN RISK! IF YOUR ACCOUNT GETS FREEZED/BANNED, I AM NOT RESPONSIBLE FOR IT!

## предупрждение! все что вы делаете с этим юзерботом, это на ваш страх и риск! если ваш аккаунт будет заблокирован/заморожен, я не несу ответственности за это!


import os
import time
import random
import asyncio
import io
import json
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError, PhoneCodeInvalidError

## get your own api, how to get it? https://my.telegram.org/auth?to=apps

API_ID = "22566570"
API_HASH = "7fa2e1ee4e929badc6588a877ab758e0"

client = TelegramClient("userbot_session", int(API_ID), API_HASH)

start_time = None
template = []
sessions = {}
pending_session = {}
session_clients = {}
client_states = {}
muted_users = set()



SESSIONS_FILE = "sessions.json"
TRL3_FILE = "trl3_state.json"

def get_client_state(client_id):
    if client_id not in client_states:
        client_states[client_id] = {
            "trl_running": False,
            "trl_task": None,
            "trl2_running": False,
            "trl2_task": None,
            "trl3_state": {"enabled": True, "targets": {}},
            "trl3_last_reply": {},
            "spam_running": False,
            "spam_task": None,
            "trl4_running": False,
            "trl4_task": None,
            "trl5_running": False,
            "trl5_task": None,
            "trl5_media": None,
            "trl5_user_id": None,
            "trl5_user_entity": None,
            "lagger_running": False,
            "lagger_task": None,
            "lagger_last_msg": {}
        }
    return client_states[client_id]

def load_trl3_state(client_id):
    state = get_client_state(client_id)
    trl3_file = f"trl3_state_{client_id}.json"
    if os.path.exists(trl3_file):
        try:
            with open(trl3_file, "r") as f:
                state["trl3_state"] = json.load(f)
        except:
            state["trl3_state"] = {"enabled": True, "targets": {}}

def save_trl3_state(client_id):
    state = get_client_state(client_id)
    trl3_file = f"trl3_state_{client_id}.json"
    with open(trl3_file, "w") as f:
        json.dump(state["trl3_state"], f)


def load_sessions():
    global sessions
    if os.path.exists(SESSIONS_FILE):
        try:
            with open(SESSIONS_FILE, "r") as f:
                sessions = json.load(f)
        except:
            sessions = {}


def save_sessions():
    with open(SESSIONS_FILE, "w") as f:
        json.dump(sessions, f)






def get_uptime():
    if not start_time:
        return ""
    delta = int(time.time() - start_time)
    days = delta // 86400
    hours = (delta % 86400) // 3600
    minutes = (delta % 3600) // 60

    parts = []
    if days > 0:
        parts.append(f"{days}д")
    if hours > 0:
        parts.append(f"{hours}ч")
    if minutes > 0 or not parts:
        parts.append(f"{minutes}м")

    return "-".join(parts)


def register_handlers(target_client, client_id=None):
    if client_id is None:
        client_id = "main"
    
    state = get_client_state(client_id)
    load_trl3_state(client_id)

    @target_client.on(events.NewMessage(pattern=r"^\.info$", outgoing=True))
    async def info_handler(event):
        uptime = get_uptime()
        ping_start = time.time()
        await event.edit("...")
        ping_end = time.time()
        latency_ms = (ping_end - ping_start) * 1000
        
        info_text = (
            "⚡ **SqqBot**\n"
            "💎 Version 1.4 (unstable)\n\n"
            f"⏰ Uptime: {uptime}\n"
            f"📶 Ping: {latency_ms:.0f}ms\n\n"
            "🔹 Type `.help` for commands."
        )
        
        await event.edit(info_text)

    @target_client.on(events.NewMessage(pattern=r"^\.help$", outgoing=True))
    async def help_handler(event):
        commands = [
            "⚡ **SqqBot - Команды**\n",
            "",
            "🔍 **Тесты/Помощь:**",
            "• `.info` - инфо о боте",
            "• `.help` - список команд",
            "• `.ping` - проверка задержки",
            "• `.uptime` - время работы",
            "",
            "👥 **Сессии:**",
            "• `.sessions` - список сессий",
            "• `.addsession (номер)` - добавить",
            "• `.removesession (номер)` - удалить",
            "",
            "🎭 **Тролль модули:**",
            "• `.shablon` - сохранить шаблон",
            "• `.trl (задержка) [текст]` - обычный трололо мод",
            "• `.trl2 (задержка) [текст] (id группы)` хуярит в группу",
            "• `.trl3 (id) [задержка]` - автоответчик",
            "• `.trl3 list/on/off/clear/clearall`",
            "• `.trl4 (задержка) (id)` - теггео",
            "• `.trl5 (id) (delay)` - теггер с медиа",
            "• `.spam (задержка) (сообщение)`",
            "• `.lagger (сек)` - спам/удаление лаг-сообщения",
            "",
            "⚙️ **Другое:**",
            "• `.mute (reply или userid)` - мут пользователя",
            "• `.restart` - перезагрузка бота",
            "• `.delmenow` - удалить все свои сообщения"
        ]
        await event.edit("\n".join(commands))

    @target_client.on(events.NewMessage(pattern=r"^\.uptime$", outgoing=True))
    async def uptime_handler(event):
        uptime = get_uptime()
        await event.edit(
            f"⏰ **Время работы**\n\n"
            f"📅 Бот онлайн: {uptime}\n\n"
            f"🕐 Запущен: {time.strftime('%H:%M:%S')}"
        )

    @target_client.on(events.NewMessage(pattern=r"^\.ping$", outgoing=True))
    async def ping_handler(event):
        ping_start = time.time()
        await event.edit("🏓 Проверяем соединение...")
        ping_end = time.time()
        latency_ms = (ping_end - ping_start) * 1000
        
        if latency_ms < 50:
            status = "🟢 Отличное"
        elif latency_ms < 100:
            status = "🟡 Хорошее"
        elif latency_ms < 200:
            status = "🟠 Среднее"
        else:
            status = "🔴 Плохое"
            
        await event.edit(
            f"🏓 **Результаты пинга**\n\n"
            f"⚡ Скорость: {latency_ms:.2f}ms\n"
            f"📊 Качество: {status}\n\n"
            f"⏰ Время: {time.strftime('%H:%M:%S')}"
        )

    @target_client.on(events.NewMessage(pattern=r"^\.sessions$",
                                        outgoing=True))
    async def sessions_handler(event):
        load_sessions()
        if not sessions:
            await event.edit("Нет сохранённых сессий.")
            return

        text = "**Сессии:**\n\n"
        for phone, data in sessions.items():
            is_active = phone in session_clients and session_clients[
                phone].is_connected()
            status = "✅" if is_active else "❌"
            text += f"{status} `{phone}`\n"

        await event.edit(text)






    @target_client.on(
        events.NewMessage(pattern=r"^\.addsession (.+)", outgoing=True))
    async def addsession_handler(event):
        global pending_session

        phone = event.pattern_match.group(1).strip()

        if not phone:
            await event.edit("Укажи номер: .addsession +79001234567")
            return

        chat_id = event.chat_id

        pending_session[chat_id] = {
            "phone": phone,
            "state": "waiting_code",
            "client": None,
            "phone_code_hash": None
        }

        session_name = f"session_{phone.replace('+', '').replace(' ', '')}"

        new_client = TelegramClient(session_name, int(API_ID), API_HASH)

        try:
            await new_client.connect()

            result = await new_client.send_code_request(phone)
            pending_session[chat_id]["client"] = new_client
            pending_session[chat_id][
                "phone_code_hash"] = result.phone_code_hash

            await event.edit(
                f"Код отправлен на {phone}\n\n**Код:**")

        except Exception as e:
            await event.edit(f"Ошибка: {str(e)}")
            if new_client:
                try:
                    await new_client.disconnect()
                except:
                    pass
            if chat_id in pending_session:
                del pending_session[chat_id]

    @target_client.on(events.NewMessage(outgoing=True))
    async def code_handler(event):
        global pending_session, session_clients

        chat_id = event.chat_id

        if chat_id not in pending_session:
            return

        session_data = pending_session[chat_id]
        text = event.raw_text.strip()

        if text.startswith("."):
            return

        if session_data["state"] == "waiting_code":
            code = text.replace(" ", "").replace("-", "")

            if not code.isdigit():
                return

            new_client = session_data["client"]
            phone = session_data["phone"]
            phone_code_hash = session_data["phone_code_hash"]

            try:
                result = await new_client.sign_in(
                    phone, code, phone_code_hash=phone_code_hash)

                if result:
                    me = await new_client.get_me()

                    load_sessions()
                    sessions[phone] = {
                        "active": True,
                        "session_name":
                        f"session_{phone.replace('+', '').replace(' ', '')}",
                        "user_id": me.id,
                        "username": me.username,
                        "first_name": me.first_name
                    }
                    save_sessions()

                    register_handlers(new_client)
                    session_clients[phone] = new_client

                    await event.edit(
                        f"✅ Сессия добавлена и запущена!\n\nАккаунт: {me.first_name} (@{me.username})"
                    )

                    del pending_session[chat_id]

            except SessionPasswordNeededError:
                pending_session[chat_id]["state"] = "waiting_2fa"
                await event.edit("Требуется 2FA\n\n**Пароль:**")

            except PhoneCodeInvalidError:
                await event.edit("Неверный код! Попробуй ещё раз.\n\n**Код:**")

            except Exception as e:
                error_msg = str(e)
                if "password" in error_msg.lower() or "2fa" in error_msg.lower(
                ):
                    pending_session[chat_id]["state"] = "waiting_2fa"
                    await event.edit("Требуется 2FA\n\n**Пароль:**")
                else:
                    await event.edit(f"Ошибка: {error_msg}")
                    if new_client:
                        await new_client.disconnect()
                    if chat_id in pending_session:
                        del pending_session[chat_id]

        elif session_data["state"] == "waiting_2fa":
            password = text
            new_client = session_data["client"]
            phone = session_data["phone"]

            try:
                await new_client.sign_in(password=password)

                me = await new_client.get_me()

                load_sessions()
                sessions[phone] = {
                    "active": True,
                    "session_name":
                    f"session_{phone.replace('+', '').replace(' ', '')}",
                    "user_id": me.id,
                    "username": me.username,
                    "first_name": me.first_name
                }
                save_sessions()

                register_handlers(new_client)
                session_clients[phone] = new_client

                await event.edit(
                    f"✅ Сессия добавлена и запущена!\n\nАккаунт: {me.first_name} (@{me.username})"
                )

                del pending_session[chat_id]

            except Exception as e:
                await event.edit(
                    f"Неверный пароль. Попробуй ещё.\n\n**Пароль:**")

    @target_client.on(
        events.NewMessage(pattern=r"^\.removesession (.+)", outgoing=True))
    async def removesession_handler(event):
        global session_clients

        phone = event.pattern_match.group(1).strip()

        load_sessions()

        if phone not in sessions:
            await event.edit(f"Сессия `{phone}` не найдена.")
            return

        session_name = sessions[phone].get("session_name", "")

        if phone in session_clients:
            try:
                await session_clients[phone].disconnect()
            except:
                pass
            del session_clients[phone]

        del sessions[phone]
        save_sessions()

        session_file = f"{session_name}.session"
        if os.path.exists(session_file):
            try:
                os.remove(session_file)
            except:
                pass

        await event.edit(f"✅ Сессия `{phone}` удалена и остановлена.")

    @target_client.on(events.NewMessage(pattern=r"^\.shablon$", outgoing=True))
    async def shablon_handler(event):
        global template
        reply = await event.get_reply_message()

        if not reply or not reply.document:
            await event.edit("Реплай на .txt файл!")
            return

        if reply.document.mime_type != "text/plain":
            await event.edit("Только .txt файлы!")
            return

        file = io.BytesIO()
        await reply.download_media(file=file)
        text = file.getvalue().decode("utf-8")
        template = [line.strip() for line in text.splitlines() if line.strip()]

        if template:
            await event.edit(f"Шаблон сохранён! ({len(template)} строк)")
        else:
            await event.edit("Пустой шаблон!")

    async def trl_loop(chat_id, delay, prefix=""):
        while state["trl_running"]:
            if not template:
                break
            line = random.choice(template)
            text = f"{prefix} {line}".strip() if prefix else line
            try:
                await target_client.send_message(chat_id, text)
            except Exception:
                pass
            await asyncio.sleep(delay)

    @target_client.on(
        events.NewMessage(pattern=r"^\.trl($| .+)", outgoing=True))
    async def trl_handler(event):
        if state["trl_running"]:
            state["trl_running"] = False
            if state["trl_task"]:
                state["trl_task"].cancel()
            await event.edit("Остановлено.")
            return

        args = event.raw_text[4:].strip().split()

        if not args:
            await event.edit("Укажи задержку: .trl <задержка> [доп текст]")
            return

        try:
            delay = int(args[0])
        except ValueError:
            await event.edit("Задержка должна быть числом!")
            return

        prefix = " ".join(args[1:]) if len(args) > 1 else ""

        if not template:
            await event.edit("Сначала сохрани шаблон через .shablon")
            return

        state["trl_running"] = True
        await event.edit("Запущено!")
        state["trl_task"] = asyncio.create_task(trl_loop(event.chat_id, delay, prefix))

    async def trl2_loop(chat_id, delay, prefix=""):
        while state["trl2_running"]:
            if not template:
                break
            line = random.choice(template)
            text = f"{prefix} {line}".strip() if prefix else line
            try:
                await target_client.send_message(chat_id, text)
            except Exception:
                pass
            await asyncio.sleep(delay)

    @target_client.on(
        events.NewMessage(pattern=r"^\.trl2($| .+)", outgoing=True))
    async def trl2_handler(event):
        if state["trl2_running"]:
            state["trl2_running"] = False
            if state["trl2_task"]:
                state["trl2_task"].cancel()
            await event.edit("Остановлено.")
            return

        args = event.raw_text[5:].strip()

        if not args:
            await event.edit("Формат: .trl2 <задержка> [доп текст] <group_id>")
            return

        parts = args.rsplit(" ", 1)
        if len(parts) < 2:
            await event.edit("Формат: .trl2 <задержка> [доп текст] <group_id>")
            return

        try:
            group_id = int(parts[1])
        except ValueError:
            await event.edit("Неверный ID группы!")
            return

        rest = parts[0].split(" ", 1)
        try:
            delay = int(rest[0])
        except ValueError:
            await event.edit("Задержка должна быть числом!")
            return

        prefix = rest[1] if len(rest) > 1 else ""

        if not template:
            await event.edit("Сначала сохрани шаблон через .shablon")
            return

        state["trl2_running"] = True
        await event.edit("Запущено!")
        state["trl2_task"] = asyncio.create_task(trl2_loop(group_id, delay, prefix))

    @target_client.on(
        events.NewMessage(pattern=r"^\.trl3($| .+)", outgoing=True))
    async def trl3_handler(event):
        args = event.raw_text[5:].strip().split()
        load_trl3_state(client_id)
        trl3_state = state["trl3_state"]

        if not args:
            await event.edit("Формат:\n.trl3 (id) [задержка] - добавить\n.trl3 list - список\n.trl3 on/off - вкл/выкл\n.trl3 clear (id) - убрать\n.trl3 clearall - очистить")
            return

        cmd = args[0].lower()

        if cmd == "list":
            if not trl3_state["targets"]:
                await event.edit("Список автоответчика пуст.")
                return
            status = "✅ ВКЛ" if trl3_state["enabled"] else "❌ ВЫКЛ"
            text = f"**Автоответчик:** {status}\n\n"
            for uid, data in trl3_state["targets"].items():
                delay = data.get("delay", 0)
                text += f"• ID: `{uid}` (задержка: {delay}с)\n"
            await event.edit(text)
            return

        if cmd == "on":
            trl3_state["enabled"] = True
            save_trl3_state(client_id)
            await event.edit("✅ Автоответчик включен")
            return

        if cmd == "off":
            trl3_state["enabled"] = False
            save_trl3_state(client_id)
            await event.edit("❌ Автоответчик выключен")
            return

        if cmd == "clear":
            if len(args) < 2:
                await event.edit("Укажи ID: .trl3 clear (id)")
                return
            uid = args[1]
            if uid in trl3_state["targets"]:
                del trl3_state["targets"][uid]
                if uid in state["trl3_last_reply"]:
                    del state["trl3_last_reply"][uid]
                save_trl3_state(client_id)
                await event.edit(f"✅ ID `{uid}` убран из списка")
            else:
                await event.edit(f"ID `{uid}` не найден в списке")
            return

        if cmd == "clearall":
            trl3_state["targets"] = {}
            state["trl3_last_reply"] = {}
            save_trl3_state(client_id)
            await event.edit("✅ Список автоответчика очищен")
            return

        try:
            user_id = int(args[0])
        except ValueError:
            await event.edit("ID должен быть числом!")
            return

        delay = 0
        if len(args) > 1:
            try:
                delay = int(args[1])
            except ValueError:
                await event.edit("Задержка должна быть числом!")
                return

        if not template:
            await event.edit("Сначала сохрани шаблон через .shablon")
            return

        trl3_state["targets"][str(user_id)] = {"delay": delay}
        save_trl3_state(client_id)
        await event.edit(f"✅ Добавлен в автоответчик: `{user_id}` (задержка: {delay}с)")




    @target_client.on(events.NewMessage(incoming=True))
    async def mute_watcher(event):
        # Проверяем, что это личное сообщение (не группа)
        if event.is_private and event.sender_id in muted_users:
            try:
                await event.delete()
            except Exception:
                pass

    @target_client.on(events.NewMessage(incoming=True))
    async def trl3_watcher(event):
        load_trl3_state(client_id)
        trl3_state = state["trl3_state"]

        if not trl3_state["enabled"] or not trl3_state["targets"] or not template:
            return

        sender_id = str(event.sender_id)
        if sender_id not in trl3_state["targets"]:
            return

        target_data = trl3_state["targets"][sender_id]
        delay = target_data.get("delay", 0)

        current_time = time.time()
        last_time = state["trl3_last_reply"].get(sender_id, 0)
        if current_time - last_time < delay:
            return

        line = random.choice(template)
        try:
            await event.reply(line)
            state["trl3_last_reply"][sender_id] = current_time
        except Exception:
            pass

    @target_client.on(events.NewMessage(pattern=r"^\.mute$", outgoing=True))
    async def mute_handler(event):
        global muted_users
        
        reply = await event.get_reply_message()
        
        if reply:
            user_id = reply.sender_id
        else:
            await event.edit("Реплайни на сообщение или укажи ID: .mute (userid)")
            return
        
        if user_id in muted_users:
            muted_users.remove(user_id)
            await event.edit(f"✅ Пользователь `{user_id}` размучен")
        else:
            muted_users.add(user_id)
            await event.edit(f"✅ Пользователь `{user_id}` замучен")

    @target_client.on(events.NewMessage(pattern=r"^\.mute (.+)", outgoing=True))
    async def mute_with_id_handler(event):
        global muted_users
        
        user_id_str = event.pattern_match.group(1).strip()
        
        try:
            user_id = int(user_id_str)
        except ValueError:
            await event.edit("ID должен быть числом!")
            return
        
        if user_id in muted_users:
            muted_users.remove(user_id)
            await event.edit(f"✅ Пользователь `{user_id}` размучен")
        else:
            muted_users.add(user_id)
            await event.edit(f"✅ Пользователь `{user_id}` замучен")



    @target_client.on(events.NewMessage(pattern=r"^\.restart$", outgoing=True))
    async def restart_handler(event):
        await event.edit(
            "⚡ **SqqBot перезагружается**\n\n"
            "🔄 Пожалуйста, подождите...\n\n"
            "💎 Бот вернется через несколько секунд\n\n"
            "📍 Статус: Перезагрузка\n\n"
            "⏰ Время: " + time.strftime('%H:%M:%S')
        )
        
        # Небольшая задержка для визуала
        await asyncio.sleep(1)
        
        # Перезапуск скрипта
        import sys
        import os
        python = sys.executable
        os.execl(python, python, *sys.argv)

    @target_client.on(events.NewMessage(pattern=r"^\.delmenow$",
                                        outgoing=True))
    async def delmenow_handler(event):
        me = await target_client.get_me()
        async for msg in target_client.iter_messages(event.chat_id,
                                                     from_user=me.id):
            try:
                await msg.delete()
            except Exception:
                pass

    async def spam_loop(chat_id, delay, message):
        while state["spam_running"]:
            try:
                await target_client.send_message(chat_id, message)
            except Exception:
                pass
            await asyncio.sleep(delay)

    async def lagger_loop(chat_id, delay):
        text = (
            "\n\n\n\n\n\n\n\n\n\n"
            ".\n"
            "\n\n\n\n\n\n\n\n\n\n"
            ".\n"
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            ".\n"
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            ".\n"
            "\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
            ","
        )
        while state["lagger_running"]:
            try:
                msg = await target_client.send_message(chat_id, text)
                state["lagger_last_msg"][str(chat_id)] = msg.id
                await asyncio.sleep(0.05)
                try:
                    await msg.delete()
                except Exception:
                    pass
            except Exception:
                pass
            await asyncio.sleep(delay)

    @target_client.on(
        events.NewMessage(pattern=r"^\.spam($| .+)", outgoing=True))
    async def spam_handler(event):
        if state["spam_running"]:
            state["spam_running"] = False
            if state["spam_task"]:
                state["spam_task"].cancel()
            await event.edit("Остановлено.")
            return

        args = event.raw_text[5:].strip().split(" ", 1)

        if len(args) < 2:
            await event.edit("Формат: .spam <задержка> <сообщение>")
            return

        try:
            delay = int(args[0])
        except ValueError:
            await event.edit("Задержка должна быть числом!")
            return

        message = args[1]

        state["spam_running"] = True
        await event.edit("Спам запущен!")
        state["spam_task"] = asyncio.create_task(
            spam_loop(event.chat_id, delay, message))

    @target_client.on(events.NewMessage(pattern=r"^\.lagger($| .+)", outgoing=True))
    async def lagger_handler(event):
        if state["lagger_running"]:
            state["lagger_running"] = False
            if state["lagger_task"]:
                state["lagger_task"].cancel()

            try:
                last_id = state.get("lagger_last_msg", {}).get(str(event.chat_id))
                if last_id:
                    try:
                        await target_client.delete_messages(event.chat_id, [last_id])
                    except Exception:
                        pass
            except Exception:
                pass

            await event.edit("✅ Lagger остановлен")
            return

        args = event.raw_text[7:].strip().split()
        if not args:
            await event.edit("Формат: .lagger <задержка_сек>")
            return

        try:
            delay = float(args[0])
            if delay < 0:
                raise ValueError
        except ValueError:
            await event.edit("Задержка должна быть числом (секунды)!")
            return

        state["lagger_running"] = True
        await event.edit(f"✅ Lagger запущен (delay: {delay}s)")
        state["lagger_task"] = asyncio.create_task(lagger_loop(event.chat_id, delay))

    async def trl4_loop(chat_id, delay, user_id, user_entity):
        while state["trl4_running"]:
            if not template:
                break
            line = random.choice(template)
            try:
                if user_entity.username:
                    mention = f"@{user_entity.username}"
                    text = f"{mention} {line}"
                    await target_client.send_message(chat_id, text)
                else:
                    first_name = user_entity.first_name or "User"
                    mention = f"[{first_name}](tg://user?id={user_id})"
                    text = f"{mention} {line}"
                    await target_client.send_message(chat_id, text, parse_mode='md')
            except Exception as e:
                print(f"trl4 error: {e}")
            await asyncio.sleep(delay)

    @target_client.on(
        events.NewMessage(pattern=r"^\.trl4($| .+)", outgoing=True))
    async def trl4_handler(event):
        if state["trl4_running"]:
            state["trl4_running"] = False
            if state["trl4_task"]:
                state["trl4_task"].cancel()
            await event.edit("Остановлено.")
            return

        args = event.raw_text[5:].strip().split()

        if len(args) < 2:
            await event.edit("Формат: .trl4 <задержка> <id юзера>")
            return

        try:
            delay = int(args[0])
        except ValueError:
            await event.edit("Задержка должна быть числом!")
            return

        try:
            user_id = int(args[1])
        except ValueError:
            await event.edit("ID должен быть числом!")
            return

        if not template:
            await event.edit("Сначала сохрани шаблон через .shablon")
            return

        try:
            user_entity = await target_client.get_entity(user_id)
        except Exception as e:
            await event.edit(f"Не удалось найти юзера: {e}")
            return

        state["trl4_running"] = True
        await event.edit("Запущено!")
        state["trl4_task"] = asyncio.create_task(
            trl4_loop(event.chat_id, delay, user_id, user_entity))

    async def trl5_loop(chat_id, delay, user_id, user_entity, media):
        while state["trl5_running"]:
            try:
                if not template:
                    break
                line = random.choice(template)
                
                if user_entity.username:
                    mention = f"@{user_entity.username}"
                    caption = f"{mention} {line}"
                else:
                    first_name = user_entity.first_name or "User"
                    mention = f"[{first_name}](tg://user?id={user_id})"
                    caption = f"{mention} {line}"
                
                await target_client.send_file(
                    chat_id, 
                    media,
                    caption=caption,
                    parse_mode='md'
                )
            except Exception as e:
                print(f"trl5 error: {e}")
            await asyncio.sleep(delay)







    @target_client.on(
        events.NewMessage(pattern=r"^\.trl5($| .+)", outgoing=True))
    async def trl5_handler(event):
        if state["trl5_running"]:
            state["trl5_running"] = False
            if state["trl5_task"]:
                state["trl5_task"].cancel()
            await event.edit("Остановлено.")
            return

        if not event.media:
            await event.edit("Кидай фотку/видео с командой в подписи!")
            return

        args = event.raw_text[5:].strip().split()

        if len(args) < 2:
            await event.edit("Формат: .trl5 <id юзера> <задержка>")
            return

        try:
            user_id = int(args[0])
        except ValueError:
            await event.edit("ID должен быть числом!")
            return

        try:
            delay = int(args[1])
        except ValueError:
            await event.edit("Задержка должна быть числом!")
            return

        if not template:
            await event.edit("Сначала сохрани шаблон через .shablon")
            return

        try:
            user_entity = await target_client.get_entity(user_id)
        except Exception as e:
            await event.edit(f"Не удалось найти юзера: {e}")
            return

        state["trl5_running"] = True
        await event.edit("Запущено!")
        state["trl5_task"] = asyncio.create_task(
            trl5_loop(event.chat_id, delay, user_id, user_entity, event.media))


register_handlers(client, "main")


async def start_saved_sessions():
    global session_clients
    load_sessions()

    for phone, data in sessions.items():
        if not data.get("active"):
            continue

        session_name = data.get("session_name")
        if not session_name:
            continue

        session_file = f"{session_name}.session"
        if not os.path.exists(session_file):
            continue

        try:
            session_client = TelegramClient(session_name, int(API_ID),
                                            API_HASH)

            await session_client.connect()

            if await session_client.is_user_authorized():
                register_handlers(session_client, phone)
                session_clients[phone] = session_client
                me = await session_client.get_me()
                print(
                    f"Session started: {me.first_name} (@{me.username}) - {phone}"
                )
            else:
                await session_client.disconnect()
                print(f"Session {phone} is not authorized, skipping")

        except Exception as e:
            print(f"Failed to start session {phone}: {e}")


async def main():
    global start_time
    print("Starting Telegram Userbot...")
    load_sessions()
    await client.start()
    start_time = time.time()
    me = await client.get_me()
    print(f"Logged in as: {me.first_name} (@{me.username})")
    
    await start_saved_sessions()

    print("Userbot is running!")
    print("type .info for commands")
    
    # Отправляем сообщение о перезагрузке если это был рестарт
    try:
        await client.send_message(
            "me",
            "⚡ **SqqBot успешно перезагружен!**\n\n"
            "💎 Бот снова готов к работе\n"
            "🔹 Все команды доступны\n"
            "🕐 Время запуска: " + time.strftime('%H:%M:%S')
        )
    except Exception:
        pass
        
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
