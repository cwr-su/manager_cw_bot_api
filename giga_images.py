import os
from io import BytesIO

from PIL import Image
from aiogram import types, Bot, Router, F
from aiogram.types.input_file import FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from manager_cw_bot_api.buttons import Buttons
from manager_cw_bot_api.giga_request import create
from manager_cw_bot_api.fsm_handler import GigaImage

router_ai_img: Router = Router()


class GigaCreator:
    """Class of create image for plus-user."""
    __query: str = ""

    def __init__(self, bot: Bot) -> None:
        self.__bot: Bot = bot

        router_ai_img.message.register(
            self.__check_generate_or_cancel,
            GigaImage.request
        )

    async def get_query(self, call: types.CallbackQuery, state: FSMContext) -> None:
        """
        Func of get query from plus-user for create image.

        :param call: Callback Query.
        :param state: FSM.

        :return: None.
        """
        await state.set_state(GigaImage.request)
        await self.__bot.edit_message_text(
            chat_id=call.message.chat.id,
            text="📸 Enter your query...",
            message_id=call.message.message_id
        )

    async def __check_generate_or_cancel(self, message: types.Message, state: FSMContext) -> None:
        """
        Check generation.

        :param message: Query from user.
        :param state: FSM.

        :return: None
        """
        var: InlineKeyboardBuilder = await Buttons.generate_image()
        self.__class__.__query = message.text
        await self.__bot.send_message(
            chat_id=message.chat.id,
            text=f"{message.from_user.first_name}, are you want to *generate image*? Are you sure?",
            reply_markup=var.as_markup(),
            parse_mode="Markdown"
        )
        router_ai_img.callback_query.register(
            self.__handler_query,
            F.data == "generate"
        )

    async def __handler_query(self, call: types.CallbackQuery) -> None:
        """
        Manage of query from plus-user for create image.

        :param call: Call-Query.
        :return: None.
        """
        query: str = self.__class__.__query

        try:
            await self.__bot.edit_message_text(
                chat_id=call.from_user.id,
                text="💫 Please, wait! I'm generating... ⏳",
                message_id=call.message.message_id
            )
        except Exception:
            await self.__bot.send_message(
                chat_id=call.from_user.id,
                text="💫 Please, wait! I'm generating... ⏳",
            )

        image_data: bytes | str = await create(query)
        try:
            if image_data == "👌🏻 Sorry! I updated the data. Please, repeat your request :)":
                var: InlineKeyboardBuilder = await Buttons.back_on_main()
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=image_data,
                    message_id=call.message.message_id,
                    reply_markup=var.as_markup()
                )
            else:
                image: Image = Image.open(BytesIO(image_data))
                temp_image: str = 'AI_Photo_Generate_By_Kandinsky_Manager_PLUS_Version.jpg'
                image.save(temp_image, 'JPEG')

                await self.__bot.send_document(
                    chat_id=call.from_user.id,
                    document=FSInputFile(temp_image),
                    caption=f"<b>{call.from_user.first_name}</b>, the new photo has been generated according to your "
                            f"request: <blockquote>{self.__class__.__query}</blockquote>\n\n"
                            f"✨ There are still generations left: ♾.\n\nThe photo is attached to the message as a "
                            f"file. Download it by clicking on the button above.\n\n"
                            f"#AI_Photo\nDeveloper: @aleksandr_twitt.",
                    parse_mode="HTML",
                    message_effect_id='5104841245755180586'
                )

                os.remove(temp_image)

                var: InlineKeyboardBuilder = await Buttons.back_on_main()
                await self.__bot.send_message(
                    chat_id=call.from_user.id,
                    text="Return to main-menu:",
                    reply_markup=var.as_markup()
                )

                await self.__bot.delete_message(
                    chat_id=call.from_user.id,
                    message_id=call.message.message_id
                )

        except Exception as ex:
            print(ex)
            var: InlineKeyboardBuilder = await Buttons.back_on_main()
            if "cannot identify image file" in str(ex) or "bytes-like object is required, not 'str'" in str(ex):
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text=image_data,
                    reply_markup=var.as_markup(),
                    message_id=call.message.message_id
                )
            else:
                await self.__bot.edit_message_text(
                    chat_id=call.from_user.id,
                    text="🤔 Oh, something wrong! 👌🏻 Please, don't worry! Write ticket or EMail: help@cwr.su.",
                    reply_markup=var.as_markup(),
                    message_id=call.message.message_id
                )
