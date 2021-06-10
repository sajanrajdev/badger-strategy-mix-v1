import brownie
from brownie import *
from config import (
  BADGER_DEV_MULTISIG,
  WANT,
  LP_COMPONENT,
  REWARD_TOKEN,
  DEFAULT_GOV_PERFORMANCE_FEE,
  DEFAULT_PERFORMANCE_FEE,
  DEFAULT_WITHDRAWAL_FEE
)
from helpers.constants import MaxUint256
from helpers.SnapshotManager import SnapshotManager


def test_deposit_withdraw_single_user_flow(deployed):
    deployer = deployed.deployer
    ## TODO: Separate into separate fixutres, because it's cooler
    vault = deployed.vault
    controller = deployed.controller
    strategy = deployed.strategy
    want = deployed.want

    settKeeper = accounts.at(vault.keeper(), force=True)

    snap = SnapshotManager(vault, strategy, controller, "StrategySnapshot")

    randomUser = accounts[6]

    initial_balance = want.balanceOf(deployer)

    # Deposit
    assert want.balanceOf(deployer) > 0

    depositAmount = int(want.balanceOf(deployer) * 0.8)
    assert depositAmount > 0

    want.approve(vault.address, MaxUint256, {"from": deployer})

    snap.settDeposit(depositAmount, {"from": deployer})
    

    # Earn
    with brownie.reverts("onlyAuthorizedActors"):
        vault.earn({"from": randomUser})

    min = vault.min()
    max = vault.max()
    remain = max - min

    # snap.settEarn({"from": settKeeper})
    vault.earn({"from": settKeeper})

    chain.sleep(15)
    chain.mine(1)

    snap.settWithdraw(depositAmount // 2, {"from": deployer})

    chain.sleep(10000)
    chain.mine(1)

    snap.settWithdraw(depositAmount // 2 - 1, {"from": deployer})

    ending_balance = want.balanceOf(deployer)

    assert initial_balance <= ending_balance ## TODO: Account for fees


## 