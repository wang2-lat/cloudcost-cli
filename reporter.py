from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from pathlib import Path

def generate_report(df, analysis, prediction, output_file=None):
    """Generate visual cost report using rich"""
    
    console = Console(record=True) if output_file else Console()
    
    # Header
    console.print("\n[bold cyan]Cloud Cost Analysis Report[/bold cyan]\n")
    
    # Summary panel
    summary = f"""
[bold]Total Cost:[/bold] ${analysis['total_cost']:.2f}
[bold]Average Daily Cost:[/bold] ${analysis['avg_daily_cost']:.2f}
[bold]Max Daily Cost:[/bold] ${analysis['max_daily_cost']:.2f}
[bold]Days Analyzed:[/bold] {len(df['date'].unique())}
    """
    console.print(Panel(summary, title="Summary", border_style="green"))
    
    # Top services table
    console.print("\n[bold yellow]Top 5 Most Expensive Services[/bold yellow]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Service", style="cyan")
    table.add_column("Cost", justify="right", style="green")
    table.add_column("% of Total", justify="right")
    
    for service, cost in analysis['top_services'].items():
        percentage = (cost / analysis['total_cost']) * 100
        table.add_row(service, f"${cost:.2f}", f"{percentage:.1f}%")
    
    console.print(table)
    
    # Cost spikes
    if analysis['cost_spikes']:
        console.print("\n[bold red]⚠️  Cost Spikes Detected[/bold red]")
        spike_table = Table(show_header=True, header_style="bold red")
        spike_table.add_column("Date", style="yellow")
        spike_table.add_column("Cost", justify="right", style="red")
        
        for date, cost in list(analysis['cost_spikes'].items())[:5]:
            spike_table.add_row(str(date)[:10], f"${cost:.2f}")
        
        console.print(spike_table)
    
    # Idle resources
    if analysis['idle_resources']:
        console.print(f"\n[bold orange]💡 Found {len(analysis['idle_resources'])} potentially idle resources[/bold orange]")
        console.print(f"Resources: {', '.join(analysis['idle_resources'][:5])}")
    
    # Prediction
    console.print("\n[bold cyan]Next Month Prediction[/bold cyan]")
    pred_panel = f"""
[bold]Predicted Cost:[/bold] ${prediction['predicted_cost']:.2f}
[bold]Trend:[/bold] {prediction['trend'].capitalize()}
[bold]Based on:[/bold] {prediction['days_analyzed']} days of data
    """
    console.print(Panel(pred_panel, title="Forecast", border_style="blue"))
    
    # Recommendations
    console.print("\n[bold green]💰 Cost Optimization Recommendations[/bold green]")
    recommendations = [
        f"Review top service: {list(analysis['top_services'].keys())[0]} (${list(analysis['top_services'].values())[0]:.2f})",
        f"Investigate {len(analysis['cost_spikes'])} cost spike(s)" if analysis['cost_spikes'] else "No unusual spikes detected",
        f"Consider removing {len(analysis['idle_resources'])} idle resource(s)" if analysis['idle_resources'] else "No idle resources found"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        console.print(f"  {i}. {rec}")
    
    console.print()
    
    # Save to file if requested
    if output_file:
        console.save_html(str(output_file))
