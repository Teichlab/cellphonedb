#!/usr/bin/env python3
import click

from cellphonedb.src.api_endpoints.terminal_api.method_terminal_api_endpoints import method_terminal_commands
from cellphonedb.src.api_endpoints.terminal_api.plot_terminal_api_endpoints import plot_terminal_commands
from cellphonedb.src.api_endpoints.terminal_api.query_terminal_api_endpoints import query_terminal_commands
from cellphonedb.src.api_endpoints.terminal_api.tools_terminal_api_endpoints import tools_terminal_commands


@click.group()
def cli():
    pass


@cli.group()
def method():
    pass


@cli.group()
def query():
    pass


@cli.group()
def tools():
    pass


@cli.group()
def plot():
    pass


method.add_command(method_terminal_commands.statistical_analysis)
method.add_command(method_terminal_commands.analysis)
query.add_command(query_terminal_commands.find_interactions_by_element)
query.add_command(query_terminal_commands.get_interaction_gene)
query.add_command(query_terminal_commands.cpdb_data_report)
tools.add_command(tools_terminal_commands.generate_genes)
tools.add_command(tools_terminal_commands.generate_interactions)
tools.add_command(tools_terminal_commands.generate_proteins)
plot.add_command(plot_terminal_commands.dot_plot)

if __name__ == '__main__':
    cli()
