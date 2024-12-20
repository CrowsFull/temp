import logging
from http import HTTPStatus
from typing import List

import aiohttp
from telegram import Bot

from bot.handlers.consts.consts import BASE_PARSE_MODE
from config.api import api_config
from config.config import BASE_CHEQUE_CHAT_ID, BASE_CHEQUE_THREAD_ID, BASE_TRONSCAN_TRANSACTION_LINK
from kafka.utils.enums import Status


async def send_status_message(bot: Bot, payload: dict) -> bool:
    status = payload.get("status")
    payment_id = payload.get("paymentId")

    if status == Status.COMPLETED:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{api_config.api_url}/export/payments/byid/{payment_id}"
                async with session.get(url, headers=api_config.api_headers) as response:

                    if response.status == HTTPStatus.OK:
                        result: dict = await response.json()

                        payment = result.get("payment")
                        payment_amount: float = int(payment.get("amount")) / 100
                        transfer_hash = payment.get("transferHash")

                        project = result.get("projects")[0]  # todo: check

                        project_name = project.get("name")
                        partner_id = project.get("partnerId")

                        # QUERY TO FIND CHAT

                        # todo: get partner info
                        partner_chat_id = BASE_CHEQUE_CHAT_ID
                        thread_id = BASE_CHEQUE_THREAD_ID

                        link = f"{BASE_TRONSCAN_TRANSACTION_LINK}{transfer_hash}" if transfer_hash is not None else '-'

                        await bot.send_message(
                            chat_id=partner_chat_id,
                            message_thread_id=thread_id,
                            text="<b>Cheque information</b>🧾\n\n"
                                 f"<b>Project</b>: {project_name}\n"
                                 f"<b>Amount</b>: {f'{payment_amount:,}'} $\n"
                                 f"<b>Link</b>:\n{link}",
                            parse_mode=BASE_PARSE_MODE
                        )
                    else:
                        logging.error(f"{response.status}: ERROR")
                        return False
        except Exception as e:
            logging.error(e)
            return False

    return True
