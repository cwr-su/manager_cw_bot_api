"""Module for generate PDF-system documents."""
import datetime
from fpdf import FPDF, FontFace


class GenerateTicketDataUniversal:
    """Class for generate ticket-data for any users."""

    @staticmethod
    async def generate(name: str, text_data: str) -> str:
        """
        Generate ticket-data.

        :param name: Name.
        :param text_data: Ticket Data (big-format).

        :return: Title of file.
        """
        pdf = FPDF()

        pdf.add_font("DinCWFont_TTF", "", "./styles/DIN2014-Regular.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "I", "./styles/DIN2014-Italic.ttf", uni=True)
        pdf.add_font("DinCWFont_TTF", "B", "./styles/DIN2014-Bold.ttf", uni=True)
        pdf.set_font("DinCWFont_TTF", "", 13)

        pdf.add_page()

        time = (datetime.datetime.
                now(datetime.timezone(datetime.timedelta(hours=3))).
                strftime('%d.%m.%Y | %H:%M:%S'))

        pdf.write_html("""
        <section>
        <table width="100%">
          <thead>
            <tr>
              <th width="40%" align='left'><a href='https://cwr.su/'><img 
              src='./styles/logo_email.png'></a></th>
              <th width="60%" align='right'>
                <h5>CODEWRITER COMPANY\nSELF-EMPLOYED LAPTEV ALEXANDER A.\nTEL.: +7 995 024-61-04, CWR.SU</h5>
              </th>
            </tr>
          </thead>
        </table>
        </section>
          <font size="22"><p align='left'>Ticket Data from Manager CW Bot's Ticket System<br>
          Данные из Тикет Системы Manager CW бота</p></font>
          <p><b>""" + name + """</b>, below you can see your TicketData, which you have 
          requested in the <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.<br><br>
          The date and time when the document was generated (Moscow time | MSK UTC+3): 
          """ + time + """.</p>
          <p>\uf000</p>
          <table width="100%">
            <thead>
              <tr>
                <th width="20%">ID | Идентификатор</th>
                <th width="30%">Sender | Отправитель</th>
                <th width="25%">Subject* | Тема</th>
                <th width="25%">Created | Дата/Время создания</th>
              </tr>
            </thead>
            <tbody>
              """ + text_data + """
            </tbody>
          </table>
          <p>*"Subject" (the word) in this case refers to the first 25 characters of the letter. 
          To view the entire email / ticket, go to <a href='https://t.me/helper_cwBot'>Manager CW Bot</a>.<br>
          This document does not provide for the display of emojis or other other symbols.</p>

          <p>Your data is <b>always safe</b>!<br>
          If you have not requested this type of document, please contact technical support by writing to the 
          email listed below.</p>
          <p><b>Important!</b> Using CW services (CWR.SU ) - you accept all the rules and the agreement written on 
          the website <a href='https://acdn.cwr.su/'><b>acdn.cwr.su</b></a> in the corresponding section 
          on the main page.<br>
          <i>If</i> you <i>don't agree with them (agreement / rules)</i>, 
          <i>destroy this document</i>.</p>
        """, tag_styles={
            "a": FontFace(color="#390085"),
            "h5": FontFace(color="#424242", size_pt=17)
        })

        pdf.add_page()

        pdf.write_html("""
        <p><i>Sincerely, the CW team.
          <br><br>
          If you have any questions about purchasing a product, please contact: 
          <a href='mailto:b2b@cwr.su'>b2b@cwr.su</a>.
          <br>
          On cooperation issues: <a href='mailto:cwr@cwr.su'>cwr@cwr.su</a>.
          <br>
          For technical issues and problems: <a href='mailto:help@cwr.su'>help@cwr.su</a>.</i>
          <br>
          <br></p>
          <p>Director and developer, creator, designer of the CW product: Laptev Alexander A.</p>
          <br>
          <center><img src="./styles/stamp.png" width=100 height=100></center>
          <p><i>*This document is valid due to the stamp at the end of the contents of this document.</i></p>
          <p align='center'>© CW | All rights reserved | 2023 - 2024.</p>
        """, tag_styles={
            "a": FontFace(color="#390085")
        })

        file_path: str = "ticket_data_from_manager_cw_bot.pdf"
        pdf.output(file_path)

        return file_path
