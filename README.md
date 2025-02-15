# Automação para Plataformas de E-commerce e ERP

Este projeto foi desenvolvido de forma independente para demonstrar minhas habilidades em automação e integração de plataformas. Ele automatiza tarefas recorrentes para diferentes plataformas, como ERP TINY, Mercado Livre, Magalu e OpenCart, com o objetivo de otimizar processos e economizar tempo.

## 📝 Descrição

Este repositório contém uma biblioteca de automação para as seguintes plataformas:

- **ERP TINY**
- **Mercado Livre**
- **Magalu**
- **OpenCart**

As automações foram criadas para facilitar a atualização de produtos, preços e exclusão de itens, com base em planilhas fornecidas pelo usuário.

## 🚟 Estrutura do Projeto

A estrutura do projeto está organizada da seguinte maneira:

- **/libraries**: Contém as bibliotecas de automação específicas para cada plataforma (TINY, Mercado Livre, Magalu e OpenCart).
- **/ajustar_produtos_opencart.py**: Arquivo independente para ajustar os produtos no OpenCart.
- **/excluir_produtos_tiny.py**: Arquivo independente para excluir produtos no ERP TINY.
- **/atualizar_precos_tiny.py**: Arquivo independente para atualizar os preços dos produtos no ERP TINY.

## ⚙️ Funcionalidades

### Arquivos Independentes

1. **ajustar_produtos_opencart.py**: 
   - Atualiza os metadados do produto, como nome, descrição, palavras-chave e preços por tipo de pessoa (física, jurídica e revenda).
   - A atualização é baseada em uma planilha, e a estrutura da planilha pode ser personalizada conforme as necessidades.
   
2. **excluir_produtos_tiny.py**: 
   - Exclui produtos no ERP TINY com base em uma planilha, limpando também os anexos dos produtos.
   - A estrutura da planilha pode ser personalizada conforme as necessidades.
   
3. **atualizar_precos_tiny.py**: 
   - Atualiza os preços dos produtos no ERP TINY com base em uma planilha.
   - Permite definir diferentes preços para tipos de clientes (físico, jurídico, revenda).

### 📔 Bibliotecas de Automação

1. **magalu.py**: 
   - Contém funções bem definidas e documentadas para ações comuns no Magalu, como atualização de preços e informações de produto.
   
2. **mercado_livre.py**: 
   - Contém funções bem definidas e documentadas para ações comuns no Mercado Livre, como atualização de preços.
   
3. **opencart.py**: 
   - Contém funções bem definidas e documentadas para ações comuns no OpenCart, como atualização de produtos, preços e inventário.
   
4. **tiny.py**: 
   - Contém funções bem definidas e documentadas para ações comuns no ERP TINY, como atualização de produtos, exclusão e ajustes de preços.
   
5. **planilhas.py**: 
   - Contém funções para atualizar planilhas, fazer logs e registrar os resultados das automações.

## 🤖 Tecnologias Utilizadas

- **Python**:
  - **Pandas**: Para manipulação de dados em planilhas.
  - **Selenium**: Para automação da interação com plataformas web.
  - **Logging**: Para registrar as operações realizadas durante a execução das automações.

## 📫 Como Usar

### 1. Instalar Dependências

Certifique-se de ter o Python instalado e as dependências necessárias. Você pode instalar as dependências usando o `pip`:

```bash
pip install pandas selenium
```

### 2. Como Rodar as Automations
Cada script pode ser executado de forma independente. Para rodar, basta executar o arquivo desejado no terminal, desde que esteja na mesma pasta que **/libraries**:
```bash
python ajustar_produtos_opencart.py
python excluir_produtos_tiny.py
python atualizar_precos_tiny.py
```
Lembre-se de fornecer as planilhas no formato correto, e fazer as adaptações necessárias na planilha e se necessário nos scripts.

### 🧿 Observações
As automações podem ficar obsoletas com o tempo devido a atualizações nas plataformas (TINY, Mercado Livre, Magalu e OpenCart), sendo necessário revisar os scripts periodicamente.
Certifique-se de testar os scripts em ambientes de desenvolvimento ou com dados de teste antes de rodar em ambientes de produção.
