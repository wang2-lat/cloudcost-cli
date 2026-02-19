import typer
from pathlib import Path
from rich.console import Console
from parser import parse_bill
from analyzer import analyze_costs
from predictor import predict_next_month
from reporter import generate_report

app = typer.Typer(help="Analyze cloud bills, find savings, and predict costs")
console = Console()

@app.command()
def analyze(
    csv_file: Path = typer.Argument(..., help="Path to cloud bill CSV file"),
    output: Path = typer.Option(None, "--output", "-o", help="Save report to file")
):
    """Analyze cloud bill and generate cost optimization report"""
    try:
        console.print(f"[cyan]Loading bill from {csv_file}...[/cyan]")
        df = parse_bill(csv_file)
        
        console.print("[cyan]Analyzing costs...[/cyan]")
        analysis = analyze_costs(df)
        
        console.print("[cyan]Predicting next month...[/cyan]")
        prediction = predict_next_month(df)
        
        generate_report(df, analysis, prediction, output)
        
        if output:
            console.print(f"[green]Report saved to {output}[/green]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

@app.command()
def predict(
    csv_file: Path = typer.Argument(..., help="Path to cloud bill CSV file")
):
    """Predict next month's cost based on historical data"""
    try:
        df = parse_bill(csv_file)
        prediction = predict_next_month(df)
        
        console.print(f"\n[bold cyan]Next Month Cost Prediction[/bold cyan]")
        console.print(f"Estimated cost: [bold green]${prediction['predicted_cost']:.2f}[/bold green]")
        console.print(f"Based on {prediction['days_analyzed']} days of data")
        console.print(f"Average daily cost: ${prediction['avg_daily_cost']:.2f}")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
