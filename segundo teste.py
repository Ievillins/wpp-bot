from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
sessoes = {}  # telefone -> lista de boletos disponíveis

@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    msg = request.form.get('Body').strip().lower()
    phone = request.form.get('From')
    response = MessagingResponse()
    reply = response.message()

    if "segunda via" in msg or "boleto" in msg:
        boletos = listar_boletos()
        if not boletos:
            reply.body("Não encontrei boletos disponíveis no momento.")
        else:
            sessoes[phone] = boletos
            texto = "Escolha um dos boletos disponíveis:\n"
            for i, b in enumerate(boletos, start=1):
                texto += f"{i}. {b['numero']} - Venc: {b['vencimento']} - R$ {b['valor']}\n"
            reply.body(texto)

    elif phone in sessoes and msg.isdigit():
        indice = int(msg) - 1
        boletos = sessoes.get(phone, [])
        if 0 <= indice < len(boletos):
            link = boletos[indice]['link']
            reply.body(f"Aqui está seu boleto: {link}")
            del sessoes[phone]  # limpa sessão
        else:
            reply.body("Opção inválida. Tente novamente.")

    else:
        reply.body("Olá! Digite 'segunda via' para receber um boleto disponível.")

    return str(response)

def listar_boletos():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://app.agiw.com.br/portal-docs/#/login")
        time.sleep(3)

        driver.find_element(By.NAME, "email").send_keys("leticia.silva@alivira.com.br")
        driver.find_element(By.NAME, "senha").send_keys("Agostinis22")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(5)

        driver.get("https://app.agiw.com.br/portal-docs/#/gerenciar;in=3")
        time.sleep(5)

        boletos = []
        linhas = driver.find_elements(By.XPATH, "//tbody/tr")
        for linha in linhas:
            colunas = linha.find_elements(By.TAG_NAME, "td")
            if len(colunas) < 6:
                continue
            numero = colunas[0].text.strip()
            valor = colunas[1].text.strip()
            vencimento = colunas[2].text.strip()

            # link simulado (ajuste conforme necessário)
            link = f"https://app.agiw.com.br/storage/boletos/{numero.replace(' ', '')}.pdf"

            boletos.append({
                'numero': numero,
                'valor': valor,
                'vencimento': vencimento,
                'link': link
            })

        return boletos

    except Exception as e:
        print("Erro ao listar boletos:", e)
        return []

    finally:
        driver.quit()

if __name__ == "__main__":
    app.run(port=5000)

