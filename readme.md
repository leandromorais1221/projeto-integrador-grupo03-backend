💰 Aplicação Financeira Pessoal

Projeto desenvolvido para a Unidade Curricular Projeto Integrador — Boas Práticas de Desenvolvimento de Software, com o objetivo de desenvolver uma aplicação para auxiliar no gerenciamento de finanças pessoais, permitindo o controle, categorização e acompanhamento das transações financeiras do usuário.

📚 Unidade Curricular

Projeto Integrador — Boas Práticas de Desenvolvimento de Software

🎯 Tema

Aplicação Financeira Pessoal

📋 Sobre o Projeto

A aplicação tem como objetivo oferecer uma solução simples e acessível para o gerenciamento de finanças pessoais, transformando os registros de movimentações em uma 
experiência organizada, centralizada e orientada à tomada de decisão.
Por meio da aplicação, o usuário poderá registrar e organizar suas transações financeiras, classificá-las por categorias e visualizar um resumo de sua situação financeira. Além disso, será possível utilizar filtros e relatórios para facilitar a análise das movimentações.

💻 Tecnologias e Justificativas

As principais tecnologias utilizadas no desenvolvimento do projeto são:

Front-end - React
Back-end - Python
Banco de Dados - SQLite

🐍 Python

O Python foi escolhido para o desenvolvimento do back-end devido à sua presença significativa no conteúdo do curso. A linguagem foi abordada em diferentes unidades curriculares, como:

Pensamento Computacional;
Práticas de Programação;
Introdução à Ciência de Dados;
Estruturas de Dados.

Dessa forma, a utilização do Python permite aplicar conhecimentos adquiridos ao longo do curso, além de facilitar o desenvolvimento e a manutenção da aplicação pela familiaridade dos integrantes da equipe com a linguagem.

⚛️ React

O React foi escolhido para o desenvolvimento do front-end devido à sua facilidade de utilização, acessibilidade e possibilidade de evolução junto ao crescimento da aplicação.

Além disso, a tecnologia apresenta uma curva de aprendizado considerada adequada para os integrantes do grupo, permitindo que todos possam contribuir para o desenvolvimento do projeto.

🗄️ SQLite

O SQLite foi escolhido como banco de dados principalmente pela sua simplicidade de configuração e utilização.

As informações são armazenadas diretamente em um único arquivo local, dispensando a necessidade de instalação e configuração de um servidor de banco de dados. Essa característica torna o SQLite uma alternativa adequada para o contexto do projeto, facilitando tanto o desenvolvimento quanto a execução da aplicação em diferentes ambientes.

👥 Equipe

Adicione aqui os integrantes do grupo.

FELIPE SANTOS DE ALENCAR
ALISON MORETTO DIAS
GIOVANNA BASTOS RODRIGUES
IAGO FARIA DOS SANTOS
LEANDRO MORAIS DOS SANTOS
MARCELO LUCIANO SILVA ARAUJO
MICHAEL DE SOUZA TEIXEIRA
THAMIRES SANTOS MUNIZ

🚀 Status do Projeto

🟡 Em desenvolvimento

O projeto está sendo desenvolvido como parte da Unidade Curricular Projeto Integrador — Boas Práticas de Desenvolvimento de Software.

⚙️ Como iniciar o projeto localmente

1. Clonar o repositório

Clone o projeto:

git clone <URL_DO_REPOSITORIO>

2. Criar o ambiente virtual

python -m venv .venv

Ative: 

.venv\Scripts\activate

4. Instalar as dependências

pip install -r requirements.txt

5. Instale o projeto

pip install -e .

5. Configurar as variáveis de configuração

Crie uma pasta na raiz do projeto com o nome 'instance'
Crie uma arquivo chamado 'config.py'
Adicione as variáveis necessárias para o projeto.

Exemplo Configuração:

SQLALCHEMY_DATABASE_URI='sqlite:///storage.db'
JWT_SECRET_KEY='Ey@gpBk=ZFm3l3Pa!FI6i4n,KDJ.nsx'

6. Executar as migrações de banco de dados

flask --app api_organiza_ai db upgrade

7. Iniciar a aplicação

Com o ambiente virtual ativado:

flask --app api_organiza_ai run --debug

A api estará disponível em: http://127.0.0.1:5000/
A documentação estará disponível em : http://127.0.0.1:5000/apidocs/

Se o projeto estiver sendo configurado pela primeira vez e não possuir migrations, consulte a documentação do projeto antes de executar flask db migrate.