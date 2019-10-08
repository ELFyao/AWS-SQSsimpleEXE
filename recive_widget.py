from tkinter import *
from PIL import Image, ImageTk
from datetime import datetime
import logging
import boto3
from botocore.exceptions import ClientError
from tkinter.messagebox import *

def retrieve_sqs_messages(sqs_queue_url, num_msgs=1, wait_time=0, visibility_time=5):
    """Retrieve messages from an SQS queue
    The retrieved messages are not deleted from the queue.
    :param sqs_queue_url: String URL of existing SQS queue
    :param num_msgs: Number of messages to retrieve (1-10)
    :param wait_time: Number of seconds to wait if no messages in queue
    :param visibility_time: Number of seconds to make retrieved messages
        hidden from subsequent retrieval requests
    :return: List of retrieved messages. If no messages are available, returned
        list is empty. If error, returns None.
    """
    # Validate number of messages to retrieve
    if num_msgs < 1:
        num_msgs = 1
    elif num_msgs > 10:
        num_msgs = 10
    # Retrieve messages from an SQS queue
    sqs_client = boto3.client('sqs', region_name='us-east-1')
    try:
        msgs = sqs_client.receive_message(QueueUrl=sqs_queue_url,
                                          MaxNumberOfMessages=num_msgs,
                                          WaitTimeSeconds=wait_time,
                                          VisibilityTimeout=visibility_time)
    except ClientError as e:
        logging.error(e)
        return None
    # Return the list of retrieved messages----------------------a list need to print *
    try:
        return msgs['Messages']
    except KeyError as e:
        logging.error(e)
        return None
def delete_sqs_message(sqs_queue_url, msg_receipt_handle):
    """Delete a message from an SQS queue
    :param sqs_queue_url: String URL of existing SQS queue
    :param msg_receipt_handle: Receipt handle value of retrieved message
    """

    # Delete the message from the SQS queue
    sqs_client = boto3.client('sqs', region_name='us-east-1')
    sqs_client.delete_message(QueueUrl=sqs_queue_url,
                              ReceiptHandle=msg_receipt_handle)
class login():
    def __init__(self):
        self.window = Tk()
        self.window.minsize(width=450, height=500)
        self.window.title("RECIVE_MESSAGE_FROM_AWS")
        image = Image.open('暴雪.png')
        img = ImageTk.PhotoImage(image)
        self.canvas1 = Canvas(self.window, width=image.width , height=image.height , bg='white')
        self.canvas1.create_image(0, 0, image=img, anchor="nw")
        self.canvas1.create_image(image.width, 0, image=img, anchor="nw")
        self.canvas1.pack()
        self.L1 = Label(self.window, text="message_log")
        self.L1.pack()
        self.T1 = Text(self.window, width=60, height=20)
        self.T1.pack(side=LEFT, fill=Y)
        self.scoll = Scrollbar()
        self.scoll.pack(side=RIGHT, fill=Y)
        self.scoll.config(command=self.T1.yview)
        self.T1.config(yscrollcommand=self.scoll.set)
        self.T1.config(state=DISABLED)
        self.loginin = Button(width=5, height=1, text="recive", activebackground="red", relief=FLAT,
                              command=self.recive_msg)
        self.loginin.pack(side=BOTTOM)
        self.window.mainloop()
    def recive_msg(self):
        sqs_queue_url = 'https://sqs.us-east-1.amazonaws.com/818531462855/TESTQueue'
        num_messages = 2

        # Set up logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(levelname)s: %(asctime)s: %(message)s')
        # Retrieve SQS messages
        msgs = retrieve_sqs_messages(sqs_queue_url, num_messages)
        if msgs is not None:
            for msg in msgs:
                print(msgs)
                logging.info(f'SQS: Message ID: {msg["MessageId"]}, '
                             f'Contents: {msg["Body"]}')
                self.T1.config(state=NORMAL)
                dt = datetime.now()
                self.T1.insert(INSERT, str(dt) + '\n')
                self.T1.insert(INSERT, 'recive:  ' + '\n')
                self.T1.insert(INSERT, 'SQS: Message ID:  '+msg["MessageId"]+'\n')
                self.T1.insert(INSERT, 'SQS: Message :  ' + msg["Body"] + '\n\n')
                self.T1.config(state=DISABLED)
            for msg in msgs:
                print(msg)
                # Remove the message from the queue
                delete_sqs_message(sqs_queue_url, msg['ReceiptHandle'])
        else:
            showinfo(title='tips', message='no message')
















login=login()


