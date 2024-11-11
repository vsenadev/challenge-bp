# COMMENTS.md

Para executar a aplicação, é necessário ter o **Python 3** e o **Flask** instalados no ambiente.

- **Instalando o Flask**: Caso o Flask ainda não esteja instalado, execute o comando abaixo para instalá-lo:

```bash
python -m venv venv
```
```bash
.\venv\Scripts\activate
```
```bash
  pip install Flask
```
```bash
  python app.py
```

- A seguinte mensagem será exibida
```bash
 Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
```

Abra um navegador e digite 
```link
http://localhost:8080/jogo/simular
```

- **Exemplo da resposta**
```json
{
    "vencedor": "cauteloso",
    "jogadores": ["cauteloso", "aleatorio", "exigente", "impulsivo"]
}
```
