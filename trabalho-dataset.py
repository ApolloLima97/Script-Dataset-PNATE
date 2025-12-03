import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns

# === Caminho do CSV ===
ARQ = r"C:\Users\PcGamer GTX 1050ti\OneDrive - MODULAR\Área de Trabalho\FATEC\analisys-fatec-v1\PNATE - REPASSES.csv"

# === Mapeamento UF -> Região ===
UF_TO_REGIAO = {}
UF_TO_REGIAO.update(dict.fromkeys(["AC", "AP", "AM", "PA", "RO", "RR", "TO"], "Norte"))
UF_TO_REGIAO.update(dict.fromkeys(["AL", "BA", "CE", "MA", "PB", "PE", "PI", "RN", "SE"], "Nordeste"))
UF_TO_REGIAO.update(dict.fromkeys(["DF", "GO", "MS", "MT"], "Centro-Oeste"))
UF_TO_REGIAO.update(dict.fromkeys(["ES", "MG", "RJ", "SP"], "Sudeste"))
UF_TO_REGIAO.update(dict.fromkeys(["PR", "RS", "SC"], "Sul"))


# === Funções utilitárias ===
def brl_para_float(serie: pd.Series) -> pd.Series:
    """
    Converte textos como 'R$ 8.852.407,34' -> 8852407.34 (float).
    Se o CSV vier com números inteiros em centavos, eles permanecerão como números.
    """
    s = serie.astype(str)
    s = s.str.replace(r'\s+', '', regex=True)
    s = s.str.replace('R$', '', regex=False)
    s = s.str.replace('.', '', regex=False)  # remove pontos de milhar
    s = s.str.replace(',', '.', regex=False)  # vírgula -> ponto
    s = s.str.replace(r'[^0-9\.\-]', '', regex=True)
    return pd.to_numeric(s, errors='coerce')


def em_reais(serie: pd.Series) -> pd.Series:
    """Converte de centavos para reais dividindo por 100."""
    return serie / 100.0


def estatisticas(dados):
    """Recebe Série numérica em CENTAVOS e retorna (em reais): média, mediana, moda, mínimo, máximo."""
    dados_r = em_reais(dados)
    media = round(dados_r.mean(skipna=True), 2)
    mediana = round(dados_r.median(skipna=True), 2)
    moda_s = dados_r.mode(dropna=True)
    moda = None if moda_s.empty else round(float(moda_s.iat[0]), 2)
    minimo = round(dados_r.min(skipna=True), 2)
    maximo = round(dados_r.max(skipna=True), 2)
    return media, mediana, moda, minimo, maximo


def fmt_moeda(v):
    """Formata números (reais) como 'R$ 1.234,56'."""
    try:
        valor = float(v)
        return f"R${valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
    except (ValueError, TypeError):
        return str(v)


def plot_pizza_por_regiao(df_base: pd.DataFrame, col: str, titulo_sufixo: str = ""):
    """Usa valores em CENTAVOS na coluna 'col' e plota pizza em REAIS (divide por 100 aqui)."""
    if "Sigla_uf" not in df_base.columns:
        print("Coluna 'Sigla_uf' não encontrada. Pulando pizza.")
        return

    valores_cent = brl_para_float(df_base[col])
    tmp = pd.DataFrame({"Sigla_uf": df_base["Sigla_uf"], col: em_reais(valores_cent)})
    tmp["Sigla_uf"] = tmp["Sigla_uf"].astype(str).str.strip().str.upper()
    tmp["Regiao"] = tmp["Sigla_uf"].map(UF_TO_REGIAO)
    tmp = tmp.loc[tmp["Regiao"].notna() & (tmp[col] > 0), ["Regiao", col]]

    if tmp.empty:
        print("Sem valores positivos para montar a pizza por regiões.")
        return

    totais = (
        tmp.groupby("Regiao")[col]
        .sum()
        .reindex(["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"])
        .fillna(0.0)
    )

    if totais.sum() <= 0:
        print("Soma total zero após filtro.")
        return

    def autopct_brl(pct):
        total = totais.sum()
        valor = pct / 100 * total
        txt = f"R${valor:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        return f"{pct:0.1f}%\n{txt}"

    fig, ax = plt.subplots(figsize=(7, 7))
    wedges, _, _ = ax.pie(
        totais.values,
        labels=totais.index,
        autopct=autopct_brl,
        startangle=90,
        counterclock=False
    )
    ax.set_title(f"Participação por Região – {col}{titulo_sufixo}")
    ax.axis('equal')

    labels_leg = [
        f"{reg} – " + f"R${val:,.0f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        for reg, val in zip(totais.index, totais.values)
    ]
    ax.legend(wedges, labels_leg, title="Totais", loc="center left", bbox_to_anchor=(1, 0.5))
    plt.tight_layout()
    plt.show()


# === Leitura do CSV ===
if not Path(ARQ).exists():
    raise FileNotFoundError(f"Arquivo não encontrado: {ARQ}")

df = pd.read_csv(ARQ, sep=None, engine='python', encoding='latin1', decimal=',')
df.columns = [c.strip() for c in df.columns]

# Base limpa e padronizada (aplica-se a TODAS as opções)
base = df.copy()
if "Sigla_uf" in base.columns:
    base["Sigla_uf"] = base["Sigla_uf"].astype(str).str.strip().str.upper()

# Exclui 'SECRETARIA' em todos os cenários
if "Entidade_executora" in base.columns:
    base = base[~base["Entidade_executora"].str.contains("SECRETARIA", case=False, na=False)].copy()


# === Loop Principal ===
while True:
    print("\nDeseja filtrar os dados?")
    print("1 - Analisar todos os estados e municípios")
    print("2 - Escolher um estado (Sigla_uf)")
    print("3 - Escolher um município específico")
    print("0 - Encerrar programa")

    opcao_filtro = input("Digite o número da opção: ")

    if opcao_filtro == "0":
        print("\nPrograma encerrado.")
        break

    df_filtro = base.copy()
    titulo_filtro = " (Brasil)"

    if opcao_filtro == "2":
        estados = sorted(base["Sigla_uf"].dropna().unique())
        print("\nEstados disponíveis:", ", ".join(estados))
        uf = input("Digite a sigla do estado (ex: SP): ").upper().strip()
        df_filtro = base[base["Sigla_uf"] == uf].copy()
        titulo_filtro = f" (Estado - {uf})"

    elif opcao_filtro == "3":
        municipio = input("Digite o nome do município: ").upper().strip()
        df_tmp = base.copy()
        df_tmp["Nome_municipio"] = df_tmp["Nome_municipio"].astype(str).str.upper().str.strip()
        df_filtro = df_tmp[df_tmp["Nome_municipio"] == municipio].copy()
        titulo_filtro = f" (Municipio - {municipio})"

    if df_filtro.empty:
        print("Nenhum dado encontrado para esse filtro.")
        continue

    print("\nEscolha a coluna para análise:")
    print("1 - Prev_ed_infantil")
    print("2 - Prev_ens_fundamental")
    print("3 - Prev_ens_medio")
    col_op = input("Digite o número da coluna: ")

    match col_op:
        case "1":
            col = "Prev_ed_infantil"
        case "2":
            col = "Prev_ens_fundamental"
        case "3":
            col = "Prev_ens_medio"
        case _:
            print("Opção inválida.")
            continue

    # Converter colunas de interesse para numérico (centrado em CENTAVOS na base)
    cols = ["Prev_ed_infantil", "Prev_ens_fundamental", "Prev_ens_medio"]
    if set(cols).issubset(df_filtro.columns):
        df_filtro[cols] = df_filtro[cols].apply(brl_para_float)

    # Série base (CENTAVOS)
    dados_geral = df_filtro[col]
    dados_sem_zeros = df_filtro.loc[df_filtro[col] > 0, col]

    # Estatísticas (em REAIS)
    media_g, mediana_g, moda_g, minimo_g, maximo_g = estatisticas(dados_geral)
    media_s, mediana_s, moda_s, minimo_s, maximo_s = estatisticas(dados_sem_zeros)
    # Soma total (em reais)
    soma_g = round(em_reais(dados_geral.sum()), 2)
    soma_s = round(em_reais(dados_sem_zeros.sum()), 2)
    
    print("=" * 65)
    print(f"{'Medida':<12} | {'Com zeros':^22} | {'Sem zeros':^22}")
    print("-" * 65)
    linhas = [
        ("Média", media_g, media_s),
        ("Mediana", mediana_g, mediana_s),
        ("Moda", moda_g, moda_s),
        ("Mínimo", minimo_g, minimo_s),
        ("Máximo", maximo_g, maximo_s),
        ("Soma total", soma_g,    soma_s), 
    ]
    for nome, val_g, val_s in linhas:
        vg, vs = fmt_moeda(val_g), fmt_moeda(val_s)
        if vg.startswith("R$"):
            vg = f"{vg[:2]:<3}{vg[2:]:>18}"
        if vs.startswith("R$"):
            vs = f"{vs[:2]:<3}{vs[2:]:>18}"
        print(f"{nome:<12} | {vg:>22} | {vs:>22}")
    print("=" * 65)
    print(f"Tipo de dado: {df_filtro[col].dtype} | N nulos: {df_filtro[col].isna().sum()}")

    

    # === Gráficos ===

    # 1️⃣ Barras comparando os três níveis (converter para REAIS aqui)
    if set(cols).issubset(df_filtro.columns):
        totais_reais = em_reais(df_filtro[cols].sum())

        plt.figure(figsize=(7, 5))
        sns.barplot(
            x=totais_reais.index,
            y=totais_reais.values,
            hue=totais_reais.index,
            palette="coolwarm",
            legend=False
        )

        plt.title(f"Totais Previstos por Etapa de Ensino – Nível{titulo_filtro}",
                  fontsize=13, fontweight='bold')
        plt.xlabel("Etapa de Ensino")
        plt.ylabel("Total Previsto (R$)")
        plt.xticks(rotation=15)
        plt.tight_layout()
        plt.show()

        # 2️⃣ Pizza por região (já converte para reais dentro da função)
        plot_pizza_por_regiao(df_filtro, col, titulo_sufixo=f" – Nível{titulo_filtro}")

        # 3️⃣ Boxplot comparativo entre os três níveis (AGREGADO POR ESTADO)
        cols_box = ["Prev_ed_infantil", "Prev_ens_fundamental", "Prev_ens_medio"]

        if set(cols_box).issubset(df_filtro.columns):
            df_box = df_filtro[["Sigla_uf"] + cols_box].copy()
            df_box["Sigla_uf"] = df_box["Sigla_uf"].astype(str).str.strip().str.upper()
            df_box[cols_box] = df_box[cols_box].apply(brl_para_float)

            df_estado = (
                df_box.groupby("Sigla_uf")[cols_box]
                .sum()
                .apply(em_reais)
                .reset_index()
            )

            df_estado = df_estado.melt(
                id_vars="Sigla_uf", var_name="Etapa", value_name="Valor_R$"
            )
            df_estado["Regiao"] = df_estado["Sigla_uf"].map(UF_TO_REGIAO)

            plt.figure(figsize=(8, 5))
            sns.boxplot(
                x="Etapa",
                y="Valor_R$",
                hue="Etapa",
                data=df_estado,
                palette="Greens",
                width=0.5,
                legend=False
            )
            plt.yscale("log")
            plt.title(
                f"Distribuição dos Investimentos por Etapa de Ensino – Nível{titulo_filtro}",
                fontsize=13,
                fontweight="bold"
            )
            plt.xlabel("Etapa de Ensino")
            plt.ylabel("Valor (R$) – Escala Logarítmica")
            plt.tight_layout()
            plt.show()

        # === Função: Dispersão por estado ===
        def plot_dispersao_estado(df_filtro, xcol, ycol, uf_to_regiao):
            df_estado = df_filtro[["Sigla_uf", xcol, ycol]].copy()
            df_estado["Sigla_uf"] = df_estado["Sigla_uf"].astype(str).str.strip().str.upper()
            df_estado[[xcol, ycol]] = df_estado[[xcol, ycol]].apply(brl_para_float)
            df_estado = df_estado.groupby("Sigla_uf")[[xcol, ycol]].sum().apply(em_reais)
            df_estado["Regiao"] = df_estado.index.map(uf_to_regiao)

            plt.figure(figsize=(8, 6))
            sns.scatterplot(
                x=xcol, y=ycol, hue="Regiao", data=df_estado,
                s=120, alpha=0.85, palette="coolwarm", edgecolor="black"
            )

            nomes = {
                "Prev_ed_infantil": "Educação Infantil",
                "Prev_ens_fundamental": "Ensino Fundamental",
                "Prev_ens_medio": "Ensino Médio",
            }

            #plt.title(
                #f"Correlação Estadual – {nomes.get(ycol)} × {nomes.get(xcol)} {titulo_filtro}",
                #fontsize=13, fontweight="bold"
            #)
            plt.xlabel(nomes.get(xcol, xcol) + " (R$)")
            plt.ylabel(nomes.get(ycol, ycol) + " (R$)")
            plt.legend(title="Região", loc="upper left")
            plt.grid(True, linestyle="--", alpha=0.4)
            plt.tight_layout()
            plt.show()

        # === Gera automaticamente as 3 combinações ===
        pares_estaduais = [
            ("Prev_ed_infantil", "Prev_ens_fundamental"),
            ("Prev_ed_infantil", "Prev_ens_medio"),
            ("Prev_ens_fundamental", "Prev_ens_medio"),
        ]

        for xcol, ycol in pares_estaduais:
            plot_dispersao_estado(df_filtro, xcol, ycol, UF_TO_REGIAO)

        # === GRÁFICO DE BARRAS COM VALOR EM CIMA ===
        totais_reais = em_reais(df_filtro[cols].sum())

        plt.figure(figsize=(7,5))
        ax = sns.barplot(
            x=["Educação Infantil", "Ensino Fundamental", "Ensino Médio"],
            y=totais_reais.values,
            palette="coolwarm",
            legend=False
        )

        # Remover título
        plt.title("")

        # Rótulos do eixo X
        plt.xlabel("Etapa de Ensino")
        plt.ylabel("Total Previsto (R$)")
        plt.xticks(rotation=0)

        # Inserir valores em cima das barras
        for i, v in enumerate(totais_reais.values):
            ax.text(
                i,
                v,
                f"R${v:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
                ha='center',
                va='bottom',
                fontsize=10,
                fontweight='bold'
            )

        plt.tight_layout()
        plt.show()


    continuar = input("\nDeseja realizar outra análise? (S/N): ").strip().upper()
    if continuar != "S":
        print("\nPrograma encerrado.")
        break
