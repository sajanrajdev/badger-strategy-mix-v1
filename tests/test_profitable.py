import brownie
from brownie import *
from helpers.constants import MaxUint256
from helpers.SnapshotManager import SnapshotManager

# TODO: Put in separate file
def test_is_profitable(deployed):
  deployer = deployed.deployer
  vault = deployed.vault
  controller = deployed.controller
  strategy = deployed.strategy
  want = deployed.want
  randomUser = accounts[6]

  initial_balance = want.balanceOf(deployer)
  
  settKeeper = accounts.at(vault.keeper(), force=True)

  snap = SnapshotManager(vault, strategy, controller, "StrategySnapshot")

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

  snap.settEarn({"from": settKeeper})

  chain.sleep(15)
  chain.mine(1)

  snap.settWithdrawAll({"from": deployer})

  ending_balance = want.balanceOf(deployer)
  
  assert initial_balance <= ending_balance ## TODO: Account for fees