from tkinter import *
import math
import re

window = Tk()
window.title('Calculator')
window.geometry('350x480+500+150')
window.config(bg='#eee9e9')

display_label = Label(window,text='0',fg='black',bg='#eee9e9',font='Georgia,serif 24 bold',anchor='e')
display_label.place(x=30,y=140,width=290,height=40)

is_deg_mode = True
is_second_mode = False

def create_button(text,fg,bg,x,y,font,command=None):
    button = Button(text=text,fg=fg,bg=bg,activeforeground=fg,activebackground=bg,
                  font=font,borderwidth=0,relief='flat',command=command)
    button.place(x=x,y=y)
    return button

def on_delete_click():
    current_text = display_label.cget('text')
    if current_text:
        new_text = current_text[:-1] if len(current_text) > 1 else '0'
        display_label.config(text=new_text)

def on_button_click(value):
    current_text = display_label.cget('text').replace('.','')
    if current_text == '0':
        new_text = value
    else:
        new_text = current_text + value
    formatted_text = format_number(new_text)
    display_label.config(text=formatted_text)

def on_operator_click(operator):
    current_text = display_label.cget('text')
    
    if operator in ['arcsin','arccos','arctan','sin', 'cos', 'tan', 'lg', 'ln']:
        if current_text == '0':
            new_text = operator + '('
        else:
            if '(' not in current_text or current_text[-1] in '+-*/÷':
                new_text = current_text + operator + '('
            else:
                new_text = current_text + operator

    elif operator in ['+', '-', 'x', '÷']:
        if current_text and not current_text[-1] in '+-x÷':
            new_text = current_text + operator
        else:
            new_text = current_text

    elif operator == '!':
        if current_text == '0':
            new_text = '0!'
        else:
            new_text = current_text + '!'

    elif operator == '√':
        if current_text == '0':
            new_text = '√'
        else:
            new_text = current_text +  '√' 
    
    elif operator == '*(-1)':
        if current_text == '0':
            new_text = '^(-1)'
        else:
            new_text = current_text + '^(-1)'
    
    elif operator == '**':
        if current_text == '0':
            new_text = '0^'
        else:
            new_text = current_text + '^'
    
    elif operator == 'π':
        if current_text == '0':
            new_text = operator
        else:
            new_text = current_text + operator
    
    elif operator == 'e':
        if current_text == '0':
            new_text = 'e'
        else:
            new_text = current_text + operator

    else:
        new_text = current_text
    
    display_label.config(text=new_text)


def remove_functions(expression):
    return re.sub(r'(arcsin|arccos|arctan|sin|cos|tan|lg|ln|√|^(-1)|!|\(|\))', '', expression)


def calculate_result():
    current_text = display_label.cget('text')
    if current_text:
        current_text = current_text.replace('÷', '/').replace('x', '*').replace(',','.')
        try:
            # Check if the expression is a scientific operation
            if any(op in current_text for op in ['arcsin','arccos','arctan','sin', 'cos', 'tan', '√','lg' ,'ln','π','e', '*(-1)', '!']):
                # Perform scientific operation
                for op in ['arcsin','arccos','arctan','sin', 'cos', 'tan', '√', 'lg', 'ln', 'π','e', '*(-1)','!']:
                    if op in current_text:
                        scientific_operation(op)
                        return
            else:
                # Perform mathematical calculation
                current_text = current_text.replace('^','**')
                result = eval(current_text)
                result = round(result,10)
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                result = str(result).replace('.', ',')
                display_label.config(text=format_number(result))
        except Exception as e:
            display_label.config(text='Error')

def apply_percentage():
    current_text = display_label.cget('text').replace('.','')
    if current_text and current_text != '0':
        try:
            numeric_value = float(current_text.replace(',','.'))
            percentage_value = numeric_value / 100
            percentage_value = round(percentage_value,10)
            if isinstance(percentage_value,float) and percentage_value.is_integer():
                percentage_value = int(percentage_value)
                display_label.config(text=str(percentage_value))
            else:
                display_label.config(text=format_number(str(percentage_value).replace('.',',')))
        except ValueError:
            display_label.config(text='Error')

def format_number(number_str):
    is_negative = number_str.startswith('-')
    number_str = number_str.lstrip('-')

    if ',' in number_str:
        parts = number_str.split(',')
        if len(parts) > 2:
            return number_str
        
        whole_part = parts[0] if parts[0] else '0'
        fractional_part = parts[1]
        try:
            formatted_whole_part = '{:,}'.format(int(whole_part)).replace(',', '.')
        except ValueError:
            return number_str
        
        result = f"{formatted_whole_part},{fractional_part}"
    else:
        try:
            result = '{:,}'.format(int(number_str)).replace(',', '.')
        except ValueError:
            return number_str
        
    if is_negative:
        return '-' + result
    return result
        
def clear_display():
    display_label.config(text='0')

def toggle_second_mode():
    global is_second_mode
    is_second_mode = not is_second_mode

    if is_second_mode:
        sin_button.config(text='sin⁻¹',command=lambda: on_operator_click('arcsin'))
        cos_button.config(text='cos⁻¹',command=lambda: on_operator_click('arccos'))
        tan_button.config(text='tan⁻¹',command=lambda: on_operator_click('arctan'))
        deg_button.config(state=DISABLED)
    else:
        sin_button.config(text='sin',command=lambda: on_operator_click('sin'))
        cos_button.config(text='cos',command=lambda: on_operator_click('cos'))
        tan_button.config(text='tan',command=lambda: on_operator_click('tan'))
        deg_button.config(state=NORMAL)


def toggle_deg_rad():
    global is_deg_mode
    is_deg_mode = not is_deg_mode
    if is_deg_mode:
        deg_button.config(text='deg')
        second_button.config(state=NORMAL)
    else:
        deg_button.config(text='rad')
        second_button.config(state=DISABLED)


def replace_special_constants(text):
        return text.replace('π',str(math.pi)).replace('e',str(math.e))

def handle_exponentiation(text):
    if '^' in text:
        base,exponent = text.split('^')
        base = replace_special_constants(base)
        try:
            exponent = float(exponent)
        except ValueError:
            return text
        if exponent > 709:
            return float('inf')
        return math.pow(float(base),exponent)
    return float(text)

def is_arctan_invalid(value):
    if 'π' in value:
        pi_multiples = re.findall(r'(\d*)π', value)
        for multiple in pi_multiples:
            if multiple and int(multiple) > 0:
                return True
    return False

def scientific_operation(operation):
    current_text = display_label.cget('text').replace(',', '.')

    try:
        
        if '√' in current_text:
            match = re.match(r'(\d*)√(\d+)', current_text)
            if match:
                multiplier = int(match.group(1)) if match.group(1) else 1
                number = int(match.group(2))
                result = multiplier * math.sqrt(number)
            else:
                result = math.sqrt(float(current_text.split('√')[-1]))
            
            if isinstance(result,float) and result.is_integer():
                result = int(result)
            else:
                result = round(result,10)

            display_label.config(text=str(result).replace('.',','))
            return
        
        current_text = remove_functions(current_text)
        current_text = replace_special_constants(current_text)

        if operation == 'sin':
            if 'π' in display_label.cget('text'):
                result = math.sin(math.pi)
            else:
                result = math.sin(math.radians(float(current_text))) if is_deg_mode else math.sin(float(current_text))

        elif operation == 'cos':

            if 'π' in display_label.cget('text'):
                pi_multiples = re.findall(r'(\d*)π', display_label.cget('text'))
                if pi_multiples:
                    for multiple in pi_multiples:
                        if multiple == '' or multiple == '1':
                            multiple = 1
                        else:
                            multiple = int(multiple)

                        if multiple % 2 == 0:
                            result = 1
                        else:
                            result = -1
            else:
                result = math.cos(math.radians(float(current_text))) if is_deg_mode else math.cos(float(current_text))

        elif operation == 'tan':
            if 'π' in display_label.cget('text'):
                result = math.tan(math.pi)
            else:
                result = math.tan(math.radians(float(current_text))) if is_deg_mode else math.tan(float(current_text))
        
        elif operation == 'arcsin':
            result = math.degrees(math.asin(float(current_text)))

        elif operation == 'arccos':
            result = math.degrees(math.acos(float(current_text)))

        elif operation == 'arctan':
            if is_arctan_invalid(display_label.cget('text')):
                display_label.config(text='Error')
                return
            else:
                result = math.degrees(math.atan(float(current_text)))

        elif operation == 'lg':
            result = math.log10(float(current_text))

        elif operation == 'ln':
            if '^' in current_text:
                current_text = handle_exponentiation(current_text)
            result = math.log(float(current_text))
        
        elif operation == '*(-1)':
            result = 1 / float(current_text)
        
        elif operation == '!':
            result = math.factorial(int(current_text))

        else:
            result = float(current_text)
 
        result = round(result, 10)
        if result.is_integer():
            result = int(result)
        display_label.config(text=format_number(str(result).replace('.', ',')))
        
    except Exception as e:
        display_label.config(text='Error')

def show_main_screen():
    global back_to_main
    if back_to_main:
        for widget in window.winfo_children():
            if widget != display_label:
                widget.place_forget()
        place_buttons()

def place_buttons():
    global main_buttons

    line_canvas =  Canvas(window,width=350,height=20,bg='#eee9e9',borderwidth=0,highlightthickness=0)
    line_canvas.create_line(0,10,300,10,fill='#666666',width=1)
    line_canvas.place(x=30,y=180)

    main_buttons = []
    buttons = [
    ('AC','orange','#eee9e9',30,200,clear_display),
    ('⌫','orange','#eee9e9',110,200,on_delete_click),
    ('%', 'orange', '#eee9e9', 190, 200,apply_percentage),
    ('÷', 'orange', '#eee9e9', 270, 200,lambda: on_operator_click('÷')),
    ('7', 'black', '#eee9e9', 30, 250,lambda: on_button_click('7')),
    ('8', 'black', '#eee9e9', 110, 250,lambda: on_button_click('8')),
    ('9', 'black', '#eee9e9', 190, 250,lambda: on_button_click('9')),
    ('x', 'orange', '#eee9e9', 270, 250,lambda: on_operator_click('x')),
    ('4', 'black', '#eee9e9', 30, 300,lambda: on_button_click('4')),
    ('5', 'black', '#eee9e9', 110, 300,lambda: on_button_click('5')),
    ('6', 'black', '#eee9e9', 190, 300,lambda: on_button_click('6')),
    ('-', 'orange', '#eee9e9', 270, 300,lambda: on_operator_click('-')),
    ('1', 'black', '#eee9e9', 30, 350,lambda: on_button_click('1')),
    ('2', 'black', '#eee9e9', 110, 350,lambda: on_button_click('2')),
    ('3', 'black', '#eee9e9', 190, 350,lambda: on_button_click('3')),
    ('+', 'orange', '#eee9e9', 270, 350,lambda: on_operator_click('+')),
    ('⏹️','orange','#eee9e9',30,400,science_mode),
    ('0', 'black', '#eee9e9', 110, 400,lambda: on_button_click('0')),
    (',', 'black', '#eee9e9', 190, 400,lambda: on_button_click(',')),
    ('=', 'orange', '#eee9e9', 270, 400,calculate_result)
    ]
    
    for text, fg, bg, x, y, *cmd in buttons:
        button = create_button(text, fg, bg, x, y, 'Georgia,serif 16 bold', *cmd)
        main_buttons.append(button)

def science_mode():
    global back_to_main,deg_button,second_button,sin_button,cos_button,tan_button
    back_to_main = True

    for widget in main_buttons:
        widget.place_forget()

    buttons_science = [
        ('x^y', 'black', '#eee9e9', 25, 240,lambda: on_operator_click('**')),
        ('lg', 'black', '#eee9e9', 95, 240,lambda: on_operator_click('lg')),
        ('ln', 'black', '#eee9e9', 165, 240,lambda: on_operator_click('ln')),
        ('(', 'black', '#eee9e9', 235, 240,lambda: on_button_click('(')),
        (')', 'black', '#eee9e9', 305, 240,lambda: on_button_click(')')),
        ('√x', 'black', '#eee9e9', 25, 280,lambda: on_operator_click('√')),
        ('AC', 'orange', '#eee9e9', 95, 280, clear_display),
        ('⌫', 'orange', '#eee9e9', 165, 280,on_delete_click),
        ('%', 'orange', '#eee9e9', 235, 280,apply_percentage),
        ('÷', 'orange', '#eee9e9', 305, 280, lambda: on_operator_click('÷')),
        ('x!', 'black', '#eee9e9', 30, 320,lambda: on_operator_click('!')),
        ('7', 'black', '#eee9e9', 95, 320, lambda: on_button_click('7')),
        ('8', 'black', '#eee9e9', 165, 320, lambda: on_button_click('8')),
        ('9', 'black', '#eee9e9', 235, 320, lambda: on_button_click('9')),
        ('x', 'orange', '#eee9e9', 300, 320, lambda: on_operator_click('x')),
        ('1/x', 'black', '#eee9e9', 23, 360,lambda: on_operator_click('*(-1)')),
        ('4', 'black', '#eee9e9', 95, 360, lambda: on_button_click('4')),
        ('5', 'black', '#eee9e9', 165, 360, lambda: on_button_click('5')),
        ('6', 'black', '#eee9e9', 235, 360, lambda: on_button_click('6')),
        ('-', 'orange', '#eee9e9', 305, 360, lambda: on_operator_click('-')),
        ('π','black','#eee9e9',28,400, lambda: on_operator_click('π')),
        ('1', 'black', '#eee9e9', 95, 400,lambda: on_button_click('1')),
        ('2', 'black', '#eee9e9', 165, 400, lambda: on_button_click('2')),
        ('3', 'black', '#eee9e9', 235, 400, lambda: on_button_click('3')),
        ('+', 'orange', '#eee9e9', 305, 400, lambda: on_operator_click('+')),
        ('⏹️', 'orange', '#eee9e9', 25, 440, show_main_screen),
        ('e','black','#eee9e9',95,440, lambda: on_operator_click('e')),
        ('0', 'black', '#eee9e9', 165, 440, lambda: on_button_click('0')),
        (',', 'black', '#eee9e9', 235, 440, lambda: on_button_click(',')),
        ('=', 'orange', '#eee9e9', 305, 440,lambda: calculate_result())
    ]


    for text, fg, bg, x, y, *cmd in buttons_science:
        create_button(text, fg, bg, x, y, 'Georgia,serif 11 bold', *cmd)
    
    deg_button = Button(window,text='deg',fg='black',bg='#eee9e9',activeforeground='black',activebackground='#eee9e9',
                        font='Georgia,serif 11 bold',borderwidth=0,relief='flat',command=toggle_deg_rad)
    deg_button.place(x=95,y=200)

    second_button = Button(window,text='2nd',fg='black',bg='#eee9e9',activeforeground='black',activebackground='#eee9e9',
                           font='Georgia,serif 11 bold',borderwidth=0,relief='flat',command=toggle_second_mode)
    second_button.place(x=25,y=200)

    sin_button = Button(window,text='sin',fg='black',bg='#eee9e9',activeforeground='black',activebackground='#eee9e9',
                        font='Georgia,serif 11 bold',borderwidth=0,relief='flat',command=lambda: on_operator_click('sin'))
    sin_button.place(x=165,y=200)

    cos_button = Button(window,text='cos',fg='black',bg='#eee9e9',activeforeground='black',activebackground='#eee9e9',
                        font='Georgia,serif 11 bold',borderwidth=0,relief='flat',command= lambda: on_operator_click('cos'))
    cos_button.place(x=235,y=200)

    tan_button = Button(window,text='tan',fg='black',bg='#eee9e9',activeforeground='black',activebackground='#eee9e9',
                        font='Georgia,serif 11 bold',borderwidth=0,relief='flat',command= lambda: on_operator_click('tan'))
    tan_button.place(x=295,y=200)


place_buttons()

window.mainloop()