import telebot
import random
import re

#@DadosDeRpg_bot
#RpgDiceBot

bot = telebot.TeleBot('xxx')

@bot.message_handler(commands=['start', 'help'])
def start(msg: telebot.types.Message):
    bot.reply_to(msg, '🎲 Olá! Use o comando /r no formato: 1d6, 2d6+1, 3d6-2, etc.')


# Handler para o comando /rolar
@bot.message_handler(commands=['r'])
def rolar(msg: telebot.types.Message):
    try:
        texto = msg.text.split(' ', 1)
        if len(texto) < 2:
            bot.reply_to(msg, "📌 Use: /r 1d6 ou 2d6+1, etc.")
            return
        comando = texto[1]
        resultado = rolar_dados(comando)
        bot.reply_to(msg, resultado)
    except Exception as e:
        bot.reply_to(msg, f"❌ Erro: {str(e)}")

# Função para interpretar e rolar dados
def rolar_dados(comando: str) -> str:
    padrao = r'(\d*)d(\d+)([+-]\d+)?'
    match = re.match(padrao, comando.replace(" ", ""))
    
    if not match:
        return "❌ Formato inválido. Use: 1d6, 2d6+1, 3d6-2, etc."
    
    qtd = int(match.group(1)) if match.group(1) else 1
    lados = int(match.group(2))
    modificador = int(match.group(3)) if match.group(3) else 0

    if qtd > 100 or lados > 1000:
        return "⚠️ Calma aí! Tenta um número menor de dados ou lados."

    resultados = [random.randint(1, lados) for _ in range(qtd)]

    if resultados[0] == lados and modificador != 0:
        total = sum(resultados) + (modificador * 2)
        return f"🎲 Rolando {comando}:\n🎯 Dados: {resultados}\n💀 Crítico: {total}"
    else:
        total = sum(resultados) + modificador
        return f"🎲 Rolando {comando}:\n🎯 Dados: {resultados}\n📊 Total: {total}"

bot.infinity_polling()