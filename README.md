# dashboard-streamlit-upe

## 1. Instalação do Streamlit

Primeiro, se preferir, usa uma máquina virtual pra instalar o streamlit pq ele dá problema com algumas versões do Python, mas não é necessário.

Stremlit é uma biblioteca Python, então pode instalar normalmente usando o pip no terminal do Win.

```bash
pip install streamlit
```

Pra conferir se deu certo digita:

```bash
streamlit hello
```

Vai abrir uma aba no navegador.

---

## 2. Instalação das bibliotecas necessárias

Instala as outras bibliotecas necessárias para fazer os gráficos. Ai vai da preferência/necessidade, até agora só usei plotly e pandas.

```bash
pip install plotly
pip install pandas
```

---

## 3. Executando o dashboard

O resto é intuitivo vc olhando o código desse repositório.

Quando quiser reproduzir na sua máquina tem que abrir o terminal na pasta em que o código tá e usar o comando:

```bash
streamlit run .\dashboard.py --server.port 8888
```

Vai abrir uma aba no navegador na porta 8888 mostrando o que vc programou.

---

## 4. Estrutura básica do código em Streamlit

A estrutura do código em streamlit basicamente sempre vai ser:

1. upload do dataset  
2. tratamento de dados (caso seu CSV não já tenha passado por um tratamento no Apachehop etc)  
3. escolha dos filtros (os atributos que ficam no menu lateral)  
4. os gráficos