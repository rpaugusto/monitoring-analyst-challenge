"""
ANÁLISE DE ANOMALIAS EM VENDAS POR HORA
Arquivo: checkout_2.csv
Formato: time = "00h", "01h", etc.
"""

# Importando bibliotecas necessárias
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# ==================== 1. CARREGAR OS DADOS ====================
print("=== CARREGANDO DADOS ===")

# Carregar o arquivo CSV
df = pd.read_csv('checkout_2.csv')

# Mostrar as primeiras linhas para entender a estrutura
print("\nPrimeiras 5 linhas do arquivo:")
print(df.head())

# Verificar informações básicas do dataset
print("\nInformações do dataset:")
print(df.info())

print("\nEstatísticas básicas:")
print(df.describe())

# ==================== 2. LIMPAR E PREPARAR OS DADOS ====================
print("\n=== PREPARANDO DADOS ===")

# Verificar se há valores nulos
print(f"Valores nulos por coluna:\n{df.isnull().sum()}")

# CORREÇÃO: Extrair hora do formato "00h", "01h", etc.
df['hour'] = df['time'].apply(lambda x: int(x.replace('h', '')))

# Criar uma coluna de hora formatada para os gráficos
df['hour_formatted'] = df['time']

print("\nDados preparados (primeiras 5 linhas):")
print(df[['time', 'hour', 'today', 'yesterday', 'avg_last_week']].head())

# ==================== 3. ANÁLISE DE ANOMALIAS ====================
print("\n=== ANALISANDO ANOMALIAS ===")

# 3.1 COMPARAR HOJE COM A MÉDIA DA ÚLTIMA SEMANA
print("\n--- Comparação: Hoje vs Média da Última Semana ---")

# Calcular a diferença percentual
df['diff_vs_avg_week'] = ((df['today'] - df['avg_last_week']) / df['avg_last_week'].replace(0, 0.1)) * 100
df['diff_vs_avg_month'] = ((df['today'] - df['avg_last_month']) / df['avg_last_month'].replace(0, 0.1)) * 100

# Substituir infinitos por 0 (quando a média é 0)
df['diff_vs_avg_week'] = df['diff_vs_avg_week'].replace([np.inf, -np.inf], 0)
df['diff_vs_avg_month'] = df['diff_vs_avg_month'].replace([np.inf, -np.inf], 0)

# Identificar anomalias: diferença > 30% para mais ou para menos
anomalias_week = df[abs(df['diff_vs_avg_week']) > 30]
anomalias_month = df[abs(df['diff_vs_avg_month']) > 30]

print(f"Total de horas com anomalia vs última semana: {len(anomalias_week)}")
print(f"Total de horas com anomalia vs último mês: {len(anomalias_month)}")

# Mostrar as anomalias encontradas
if len(anomalias_week) > 0:
    print("\n⚠️ Horas com anomalia (vs última semana):")
    for idx, row in anomalias_week.iterrows():
        if row['diff_vs_avg_week'] > 0:
            tipo = "📈 ACIMA"
        else:
            tipo = "📉 ABAIXO"
        print(f"  {row['time']}: {tipo} - {abs(row['diff_vs_avg_week']):.1f}% diferente")
else:
    print("  Nenhuma anomalia encontrada vs última semana!")

# 3.2 COMPARAR HOJE COM ONTEM
print("\n--- Comparação: Hoje vs Ontem ---")

df['diff_vs_yesterday'] = ((df['today'] - df['yesterday']) / df['yesterday'].replace(0, 0.1)) * 100
df['diff_vs_yesterday'] = df['diff_vs_yesterday'].replace([np.inf, -np.inf], 0)
anomalias_yesterday = df[abs(df['diff_vs_yesterday']) > 50]  # 50% de diferença

print(f"Total de horas com grande diferença vs ontem: {len(anomalias_yesterday)}")

if len(anomalias_yesterday) > 0:
    print("Horas com grande diferença vs ontem:")
    for idx, row in anomalias_yesterday.iterrows():
        if row['diff_vs_yesterday'] > 0:
            print(f"  {row['time']}: +{row['diff_vs_yesterday']:.1f}% maior que ontem")
        else:
            print(f"  {row['time']}: {row['diff_vs_yesterday']:.1f}% menor que ontem")

# 3.3 ENCONTRAR PADRÕES SUSPEITOS
print("\n--- Padrões Suspeitos ---")

# Encontrar horas com vendas muito baixas (abaixo de 5)
baixas_vendas = df[df['today'] < 5]
print(f"Horas com vendas muito baixas (<5):")
if len(baixas_vendas) > 0:
    for idx, row in baixas_vendas.iterrows():
        print(f"  {row['time']}: {row['today']} vendas")
else:
    print("  Nenhuma hora com vendas muito baixas")

# Encontrar picos de vendas (acima de 40)
picos_vendas = df[df['today'] > 40]
print(f"\nHoras com picos de vendas (>40):")
if len(picos_vendas) > 0:
    for idx, row in picos_vendas.iterrows():
        print(f"  {row['time']}: {row['today']} vendas")
else:
    print("  Nenhum pico de vendas encontrado")

# ==================== 4. QUERY SQL SIMULADA ====================
print("\n=== QUERY SQL PARA ENCONTRAR ANOMALIAS ===")

sql_query = """
-- Query para encontrar horas com anomalias
-- Consideramos anomalia quando as vendas de hoje estão 30% acima ou abaixo da média da semana

SELECT 
    time,
    today,
    avg_last_week,
    ROUND(((today - avg_last_week) / NULLIF(avg_last_week, 0) * 100), 2) AS percentual_diferenca,
    CASE 
        WHEN ((today - avg_last_week) / NULLIF(avg_last_week, 0) * 100) > 30 THEN '🔴 ALERTA: VENDAS MUITO ACIMA'
        WHEN ((today - avg_last_week) / NULLIF(avg_last_week, 0) * 100) < -30 THEN '🔵 ALERTA: VENDAS MUITO ABAIXO'
        ELSE '🟢 NORMAL'
    END AS status
FROM vendas_por_hora
WHERE ABS((today - avg_last_week) / NULLIF(avg_last_week, 0) * 100) > 30
ORDER BY percentual_diferenca DESC;
"""

print(sql_query)

# ==================== 5. GRÁFICOS ====================
print("\n=== GERANDO GRÁFICOS ===")

# Configurar o estilo dos gráficos
plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('Análise de Vendas por Hora - Checkout', fontsize=16, fontweight='bold')

# GRÁFICO 1: Comparação Hoje vs Médias
ax1 = axes[0, 0]
ax1.plot(df['hour_formatted'], df['today'], marker='o', linewidth=2, label='Hoje', color='blue')
ax1.plot(df['hour_formatted'], df['avg_last_week'], marker='s', linewidth=2, label='Média Semana', color='green')
ax1.plot(df['hour_formatted'], df['avg_last_month'], marker='^', linewidth=2, label='Média Mês', color='orange')
ax1.set_title('Vendas: Hoje vs Médias Históricas', fontweight='bold')
ax1.set_xlabel('Hora do dia')
ax1.set_ylabel('Número de vendas')
ax1.legend()
ax1.grid(True, alpha=0.3)
ax1.tick_params(axis='x', rotation=45)

# GRÁFICO 2: Diferença Percentual vs Média da Semana
ax2 = axes[0, 1]
cores = ['red' if x > 30 else 'blue' if x < -30 else 'gray' for x in df['diff_vs_avg_week']]
barras = ax2.bar(df['hour_formatted'], df['diff_vs_avg_week'], color=cores, alpha=0.7)
ax2.axhline(y=30, color='red', linestyle='--', label='Limite superior (30%)')
ax2.axhline(y=-30, color='red', linestyle='--', label='Limite inferior (-30%)')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
ax2.set_title('Diferença Percentual: Hoje vs Média da Semana', fontweight='bold')
ax2.set_xlabel('Hora do dia')
ax2.set_ylabel('Diferença percentual (%)')
ax2.legend()
ax2.tick_params(axis='x', rotation=45)

# GRÁFICO 3: Comparação Hoje vs Ontem vs Semana Passada
ax3 = axes[1, 0]
ax3.plot(df['hour_formatted'], df['today'], marker='o', linewidth=2, label='Hoje', color='blue')
ax3.plot(df['hour_formatted'], df['yesterday'], marker='s', linewidth=2, label='Ontem', color='purple')
ax3.plot(df['hour_formatted'], df['same_day_last_week'], marker='^', linewidth=2, label='Semana passada', color='brown')
ax3.set_title('Comparação: Hoje, Ontem e Semana Passada', fontweight='bold')
ax3.set_xlabel('Hora do dia')
ax3.set_ylabel('Número de vendas')
ax3.legend()
ax3.grid(True, alpha=0.3)
ax3.tick_params(axis='x', rotation=45)

# GRÁFICO 4: Gráfico de Barras das Vendas de Hoje
ax4 = axes[1, 1]
cores_hoje = ['orange' if x < 5 else 'green' if x > 40 else 'steelblue' for x in df['today']]
barras = ax4.bar(df['hour_formatted'], df['today'], color=cores_hoje, alpha=0.7)
ax4.set_title('Vendas de Hoje por Hora', fontweight='bold')
ax4.set_xlabel('Hora do dia')
ax4.set_ylabel('Número de vendas')
ax4.axhline(y=df['avg_last_week'].mean(), color='red', linestyle='--', label=f'Média Semana: {df["avg_last_week"].mean():.1f}')
ax4.legend()
ax4.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('analise_vendas_checkout.png', dpi=300, bbox_inches='tight')
print("✅ Gráfico salvo como 'analise_vendas_checkout.png'")

# ==================== 6. RELATÓRIO DE INSIGHTS ====================
print("\n" + "="*60)
print("📊 RELATÓRIO DE ANOMALIAS E INSIGHTS")
print("="*60)

# Insight 1: Média geral
media_hoje = df['today'].mean()
media_historica = df['avg_last_week'].mean()
print(f"\n📊 INSIGHT 1: MÉDIA DE VENDAS")
print(f"   • Média de vendas hoje: {media_hoje:.1f} vendas/hora")
print(f"   • Média histórica (semana): {media_historica:.1f} vendas/hora")
print(f"   • Diferença: {((media_hoje - media_historica)/media_historica*100):.1f}%")

# Insight 2: Melhor e pior hora
melhor_hora = df.loc[df['today'].idxmax()]
pior_hora = df.loc[df['today'].idxmin()]
print(f"\n⏰ INSIGHT 2: MELHOR E PIOR HORA DO DIA")
print(f"   • Melhor hora: {melhor_hora['time']} - {melhor_hora['today']} vendas")
print(f"   • Pior hora: {pior_hora['time']} - {pior_hora['today']} vendas")

# Insight 3: Anomalias encontradas
print(f"\n⚠️ INSIGHT 3: ANOMALIAS IDENTIFICADAS")
print(f"   • Total de horas com anomalia (vs semana): {len(anomalias_week)}")
print(f"   • Total de horas com anomalia (vs mês): {len(anomalias_month)}")

if len(anomalias_week) > 0:
    print(f"\n   Horas críticas:")
    for idx, row in anomalias_week.iterrows():
        if row['diff_vs_avg_week'] > 0:
            print(f"     - {row['time']}: {row['diff_vs_avg_week']:.1f}% ACIMA do normal")
        else:
            print(f"     - {row['time']}: {abs(row['diff_vs_avg_week']):.1f}% ABAIXO do normal")

# Insight 4: Padrão semanal
print(f"\n📅 INSIGHT 4: COMPARAÇÃO COM MESMO DIA DA SEMANA PASSADA")
df['diff_vs_same_day'] = ((df['today'] - df['same_day_last_week']) / df['same_day_last_week'].replace(0, 0.1)) * 100
df['diff_vs_same_day'] = df['diff_vs_same_day'].replace([np.inf, -np.inf], 0)
media_diff_semana = df['diff_vs_same_day'].mean()
print(f"   • Diferença média vs mesmo dia semana passada: {media_diff_semana:.1f}%")
print(f"   • {'📈 AUMENTO' if media_diff_semana > 0 else '📉 QUEDA'} nas vendas em relação à semana passada")

# Insight 5: Recomendações
print(f"\n💡 INSIGHT 5: RECOMENDAÇÕES")
print(f"   • Configurar alertas para diferenças > 30% vs média histórica")
print(f"   • Investigar causas das horas com vendas muito baixas (madrugada)")
print(f"   • Analisar picos de vendas nas horas {melhor_hora['time']} para identificar oportunidades")
print(f"   • Monitorar horário das {pior_hora['time']} que tem baixo desempenho")

print("\n" + "="*60)
print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
print("="*60)

# ==================== 7. SALVAR RESULTADOS ====================
print("\n=== SALVANDO RESULTADOS ===")

# Salvar análise completa em CSV
df.to_csv('analise_completa_checkout.csv', index=False)
print("✅ Análise completa salva em 'analise_completa_checkout.csv'")

# Salvar apenas anomalias em CSV
if len(anomalias_week) > 0:
    anomalias_week.to_csv('anomalias_checkout.csv', index=False)
    print("✅ Anomalias salvas em 'anomalias_checkout.csv'")
else:
    print("ℹ️ Nenhuma anomalia encontrada para salvar")

print("\n🎉 TUDO PRONTO! Verifique os arquivos gerados na pasta.")