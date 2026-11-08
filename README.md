# HB Bots

Hub gráfico para abrir quatro versões de bots, pesquisar produtos em lojas e usar o Auto Typer.

## Downloads

As versões para Windows e Linux são publicadas na página **Releases** deste repositório. No Windows, baixe `HB-Bots.exe`. No Linux, baixe `HB-Bots`, torne o arquivo executável e abra-o a partir de uma sessão gráfica.

## Linux e Auto Typer

A interface gráfica funciona em Linux com Tk/Tkinter. O Auto Typer usa `pynput` e foi preparado para sessões X11. Em Wayland, o sistema pode bloquear a simulação de teclas por segurança; nesse caso, use uma sessão X11.

## Criar uma versão local

Instale Python 3.14 e os pacotes:

```bash
python -m pip install -r requirements.txt
```

Gere o executável com PyInstaller para o seu sistema. O workflow em `.github/workflows/build-release.yml` cria builds para Windows e Linux e publica uma Release ao enviar uma tag `v*`.

## Componentes

- `hub_app.py`: interface gráfica e janelas dos bots.
- `robo.py`, `bot.v2.py`, `bot.v3.py`, `botv3.5.py`: versões iniciadas pelo hub.
