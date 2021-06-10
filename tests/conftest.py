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
from dotmap import DotMap
from scripts.deploy import deploy
import pytest

@pytest.fixture
def tokens():
  return [WANT, LP_COMPONENT, REWARD_TOKEN]

@pytest.fixture
def deployed():
  """
    Deploys, vault, controller and strats and wires them up for you to test
  """

  return deploy()
