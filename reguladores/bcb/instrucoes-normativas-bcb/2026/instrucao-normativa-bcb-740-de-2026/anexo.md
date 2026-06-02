ANEXO I À INSTRUÇÃO NORMATIVA BCB Nº 740, DE 29 DE MAIO DE 2026
Este Anexo detalha os critérios para os testes em produção relativos ao compartilhamento de serviço otimizado de iniciação de transação de pagamento com compartilhamento de dados (jornada otimizada) no Open Finance, conforme o papel desempenhado pelas instituições participantes, seja como instituição detentora de conta e transmissora de dados ou como instituição iniciadora de transação de pagamento e receptora de dados.
Os testes em produção devem estar de acordo com a regulamentação do Banco Central do Brasil e com a política de testes em produção da Estrutura de Governança do Open Finance.
1. Critérios gerais
Com vistas a garantir a adequada qualidade dos testes em produção, a Estrutura de Governança do Open Finance deve avaliar o cumprimento dos requisitos dispostos neste Anexo pelas instituições participantes dos testes em produção da jornada otimizada.
Essa avaliação deve ser realizada nos pontos de controle a serem realizados nas seguintes datas:
I - 8 de maio de 2026;
II - 22 de maio de 2026;
III - 5 de junho de 2026; e
IV - 22 de junho de 2026
1.1 Integração com ferramentas
As instituições participantes dos testes em produção da jornada otimizada precisam garantir a adequada integração com a plataforma de coleta de métricas (PCM) e ter 95% ou mais de chamadas pareadas com status "PAIRED" e 100% de dados adicionais (additionalInfos) reportados para acompanhamento relativos aos produtos Transferências Inteligentes e compartilhamento do serviço de iniciação de transação de pagamento sem redirecionamento (jornada sem redirecionamento), bem como para acompanhamento dos consentimentos para compartilhamento de dados (API Consentimentos).
As instituições participantes dos testes em produção da jornada otimizada devem garantir adequada qualidade das informações reportadas à PCM.
Nenhum ticket de qualidade da PCM relacionado a pagamentos deve estar em aberto nos pontos de controle definidos na seção 1.
1.2 Comportamento bilateral
As instituições participantes dos testes em produção da jornada otimizada devem garantir que nenhum ticket bilateral relacionado aos testes esteja em aberto durante os pontos de controle definidos na seção 1.
2. Critérios específicos
2.1 Engajamento
O engajamento das instituições participantes dos testes em produção da jornada otimizada é etapa fundamental para testar sua maturidade. Dessa forma, as instituições precisam garantir quantidade mínima de volumetria de criação de consentimentos e de liquidação de pagamentos para cada um dos produtos testados na jornada otimizada e os dados referentes a esses consentimentos e pagamentos precisam ser identificados por meio da PCM.
De forma a garantir que a quantidade mínima total de volumetria de criação de consentimentos e de liquidação de pagamentos será atingida, haverá acompanhamento intermediário da volumetria de acordo com os pontos de controle definidos na seção 1, nos percentuais de 30, 50, 80 e 100, respectivamente.
2.1.1 Instituições detentoras de conta e transmissoras de dados
As instituições detentoras de conta e transmissoras de dados devem garantir que, no mínimo:
I - cem consentimentos de Transferências Inteligentes sejam autorizados, sendo que ao menos vinte sejam referentes a pessoas jurídicas, quando aplicável;
II - cem vínculos de conta (jornada sem redirecionamento) sejam autorizados, sendo que ao menos vinte sejam referentes a pessoas jurídicas, quando aplicável;
III - quarenta pagamentos de Transferências Inteligentes sejam liquidados, sendo que ao menos dez sejam referentes a pessoas jurídicas, quando aplicável; e
IV - quarenta pagamentos de jornada sem redirecionamento sejam liquidados, sendo que ao menos dez sejam referentes a pessoas jurídicas, quando aplicável.
As instituições de que trata esta subseção devem garantir que seja:
I - autorizado um consentimento e que seja liquidado um pagamento referente a Transferências Inteligentes, com ao menos 50% das instituições iniciadoras de transação de pagamento e receptoras de dados participantes dos testes em produção da jornada otimizada; e
II - autorizado um vínculo de conta e que seja liquidado um pagamento referente à jornada sem redirecionamento, com ao menos 50% das instituições iniciadoras de transação de pagamento e receptoras de dados participantes dos testes em produção da jornada otimizada.
2.1.2 Instituições iniciadoras de transação de pagamento e receptoras de dados
As instituições iniciadoras de transação de pagamento e receptoras de dados devem garantir que, no mínimo:
I - cem consentimentos de Transferências Inteligentes sejam autorizados, sendo que ao menos vinte sejam referentes a pessoas jurídicas, quando aplicável;
II - cem vínculos de conta (jornada sem redirecionamento) sejam autorizados, sendo que ao menos vinte sejam referentes a pessoas jurídicas, quando aplicável;
III - quarenta pagamentos de Transferências Inteligentes sejam liquidados, sendo que ao menos dez sejam referentes a pessoas jurídicas, quando aplicável; e
IV - quarenta pagamentos de jornada sem redirecionamento sejam liquidados, sendo que ao menos vinte pagamentos sejam pagamentos imediatos e dez pagamentos sejam referentes a pessoas jurídicas, quando aplicável.
As instituições de que trata esta subseção devem garantir que seja:
I - autorizado um consentimento e que seja liquidado um pagamento referente a Transferências Inteligentes com:
a) ao menos 50% das instituições detentoras de contas participantes dos testes em produção da jornada otimizada; e
b) todas as principais marcas das instituições detentoras de conta relacionadas no Anexo II; e
II - autorizado um vínculo de conta e que seja liquidado um pagamento referente à jornada sem redirecionamento com:
a) ao menos 50% das instituições detentoras de contas participantes dos testes em produção da jornada otimizada; e
b) todas as principais marcas das instituições detentoras de conta, conforme definição no Anexo II.
2.2 Comportamento funcional e de segurança
As instituições detentoras de conta e transmissoras de dados devem realizar testes funcionais e de segurança, devendo obter sucesso em todos os testes da ferramenta de validação em produção (FVP) Manual, por servidor, para usuários pessoas natural e jurídica, quando aplicável:
I - para Transferências Inteligentes, em cinco testes de curta duração;
II - para jornada sem redirecionamento, em cinco testes de curta duração; e
III - para outros cenários, em três testes de curta duração.
As instituições nas quais o fornecedor da Estrutura de Governança do Open Finance não possui conta são responsáveis pela própria obtenção de sucesso. As demais instituições terão seus testes executados pelo fornecedor contratado.
Os testes serão executados variando os ambientes entre mobile Android, mobile IOS e desktop.
Tendo em vista o estabelecido no art. 5º, e considerando que, conforme a Resolução BCB nº 463, de 22 de abril de 2025, os prazos máximos para atendimento dos tickets relacionados aos testes em produção da jornada otimizada podem ser reduzidos pelo Banco Central do Brasil, deve ser atribuído o prazo máximo de dois dias úteis para atendimento dos tickets gerados no escopo desta subseção.
2.3 Implementação de jornada
A implementação da jornada de acordo com o definido na regulamentação e no Guia de Experiência do Usuário do Open Finance é aspecto fundamental para que se garanta padronização na experiência do cliente nas diferentes instituições participantes.
Para avaliar o grau de aderência das instituições participantes dos testes em produção da jornada otimizada, a Estrutura de Governança do Open Finance aplicará questionário baseado no Guia de Experiência do Usuário vigente.
2.3.1 Instituições detentoras de conta e transmissoras de dados
Os testes serão realizados via mobile, com usuários pessoa natural, nas principais marcas das instituições de que trata esta subseção relacionadas no Anexo II, relativos aos seguintes cenários:
I - criação e cancelamento de consentimento de Transferências Inteligentes; e
II - criação, edição e cancelamento de consentimento de jornada sem redirecionamento.
2.3.2 Instituições iniciadoras de transação de pagamento e receptoras de dados
Os testes serão divididos em dois grupos da seguinte forma:
I - teste 1: realizado via mobile com usuários pessoa natural; e
II - teste 2: realizado preferencialmente via desktop com usuários pessoa jurídica, quando aplicável.
As instituições de que trata esta subseção devem obter sucesso:
I - na criação e cancelamento do consentimento de pagamento atrelado a Transferências Inteligentes (teste 1);
II - na criação e cancelamento do consentimento de dados atrelado a Transferências Inteligentes (teste 2);
III - na criação, edição e cancelamento do vínculo de contas de atrelado à jornada sem redirecionamento (teste 1); e
IV - na criação e cancelamento do consentimento de dados atrelado à jornada sem redirecionamento (teste 2).
ANEXO II À INSTRUÇÃO NORMATIVA BCB Nº 740, DE 29 DE MAIO DE 2026
As instituições detentoras de conta e suas principais marcas, referenciadas no Anexo I, são as seguintes:
I - Banco do Brasil (marca "Banco do Brasil" para clientes pessoa natural e pessoa jurídica);
II - Banco PAN (marca "Banco PAN" para clientes pessoa natural);
III - Bradesco (marca "Bradesco Pessoa Física" para clientes pessoa natural e marca "Bradesco Pessoa Jurídica" para clientes pessoa jurídica);
IV - BTG Pactual (marca "BTG Banking" para clientes pessoa natural e marca "BTG Empresas" para clientes pessoa jurídica);
V - C6 (marca "C6 Bank" para clientes pessoa natural e pessoa jurídica);
VI - Caixa Econômica Federal (marca "CAIXA" para clientes pessoa natural e pessoa jurídica);
VII - Digio (marca "Banco Digio" para clientes pessoa natural);
VIII - Itaú (marca "Itaú" para clientes pessoa natural e marca "Itaú Empresas" para clientes pessoa jurídica);
IX - Mercado Pago (marca "Mercado Pago" para clientes pessoa natural e pessoa jurídica);
X - Neon Pagamentos (marca "Neon" para clientes pessoa natural);
XI - Nu Pagamentos (marca "Nubank" para clientes pessoa natural e pessoa jurídica);
XII - Pagseguro (marca "PagBank" para clientes pessoa natural e pessoa jurídica);
XIII - PicPay (marca "PicPay" para clientes pessoa natural e marca "PicPay Negócios" para clientes pessoa jurídica);
XIV - Santander (marca "Banco Santander Pessoa Física" para clientes pessoa natural e marca "Banco Santander Pessoa Jurídica" para clientes pessoa jurídica);
XV - Sicredi (marca "Sicredi" para clientes pessoa natural e pessoa jurídica); e
XVI - Sicoob (marca "Sicoob" para clientes pessoa natural e pessoa jurídica).
NOTA 444/2026-BCB/DENOR, DE 22 DE MAIO DE 2026
Fundamenta proposta de edição de instrução normativa que estabelece as orientações, as condições e os prazos para a realização de testes em produção pelas instituições participantes relativos ao compartilhamento​ do serviço otimizado de iniciação de transação de pagamento com compartilhamento de dados (jornada otimizada) no Open Finance.
Senhores Chefes do Denor, do Desuc e do Desup,
A presente Nota fundamenta proposta de edição de instrução normativa pelo Departamento de Regulação do Sistema Financeiro (Denor), pelo Departamento de Supervisão de Cooperativas e de Instituições Não Bancárias (Desuc) e pelo Departamento de Supervisão Bancária (Desup), no uso da atribuição prevista no art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 44, §1º, da Resolução Conjunta nº 1, de 4 de maio de 2020, e na Resolução BCB nº 406, de 2 de agosto de 2024,
2. A respeito, a proposta trata de edição de instrução normativa que estabelece as orientações, as condições e os prazos para a realização de testes em produção pelas instituições participantes relativos ao compartilhamento do serviço otimizado de iniciação de transação de pagamento com compartilhamento de dados (jornada otimizada) no Open Finance.
3. Em atendimento ao previsto no art. 5º da Lei nº 13.874, de 20 de setembro de 2019, o Decreto nº 10.411, de 30 de junho de 2020, determina que as propostas de atos normativos de interesse geral de agentes econômicos formuladas por órgãos e entidades da administração pública federal direta, autárquica e fundacional, bem como por colegiados por meio do órgão ou da entidade encarregada de lhe prestar apoio administrativo, sejam precedidas de Análise de Impacto Regulatório (AIR).
4. Contudo, a proposta em comento divulga detalhamento dos testes em produção a serem realizados pelas instituições participantes em relação à jornada otimizada, etapa que é fundamental para garantir adequado funcionamento dessa nova jornada, tanto em matéria de funcionalidade quanto de segurança, de modo que considero que tal proposta enquadra-se na possibilidade de dispensa de AIR estabelecida no art. 4º, inciso V, alíneas "b" e "c", do Decreto nº 10.411, de 2020, por visar à preservação da higidez dos mercados financeiros e dos sistemas de pagamentos.
À consideração de V.Sa.
JANAÍNA PIMENTA ATTIE IVENS ARUA NEVES DE MIRANDA
​Consultora do Denor Chefe Adjunto do Desuc
MARCO ANTONIO GUIMARÃES VERRONE
Chefe Adjunto do Desup
De acordo.
MARDILSON FERNANDES QUEIROZ ADALBERTO FELINTO DA CRUZ JUNIOR
Chefe do Denor Chefe do Desuc
RICARDO SIVIERI ZENI
Chefe do Desup
