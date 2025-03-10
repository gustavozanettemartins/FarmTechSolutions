import requests

# Substitua pela sua API Key da ClimaTempo
API_KEY = "31b462e81363e22b5904546c9130f24b"

CITY_ID = "5099"  # Braço do Norte, SC

# URL da API para obter o clima atual
URL = f"http://apiadvisor.climatempo.com.br/api/v1/weather/locale/{CITY_ID}/current?token={API_KEY}"

# Fazendo a requisição para a API
response = requests.get(URL)

# Verificando se a resposta foi bem-sucedida
if response.status_code == 200:
    data = response.json()
    cidade = data["name"]
    temperatura = data["data"]["temperature"]
    condicao = data["data"]["condition"]
    umidade = data["data"]["humidity"]
    vento = data["data"]["wind_velocity"]

    # Exibindo os dados
    print(f"🌍 Cidade: {cidade}")
    print(f"🌡️ Temperatura: {temperatura}°C")
    print(f"💧 Umidade: {umidade}%")
    print(f"🌪️ Velocidade do Vento: {vento} km/h")
    print(f"🌤️ Condição do tempo: {condicao}")

else:
    print("Erro ao obter os dados. Verifique sua API Key e tente novamente.")
