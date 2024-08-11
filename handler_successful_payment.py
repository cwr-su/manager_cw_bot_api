"""Module of the control successful payments."""
from aiogram import types, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.handler_db_sub_operations import HandlerDB


class HandlerSP:
    """Class-handler for successful payments."""
    @staticmethod
    async def add_new_record(
            bot: Bot,
            message: types.Message | types.CallbackQuery,
            admin_id: int,
            mode="TGStar",
            yookassa_ref_token="yookassa"
    ) -> None:
        """
        Add a new record in database.

        :param bot: The object of Telegram Bot.
        :param message: Message of the successful payment by Stars.
        :param admin_id: Telegram Admin ID.
        :param mode: Mode of process successful payment.
        :param yookassa_ref_token: Yookassa refund-token.

        :return: bool.
        """
        var: InlineKeyboardBuilder = await Buttons.back_on_main()
        try:
            if mode == "TGStar":
                ref_token: str = message.successful_payment.telegram_payment_charge_id
            else:
                ref_token: str = yookassa_ref_token

            msg: types.Message = await bot.send_message(
                chat_id=message.from_user.id,
                text=f"💖 Thanks! I received the payment!\n\n🔐 Token for refund stars / money: "
                     f"<code>{ref_token}</code>\n\nPlease, wait! I'm activating "
                     f"your subscription...⏳",
                message_effect_id="5046509860389126442",
                parse_mode="HTML"
            )
            result: tuple = await HandlerDB.insert_new_record_for_subscribe(
                message=message,
                days=30,
                token_successful_payment=ref_token,
            )
            res: bool = result[0]
            des: str = result[1]

            if res is True:
                await HandlerDB.yookassa_delete_record_conf_id(message.from_user.id)
                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    text=f"✅ <b>Successful! Done!</b>\nYour PLUS is <b>activated</b>!\n\nNow you can:\n"
                         f"- Use 💥 AI-Generate IMG 🖼\n"
                         f"- 🧠 Use AI-Assistance (👑 PRO-Mode)\n"
                         f"- and more ⚡, only MORE ✨!\n\n"
                         f"🔐 Your refund token:\n<code>{ref_token}</code>.",
                    message_id=msg.message_id,
                    parse_mode="HTML",
                    reply_markup=var.as_markup()
                )
                await bot.send_message(
                    chat_id=admin_id,
                    text=f"🆕 Admin, PLUS +1 person! 🔥",
                    reply_markup=var.as_markup()
                )

            else:
                await bot.edit_message_text(
                    chat_id=message.from_user.id,
                    text=f"❌ <b>Failed!</b>\nYour PLUS <b>isn't activated</b>!\n\nNow you should:\n"
                         f"- write on EMail: help@cwr.su\n\n"
                         f"🔐 Your refund token:\n<code>{ref_token}</code>.",
                    message_id=msg.message_id,
                    parse_mode="HTML"
                )

                if des == "error":
                    await bot.refund_star_payment(
                        user_id=message.from_user.id,
                        telegram_payment_charge_id=ref_token
                    )

                    await bot.edit_message_text(
                        chat_id=message.from_user.id,
                        text=f"✨ <b>{message.from_user.first_name}</b>, you already have a PLUS subscription. "
                             f"💞 We have <b>returned</b> the stars back to your account.",
                        message_id=msg.message_id,
                        reply_markup=var.as_markup(),
                        parse_mode="HTML"
                    )
        except Exception as ex:
            await bot.send_message(
                chat_id=admin_id,
                text=f"❕ Admin, we have a problem with successful payment! Error (exception): {ex}.",
                reply_markup=var.as_markup()
            )
