import os
import time
import subprocess
import sys

def check_dependencies():
    """Garante que a biblioteca 'rich' está instalada para a interface."""
    try:
        import rich
    except ImportError:
        print("Instalando a biblioteca de interface 'rich' necessária...")
        subprocess.run([sys.executable, "-m", "pip", "install", "rich"], check=True)
        import rich
    return rich

rich_module = check_dependencies()
from rich.console import Console
from rich.panel import Panel
from rich.status import Status
from rich.prompt import Confirm

console = Console()

def run_command(command, description):
    """Executa um comando shell com um spinner."""
    with console.status(f"[bold green]{description}...", spinner="dots"):
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode != 0:
            console.print(f"[bold red]Erro durante: {description}")
            console.print(result.stderr)
            return False
        return True

def wait_for_postgres():
    """Aguarda o container do banco de dados ficar saudável."""
    with console.status("[bold yellow]Aguardando o banco de dados ficar pronto e saudável...", spinner="bouncingBar"):
        while True:
            # Usamos 'docker compose ps' para verificar o status.
            # Funciona em Windows, Linux e Mac se o Docker estiver instalado.
            result = subprocess.run("docker compose ps db", shell=True, capture_output=True, text=True)
            output = result.stdout.lower()
            if "healthy" in output or "up" in output:
                # Se o docker-compose.yml tiver um healthcheck, 'healthy' é o melhor indicador.
                if "healthy" in output or ("up" in output and "starting" not in output):
                    break
            time.sleep(2)
    console.print("[bold green]✔ O banco de dados está pronto![/bold green]")

def check_pdf():
    """Verificação interativa do arquivo document.pdf."""
    while True:
        if os.path.exists("document.pdf"):
            console.print("[bold green]✔ Arquivo document.pdf encontrado[/bold green]")
            return True
        else:
            console.print(Panel(
                "[bold red]Arquivo 'document.pdf' não encontrado![/bold red]\n\n"
                "Por favor, coloque seu arquivo PDF na pasta raiz e nomeie-o como [bold]document.pdf[/bold].",
                title="Arquivo Ausente",
                border_style="red"
            ))
            input("\nPressione Enter assim que colocar o arquivo na pasta raiz...")

def main():
    console.clear()
    console.print(Panel.fit(
        "[bold cyan]Gerenciador do Aplicativo de Busca Semântica[/bold cyan]",
        border_style="blue",
        padding=(1, 5)
    ))
    
    # 1. Iniciar Containers
    if not run_command("docker compose up -d", "Iniciando os containers Docker"):
        console.print("[bold red]Falha ao iniciar o Docker. Certifique-se de que o Docker está rodando e você está na raiz do projeto.[/bold red]")
        sys.exit(1)
        
    # 2. Aguardar Banco de Dados
    wait_for_postgres()
    
    # 3. Verificar PDF
    check_pdf()
    
    # 4. Ingestão
    console.print("\n[bold yellow]Passo 1: Ingerindo o documento...[/bold yellow]")
    process = subprocess.run([sys.executable, "src/ingest.py"])
    if process.returncode != 0:
        console.print("[bold red]A ingestão falhou. Por favor, verifique seu arquivo .env e suas chaves de API.[/bold red]")
        sys.exit(1)
    
    # 5. Chat
    console.print("\n[bold yellow]Passo 2: Iniciando a Interface de Chat...[/bold yellow]")
    console.print("[italic white]Para sair do chat, digite 'sair'. Para parar o app, use Ctrl+C.[/italic white]\n")
    
    try:
        subprocess.run([sys.executable, "src/chat.py"])
    except KeyboardInterrupt:
        pass
    
    console.print("\n[bold blue]Obrigado por usar a Busca Semântica![/bold blue]")
    
    if Confirm.ask("Gostaria de desligar os containers Docker?", choices=["s", "n"], default="s"):
        run_command("docker compose down", "Parando os containers")
        console.print("[bold green]Containers parados. Até logo![/bold green]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold red]Operação cancelada pelo usuário.[/bold red]")
        sys.exit(0)
