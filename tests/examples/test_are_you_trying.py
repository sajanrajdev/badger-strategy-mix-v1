from helpers.constants import MaxUint256


def test_deploy_settings(deployer, sett, strategy, want):
  """
    Verifies that you set up the Strategy properly
  """
  # Setup
  startingBalance = want.balanceOf(deployer)
  
  depositAmount = startingBalance // 2
  assert startingBalance >= depositAmount
  assert startingBalance >= 0
  # End Setup

  # Deposit
  assert want.balanceOf(sett) == 0

  want.approve(sett, MaxUint256, {"from": deployer})
  sett.deposit(depositAmount, {"from": deployer})

  # Did the deposit move funds into Strat and not in sett?
  assert want.balanceOf(sett) == 0

  # Did the strategy do something with the asset?
  assert strategy.balanceOf(want) == 0

  # Change to this if the strat is supposed to hodl and do nothing
  #assert strategy.balanceOf(want) = depositAmount


  