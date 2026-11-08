# HB Bots

Hub gráfico para abrir quatro versões de bots, pesquisar produtos em lojas e usar o Auto Typer.

## Downloads

Baixe a versão desejada na [página de Releases](https://github.com/devworkscodes-ui/hb-bots/releases/latest):

- **Windows:** `HB-Bots.exe`
- **Linux:** `HB-Bots`

## Executar no Linux

1. Baixe o arquivo `HB-Bots` da Release e abra um terminal na pasta onde ele foi salvo.
2. Torne o arquivo executável:

   ```bash
chmod +x HB-Bots
```

3. Inicie o hub:

   ```bash
./HB-Bots
```

O aplicativo precisa de uma sessão gráfica Linux. O Auto Typer funciona melhor em **X11**. Em **Wayland**, o sistema pode bloquear a simulação de teclas; se isso ocorrer, entre numa sessão X11.

## Criar uma versão local

Instale Python 3.14 e os pacotes:

```bash
python -m pip install -r requirements.txt
```

O workflow em `.github/workflows/build-release.yml` cria versões para Windows e Linux e publica uma Release.

## Componentes

- `hub_app.py`: interface gráfica e janelas dos bots.
- `robo.py`, `bot.v2.py`, `bot.v3.py`, `botv3.5.py`: versões iniciadas pelo hub.
