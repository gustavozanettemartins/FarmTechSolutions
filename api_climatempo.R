library(httr)
library(jsonlite)

# Substitua pela sua API Key da ClimaTempo
api_key <- "31b462e81363e22b5904546c9130f24b"
city_id <- "5099"  # Braço do Norte, SC

# URL da API para obter o clima atual
url <- sprintf("http://apiadvisor.climatempo.com.br/api/v1/weather/locale/%s/current?token=%s", city_id, api_key)

# Fazendo a requisição para a API
response <- GET(url)

# Verificando se a resposta foi bem-sucedida
if (status_code(response) == 200) {
  # Converte a resposta para uma lista R a partir do JSON
  data <- content(response, as = "parsed", type = "application/json")
  
  cidade <- data$name
  temperatura <- data$data$temperature
  condicao <- data$data$condition
  umidade <- data$data$humidity
  vento <- data$data$wind_velocity
  
  # Exibindo os dados
  cat("🌍 Cidade:", cidade, "\n")
  cat("🌡️ Temperatura:", temperatura, "°C\n")
  cat("💧 Umidade:", umidade, "%\n")
  cat("🌪️ Velocidade do Vento:", vento, "km/h\n")
  cat("🌤️ Condição do tempo:", condicao, "\n")
} else {
  cat("Erro ao obter os dados. Verifique sua API Key e tente novamente.\n")
}
