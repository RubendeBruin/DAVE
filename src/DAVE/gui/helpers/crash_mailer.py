import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from DAVE.gui.helpers.gui_logger import DAVE_GUI_LOGGER


def create_draft_with_attachment(filename, subject, body, to, file_path):
    msg = MIMEMultipart()
    # msg['From'] = 'your-email@example.com'
    msg['To'] = to
    msg['Subject'] = subject
    msg['X-Unsent'] = '1'

    msg.attach(MIMEText(body, 'plain'))

    with open(file_path, "rb") as attachment_file:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment_file.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= "+os.path.basename(file_path))
        msg.attach(part)

    with open(filename, 'w') as draft_file:
        draft_file.write(msg.as_string())

    os.startfile(filename)

# Example: create_draft_with_attachment("Subject", "Body", "receiver-email@example.com", "c:/data/test.dave")


def compile_and_mail(info = None):
    """Compiles the log and sends it to the DAVE developers"""

    # get the temp directory
    from DAVE.settings import PATH_TEMP

    # save the log
    log_path = PATH_TEMP / "DAVEgui_log.txt"
    with open(log_path, "w") as log_file:
        log_file.write(DAVE_GUI_LOGGER.get_log())

    # create the draft
    to = "bugreports@rdbr.nl"
    body = """    
Dear DAVE developers,

I have encountered a problem with DAVE. I have attached the log file to this email.
The log-file contains information about the problem and the actions I took before the problem occurred.
It also contains the Python code that was executed in the GUI and the model in its current state.

""" + ("\nThe error is:\n\n-------------------------\n\n" + info + "\n\n----------------------------\n" if info is not None else "") + """
[X] Please treat this confidentially.
[ ] Contact me if you have any questions.
[ ] Contact me when the problem is fixed.

Some information about what I was doing when the problem occurred:

"I tried to dissolve a crane" <-- replace this with your own description if relevant

    """


    email_filename = PATH_TEMP / "DAVE_crash_report.eml"
    create_draft_with_attachment(email_filename,
                                 "DAVE crash report",
                                 body = body,
                                 to = to,
                                 file_path = log_path)






