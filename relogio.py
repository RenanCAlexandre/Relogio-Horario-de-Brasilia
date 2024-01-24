import requests
import tkinter as tk
from tkinter.font import Font
from datetime import datetime
import time

def ajustar_janela_ao_conteudo(root):
    root.update_idletasks()
    largura = root.winfo_reqwidth()
    altura = root.winfo_reqheight()
    largura_tela = root.winfo_screenwidth()
    altura_tela = root.winfo_screenheight()
    x_pos = (largura_tela - largura) // 2
    y_pos = (altura_tela - altura) // 2
    root.geometry(f"{largura + 20}x{altura}+{x_pos - 50}+{y_pos - 120}")

log_erro = ('Erro ao consultar o horário de Brasília', 'Verifique sua Internet!')

def obter_horario_brasilia():
    try:
        response = requests.get('http://worldtimeapi.org/api/timezone/America/Sao_Paulo')
        response.raise_for_status()
        dados = response.json()
        horario_brasilia = dados['datetime']
        return datetime.strptime(horario_brasilia, "%Y-%m-%dT%H:%M:%S.%f%z")
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
        return None

def buscar_horario():
    horario_completo = obter_horario_brasilia()
    if horario_completo:
        hora, minutos, segundos = horario_completo.hour, horario_completo.minute, horario_completo.second
        return f'{hora}:{minutos:02d}:{segundos:02d}'
    return log_erro[1]

def buscar_data():
    horario_completo = obter_horario_brasilia()
    if horario_completo:
        meses_dict = {1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho', 7: 'Julho',
                      8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'}
        dia_semana_list = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
        dia_semana_numero = horario_completo.weekday()
        dia_semana_escrito = dia_semana_list[dia_semana_numero]
        dia, mes_numero, ano = horario_completo.day, horario_completo.month, horario_completo.year
        mes_escrito = meses_dict.get(mes_numero, '')
        return f'{dia_semana_escrito}, {dia} de {mes_escrito} de {ano}'
    return log_erro[1]

def atualizar_label():
    try:
        label_horario.config(text=buscar_horario())
        label_data.config(text=buscar_data())
        milissegundos_restantes = 1000 - int(time.time() * 1000) % 1000
        janela.after(milissegundos_restantes, atualizar_label)
        janela.after(900, ajustar_janela_ao_conteudo, janela)
    except Exception as e:
        print(f"Erro na atualização da label: {e}")
        janela.after(900, atualizar_label)
        janela.after(900, ajustar_janela_ao_conteudo, janela)

janela = tk.Tk()
janela.title('Horário Oficial')

fonte_data = Font(size=20, weight="bold")
fonte_horario = Font(size=26, weight="bold")

label_data = tk.Label(janela, text='', font=fonte_data)
label_data.pack(pady=5)

label_horario = tk.Label(janela, text='', font=fonte_horario)
label_horario.pack(pady=5)

atualizar_label()
ajustar_janela_ao_conteudo(janela)

janela.mainloop()
