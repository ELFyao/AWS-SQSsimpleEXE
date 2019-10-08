from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
from boto3 import *
from boto3 import Session
from botocore.exceptions import ClientError
import logging
sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/818531462855/TESTQueue'
def send_sqs_message(sqs_queue_url, msg_body):
    sqs_client = client('sqs', region_name='us-east-1')
    try:
        msg = sqs_client.send_message(QueueUrl=sqs_queue_url,
                                      MessageBody=msg_body)
    except ClientError as e:
        logging.error(e)
        return None
    return msg

class login():
    def __init__(self):
        self.window = Tk()
        self.window.minsize(width=450, height=500)
        self.window.title("SEND_MESSAGE_TO_AWS")
        image = Image.open('暴雪.png')
        img = ImageTk.PhotoImage(image)
        self.canvas1 = Canvas(self.window, width=image.width , height=image.height , bg='white')
        self.canvas1.create_image(0, 0, image=img, anchor="nw")
        self.canvas1.create_image(image.width, 0, image=img, anchor="nw")
        self.canvas1.pack()

        self.L2 = Label(self.window, text="send_message")
        self.L2.pack()
        self.T2 = Text(self.window, width=60, height=5, bd=0, relief=FLAT)
        self.T2.pack()
        self.loginin = Button(width=5, height=1, text="send", activebackground="red", relief=FLAT,
                              command=lambda: self.indicate(self.send()))
        self.loginin.pack()

        self.L1 = Label(self.window, text="message_log")
        self.L1.pack()
        self.T1 = Text(self.window,width=60,height=20)
        self.T1.pack(side=LEFT,fill=Y)
        self.scoll = Scrollbar()
        self.scoll.pack(side=RIGHT,fill=Y)
        self.scoll.config(command=self.T1.yview)
        self.T1.config(yscrollcommand=self.scoll.set)
        self.T1.config(state=DISABLED)
        self.window.mainloop()
    def send(self):
        msg = self.T2.get('1.0', END)
        self.T2.delete('1.0', END)
        return msg
    def indicate(self,text):
        if text == "\n":
            pass
        else:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(levelname)s: %(asctime)s: %(message)s')
            msg = send_sqs_message(sqs_queue_url, text)
            if msg is not None:
                logging.info(f'Sent SQS message ID: {msg["MessageId"]}')
                self.T1.config(state=NORMAL)
                dt = datetime.now()
                self.T1.insert(INSERT, str(dt)+'\n')
                self.T1.insert(INSERT, 'send:  '+text + '\n')
                self.T1.config(state=DISABLED)

login=login()

