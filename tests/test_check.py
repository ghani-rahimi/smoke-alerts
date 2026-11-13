from smoke_alerts.check import decide


def test_first_crossing_sends():
    assert decide("BARGO", 40, 25, already_alerting=False) == (True, True)


def test_stays_quiet_while_still_high():
    assert decide("BARGO", 60, 25, already_alerting=True) == (False, True)


def test_resets_when_back_under():
    assert decide("BARGO", 12, 25, already_alerting=True) == (False, False)
