# AV1 - ETL Spotify & YouTube (Postgres + Streamlit)

Este projeto foi adaptado para usar **PostgreSQL** via Docker Compose e inclui amostras de dados e imagens do dashboard para anexar ao envio no Classroom.

## Mudanças principais
- `docker-compose.yml` agora inclui um serviço `db` (Postgres 15) e ajusta `app` para depender do banco.
- Adicionados dados de amostra em `data/` para facilitar testes offline.
- Dashboard melhorado com mais gráficos e filtros (arquivo `app.py`).
- Geradas imagens PNG do dashboard em `artifacts/` para anexar ao material de entrega.

## Como rodar com Docker (recomendado)
1. Copie `config.example.env` para `.env` e ajuste se necessário.
2. Build e run:
```bash
docker-compose up --build
```
3. Acesse: http://localhost:8501

## Como rodar localmente (sem Docker)
1. Crie e ative um ambiente virtual.
2. Instale dependências:
```bash
pip install -r requirements.txt
pip install psycopg2-binary
```
3. Configure `DATABASE_URL` no `.env` para apontar ao seu PostgreSQL (ou use o default sqlite do projeto).
4. Execute os scripts ETL (os arquivos de extração dependem de credenciais das APIs):
```bash
python extract_spotify.py
python extract_youtube.py
python transform_load.py
```

## Subir no GitHub (comandos prontos)
```bash
git init
git add .
git commit -m "feat: AV1 ETL Spotify+YouTube - Postgres, dashboard melhorado, sample data"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/av1-etl-spotify-youtube.git
git push -u origin main
```
Substitua `https://github.com/SEU_USUARIO/av1-etl-spotify-youtube.git` pelo repositório que você criar no GitHub.

---
