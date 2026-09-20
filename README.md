# Projeto-final-curso---Luxury-Wheels – Sistema de Gestão de Aluguer de Veículos

Aplicação desktop desenvolvida como projeto final de curso, para gestão completa de um negócio de aluguer de veículos de luxo.

## Tecnologias
- Python
- Tkinter (interface gráfica)
- SQLite (base de dados)
- openpyxl (exportação para Excel)

## Funcionalidades principais
- Login com autenticação
- Gestão completa (CRUD) de clientes, veículos, formas de pagamento e reservas
- Base de dados relacional com 5 tabelas (utilizadores, clientes, veículos, formas de pagamento, reservas)
- Dashboard com indicadores: aluguéres ativos, últimos clientes registados, veículos disponíveis por categoria, total financeiro mensal e alertas de vencimento (seguro/inspeção)
- Exportação de dados para Excel em todos os módulos
- Validações de datas, formulários e regras de negócio (ex.: impedir eliminar veículos com reservas ativas)

## Resultado
Projeto avaliado com nota de 88/100.

## Melhorias futuras
- Hashing de passwords (atualmente em texto simples)
- Refatoração para arquitetura modular (separar interface, base de dados e lógica de negócio)
- Uso de tipos SQL mais adequados para valores monetários

## Como executar

1. Certifica-te que tens Python instalado (3.x)
2. Instala a dependência necessária: pip install openpyxl
3. Corre a aplicação: python projeto_b.py
4. **Nota:** `tkinter` e `sqlite3` já vêm incluídos por defeito na instalação do Python, não precisas de os instalar.
