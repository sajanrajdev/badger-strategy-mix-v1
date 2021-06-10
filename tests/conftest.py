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
import pytest

@pytest.fixture
def tokens():
    return [WANT, LP_COMPONENT, REWARD_TOKEN]

@pytest.fixture
def deployed():
  """
    Deploys, vault, controller and strats and wires them up for you to test
  """
  deployer = accounts[0]

  strategist = deployer
  keeper = deployer
  guardian = deployer

  controller = Controller.deploy({"from": deployer})
  controller.initialize(
    BADGER_DEV_MULTISIG,
    strategist,
    keeper,
    BADGER_DEV_MULTISIG
  )

  sett = SettV3.deploy({"from": deployer})
  sett.initialize(
    WANT,
    controller.address,
    BADGER_DEV_MULTISIG,
    keeper,
    guardian,
    False,
    "prefix",
    "PREFIX"
  )



  strategy = MyStrategy.deploy({"from": deployer})
  strategy.initialize(
    BADGER_DEV_MULTISIG,
    strategist,
    controller.address,
    keeper,
    guardian,
    [WANT, LP_COMPONENT, REWARD_TOKEN],
    [DEFAULT_GOV_PERFORMANCE_FEE, DEFAULT_PERFORMANCE_FEE, DEFAULT_WITHDRAWAL_FEE]
  )

  return {"controller": controller, "vault": sett, "sett": sett, "strategy": strategy}