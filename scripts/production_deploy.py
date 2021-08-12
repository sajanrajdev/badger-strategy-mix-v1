import time

from brownie import (
    accounts,
    network,
    MyStrategy, 
    SettV3, 
    AdminUpgradeabilityProxy,
    Controller,
    BadgerRegistry,
)

from config import (
  WANT,
  PROTECTED_TOKENS,
  FEES,
  REGISTRY
)

from dotmap import DotMap
import click
from rich.console import Console

console = Console()

sleep_between_tx = 1

def main():
    dev = connect_account()

    # Get actors from registry
    registry = BadgerRegistry.at(REGISTRY)

    strategist = registry.get("governance")
    guardian = registry.get("guardian")
    keeper = registry.get("keeper")
    proxyAdmin = registry.get("proxyAdmin")
    

    # Deploy controller
    controller = deploy_controller(dev, proxyAdmin)

    # Deploy Vaults and Strategies
    deploy_vaults_and_strategies(
        controller.address, 
        dev.address, # Deployer will be set as governance for testing stage
        strategist, 
        keeper, 
        guardian,
        dev,
        proxyAdmin
    )

def deploy_controller(dev, proxyAdmin):

    controller_logic = Controller.at("0x01d10fdc6b484BE380144dF12EB6C75387EfC49B") # Controller Logic

    # Deployer address will be used for all actors as controller will only be used for testing
    args = [
        dev.address,
        dev.address,
        dev.address,
        dev.address,
    ]

    controller_proxy = AdminUpgradeabilityProxy.deploy(
        controller_logic, 
        proxyAdmin, 
        controller_logic.initialize.encode_input(*args), 
        {'from': dev}
    )
    time.sleep(sleep_between_tx)

    ## We delete from deploy and then fetch again so we can interact
    AdminUpgradeabilityProxy.remove(controller_proxy)
    controller_proxy = Controller.at(controller_proxy.address)

    console.print(
        "[green]Controller was deployed at: [/green]", controller_proxy.address
    )

    return controller_proxy
    

def deploy_vaults_and_strategies(
    controller, 
    governance, 
    strategist, 
    keeper, 
    guardian, 
    dev,
    proxyAdmin
):
    # Deploy Vault

    args = [
        WANT,
        controller,
        governance,
        keeper,
        guardian,
        False,
        '',
        '',
    ]

    print("Vault Arguments: ", args)

    vault_logic = SettV3.at("0xAF0B504BD20626d1fd57F8903898168FCE7ecbc8") # SettV3 Logic
    time.sleep(sleep_between_tx)

    vault_proxy = AdminUpgradeabilityProxy.deploy(
        vault_logic, 
        proxyAdmin, 
        vault_logic.initialize.encode_input(*args), 
        {'from': dev}
    )
    time.sleep(sleep_between_tx)

    ## We delete from deploy and then fetch again so we can interact
    AdminUpgradeabilityProxy.remove(vault_proxy)
    vault_proxy = SettV3.at(vault_proxy.address)

    console.print(
        "[green]Vault was deployed at: [/green]", vault_proxy.address
    )

    assert vault_proxy.paused()

    vault_proxy.unpause({"from": dev})

    assert vault_proxy.paused() == False

    # Deploy Strategy

    args = [
        governance,
        strategist,
        controller,
        keeper,
        guardian,
        PROTECTED_TOKENS,
        FEES,
    ]

    print("Strategy Arguments: ", args)

    strat_logic = MyStrategy.deploy({"from": dev})
    time.sleep(sleep_between_tx)

    strat_proxy = AdminUpgradeabilityProxy.deploy(
        strat_logic, 
        proxyAdmin, 
        strat_logic.initialize.encode_input(*args), 
        {'from': dev}
    )
    time.sleep(sleep_between_tx)

    console.print(
        "[green]Strategy was deployed at: [/green]", strat_proxy.address
    )



def connect_account():
    click.echo(f"You are using the '{network.show_active()}' network")
    dev = accounts.load(click.prompt("Account", type=click.Choice(accounts.load())))
    click.echo(f"You are using: 'dev' [{dev.address}]")
    return dev