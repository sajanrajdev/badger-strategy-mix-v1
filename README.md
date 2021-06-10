# Yearn Strategy Brownie Mix


## What you'll find here

- Basic Solidity Smart Contract for creating your own Yearn Strategy ([`contracts/MyStrategy.sol`](contracts/MyStrategy.sol))

- Interfaces for some of the most used DeFi protocols on ethereum mainnet. ([`interfaces/`](`interfaces/`))
- Dependencies for OpenZeppeling and other libraries. ([`deps/`](`deps/`))

- Sample test suite that runs on mainnet fork. ([`tests/`](tests))

This mix is configured for use with [Ganache](https://github.com/trufflesuite/ganache-cli) on a [forked mainnet](https://eth-brownie.readthedocs.io/en/stable/network-management.html#using-a-forked-development-network).

## How does it work for the User

Let's say Alice holds 100 DAI and wants to start earning yield % on them.

For this Alice needs to `DAI.approve(vault.address, 100)`.

Then Alice will call `Vault.deposit(100)`.

Vault will then transfer 100 DAI from Alice to itself, and mint Alice the corresponding shares.

Alice can then redeem those shares using `Vault.withdrawAll()` for the corresponding DAI balance (exchanged at `Vault.pricePerShare()`).

## Installation and Setup

1. [Install Brownie](https://eth-brownie.readthedocs.io/en/stable/install.html) & [Ganache-CLI](https://github.com/trufflesuite/ganache-cli), if you haven't already.

2. Sign up for [Infura](https://infura.io/) and generate an API key. Store it in the `WEB3_INFURA_PROJECT_ID` environment variable.

```bash
export WEB3_INFURA_PROJECT_ID=YourProjectID
```

3. Sign up for [Etherscan](www.etherscan.io) and generate an API key. This is required for fetching source codes of the mainnet contracts we will be interacting with. Store the API key in the `ETHERSCAN_TOKEN` environment variable.

```bash
export ETHERSCAN_TOKEN=YourApiToken
```

4. Download the mix.

```bash
brownie bake yearn-strategy
```

## Basic Use

To deploy the demo Yearn Strategy in a development environment:

1. Open the Brownie console. This automatically launches Ganache on a forked mainnet.

```bash
  brownie console
```

2. Run Scripts for Deployment
```
  brownie run deploy
```

Deployment will set up a Vault, Controller and deploy your strategy

## Adding Configuration

## Specifying additional testing steps and checks
In order to snapshot certain balances, we use the Snapshot manager.
This class helps with verifying that ordinary procedures (deposit, withdraw, harvest), happened correctly.

See `/helpers/StrategyCoreResolver.py` for the base resolver that all strategies use
Edit `/helpers/StrategyResolver.py` to specify and verify how an ordinary harvest should behave

## Add your custom testing
Check the various tests under `/tests`
The file `/tests/test_custom` is already set up for you to write custom tests there

## Implementing Strategy Logic

[`contracts/MyStrategy.sol`](contracts/MyStrategy.sol) is where you implement your own logic for your strategy. In particular:
## TODO CHANGE THESE
* Customize the `initialize` Method
* Set a name in `MyStrategy.getName()`
* Set a version in `MyStrategy.version()`
* Write a way to calculate the want invested in `MyStrategy.balanceOfPool()`
* Write a method that returns true if the Strategy should be tended in `MyStrategy.isTendable()`
* Set a version in `MyStrategy.version()`
* Invest your want tokens via `Strategy._deposit()`.
* Take profits and repay debt via `Strategy.harvest()`.
* Unwind enough of your position to payback withdrawals via `Strategy._withdrawSome()`.
* Unwind all of your positions via `Strategy._withdrawAll()`.
* Rebalance the Strategy positions via `Strategy.tend()`.
* Make a list of all position tokens that should be protected against movements via `Strategy.protectedTokens()`.

## Testing

To run the tests:

```
brownie test
```

The example tests provided in this mix start by deploying and approving your [`Strategy.sol`](contracts/Strategy.sol) contract. This ensures that the loan executes succesfully without any custom logic. Once you have built your own logic, you should edit [`tests/test_flashloan.py`](tests/test_flashloan.py) and remove this initial funding logic.

See the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/tests-pytest-intro.html) for more detailed information on testing your project.

## Debugging Failed Transactions

Use the `--interactive` flag to open a console immediatly after each failing test:

```
brownie test --interactive
```

Within the console, transaction data is available in the [`history`](https://eth-brownie.readthedocs.io/en/stable/api-network.html#txhistory) container:

```python
>>> history
[<Transaction '0x50f41e2a3c3f44e5d57ae294a8f872f7b97de0cb79b2a4f43cf9f2b6bac61fb4'>,
 <Transaction '0xb05a87885790b579982983e7079d811c1e269b2c678d99ecb0a3a5104a666138'>]
```

Examine the [`TransactionReceipt`](https://eth-brownie.readthedocs.io/en/stable/api-network.html#transactionreceipt) for the failed test to determine what went wrong. For example, to view a traceback:

```python
>>> tx = history[-1]
>>> tx.traceback()
```

To view a tree map of how the transaction executed:

```python
>>> tx.call_trace()
```

See the [Brownie documentation](https://eth-brownie.readthedocs.io/en/stable/core-transactions.html) for more detailed information on debugging failed transactions.


## Deployment

When you are finished testing and ready to deploy to the mainnet:

1. [Import a keystore](https://eth-brownie.readthedocs.io/en/stable/account-management.html#importing-from-a-private-key) into Brownie for the account you wish to deploy from.
2. Edit [`scripts/deploy.py`](scripts/deploy.py) and add your keystore ID according to the comments.
3. Run the deployment script on the mainnet using the following command:

```bash
$ brownie run deployment --network mainnet
```

You will be prompted to enter your keystore password, and then the contract will be deployed.


## Known issues

### No access to archive state errors

If you are using Ganache to fork a network, then you may have issues with the blockchain archive state every 30 minutes. This is due to your node provider (i.e. Infura) only allowing free users access to 30 minutes of archive state. To solve this, upgrade to a paid plan, or simply restart your ganache instance and redploy your contracts.

# Resources

- Yearn [Discord channel](https://discord.com/invite/6PNv2nF/)
- Brownie [Gitter channel](https://gitter.im/eth-brownie/community)
- Alex The Entreprenerd on [Twitter](https://twitter.com/GalloDaSballo)