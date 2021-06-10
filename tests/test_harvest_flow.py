from brownie import Contract
from config import (
  BADGER_DEV_MULTISIG,
  WANT,
  LP_COMPONENT,
  REWARD_TOKEN,
  DEFAULT_GOV_PERFORMANCE_FEE,
  DEFAULT_PERFORMANCE_FEE,
  DEFAULT_WITHDRAWAL_FEE
)

def test_deposit_withdraw_single_user_flow(deployed, tokens):
    deployer = accounts[0]
    vault = deployed["vault"]
    controller = deployed["controller"]
    strategy = deployed["strategy"]

    settKeeper = accounts.at(vault.keeper(), force=True)

    snap = BalanceSnapshotter(tokens, [deployer.address, vault.address, controller.address, strategy.address])

    randomUser = accounts[6]

    ## Get some WANT
    want = Contract(WANT, deployer)
    want.mint(deployer, 500000)

    print("== Testing == ", settConfig["id"], want.address)
    # Deposit
    assert want.balanceOf(deployer) > 0

    depositAmount = int(want.balanceOf(deployer) * 0.8)
    assert depositAmount > 0

    want.approve(vault, MaxUint256, {"from": deployer})

    before = snap.snap()
    snap.settDeposit(depositAmount, {"from": deployer})
    after = snap.snap()

    snap.diff_last_two()

    # Earn
    with brownie.reverts("onlyAuthorizedActors"):
        vault.earn({"from": randomUser})

    min = vault.min()
    max = vault.max()
    remain = max - min

    snap.settEarn({"from": settKeeper})

    chain.sleep(15)
    chain.mine(1)

    snap.settWithdraw(depositAmount // 2, {"from": deployer})

    chain.sleep(10000)
    chain.mine(1)

    snap.settWithdraw(depositAmount // 2 - 1, {"from": deployer})