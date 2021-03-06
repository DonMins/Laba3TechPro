import tkinter
import messagess
from tkinter import messagebox, simpledialog
import random
import json
import threading
import modell

CLOSING_PROTOCOL = "WM_DELETE_WINDOW"
END_OF_LINE = "\n"
KEY_RETURN = "<Return>"
TEXT_STATE_DISABLED = "disabled"
TEXT_STATE_NORMAL = "normal"


class EzChatUI(object):
    def __init__(self, application):
        self.application = application
        self.gui = None
        self.frame = None
        self.input_field = None
        self.message = None
        self.message_list = None
        self.scrollbar = None
        self.send_button = None
        self.first_button = None
        self.second_button = None
        self.third_button = None
        self.forth_button = None
        self.exit_button = None
        self.repeat_button = None

        self.text = [random.randint(-4, -1) for i in range(4)]

        self.isButton1 = False
        self.isButton2 = False
        self.isButton3 = False
        self.isButton4 = False
        self.sign = [0,0,0,0]

    def show(self):
        self.gui = tkinter.Tk()  # создали класс для пользования библиотекой
        return self.input_dialogs()  # сообщения выводимые - по поводу сервака, порта и имени

    def loop(self):
        self.gui.mainloop()  # без неё не создается окно

    def setButton(self):
        self.first_button = tkinter.Button(self.gui, text=str(self.text[0]), command=self.application.send,
                                           bg="#E2DF69", width=10)

        self.first_button.pack(side=tkinter.RIGHT, padx=10, pady=10)  # размещение кнопки на платформе
        self.first_button.bind("<Button-1>", self.change1)

        self.second_button = tkinter.Button(self.gui, text=str(self.text[1]), command=self.application.send,
                                            bg="#E2DF69", width=10)
        self.second_button.pack(side=tkinter.RIGHT, padx=10, pady=10)  # размещение кнопки на платформе
        self.second_button.bind("<Button-1>", self.change2)

        self.third_button = tkinter.Button(self.gui, text=str(self.text[2]), command=self.application.send,
                                           bg="#E2DF69", width=10)
        self.third_button.pack(side=tkinter.RIGHT, padx=10, pady=10)  # размещение кнопки на платформе
        self.third_button.bind("<Button-1>", self.change3)

        self.forth_button = tkinter.Button(self.gui, text=str(self.text[3]), command=self.application.send,
                                           bg="#E2DF69", width=10)

        self.forth_button.pack(side=tkinter.RIGHT, padx=10, pady=10)  # размещение кнопки на платформе
        self.forth_button.bind("<Button-1>", self.change4)

        self.exit_button = tkinter.Button(self.gui, text=str("ВЫХОД"), command=self.on_closing,
                                          bg="#E2DF69", width=10)

        self.exit_button.pack(side=tkinter.LEFT, padx=10, pady=10)  # размещение кнопки на платформе
        self.exit_button.bind("<Button-1>")

        self.repeat_button = tkinter.Button(self.gui, text=str("ПОВТОР"), command=self.repeat,
                                            bg="#E2DF69", width=10)

        self.repeat_button.pack(side=tkinter.LEFT, padx=10, pady=10)  # размещение кнопки на платформе
        self.repeat_button.bind("<Button-1>")
        self.repeat_button.pack_forget()


    def fill_frame(self):

        self.frame = tkinter.Frame(self.gui, highlightbackground="black", highlightcolor="green", highlightthickness=2,
                                   width=100, height=100, bd=1)  # предназначен для организации виджетов внутри окна

        self.scrollbar = tkinter.Scrollbar(self.frame)
        self.message_list = tkinter.Text(self.frame, state=TEXT_STATE_DISABLED, width=100,
                                         height=20,
                                         bg="#D7EADC")  # позволяет пользователю ввести любое количество текста

        self.scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)  # прокрутить - правая сторона
        self.message_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.message = tkinter.StringVar()
        self.frame.pack()
        self.setButton()

    def change4(event, self):
        event.isButton4 = True
        event.message.set(str(event.text[3]))

    def change3(event, self):
        event.isButton3 = True
        event.message.set(str(event.text[2]))

    def change2(event, self):
        event.isButton2 = True
        event.message.set(str(event.text[1]))

    def change1(event, self):
        event.isButton1 = True
        event.message.set(str(event.text[0]))

    def updateButton(event):
        if (event.isButton1):
            event.text[0] = random.randint(-4, -1)
            event.first_button['text'] = event.text[0]
        if (event.isButton2):
            event.text[1] = random.randint(-4, -1)
            event.second_button['text'] = event.text[1]
        if (event.isButton3):
            event.text[2] = random.randint(-4, -1)
            event.third_button['text'] = event.text[2]
        if (event.isButton4):
            event.text[3] = random.randint(-4, -1)
            event.forth_button['text'] = event.text[3]


    def hill(self):
            self.isButton4 = False
            self.isButton3 = False
            self.isButton2 = False
            self.isButton1 = False

    def input_dialogs(self):  # simpledialog.askstring - импортированное окошка позволяющее ввести одну строку
        self.gui.lower()  # размещает поверх всех других окон
        self.application.username = simpledialog.askstring(messagess.USERNAME, messagess.INPUT_USERNAME,
                                                           parent=self.gui)
        if self.application.username is None:
            return False

        self.gui.title(messagess.TITLE + self.application.username)  # заголовок
        self.fill_frame()  # наполняем наше окно

        self.show_message(" У каждого игрока по 10 карт в колоде и 4 в руке ")
        if(self.application.countClients==1):
            self.forth_button['state'] = TEXT_STATE_DISABLED
            self.third_button['state'] = TEXT_STATE_DISABLED
            self.second_button['state'] =TEXT_STATE_DISABLED
            self.first_button['state'] = TEXT_STATE_DISABLED
        self.gui.protocol(CLOSING_PROTOCOL,
                          self.on_closing)  # получает два аргумента: название события и функцию, которая будет вызываться при наступлении указанного события
        return True

    def alert(self, title, message):  # выводим сообщения в табличке...
        messagebox.showerror(title, message)

    def whatToBlock(self,sign):
        number=0
        for i in range(4):  # посчитали сколько заблоченно
            if(sign[i]==1):
                number+=1
        return number

    def show_message(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)  # вывод сообщения
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)  # добавить текст в конец сообщения

        self.message_list.configure(state=TEXT_STATE_DISABLED)  # вывод сообщения

        # взяте карт из колоды и update кнопок

        self.application.cardRival = self.application.cardRival-1

        coontOut = abs(self.application.getCountOut())
        if (self.application.allCard > 4):
            for i in range(coontOut):
                self.text[i] = random.randint(-4, -1)

        self.forth_button['text'] = str(self.text[3])
        self.third_button['text'] = str(self.text[2])
        self.second_button['text'] = str(self.text[1])
        self.first_button['text'] = str(self.text[0])

        self.forth_button['state'] = TEXT_STATE_NORMAL
        self.third_button['state'] = TEXT_STATE_NORMAL
        self.second_button['state'] = TEXT_STATE_NORMAL
        self.first_button['state'] = TEXT_STATE_NORMAL



        if(self.application.allCard < 4):
            if(self.isButton4==True ):
                self.forth_button['state'] = TEXT_STATE_DISABLED
                self.sign[3]=1
            if (self.isButton3 == True ):
                self.third_button['state'] = TEXT_STATE_DISABLED
                self.sign[2] = 1
            if (self.isButton2 == True ):
                self.second_button['state'] = TEXT_STATE_DISABLED
                self.sign[1] = 1
            if (self.isButton1 == True ):
                self.first_button['state'] = TEXT_STATE_DISABLED
                self.sign[0] = 1

            print("we are here",self.application.allCard )

            howMany = abs(self.application.allCard - self.whatToBlock(self.sign))


            if(howMany==1):
                r=2-howMany
            else: r=4-howMany

            for i in range(r):
                for j in range(4):
                    if (self.sign[j] == 0):
                        if (j == 0):
                            self.first_button['state'] = TEXT_STATE_DISABLED
                            self.sign[0] = 1
                        else:
                            if (j == 1):
                                self.second_button['state'] = TEXT_STATE_DISABLED
                                self.sign[1] = 1
                            else:
                                if (j == 2):
                                    self.third_button['state'] = TEXT_STATE_DISABLED
                                    self.sign[2] = 1
                                else:
                                    if (j == 3):
                                        self.forth_button['state'] = TEXT_STATE_DISABLED
                                        self.sign[3] = 1
                                    break
                                break
                            break
                        break



        if (self.application.loser == True):
            self.application.loser = False
            self.forth_button['state'] = TEXT_STATE_DISABLED
            self.third_button['state'] = TEXT_STATE_DISABLED
            self.second_button['state'] = TEXT_STATE_DISABLED
            self.first_button['state'] = TEXT_STATE_DISABLED
            self.againCheck()
        if(self.application.countClients==1):
            self.forth_button['state'] = TEXT_STATE_DISABLED
            self.third_button['state'] = TEXT_STATE_DISABLED
            self.second_button['state'] = TEXT_STATE_DISABLED
            self.first_button['state'] = TEXT_STATE_DISABLED

    def againCheck(self):
        self.repeat_button.pack(side=tkinter.LEFT, padx=10, pady=10)  # размещение кнопки на платформе

    def repeat(self):
        self.application.cardRival = 14
        self.application.allCard = 14
        self.application.countOut = 0
        self.forth_button['state'] = TEXT_STATE_NORMAL
        self.third_button['state'] = TEXT_STATE_NORMAL
        self.second_button['state'] = TEXT_STATE_NORMAL
        self.first_button['state'] = TEXT_STATE_NORMAL
        self.show_message(" У каждого игрока по 10 карт в колоде и 4 в руке ")
        self.application.winner = False
        self.application.again = False
        self.application.loser = False
        self.application.receive_worker = threading.Thread(target=self.application.receive)
        self.application.receive_worker.start()
        self.repeat_button.pack_forget()
        self.isButton1 = False
        self.isButton2 = False
        self.isButton3 = False
        self.isButton4 = False
        self.sign = [0, 0, 0, 0]

    def show_message_final(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)  # вывод сообщения
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)  # добавить текст в конец сообщения
        self.message_list.configure(state=TEXT_STATE_DISABLED)  # вывод сообщения
        if (self.application.winner == True):
            self.application.winner = False
            self.againCheck()

    def show_message_final2(self, message):
        self.message_list.configure(state=TEXT_STATE_NORMAL)  # вывод сообщения
        self.message_list.insert(tkinter.END, str(message) + END_OF_LINE)  # добавить текст в конец сообщения
        self.message_list.configure(state=TEXT_STATE_DISABLED)  # вывод сообщения

        self.forth_button['state'] =TEXT_STATE_DISABLED
        self.third_button['state'] = TEXT_STATE_DISABLED
        self.second_button['state'] = TEXT_STATE_DISABLED
        self.first_button['state'] = TEXT_STATE_DISABLED

    def on_closing(self):
        self.application.send_end()
        self.application.exit()
        self.gui.destroy()  # уничтожение виджета и всех его потомков
        self.application.sock.close()
