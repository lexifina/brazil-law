ANEXO À INSTRUÇÃO NORMATIVA BCB Nº 720​, DE 2 DE ABRIL DE 2026
Manual de Segurança do Open Finance Versão 5.0
Sumário de alterações
Data
Versão
Descrição das alterações
2/4/2026
5.0
Aprimoramentos na redação do texto, sem alteração de mérito.
Atualização de referências.
Atualização da redação sobre o escopo de aplicação dos requisitos mínimos de segurança, com base na Resolução Conjunta nº 1, de 2020.
Alteração dos itens 3.1 e 3.9, para adequar ao escopo de aplicação atualizado dos requisitos mínimos de segurança.
Inclusão do item 3.10, dispondo sobre excepcionalidade do uso de certificados digitais para compartilhamento de dados sobre canais de atendimento e para o compartilhamento de produtos e serviços de que trata o art. 5º, inciso I, alíneas "a" e "b", da Resolução Conjunta nº 1, de 2020, renumerando-se os demais itens.
Alteração do item 3.15, dispondo sobre os certificados utilizados para comunicação de sistemas Front-End.
Inclusão dos itens 3.28 a 3.30, dispondo sobre os mecanismos adotados para validação de certificados digitais.
Inclusão do item 6.18 sobre a disponibilidade de parâmetros para seleção de mecanismos de verificação de que trata o item 3.28.
Termos de Uso
Este manual detalha os requisitos técnicos para a implementação dos elementos necessários à operacionalização do Open Finance, complementando a regulamentação vigente sobre o tema.
O manual será revisto e atualizado periodicamente a fim de preservar a compatibilidade com a regulamentação, bem como para incorporar os aprimoramentos decorrentes da evolução do Open Finance e da tecnologia.
Informações mais detalhadas e exemplos da aplicação deste manual poderão ser encontrados nos guias e tutoriais disponíveis no Portal do Open Finance no Brasil, na Área do Desenvolvedor.
Sugestões, críticas ou pedidos de esclarecimentos de dúvidas relativas ao conteúdo deste documento podem ser enviados ao Banco Central do Brasil por meio dos canais institucionais dessa autarquia.
Referências
Estas especificações baseiam-se, referenciam, e complementam, quando aplicável, os seguintes documentos:
Referência
Origem
Resolução Conjunta nº 1, de 2020
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20Conjunta&numero=1
Resolução BCB nº 85, de 2021
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=85
Resolução BCB nº 109, de 2021
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=109
Instrução Normativa BCB nº 136, de 2021
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Instru%C3%A7%C3%A3o%20Normativa%20BCB&numero=136
Resolução CMN nº 4.893, de 2021
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20CMN&numero=4893
Resolução BCB nº 400, de 2024
https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20BCB&numero=400
Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709, de 2018)
http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm
OWASP API Security Project
https://owasp.org/www-project-api-security/
CWE TOP 25 Most Dangerous Software Errors
https://www.sans.org/top25-software-errors
CWE Top 25 Most Dangerous Software Weaknesses
https://cwe.mitre.org/top25/
NIST Cybersecurity Framework
https://www.nist.gov/cyberframework
ICP Brasil - Manual de Condutas Técnicas 7 – Volume I
https://www.gov.br/iti/pt-br/centrais-de-conteudo/mct-7-vol-1-v-2-2-pdf
Medida Provisória nº 2.200-2, de 24 de agosto de 2001
http://www.planalto.gov.br/ccivil_03/mpv/antigas_2001/2200-2.htm
Chartered Professional Accountants – Canada: Principles and Criteria and Practitioner Guidance
https://www.cpacanada.ca/business-and-accounting-resources/audit-and-assurance/Overview-of-WebTrust-services/Principles-and-criteria
RFC 2818 - HTTP Over TLS
https://datatracker.ietf.org/doc/html/rfc2818
RFC 5280 - Internet X.509 Public Key Infrastructure Certificate and Certificate Revocation List (CRL) Profile
https://datatracker.ietf.org/doc/html/rfc5280
BCP 195/RFC 7525 - Recommendations for Secure Use of Transport Layer Security (TLS) and Datagram Transport Layer Security (DTLS)
https://tools.ietf.org/html/rfc7525
1. Introdução
Este manual detalha em termos operacionais as diretrizes de segurança estabelecidas pela Resolução Conjunta nº 1, de 4 de maio de 2020, e pela Resolução BCB nº 32, de 29 de outubro de 2020. Ele contém tanto os requisitos mínimos de segurança obrigatórios para as instituições participantes como para os demais elementos que compõem a Estrutura Responsável pela Governança do Open Finance.
Para garantir a segurança do Open Finance no País, a regulamentação vigente estabelece a obrigatoriedade de se cumprir uma série de medidas, entre as quais as descritas neste manual.
No tocante aos requisitos obrigatórios para as instituições participantes, este manual apresenta as seguintes seções: 2. governança, 3. proteção, 4. detecção e 5. reação. Os requisitos obrigatórios para a Estrutura de Governança do Open Finance constam da Seção 6.
Este manual prescreve os requisitos mínimos de segurança necessários para o compartilhamento de dados e serviços no Open Finance, conforme Resolução Conjunta nº 1, de 2020.
À medida que o Open Finance abranger o compartilhamento de outros dados e serviços, novos requisitos de segurança poderão ser acrescentados a este manual, em complemento à regulamentação aplicável.
Ao longo deste documento será constante o uso de siglas para designar algumas expressões cotidianas dos profissionais da área de segurança da informação. Alguns exemplos das mais frequentemente utilizadas, com as correspondentes definições, são as seguintes:
I - ACL: Access Control List;
II - API: Application Programming Interface;
III - ETIR: Equipe de Tratamento de Incidentes;
IV - HTTP: HyperText Transfer Protocol;
V - ICP-Brasil: Infraestrutura de Chaves Públicas Brasileira;
VI - IP: Internet Protocol;
VII - NTP: Network Time Protocol;
VIII - PFS: Perfect Forward Secrecy;
IX - PGP: Pretty Good Privacy;
X - TCP: Transmission Control Protocol;
XI - TLS: Transport Layer Security;
XII - URI: Uniform Resource Identifier; e
XIII - UTC: Universal Time Coordinated.
2. Governança
2.1 As instituições participantes do Open Finance devem adotar processos para acompanhar a publicação e a entrada em vigor de atos normativos com impacto no tema, de forma a estarem permanentemente atualizadas com as determinações regulamentares.
2.2 Compõem, de forma não exaustiva, o rol de atos normativos cuja observância é essencial pelas instituições participantes do Open Finance:
I - a Resolução Conjunta nº 1, de 2020;
II - as Resoluções editadas pelo Conselho Monetário Nacional (CMN) e pelo Banco Central do Brasil aplicáveis às instituições participantes, em especial as que dispõem sobre a política de segurança cibernética e sobre os requisitos para a contratação de serviços de processamento e armazenamento de dados e computação em nuvem; e
III - a Lei Geral de Proteção de Dados Pessoais (LGPD – Lei nº 13.709, de 2018).
2.3 O plano de ação e resposta a incidentes das instituições participantes deve abranger os procedimentos e os controles a serem utilizados na prevenção e resposta a incidentes que afetem sistemas, APIs e outros recursos relacionados à implementação e à operação do Open Finance, de forma compatível com a política de segurança cibernética da instituição e com a regulamentação vigente.
2.4 As instituições participantes devem definir procedimentos e controles voltados à prevenção e ao tratamento de incidentes a serem adotados pelas empresas prestadoras de serviços a terceiros que manuseiem dados ou informações requeridos para a condução das atividades relativas ao Open Finance, em compatibilidade com a política de que trata o item 2.3 e com a regulamentação vigente.
2.5 Os procedimentos e controles de que trata o item 2.4 devem ser divulgados às empresas prestadoras de serviços mediante linguagem clara, acessível e em nível de detalhamento compatível com as funções desempenhadas e sensibilidade das informações.
2.6 As instituições participantes, previamente à contratação de serviços requeridos para a condução das atividades relativas ao Open Finance, devem adotar procedimentos que contemplem a verificação da capacidade do potencial prestador de serviço de assegurar o cumprimento da legislação e da regulamentação vigente.
2.7 As instituições devem armazenar e processar os dados discriminados na etapa de consentimento segundo a finalidade para a qual foram compartilhados de maneira segura, observadas a legislação e a regulamentação vigentes.
2.8 As instituições participantes devem manter suas informações cadastrais permanentemente atualizadas no Diretório de Participantes do Open Finance, observada a regulamentação vigente.
3. Proteção
3.1 Os acessos aos dados e aos serviços no âmbito do Open Finance devem ser realizados exclusivamente por meio de APIs.
3.2 Os sistemas e APIs relacionados ao Open Finance devem ser mantidos em rede interna segregada logicamente de redes ordinariamente utilizadas por estações de trabalho ou redes sem fio.
3.3 As instituições transmissoras de dados e detentoras de conta devem implementar controles de tráfego de entrada e saída, de forma a permitir apenas o necessário para comunicação com as APIs de Open Finance.
3.4 As instituições devem implementar criptografia na comunicação com as APIs de Open Finance expostas publicamente, por meio do protocolo TLS na versão 1.2 ou superior, utilizando cifras (cipher suites) que atendam ao requisito de perfect forward secrecy (PFS).
3.5 As funcionalidades "TLS Session Resumption" e "TLS Renegotiation" devem ser desabilitadas.
3.6 As instituições devem aplicar controles de segurança na camada de aplicação que permitam a inspeção de ameaças e o bloqueio de ataques de injeção de código, entre outros, adequados às tecnologias utilizadas nas APIs.
3.7 As instituições não devem expor os repositórios de dados utilizados no Open Finance diretamente à internet.
3.8 As instituições participantes devem verificar e garantir que a quantidade, a ordem, o formato, o tamanho e o conteúdo dos campos das requisições de acesso às APIs, bem como suas respostas, estejam de acordo com os estabelecidos pelas definições de Open Finance.
3.9 Para assinatura de mensagens e comunicação segura com APIs usadas para os compartilhamentos de dados e de serviços, devem ser utilizados certificados digitais válidos, emitidos por autoridade certificadora participante da ICP-Brasil, de acordo com os padrões para certificação digital estabelecidos pela Estrutura de Governança do Open Finance.
3.10 O disposto no item 3.9 não se aplica ao compartilhamento de dados sobre canais de atendimento nem ao compartilhamento de dados sobre produtos e serviços de que trata o art. 5º, inciso I, alíneas "a" e "b", da Resolução Conjunta no 1, de 2020.
3.11 Os certificados digitais de que trata o item 3.9 devem contemplar mecanismos para a proteção dos canais de comunicação e para a assinatura ou criptografia de mensagens trocadas com APIs.
3.12 Admite-se, para emprego no ambiente de testes de APIs de que trata o art. 12, inciso IV da Resolução BCB nº 32, de 2020, o uso de certificados digitais emitidos pelo serviço de Diretório da Estrutura de Governança do Open Finance.
3.13 Os certificados requeridos para as contratações de parceria devem observar a legislação e a regulamentação em vigor e seguir, no que couber, os padrões de certificado digital definidos pela Estrutura de Governança do Open Finance. Os padrões de que trata este item devem contemplar a formatação do certificado, os algoritmos criptográficos e os atributos estabelecidos.
3.14 Para o estabelecimento de conexões TLS das chamadas de endpoints confidenciais devem ser utilizados os seguintes algoritmos:
I - ‘TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256’; e
II - ‘TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384’.
3.15 Os certificados utilizados para comunicação de sistemas Front-End, acessados diretamente por clientes das instituições participantes, em especial para realizar autenticação, devem:
I - ser do tipo Extended Validation (EV); e
II - ser emitidos por autoridade certificadora em funcionamento, em conformidade com os princípios e critérios WebTrust.
3.16 Os procedimentos e controles relativos à criptografia devem contemplar meios seguros de armazenamento, transferência, utilização e destruição de segredos ou chaves empregados no âmbito do Open Finance, observada a regulamentação vigente.
3.17 Recomenda-se utilizar os seguintes algoritmos criptográficos para proteção e armazenamento de segredos no âmbito do Open Finance:
I - ‘AES-256bits’ ou superior;
II - ‘SHA-256bits’ ou superior; e
III - ‘RSA-2048bits’ ou superior.
3.18 É recomendável que os segredos e as chaves utilizados para autenticar, proteger e garantir a integridade de dados sejam gerados de maneira a respeitar processos de duplo controle e tratamento de segredo (split-knowledge), armazenando registros de log que incluam data de geração, participantes e responsáveis pela custódia, quando aplicável e de forma compatível com a regulamentação vigente.
3.19 As instituições participantes devem implementar procedimentos e controles de segurança para análise de vulnerabilidades nas etapas de desenvolvimento e de utilização em produção das versões das APIs utilizadas no Open Finance, observada a regulamentação vigente.
3.20 As vulnerabilidades de que trata o item 3.19 devem ser categorizadas e priorizadas de acordo com classificação de risco.
3.21 Os participantes devem implementar processos de revisão periódica das configurações dos sistemas e das APIs utilizados no Open Finance, para garantir que somente portas e serviços autorizados estejam habilitados, observada a regulamentação vigente.
3.22 As instituições participantes devem garantir que portais e aplicações relacionados à implementação e à operação do Open Finance possuam meios de autenticação adequados e controle de autorização em observância à regulamentação vigente.
3.23 O processo de autenticação deve ser sempre realizado por meio de canal de comunicação seguro, utilizando criptografia TLS 1.2 ou superior, de forma compatível com a regulamentação vigente.
3.24 Os acessos remotos para administração de sistemas ou da infraestrutura relacionados ao Open Finance devem ser realizados mediante uso de múltiplos fatores de autenticação, observada, no que couber, a compatibilidade com a regulamentação vigente.
3.25 As instituições devem implementar processo formal de aplicação de patch que contemple os sistemas relacionados à implementação do Open Finance, de forma compatível com a política de segurança cibernética da instituição, observada regulamentação vigente.
3.26 Os sistemas e APIs relacionados ao Open Finance devem possuir relógio sincronizado com fonte confiável de tempo, por exemplo, por meio do uso do protocolo NTP.
3.27 As APIs e os sistemas relacionados ao Open Finance devem ser implementados usando padrões de configuração segura (hardening), observada a regulamentação vigente.
3.28 As instituições participantes devem utilizar mecanismos para verificar a validade dos certificados digitais de que trata o item 3.9.
3.29 A seleção dos mecanismos de que trata o item 3.28 deve estar de acordo com os parâmetros definidos pela Estrutura de Governança do Open Finance.
3.30 As instituições participantes devem ser capazes de verificar a validade dos certificados digitais mesmo diante de indisponibilidade temporária dos mecanismos de que trata o item 3.28.
4. Detecção
4.1 As instituições participantes devem manter trilhas de auditoria contendo, no mínimo, endereço IP de origem da chamada, porta de comunicação de origem da chamada, data, hora, sistema, usuário (quando aplicável), objeto, falha ou sucesso da ação das configurações realizadas nos sistemas e APIs relacionados ao Open Finance, observadas a legislação e regulamentação vigentes.
4.2 As instituições participantes devem monitorar os registros relativos aos acessos das APIs relacionadas ao Open Finance, em especial os registros que indicarem erros internos (ex: status HTTP 500) ou requisições inválidas (ex: status HTTP 400), observada a regulamentação vigente.
4.3 As instituições participantes devem monitorar a volumetria e o padrão das requisições às APIs relacionadas ao Open Finance, para detecção de incidentes relacionados aos incisos I a IV do item 5.5.
5. Reação
5.1 É facultado às instituições participantes implementar bloqueio de acessos às suas APIs, com vistas a tratar riscos cibernéticos ou para tratar incidentes cibernéticos em andamento. A implementação desses bloqueios deve ser compatível com a política de segurança cibernética da instituição.
5.2 Em caso de comprometimento de qualquer credencial relacionada ao Open Finance, a instituição participante deve revogá-la tempestivamente perante o Diretório de Participantes e compartilhar essa informação com as demais instituições participantes, observada a regulamentação vigente.
5.3 No caso de comprometimento de certificados de segurança, a instituição participante do Open Finance deve solicitar tempestivamente a revogação do certificado comprometido à autoridade certificadora e compartilhar essa informação com a Estrutura de Governança do Open Finance e com as demais instituições participantes, observada a regulamentação vigente.
5.4 Sem prejuízo do dever de sigilo e da livre concorrência, as instituições participantes devem compartilhar com as demais instituições participantes e com a Estrutura de Governança do Open Finance informações sobre incidentes cibernéticos que afetem os serviços do Open Finance, observando a regulamentação vigente.
5.5 No âmbito do Open Finance, observada a regulamentação vigente, o plano de ação e resposta a incidentes deve contemplar, no mínimo, procedimentos para prevenir e responder a incidentes que possam implicar:
I - acesso não autorizado;
II - vazamento de dados;
III - negação de serviço; e
IV - falha na integridade de dados.
6. Estrutura de Governança do Open Finance
6.1 Cada instituição deve cadastrar no Diretório de Participantes os dados de contato de seus representantes para tratamento de incidentes com, no mínimo, e-mail, chaves criptográficas PGP (se houver) e campo para dados adicionais. Tais dados devem ser disponibilizados pelo Diretório para acesso aos demais participantes.
6.2 Cada instituição deve disponibilizar os contatos de e-mail das equipes de segurança conforme a RFC 2142 (abuse e security).
6.3 O acesso às áreas restritas do Diretório de Participantes deve ser:
I - permitido apenas a usuários autorizados pelas instituições participantes ou pela Estrutura de Governança do Open Finance; e
II - condicionado à autenticação por múltiplos fatores.
6.4 Os acessos ao Diretório devem ser registrados em trilhas de auditoria, que devem conter, no mínimo, data e hora do acesso na timezone UTC, endereço IP de origem da chamada, porta de comunicação origem da chamada, URI acessada, método HTTP utilizado e status de retorno, observada a legislação e a regulamentação vigentes.
6.5 A Estrutura de Governança do Open Finance deve implementar e manter política de segurança cibernética formulada com base em princípios e diretrizes que busquem assegurar a confidencialidade, a integridade e a disponibilidade dos dados e dos sistemas de informação utilizados, com vistas a contemplar as atividades de que trata o art. 12 da Resolução BCB nº 32, de 2020.
6.6 A política de que trata o item 6.5 deve contemplar:
I - os procedimentos e controles para reduzir a vulnerabilidade a incidentes;
II - a execução, no mínimo anual, de testes de intrusão;
III - os mecanismos para disseminação da cultura de segurança cibernética; e
IV - a difusão de boas práticas de segurança cibernética aos participantes e a outras partes interessadas na implementação e na operação do Open Finance no Brasil.
6.7 A Estrutura de Governança do Open Finance deve implementar e manter plano de ação e resposta a incidentes visando à implementação da política de segurança cibernética de que trata o item 6.5.
6.8 O plano de ação e resposta a incidentes mencionado no item 6.7 deve contemplar as rotinas, os procedimentos, os controles e as tecnologias a serem utilizados na prevenção, no monitoramento e na resposta a incidentes que afetem os serviços definidos no art. 12 da Resolução BCB nº 32, de 2020.
6.9 O monitoramento dos serviços de que trata o item 6.8 deve ser realizado de forma permanente e estar disponível 24 horas por dia, 7 dias por semana.
6.10 A política referida no item 6.5 e o plano de ação e resposta a incidentes mencionado no item 6.7 devem ser aprovados pelo Órgão de Direção Superior da Estrutura de Governança do Open Finance, após prévia avaliação técnica.
6.11 Os testes de intrusão mencionados no inciso II do item 6.6 devem ser realizados com independência e imparcialidade por pessoa natural ou empresa especializada contratada para essa finalidade.
6.12 As vulnerabilidades identificadas nos testes de intrusão devem ser documentadas e tempestivamente tratadas pela Estrutura de Governança do Open Finance.
6.13 A Estrutura de Governança do Open Finance deverá instituir Equipe de Tratamento de Incidentes responsável por:
I - prevenir e tratar incidentes cibernéticos que afetem as atividades de que trata o art. 12 da Resolução BCB nº 32, de 2020;
II - monitorar a utilização de credenciais de acesso dos participantes às atividades referenciadas no Inciso I; e
III - responder por eventuais violações de acesso caso utilizadas as credenciais de que trata o Inciso II.
6.14 É responsabilidade da Equipe de Tratamento de Incidentes que trata o item 6.13, no âmbito de suas atribuições, apoiar o tratamento de incidentes que possam implicar risco ao funcionamento de sistemas relacionados à implementação do Open Finance, especialmente para promover:
I - a difusão e o compartilhamento de indicadores de comprometimento e de informações de inteligência cibernética; e
II - o monitoramento e o tratamento de incidentes envolvendo as atividades de que trata o art. 12 da Resolução BCB nº 32, de 2020.
6.15 As informações sobre incidentes cibernéticos citados no Inciso I do item 6.13 devem ser:
I - compartilhadas com os representantes para tratamento de incidentes das instituições participantes; e
II - disponibilizadas ao Banco Central do Brasil, observada a regulamentação em vigor.
6.16 A Estrutura de Governança do Open Finance deve disponibilizar no Portal do Open Finance no Brasil:
I - os padrões de segurança e dos certificados digitais para fins de compartilhamento de dados e de serviços no escopo do Open Finance, observada a regulamentação em vigor; e
II - as instruções para subsidiar a emissão de certificados digitais requeridos para as contratações de parceria para fins de compartilhamento previstas na regulamentação em vigor.
6.17 O Diretório de Participantes do Open Finance deve disponibilizar mecanismos que permitam às autoridades registradoras a validação de atributos dos certificados digitais de que trata o item 3.9.
6.18 A Estrutura de Governança do Open Finance deve disponibilizar às instituições participantes os parâmetros para seleção de mecanismos de verificação de que trata o item 3.29, contemplando, no mínimo:
I - a frequência mínima esperada de atualização das informações disponibilizadas por meio do mecanismo selecionado;
II - a tolerância mínima a falhas na utilização do mecanismo selecionado; e
III - a alternativa para verificação da validade do certificado de que trata o item 3.9, no caso de indisponibilidade do mecanismo selecionado.
Brasília, 2 de abril de 2026.
​NOTA 227/2026-BCB/DENOR, DE 20 de MARÇO de 2026
Fundamenta proposta de edição de instrução normativa que estabelece a versão 5.0 do Manual de Segurança do Open Finance.
Senhores Chefes do Denor e do Deinf,
1. A presente Nota fundamenta proposta de edição de instrução normativa pelo Departamento de Regulação do Sistema Financeiro (Denor) e pelo Departamento de Tecnologia da Informação (Deinf), no uso da atribuição que lhes confere o art. 23, inciso I, alínea "a", do Regimento Interno do Banco Central do Brasil, anexo à Resolução BCB nº 340, de 21 de setembro de 2023, com base no art. 51, inciso IX, da Resolução Conjunta nº 1, de 4 de maio de 2020, que dispõe sobre a implementação do Open Finance.
2. ​A respeito, a proposta trata de edição de instrução normativa que estabelece a versão 5.0 do Manual de Segurança do Open Finance, revogando a Instrução Normativa BCB nº 305, de 15 de setembro de 2022, que divulga a versão 4.0 do Manual de Segurança do Open Finance.
3. As alterações referem-se às atualizações no escopo de aplicação dos requisitos mínimos de segurança, para deixá-lo mais alinhado com o escopo vigente de dados e de serviços compartilhados no âmbito do Open Finance, conforme Resolução Conjunta nº 1, de 2020. Adicionalmente, foram propostas atualizações de caráter formal em expressões do texto.
4. Cumpre ressaltar que, por força do art. 5º da Lei nº 13.874, de 20 de setembro de 2019, as propostas de edição e de alteração de atos normativos de interesse geral de agentes econômicos ou de usuários dos serviços prestados, editadas por órgão ou entidade da administração pública federal, incluídas as autarquias e as fundações públicas, serão precedidas da realização de análise de impacto regulatório (AIR), que conterá informações e dados sobre os possíveis efeitos do ato normativo para verificar a razoabilidade do seu impacto econômico.
5. Por sua vez, o Decreto nº 10.411, de 30 de junho de 2020, que regulamenta essa Lei, em seu art. 4º, caput, incisos V, alíneas "b" e "c", estabelece que a AIR poderá ser dispensada, desde que haja decisão fundamentada do órgão ou da entidade competente, nas hipóteses de ato normativo que vise a preservar liquidez, solvência ou higidez dos mercados financeiros, de capitais e de câmbio e dos sistemas de pagamentos.
6. Nesse sentido, as alterações ora propostas no manual de segurança referentes às atualizações de escopo e de expressões citadas e aos requisitos de proteção observados pelos participantes do Open Finance buscam, em conjunto, preservar a higidez dos mercados financeiros e dos sistemas de pagamentos, ao esclarecer que os certificados utilizados para comunicação de sistemas Front-End, acessados diretamente por clientes das referidas instituições, sejam emitidos por autoridade certificadora em funcionamento, em conformidade com os princípios e critérios WebTrust (selo que representa que a autoridade certificadora foi auditada e está em conformidade com os requisitos do Webtrust Seal Program), e ao estabelecer regras relativas à seleção e ao uso de mecanismos para verificar a validade dos certificados digitais, mesmo em situações de indisponibilidade temporárias desses mecanismos. Nesse sentido, de acordo com o art. 4º, inciso V, alíneas "b" e "c", do citado Decreto nº 10.411, de 2020, o ato normativo ora proposto está dispensado de elaboração de AIR.
À consideração de V.Sa.
JANAÍNA PIMENTA ATTIE VERUSKA ROCHA DE ARAGÃO
Consultora do Denor Chefe Adjunta do Deinf
De acordo.
MARDILSON FERNANDES QUEIROZ CAIO MOREIRA FERNANDES
Chefe do Denor Chefe do Deinf
