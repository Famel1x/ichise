from flet import *
import random
import pyperclip
import openai
from googletrans import Translator
import threading
from datetime import datetime 
import time
from pytz import timezone

#v1.2.0 pre-relise


class CalculatorApp(UserControl):
    def build(self):
        self.reset()
        self.result = Text(value="0", color=colors.WHITE, size=20)

        # application's root control (i.e. "view") containing all other controls
        return Container(
            width=300,
            bgcolor=colors.BLACK,
            border_radius=border_radius.all(20),
            padding=20,
            content=Column(
                
                controls=[
                    Text("Удобный калькулятор)"),
                    Row(controls=[self.result], alignment="end"),
                    Row(
                        controls=[
                            ElevatedButton(
                                text="AC",
                                bgcolor=colors.BLUE_GREY_100,
                                color=colors.BLACK,
                                expand=1,
                                on_click=self.button_clicked,
                                data="AC",
                            ),
                            ElevatedButton(
                                text="+/-",
                                bgcolor=colors.BLUE_GREY_100,
                                color=colors.BLACK,
                                expand=1,
                                on_click=self.button_clicked,
                                data="+/-",
                            ),
                            ElevatedButton(
                                text="%",
                                bgcolor=colors.BLUE_GREY_100,
                                color=colors.BLACK,
                                expand=1,
                                on_click=self.button_clicked,
                                data="%",
                            ),
                            ElevatedButton(
                                text="/",
                                bgcolor=colors.ORANGE,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="/",
                            ),
                        ],
                    ),
                    Row(
                        controls=[
                            ElevatedButton(
                                text="7",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="7",
                            ),
                            ElevatedButton(
                                text="8",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="8",
                            ),
                            ElevatedButton(
                                text="9",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="9",
                            ),
                            ElevatedButton(
                                text="*",
                                bgcolor=colors.ORANGE,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="*",
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            ElevatedButton(
                                text="4",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="4",
                            ),
                            ElevatedButton(
                                text="5",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="5",
                            ),
                            ElevatedButton(
                                text="6",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="6",
                            ),
                            ElevatedButton(
                                text="-",
                                bgcolor=colors.ORANGE,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="-",
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            ElevatedButton(
                                text="1",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="1",
                            ),
                            ElevatedButton(
                                text="2",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="2",
                            ),
                            ElevatedButton(
                                text="3",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="3",
                            ),
                            ElevatedButton(
                                text="+",
                                bgcolor=colors.ORANGE,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="+",
                            ),
                        ]
                    ),
                    Row(
                        controls=[
                            ElevatedButton(
                                text="0",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=2,
                                on_click=self.button_clicked,
                                data="0",
                            ),
                            ElevatedButton(
                                text=".",
                                bgcolor=colors.WHITE24,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data=".",
                            ),
                            ElevatedButton(
                                text="=",
                                bgcolor=colors.ORANGE,
                                color=colors.WHITE,
                                expand=1,
                                on_click=self.button_clicked,
                                data="=",
                            ),
                        ]
                    ),
                ],
            ),
        )

    def button_clicked(self, e):
        data = e.control.data
        if self.result.value == "Error" or data == "AC":
            self.result.value = "0"
            self.reset()

        elif data in ("1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "."):
            if self.result.value == "0" or self.new_operand == True:
                self.result.value = data
                self.new_operand = False
            else:
                self.result.value = self.result.value + data

        elif data in ("+", "-", "*", "/"):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.operator = data
            if self.result.value == "Error":
                self.operand1 = "0"
            else:
                self.operand1 = float(self.result.value)
            self.new_operand = True

        elif data in ("="):
            self.result.value = self.calculate(
                self.operand1, float(self.result.value), self.operator
            )
            self.reset()

        elif data in ("%"):
            self.result.value = float(self.result.value) / 100
            self.reset()

        elif data in ("+/-"):
            if float(self.result.value) > 0:
                self.result.value = "-" + str(self.result.value)

            elif float(self.result.value) < 0:
                self.result.value = str(
                    self.format_number(abs(float(self.result.value)))
                )

        self.update()

    def format_number(self, num):
        if num % 1 == 0:
            return int(num)
        else:
            return num

    def calculate(self, operand1, operand2, operator):

        if operator == "+":
            return self.format_number(operand1 + operand2)

        elif operator == "-":
            return self.format_number(operand1 - operand2)

        elif operator == "*":
            return self.format_number(operand1 * operand2)

        elif operator == "/":
            if operand2 == 0:
                return "Error"
            else:
                return self.format_number(operand1 / operand2)

    def reset(self):
        self.operator = "+"
        self.operand1 = 0
        self.new_operand = True


ones_refresh = True
validation = False
blizTimeToOtdih = ""

def main(page: Page):
    page.title = "Обучение 24.07.23 ichise edition"
    page.window_width = 1700
    page.window_height =800



    openai.api_key = "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"


    translator = Translator(service_urls=['translate.googleapis.com'])
    gpt_result = ""

    

    def askGPT(e):
        text  = f"Прочитайте сообщение клиента. Составьте ответ, который сможет повысить лояльность клиента от имени техподержки. Сообщение: {gptVopros.value} . написать {gptDlinna.value} слов"
        print("Мыслим....")
        textEn = translator.translate(text = text, dest = "en")
        print("переведено!")

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": textEn.text}])
        
        print("Получили ответ")

        answer = translator.translate(text = f"{completion.choices[0].message.content}", dest = "ru")
        print("переведено!")
        gpt_result = answer.text
        gptOtvet.value = gpt_result
        print("Вставленно!")
        page.update()
    
    def cikleTime():
            global ones_refresh
            while True:
                ones_refresh = False
                
                
                now = datetime.now() 
                current_time = now.strftime("%H:%M:%S") 
                
                moscow = timezone('Europe/Moscow')
                moscowTime = datetime.now(moscow)

                moscow_time = moscowTime.strftime("%H:%M:%S")
                print("Moscow Time =", moscow_time, " Current Time =", current_time)

                moscow_hour = moscowTime.hour
                moscow_min = moscowTime.minute
                moscow_sec = moscowTime.second

                
                
                def validate_time(alarm_time):
                    global validation
                    if validation == False:
                        if len(alarm_time)!= 8:
                            return False
                        else:
                            if int(alarm_time[0:2]) >23:
                                return False
                            elif int(alarm_time[3:5]) >59:
                                return False
                            elif int(alarm_time[6:8]) >59:
                                return False
                            else:
                                validation = True
                                print("Время валид")
                                count_down()
                                return True
                    else:
                        count_down()
                        return True
                
                alarm_time = firsPer

                alarm_hour = int(alarm_time[0:2])
                alarm_min = int(alarm_time[3:5])
                alarm_sec = int(alarm_time[6:8])

                def count_down():
                    global blizTimeToOtdih
                    hour = int(alarm_hour) - int(moscow_hour)
                    min = int(alarm_min) - int(moscow_min)
                    sec = int(alarm_sec) - int(moscow_sec)
                    
                    if sec < 0:
                        min -= 1
                        sec += 60
                    if min < 0: 
                        hour -= 1
                        min +=60
                    
                    
                    blizTimeToOtdih =  (f"{hour}:{min}:{sec}")
                   

                

                
                if validate_time(alarm_time) == True:
                    global validation
                    if validation ==False:
                        print("Уведомление о постановке на будильник")

                    if alarm_hour == moscow_hour:
                        if alarm_min == moscow_min:
                            if alarm_sec == moscow_sec:
                                print("Перерыв")
                
                else:
                    print("Время не верное")

                    
                curTimeText.value = current_time
                mosTimeText.value = moscow_time
                blizTimeToOtdihText.value = blizTimeToOtdih

                

                page.update()
                time.sleep(1)
    
    
    def curentTime(e):
        global ones_refresh
        
        if ones_refresh == True:
            
            t = threading.Thread(target=cikleTime)
            t.start()
        
        

    def thre(e):
        f = threading.Thread(target=askGPT)
        f.start()

    def button_clicked(e):
        try:
            zakazal1 = float(zakazal.value)
            dolzhen1 = float(dolzhen.value)
            poluchil1 = float(poluchil.value)
            zaplatil1 = float(zaplatil.value)


            za_1gramm = dolzhen1/zakazal1
            obazan_oplat = za_1gramm*poluchil1
            razn =  zaplatil1 - obazan_oplat
            za_1Kg = za_1gramm*1000

            razn_text.value = f"{razn}"
            za_1kg_text.value = f"{za_1Kg}"
            pyperclip.copy(razn)
            page.update()
        except :
            pass

    def copy(dans:str):
        pyperclip.copy(dans)

    mosTimeText = Text("None")
    curTimeText = Text("None")
    blizTimeToOtdihText  = Text("None",color = colors.PINK_200)


    #перерывы

    firsPer = "21:00:00"
    secPer = "None"
    thridPer = "None"
    

    firsPer_text = Text(f"1) {firsPer}")
    secPer_text = Text(f"2) {secPer}")
    thridPer_text = Text(f"3) {thridPer}")
    
    nomerPer = TextField(
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width= 60,
                        text_align="center",
                        value="30")
    addPer = TextField(
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width= 60,
                        text_align="center",
                        value="30")


    #GPT-ответы
    gptVopros = TextField(
                        multiline=True,
                        min_lines=1,
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width= 300,
                        text_align="center",)
    gptDlinna = TextField(
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width= 60,
                        text_align="center",
                        value="30")
    gptOtvet = TextField(
                    multiline=True,
                    min_lines=1,
                    bgcolor=colors.GREY_400, 
                    color= colors.BLACK,
                    border=InputBorder.UNDERLINE,
                    width=450,
                    )

        
    #Конвертер:
    za_1kg_text = Text()
    razn_text = Text()      
    zakazal = TextField(
                        
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width=80,
                        text_align="center",
                        
                        )
    dolzhen = TextField(
                        
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width=80,
                        text_align="center",

                        )    
    poluchil = TextField(
                            
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width=80,
                        text_align="center"
                        )   
    zaplatil = TextField(
                        
                        bgcolor=colors.GREY_400, 
                        color= colors.BLACK,
                        border=InputBorder.UNDERLINE,
                        width=80,
                        text_align="center"
                        )

    # create application instance
    calc = CalculatorApp()
    
    gpt_result = " "
    # add application's root control to the page
    page.add(
        Column([
            Row([
                #
                Column([
                    Container(#всё что связано с временем
                        width=300,
                        height=200,
                        bgcolor="black",
                        border_radius=10,
                        content= Column([
                                    
                                    IconButton(
                                        
                                        icon= icons.REFRESH,
                                        on_click=curentTime
                                    ),
                                    Row([
                                        Container(width=10),
                                        Text("Ваше время: "),
                                        curTimeText
                                    ]),
                                    Row([ 
                                        Container(width=10),
                                        Text("Московсое время: "),
                                        mosTimeText
                                    ]),
                                    Row([
                                        Container(width=10),    
                                        Text("До ближайшего перерыва: ", color=colors.PINK_200,),
                                        blizTimeToOtdihText
                                    ]),
                                    ])
                            
                    ),
                    #Калькулятор
                    calc, 
                ]),

                
                
                
                #Блок разделений
                Container(width=5),
                #Блок с перерывами
                Column([
                    Row([
                       Container(
                        width=245,
                        height=200,
                        bgcolor="black",
                        border_radius=10,
                        content=Column([
                            Container(width=10),
                            Row([
                                Container(width=10),
                                Text("Список перерывов: "),
                            ]),
                            Row([
                                Container(width=10),
                                firsPer_text,
                            ]),
                            Row([
                                Container(width=10),
                                secPer_text,
                            ]),
                            Row([
                                Container(width=10),
                                thridPer_text,
                            ]),

                        ])
                        #Блок с изменениями перерывов
                        ),  
                        Container(
                            width=245,
                            height=200,
                            bgcolor="black",
                            border_radius=10,
                            content=Column([
                                Container(width=10),
                                Row([
                                    Container(width=10),
                                    Text("Изменить перерыв: ")
                                ]),
                                Row([
                                    Container(width=10),
                                    Text("Изменить перерыв: ")
                                ]),
                                Row([
                                    Container(width=10),
                                    Text("Изменить перерыв: ")
                                ]),


                            ])
                        ), 
                    ]),
                    Container(#Конвертер
                        width=500,
                        height=350,
                        bgcolor="black",
                        border_radius=10,
                        content= Column(
                            controls=[
                                Container(
                                Row([
                                    Text(""),
                                    Column([
                                        Text(""),
                                        Text("Удобный конвертер (Всё в граммах)"),
                                    ]),
                                    
                                ]),
                                
                                
                            ),
                                    Column(
                                    [   Container(
                                        height=20
                                    ),
                                    Row([
                                        Text(""),
                                        Text("Заказал:",width=80),
                                        zakazal,

                                        Text("Должен был заплатить: ",width=120, ),
                                        dolzhen,
                                    ]),
                                    Container(
                                        height=20
                                    ),
                                    Row([
                                        Text(""),
                                        Text("Получил:",width=80,),
                                        poluchil,

                                        Text("Заплатил: ",width=120),
                                        zaplatil,
                                    ]),
                                    Container(
                                        height=20
                                    ),
                                    Row([
                                        Container(
                                            width=20
                                        ),
                                        # 1) Цена за килограмм 
                                        # 2) Изменение цены
                                        Column([
                                            Text("Цена за килограмм: "),
                                            za_1kg_text
                                        ]),
                                        Container(
                                            width=30    
                                        ),
                                        Column([
                                            Text("Изменение цены: "),
                                            razn_text
                                        ]),
                                        Column([
                                            ElevatedButton(
                                                text = "Расчитать",
                                                on_click=button_clicked
                                            ),
                                           
                                        ]),
                                        
                                        
                                        
                                    ]),
                                    
                                ]
                            ),
                            
                        ]
                    )
                    
                ),
                    
                ]),
                
                 
                #Контейнер для генерации ответов если самим лень писать
                Container(
                    width=830,
                    height=600,
                    bgcolor="black",
                    border_radius=10,
                    content=Column(
                        controls=[
                            Container(
                                Row([
                                    Text(""),
                                    Column([
                                        Text("Если самому лень писать ответы то воспользуйся этим ↓"),

                                    ]),
                                    Text("Введите количесвто слов: ", color=colors.PINK_200,),
                                    gptDlinna,
                                    ElevatedButton(
                                                text = "Получить ответ",
                                                on_click=askGPT
                                            ),
                                    
                                ]),
                                
                                
                            ),
                            Column([
                                Row([
                                    Text(""),
                                    Column([
                                        Text("Напиши текст сообщения: "),
                                        gptVopros
                                    ]),
                                    Container(width=30),
                                    Column([
                                        Text("Ответ займёт от 1 до 3х минут в зависимости от интернета"),
                                        gptOtvet
                                    ])
                                    
                                ])
                                
                            ]),
                            
                        ]
                    )

                )
                    
             ]),
            Row([
                
                
                


            ])
            
        ])
        
    )


    #horny?
    
    

app(target=main)