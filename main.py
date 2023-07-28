from flet import *
import random




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





def main(page: Page):
    page.title = "Обучение 24.07.23 ichise edition"
    page.window_width = 910
    page.window_height = 410
    page.window_left = 400
    page.window_top = 200 


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
            page.update()
        except :
            pass

    


    
        
        
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


    # add application's root control to the page
    page.add(
        Column([
            Row([
                calc, 
                Container(width=50),
                Container(
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
                                        ElevatedButton(
                                            text = "Расчитать",
                                            on_click=button_clicked
                                        ),
                                        
                                        
                                    ]),
                                    
                                ]
                            ),
                            
                        ]
                    )
                    
                )
                
                    
            ]),
            
        ])
        
    )


    #horny?


app(target=main)