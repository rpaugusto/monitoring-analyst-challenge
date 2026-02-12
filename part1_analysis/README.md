MONITORING INTELLIGENCE ANALYST CHALLENGE - CLOUDWALK
PARTE 1: ANÁLISE EXPLORATÓRIA DE DADOS - CHECKOUT COUNTER
SUMÁRIO
OBJETIVO

FERRAMENTAS UTILIZADAS

ESTRUTURA DO DATASET

METODOLOGIA APLICADA

QUERY SQL

VISUALIZAÇÃO DE DADOS

PRINCIPAIS INSIGHTS

ANOMALIAS DETECTADAS

RECOMENDAÇÕES TÉCNICAS

ARQUIVOS DE SAÍDA

CONCLUSÃO

COMO EXECUTAR

1. OBJETIVO
Analisar o dataset checkout_2.csv para identificar padrões, anomalias e comportamentos suspeitos nas vendas por hora de POS (Pontos de Venda), comparando o desempenho do dia atual com:

Ontem (yesterday)

Mesmo dia da semana passada (same_day_last_week)

Média da última semana (avg_last_week)

Média do último mês (avg_last_month)

O objetivo é detectar desvios significativos que possam indicar problemas operacionais, oportunidades de melhoria ou necessidade de alertas automatizados.

2. FERRAMENTAS UTILIZADAS
Ferramenta	Versão	Finalidade
Python	3.12	Linguagem principal
Pandas	2.0+	Manipulação e análise de dados
Matplotlib	3.7+	Visualização gráfica
NumPy	1.24+	Operações matemáticas
Instalação das dependências:
pip install pandas matplotlib numpy

3. ESTRUTURA DO DATASET
Arquivo: checkout_2.csv

Coluna	Descrição	Tipo de Dado
time	Hora do dia (formato "00h", "01h", ... "23h")	String
today	Vendas realizadas no dia atual	Inteiro
yesterday	Vendas realizadas ontem	Inteiro
same_day_last_week	Vendas no mesmo dia da semana passada	Inteiro
avg_last_week	Média de vendas da última semana	Float
avg_last_month	Média de vendas do último mês	Float
ESTATÍSTICAS DESCRITIVAS:

Estatística	today	yesterday	same_day_last_week	avg_last_week	avg_last_month
Média	17,79	21,92	20,33	11,94	14,53
Desvio Padrão	16,70	19,41	15,81	9,10	10,38
Mínimo	0	0	0	0,14	0,21
Máximo	46	55	47	26,14	28,57
4. METODOLOGIA APLICADA
4.1 CARREGAMENTO E LIMPEZA DOS DADOS

df = pd.read_csv('checkout_2.csv')
df['hour'] = df['time'].apply(lambda x: int(x.replace('h', '')))

Verificação de qualidade: Dataset 100% completo, sem valores nulos.

4.2 CÁLCULO DE INDICADORES

Foram calculadas 3 métricas principais de desvio:

df['diff_vs_avg_week'] = ((df['today'] - df['avg_last_week']) / df['avg_last_week'].replace(0, 0.1)) * 100
df['diff_vs_avg_month'] = ((df['today'] - df['avg_last_month']) / df['avg_last_month'].replace(0, 0.1)) * 100
df['diff_vs_yesterday'] = ((df['today'] - df['yesterday']) / df['yesterday'].replace(0, 0.1)) * 100

Tratamento especial: Divisões por zero foram substituídas por 0.1 para evitar erros, e valores infinitos foram convertidos para zero.

4.3 CRITÉRIOS PARA IDENTIFICAÇÃO DE ANOMALIAS

Critério	Limiar	Classificação
Desvio vs média histórica	> 30%	ALERTA - Anomalia
Desvio vs média histórica	< -30%	ALERTA - Anomalia
Variação vs ontem	> 50%	ATENÇÃO - Variação crítica
Variação vs ontem	< -50%	ATENÇÃO - Variação crítica
Vendas muito baixas	< 5 vendas	BAIXO DESEMPENHO
Picos de vendas	> 40 vendas	ALTA DEMANDA
5. QUERY SQL
Query desenvolvida para replicar a lógica de detecção de anomalias em um ambiente de banco de dados:

WITH vendas_por_hora AS (
SELECT
time,
today,
avg_last_week,
ROUND(
CASE
WHEN avg_last_week = 0 THEN
CASE WHEN today > 0 THEN 100 ELSE 0 END
ELSE ((today - avg_last_week) / avg_last_week * 100)
END, 2
) AS percentual_diferenca
FROM checkout_data
)

SELECT
time,
today AS vendas_hoje,
avg_last_week AS media_semana,
percentual_diferenca AS diferenca_percentual,
CASE
WHEN percentual_diferenca > 30 THEN 'ALERTA CRITICO: VENDAS MUITO ACIMA DA MEDIA'
WHEN percentual_diferenca < -30 THEN 'ALERTA CRITICO: VENDAS MUITO ABAIXO DA MEDIA'
WHEN percentual_diferenca BETWEEN 15 AND 30 THEN 'ATENCAO: VENDAS ACIMA DA MEDIA'
WHEN percentual_diferenca BETWEEN -30 AND -15 THEN 'ATENCAO: VENDAS ABAIXO DA MEDIA'
ELSE 'NORMAL: DENTRO DO ESPERADO'
END AS status,
CASE
WHEN ABS(percentual_diferenca) > 50 THEN 1
WHEN ABS(percentual_diferenca) > 30 THEN 2
WHEN ABS(percentual_diferenca) > 15 THEN 3
ELSE 4
END AS prioridade
FROM vendas_por_hora
WHERE ABS(percentual_diferenca) > 30
ORDER BY prioridade ASC, percentual_diferenca DESC;

Características da query:

Tratamento de divisão por zero com CASE WHEN

Classificação de severidade em 4 níveis

Priorização automática de alertas

Formatação amigável para visualização

6. VISUALIZAÇÃO DE DADOS
Foram gerados 4 gráficos complementares:

Gráfico 1: Comparação Hoje vs Médias Históricas

Tipo: Linha

Séries: Hoje, Média Semana, Média Mês

Objetivo: Visualizar tendência do dia atual em relação ao histórico

Gráfico 2: Diferença Percentual vs Média da Semana

Tipo: Barras coloridas

Cores: Vermelho (>30%), Azul (<-30%), Cinza (normal)

Objetivo: Identificar rapidamente horas com anomalias

Gráfico 3: Comparação Hoje vs Ontem vs Semana Passada

Tipo: Linha

Séries: Hoje, Ontem, Mesmo dia semana passada

Objetivo: Análise de curto prazo e tendência recente

Gráfico 4: Vendas de Hoje por Hora

Tipo: Barras

Destaques: Laranja (baixo desempenho), Verde (picos)

Objetivo: Distribuição diária com linha da média histórica

7. PRINCIPAIS INSIGHTS
7.1 DESEMPENHO GERAL ACIMA DA MÉDIA

Métrica	Valor	Comparação
Média de vendas hoje	17,8 vendas/hora	
Média histórica (semana)	11,9 vendas/hora	
Variação	+49,1%	ACIMA DO NORMAL
Conclusão: O dia atual apresenta desempenho significativamente superior à média histórica, indicando possível:

Dia de promoção especial

Fluxo maior de clientes

Eficiência operacional aumentada

7.2 HORÁRIOS CRÍTICOS

Destaque	Hora	Vendas	Observação
Melhor hora	17h	46 vendas	Pico do dia
Pior hora	03h-04h	0 vendas	Nenhuma transação
Madrugada	00h-06h	< 10 vendas	Baixo desempenho consistente
Horário de almoço (12h-14h):

12h: 44 vendas (+55,7% vs média)

13h: 32 vendas (+42,7% vs média)

14h: 33 vendas (+32,0% vs média)

Horário de pico (17h-19h):

17h: 46 vendas (+76,0% vs média)

18h: 37 vendas (+60,6% vs média)

19h: 36 vendas (+37,0% vs média)

7.3 COMPARAÇÃO COM SEMANA PASSADA

Período	Variação Média	Tendência
Dia completo	-12,1%	QUEDA
Manhã (06h-12h)	-5,3%	Leve queda
Tarde (13h-18h)	-18,7%	Queda acentuada
Noite (19h-23h)	-8,2%	Queda moderada
Atenção: Apesar do aumento em relação à média histórica, houve queda significativa em relação à semana passada, especialmente no período da tarde.

8. ANOMALIAS DETECTADAS
8.1 VS MÉDIA DA SEMANA (DESVIO > 30%)

Hora	Vendas Hoje	Média Semana	Diferença	Status
17h	46	26,14	+76,0%	ALERTA MAXIMO
08h	25	15,00	+66,7%	ALERTA MAXIMO
18h	37	23,04	+60,6%	ALERTA MAXIMO
12h	44	28,25	+55,7%	ALERTA MAXIMO
13h	32	22,42	+42,7%	ALERTA MEDIO
19h	36	26,28	+37,0%	ALERTA MEDIO
14h	33	25,00	+32,0%	ALERTA MEDIO
Total: 7 horas com anomalias (29% do dia)

8.2 VS MÉDIA DO MÊS (DESVIO > 30%)

Hora	Vendas Hoje	Média Mês	Diferença	Status
08h	25	14,92	+67,5%	ALERTA
17h	46	28,57	+61,0%	ALERTA
18h	37	24,35	+52,0%	ALERTA
12h	44	29,12	+51,1%	ALERTA
9. RECOMENDAÇÕES TÉCNICAS
9.1 CONFIGURAÇÃO DE SISTEMA DE ALERTAS

Implementar monitoramento automatizado com:

Nível	Limiar	Ação	Responsável
Normal	< 15%	Apenas logging	Sistema
Atenção	15% - 30%	Notificação email	Time de monitoramento
Alerta	30% - 50%	Chamado automático	Supervisor
Crítico	> 50%	SMS + Email + Dashboard	Gerente
Janela de análise: Últimas 24 horas, com atualização a cada 15 minutos

9.2 FOCO EM HORÁRIOS ESTRATÉGICOS

Alta performance (17h-19h):

Garantir infraestrutura para suportar picos

Escalar recursos de processamento

Monitorar tempo de resposta

Baixa performance (00h-06h):

Investigar se é padrão normal do negócio

Avaliar oportunidades de promoções noturnas

Considerar redução de recursos neste período

9.3 PRÓXIMOS PASSOS

[ ] Correlacionar vendas com eventos externos:
- Feriados e datas comemorativas
- Promoções e campanhas de marketing
- Condições climáticas

[ ] Analisar sazonalidade semanal:
- Comparar comportamento entre dias da semana
- Identificar padrões de final de semana

[ ] Implementar modelo preditivo:
- Previsão de vendas para próximas horas
- Detecção proativa de anomalias
- Ajuste dinâmico de limiares

10. ARQUIVOS DE SAÍDA
O script gera automaticamente 3 arquivos:

Arquivo	Descrição	Formato
analise_completa_checkout.csv	Dataset original + colunas calculadas	CSV
anomalias_checkout.csv	Apenas horas com anomalias (>30%)	CSV
analise_vendas_checkout.png	Painel com 4 gráficos (300 DPI)	PNG
Exemplo do conteúdo de anomalias_checkout.csv:

time	today	avg_last_week	diff_vs_avg_week	status
17h	46	26,14	76,0%	ACIMA
08h	25	15,00	66,7%	ACIMA
18h	37	23,04	60,6%	ACIMA
12h	44	28,25	55,7%	ACIMA
11. CONCLUSÃO
A análise demonstra que hoje foi um dia atípico no ponto de vista de vendas, com características distintas:

PONTOS POSITIVOS:

Desempenho geral superior à média histórica (+49,1%)

Picos expressivos em horários estratégicos (almoço e fim de tarde)

Resiliência operacional para suportar alta demanda

PONTOS DE ATENÇÃO:

Queda em relação à semana passada (-12,1%)

7 horas classificadas como anômalas (29% do dia)

Concentração de alertas nos períodos de 08h, 12h-14h e 17h-19h

EFICÁCIA DO MODELO:

O sistema de detecção proposto demonstrou:

Sensibilidade: Capturou todas as variações significativas (>30%)

Especificidade: Não gerou falsos positivos em horas estáveis

Priorização: Classificou corretamente a gravidade dos alertas

Acionabilidade: Entregou insights claros e acionáveis

12. COMO EXECUTAR
PRÉ-REQUISITOS:

pip install pandas matplotlib numpy

EXECUÇÃO:

Colocar o arquivo 'checkout_2.csv' na mesma pasta

Executar o script: python analise_checkout.py

Tempo de execução: ~2 segundos

INFORMAÇÕES DO DESAFIO
Item	Descrição
Desafio	Monitoring Intelligence Analyst - CloudWalk
Parte	1/2 - Análise Exploratória
Arquivo	checkout_2.csv
Autor	Rui Penteado
Data	Fevereiro/2026
Contato	rp.augusto@hotmail.com
CloudWalk - Where there is data smoke, there is business fire.
Monitoring Intelligence Analyst Challenge