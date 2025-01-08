import openai
import json
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
import os
from config import OPENAI_API_KEY

# Initialize Rich console for better formatting
console = Console()

# Set your OpenAI API key
openai.api_key = OPENAI_API_KEY

def get_aws_command(query, language="english"):
    system_prompt = """You are an AWS CLI expert. Convert the user's natural language query into the correct AWS CLI command.
    The user might ask in Turkish or English. If the query is in Turkish, still provide the AWS CLI command in English.
    For EC2 instances, always include necessary parameters like --image-id, --instance-type, --count, and --block-device-mappings.
    Provide only the command itself without any explanation. If you're not sure about the command, respond with 'UNKNOWN'.
    Make sure the command follows AWS CLI best practices and includes necessary parameters."""
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": query}
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        command = response.choices[0].message.content.strip()
        return command if command != "UNKNOWN" else None
        
    except Exception as e:
        console.print(f"[red]Detailed Error: {str(e)}[/red]")
        import traceback
        console.print(f"[red]{traceback.format_exc()}[/red]")
        return None

def main():
    # Rich console'u geniş çıktı için yapılandır
    console = Console(width=200)  # Terminal genişliğini artır
    
    console.print(Panel.fit(
        "[yellow]AWS CLI Assistant[/yellow]\n"
        "Type your query in natural language, and I'll convert it to an AWS CLI command.\n"
        "Type 'quit' or 'exit' to end the program.",
        title="Welcome"
    ))

    while True:
        try:
            query = console.input("\n[green]Enter your query[/green]: ")
            
            if query.lower() in ['quit', 'exit']:
                console.print("[yellow]Goodbye![/yellow]")
                break
                
            if not query.strip():
                continue
                
            with console.status("[cyan]Generating AWS CLI command...[/cyan]"):
                command = get_aws_command(query)
                
            if command:
                console.print("\n[bold cyan]Generated AWS CLI command:[/bold cyan]")
                # Basit metin formatında göster
                print("\n" + command + "\n")
                
                # Ask if user wants to execute the command
                execute = console.input("\n[yellow]Do you want to execute this command? (y/N): [/yellow]").lower()
                if execute == 'y':
                    os.system(command)
            else:
                console.print("[red]Sorry, I couldn't generate a command for your query.[/red]")
                
        except KeyboardInterrupt:
            console.print("\n[yellow]Goodbye![/yellow]")
            break
        except Exception as e:
            console.print(f"[red]Error: {str(e)}[/red]")

if __name__ == "__main__":
    main() 