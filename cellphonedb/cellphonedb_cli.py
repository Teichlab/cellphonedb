#!/usr/bin/env python3
import os

import click

import cellphonedb.src.api_endpoints.terminal_api.database_terminal_api_endpoints.database_terminal_commands
from cellphonedb.src.api_endpoints.terminal_api import database_terminal_api_endpoints
from cellphonedb.src.api_endpoints.terminal_api.method_terminal_api_endpoints import method_terminal_commands
from cellphonedb.src.exceptions.MissingR import MissingR

try:
    from cellphonedb.src.api_endpoints.terminal_api.plot_terminal_api_endpoints import plot_terminal_commands
except MissingR:
    print('As there is no R environment set up, some functionalities will be disabled, e.g. plot')

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
def database():
    pass


method.add_command(method_terminal_commands.statistical_analysis)
method.add_command(method_terminal_commands.analysis)
query.add_command(query_terminal_commands.find_interactions_by_element)
query.add_command(query_terminal_commands.get_interaction_gene)

database.add_command(database_terminal_api_endpoints.database_terminal_commands.download)
database.add_command(database_terminal_api_endpoints.database_terminal_commands.list_remote)
database.add_command(database_terminal_api_endpoints.database_terminal_commands.list_local)

if locals().get('plot_terminal_commands'):
    @cli.group()
    def plot():
        pass


    plot.add_command(plot_terminal_commands.dot_plot)
    plot.add_command(plot_terminal_commands.heatmap_plot)

advanced_flag_var = 'ADVANCED'

if os.getenv(advanced_flag_var, None):
    @cli.group()
    def tools():
        pass


    database.add_command(database_terminal_api_endpoints.database_terminal_commands.collect)
    tools.add_command(tools_terminal_commands.generate_genes)
    tools.add_command(tools_terminal_commands.generate_proteins)
    tools.add_command(tools_terminal_commands.generate_complex)
    tools.add_command(tools_terminal_commands.generate_interactions)
    tools.add_command(tools_terminal_commands.filter_all)
    tools.add_command(tools_terminal_commands.generate_filter_and_collect)

if __name__ == '__main__':
    cli()
