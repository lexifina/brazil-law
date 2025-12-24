ANEXO À INSTRUÇÃO NORMATIVA BCB Nº 695, DE 23 DE DEZEMBRO DE 2025
Manual das Interfaces de Comunicação Versão 1.12
Histórico de revisão
Data
Versão
Descrição das alterações
14/11/2019
1.0
Versão inicial.
17/01/2020
1.1
Conectividade:
- Inclusão de referência ao Manual de Redes da RSFN;
- Atualização do link para o Manual de Segurança RSFN;
- Detalhamento do comportamento do DNS.
Endpoints:
- Mudança da URL base de produção e inclusão da URL de homologação;
Endpoint Entrada:
- Esclarecimento sobre idempotência no envio de mensagens duplicadas.
Endpoint Saída:
- Esclarecimento sobre interrupção.
Diversos:
- Cabeçalhos SPI-ResourceId e SPI-PullNext alterados para PI-ResourceId e PI-PullNext.
17/02/2020
1.2
Incluída a interface do DICT.
Renomeado o arquivo de “Manual da Interface de Comunicação” para “Manual das Interfaces de Comunicação”.
28/07/2020
1.3
Retiradas referências ao documento de especificações e alterado o título e nome do arquivo.
DICT: Modificada a sessão do DICT para referenciar assinatura de mensagens.
ICOM:
- Remoção de “Transfer-Encoding: gzip, chunked” para envio compactado. Recomendação de uso de “ContentEncoding” para essa finalidade;
- Admitidos novos cabeçalhos;
- Adoção de envio e recebimento de múltiplas mensagens em uma mesma requisição (multipart);
- Incluído o endpoint Catálogo: versões das mensagens aceitas e enviadas pela API;
- Remoção da seção “Pendências”.
ARQ: incluída documentação sobre o serviço de transferência de arquivos.
12/08/2020
1.4
Alterado padrão visual.
Adicionada seção com dicas para melhoria de desempenho na leitura de mensagens em situação de carga.
Alteração nas portas HTTPS para os serviços ICOM e ARQ.
19/08/2020
1.5
Correção na documentação de PI-ResourceId nos casos de requisições multipart no endpoint de saída.
06/10/2020
1.6
API ARQ: informação sobre uso de cabeçalhos ETag, “ETag”, “Last-Modified”, “If-None-Match” e “If-ModifiedSince”.
Cabeçalho Host deverá ser enviado sem a porta (ICOM, DICT e ARQ).
14/10/2020
1.7
Criação da seção 2.2.1.5 - Limitação da Quantidade Máxima de Transações Agendadas por Unidade de Tempo.
Ajuste pontual na definição do PI-Resource-ID, na seção 2.2.1.3.
30/04/2021
1.8
Criação da seção 2.2.1.6 – Limitação de Tráfego de Mensagens e Operações.
04/01/2022
1.9
Alteração nos valores da seção 2.2.1.5 – Limitação da quantidade máxima de transações agendadas por unidade de tempo.
17/10/2022
1.10
Inclusão do texto na seção 2.2.1.6. para alteração dos parâmetros de balde dos participantes, a critério do BACEN.
31/03/2023
1.11
- Alteração nos valores do bucket e do acréscimo de tokens na seção 2.2.1.6 – com validade a partir de 02/05/2023.
- Criação da seção 1.2 - Canais de transmissão de mensagens – com validade a partir de 29/10/2023.
- Alterações nos textos das seções 2.2, 2.2.1.5, 2.2.1.6, 2.2.2.10 para inclusão das especificações relativas ao canal secundário – com validade a partir de 29/10/2023.
23/12/2025
1.12
- Remove texto desatualizado na seção Apresentação - Remove menções às datas passadas de implantação do canal secundário nas seções 1.2, 2.2 e 2.2.1.5
- Remove todo o item desatualizado “Limitação da quantidade máxima de transações agendadas por unidade de tempo”
- Adiciona bucket para trck.002
- Adiciona informação sobre o tempo de exclusão dos arquivos no ARQ
NOTA
O Decreto nº 10.411, de 30 de junho de 2020, prevê a obrigatoriedade da realização de análise de impacto regulatório (AIR) para a edição de atos normativos de interesse geral produzidos pelos órgãos e entidades da administração pública federal direta e indireta.
Todavia, consoante se definiu no parágrafo 8 do Voto 280/2021–BCB, de 10 de novembro de 2021, o Regulamento do Pix, inclusive os demais documentos que o integram ou que o detalham e complementam, não se caracterizam como ato regulatório de força cogente, ostentando, em verdade, natureza eminentemente contratual. Assim, modificações promovidas no referido regulamento e nos demais documentos que o integram ou que o detalham e complementam não se sujeitam à produção prévia de AIR.
Dessa forma, fica a presente Instrução Normativa dispensada da prévia produção de AIR.
Ricardo Pereira Araújo
Chefe do Departamento de Competição e de Estrutura do Mercado Financeiro, substituto​
