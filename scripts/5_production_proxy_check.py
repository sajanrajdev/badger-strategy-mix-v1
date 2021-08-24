from brownie import network, BadgerRegistry, Controller, SettV3, web3
from config import REGISTRY
from helpers.constants import AddressZero
from rich.console import Console

console = Console()

ADMIN_SLOT = int(
    0xb53127684a568b3173ae13b9f8a6016e243e63b6e8ee1178d6a717850b5d6103
)

def main():
    """
    Checks that the proxyAdmin of all contracts added to the BadgerRegistry match
    the proxyAdminTimelock address from the same registry. How to run:

    1. Add all keys for the network's registry to the 'keys' array below.
    
    2. Add all authors' addresses with vaults added to the registry into the 'authors' array below. 

    3. Run the script and review the console output.
    """

    console.print("You are using the", network.show_active(), "network")

    # Get production registry
    registry = BadgerRegistry.at(REGISTRY)

    # Get proxyAdminTimelock address to compare to
    proxyAdmin = registry.get("proxyAdminTimelock")
    assert proxyAdmin != AddressZero
    console.print("[cyan]proxyAdminTimelock:[/cyan]", proxyAdmin)

    # NOTE: Add all existing keys from your network's registry. For example:
    keys = [
        "governance",
        "guardian",
        "keeper",
        "controller",
        "badgerTree",
        "devGovernancce",
        "paymentsGovernance",
        "governanceTimelock",
        "proxyAdminDev",
        "rewardsLogger",
        "keeperAccessControl",
        "proxyAdminDfdBadger",
        "dfdBadgerSharedGovernance"
    ]

    # NOTE: Add all authors from your network registry. For example:
    authors = [
        "0xeE8b29AA52dD5fF2559da2C50b1887ADee257556"
    ]

    check_by_keys(registry, proxyAdmin, keys)
    check_vaults_and_strategies(registry, proxyAdmin, authors)


def check_by_keys(registry, proxyAdmin, keys):
    console.print("[blue]Checking proxyAdmins by key...[/blue]")
    # Check the proxyAdmin of the different proxy contracts
    for key in keys:
        proxy = registry.get(key)
        if proxy == AddressZero:
            console.print(
                key, ":[red] key doesn't exist on the registry![/red]"
            )
            continue
        check_proxy_admin(proxy, proxyAdmin, key)


def check_vaults_and_strategies(registry, proxyAdmin, authors):
    console.print("[blue]Checking proxyAdmins from vaults and strategies...[/blue]")

    vaultStatus = [0, 1, 2]

    vaults = []
    strategies = []
    stratNames = []

    # get vaults by author
    for author in authors:
        vaults += registry.getVaults("v1", author)
        vaults += registry.getVaults("v2", author)

    # Get promoted vaults
    for status in vaultStatus:
        vaults += registry.getFilteredProductionVaults("v1", status)
        vaults += registry.getFilteredProductionVaults("v2", status)

    # Get strategies from vaults and check vaults' proxyAdmins
    for vault in vaults:
        vaultContract = SettV3.at(vault)
        # get Controller
        controller = Controller.at(vaultContract.controller())
        strategies.append(controller.strategies(vaultContract.token()))
        stratNames.append(vaultContract.name().replace("Badger Sett ", "Strategy "))
        # Check vault proxyAdmin
        check_proxy_admin(vault, proxyAdmin, vaultContract.name())


    for strat in strategies:
    # Check strategies' proxyAdmin
        check_proxy_admin(strat, proxyAdmin, stratNames[strategies.index(strat)])


def check_proxy_admin(proxy, proxyAdmin, key):
    # Get proxyAdmin address form the proxy's ADMIN_SLOT 
    val = web3.eth.getStorageAt(proxy, ADMIN_SLOT).hex()
    address = "0x" + val[26:66]

    # Check differnt possible scenarios
    if address == AddressZero:
        console.print(
            key, ":[red] admin not found on slot (GnosisSafeProxy?)[/red]"
        )
    elif address != proxyAdmin:
        console.print(
            key, ":[red] admin is different to proxyAdminTimelock[/red] - ", 
            address
        )
    else:
        assert address == proxyAdmin
        console.print(
            key, ":[green] admin matches proxyAdminTimelock![/green]"
        )