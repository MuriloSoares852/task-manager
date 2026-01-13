# Sistema de Gerenciamento de Tarefas - TechFlow Solutions

## Sobre o Projeto
Este projeto foi desenvolvido como parte da disciplina de Engenharia de Software e implementa um sistema completo de gerenciamento de tarefas seguindo metodologias ágeis. O sistema permite que equipes acompanhem o fluxo de trabalho em tempo real, priorizem tarefas críticas e monitorem o desempenho através de uma interface web intuitiva.

### Objetivo
Desenvolver uma solução prática para gestão de tarefas que atenda às necessidades da startup de logística fictícia, aplicando conceitos de:

Metodologias Ágeis (Kanban)
Desenvolvimento orientado a testes (TDD)
Integração e entrega contínua (CI/CD)
Controle de qualidade de software

### Arquitetura e Tecnologias
Stack Tecnológica

Backend: Python 3.9+ com Flask
Banco de Dados: SQLite (desenvolvimento)
Testes: Pytest com cobertura de código
CI/CD: GitHub Actions
Frontend: HTML5, CSS3, JavaScript (Vanilla)

### Funcionalidades Implementadas
### CRUD Completo

Create: Criar novas tarefas com título, descrição, prioridade e status
Read: Visualizar todas as tarefas ou filtrar por status
Update: Atualizar informações de tarefas existentes
Delete: Remover tarefas concluídas ou obsoletas

### Recursos Adicionais

Dashboard com estatísticas em tempo real
Filtros por status (Pendente, Em Progresso, Concluída)
Sistema de prioridades (Baixa, Média, Alta)
Interface responsiva e moderna
API RESTful documentada

### Metodologia Ágil Utilizada
Kanban
O projeto utiliza a metodologia Kanban para gestão visual do fluxo de trabalho, implementada através do GitHub Projects com as seguintes colunas:

To Do (A Fazer): Tarefas planejadas aguardando início

In Progress (Em Progresso): Tarefas em desenvolvimento ativo

Done (Concluído): Tarefas finalizadas e testadas

### Instalação e Execução
Pré-requisitos

Python 3.9 ou superior
pip (gerenciador de pacotes Python)
Git

Passo a Passo

Clone o repositório

bashgit clone https://github.com/SEU_USUARIO/task-manager.git
cd task-manager

Crie um ambiente virtual (recomendado)

bashpython -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

Instale as dependências

bashpip install -r requirements.txt

Execute a aplicação

bashpython app.py

Acesse no navegador

http://localhost:5000
