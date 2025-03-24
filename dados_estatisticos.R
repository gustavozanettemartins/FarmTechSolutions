# Solicita ao usuário o caminho completo do arquivo CSV
caminho_csv <- readline(prompt = "Digite o caminho completo(absoluto) do arquivo CSV: ")

# Lê os dados do arquivo CSV
# Ajuste 'sep' e 'dec' conforme o formato do seu CSV
dados <- read.csv(caminho_csv, sep = ";", dec = ".", header = TRUE, stringsAsFactors = FALSE)

# Verifica se há dados no arquivo
if(nrow(dados) == 0) {
  stop("O arquivo CSV não contém dados.")
}

# Cálculo das médias
media_plantas_por_rua <- mean(dados$qtd_plantas_total / dados$qtd_ruas)
media_custo_por_planta <- mean(dados$custo_total / dados$qtd_plantas_total)
media_custo_por_rua <- mean(dados$custo_total / dados$qtd_ruas)

# Cálculo dos desvios padrão, tratando o caso de apenas uma linha (retorna 0)
desvio_plantas_por_rua <- if(nrow(dados) > 1) sd(dados$qtd_plantas_total / dados$qtd_ruas) else 0
desvio_custo_por_planta <- if(nrow(dados) > 1) sd(dados$custo_total / dados$qtd_plantas_total) else 0
desvio_custo_por_rua <- if(nrow(dados) > 1) sd(dados$custo_total / dados$qtd_ruas) else 0

# Impressão dos resultados
cat("Média de plantas por rua:", media_plantas_por_rua, "\n")
cat("Desvio padrão (plantas por rua):", desvio_plantas_por_rua, "\n\n")

cat("Média de custo por planta:", media_custo_por_planta, "\n")
cat("Desvio padrão (custo por planta):", desvio_custo_por_planta, "\n\n")

cat("Média de custo por rua:", media_custo_por_rua, "\n")
cat("Desvio padrão (custo por rua):", desvio_custo_por_rua, "\n")

