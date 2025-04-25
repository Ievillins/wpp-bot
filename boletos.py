boletos_mock = {
    "12345678900": "https://exemplo.com/boletos/12345678900.pdf",
    "ped123": "https://exemplo.com/boletos/ped123.pdf"
}

def buscar_boleto(identificador):
    return boletos_mock.get(identificador.lower())
