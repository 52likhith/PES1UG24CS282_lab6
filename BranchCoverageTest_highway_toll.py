import pytest

from highway_toll import pass_advice, toll_charge, toll_for


def test_axles_below_minimum_takes_invalid_branch():
    with pytest.raises(ValueError):
        toll_for(1, False, False)


def test_axles_at_minimum_takes_supported_toll_branch():
    assert toll_for(2, False, False) == 100


def test_axles_outside_supported_table_takes_default_branch():
    assert toll_for(6, False, False) == 400


def test_peak_branch_is_true():
    assert toll_for(4, True, False) == 312.5


def test_peak_branch_is_false():
    assert toll_for(4, False, False) == 250


def test_fastag_branch_is_true_for_two_axles():
    assert toll_for(2, False, True) == 90.0


def test_fastag_branch_is_false():
    assert toll_for(2, False, False) == 100


def test_fastag_branch_for_non_two_axles():
    assert toll_for(3, False, True) == 142.5


def test_exempt_vehicle_branch_is_true():
    assert toll_charge("ambulance", 5, True, False) == 0


def test_exempt_vehicle_branch_is_false():
    assert toll_charge("car", 2, False, False) == 100


def test_pass_advice_cost_greater_than_pass_price():
    assert pass_advice([(True, False)], 4, 300) == "buy_pass"


def test_pass_advice_cost_equals_pass_price():
    assert pass_advice([(False, False)], 2, 100) == "either"


def test_pass_advice_cost_less_than_pass_price():
    assert pass_advice([(False, True)], 2, 100) == "pay_per_trip"


def test_pass_advice_loop_with_zero_trips():
    assert pass_advice([], 2, 0) == "either"


@pytest.mark.parametrize(
    ("trips", "expected"),
    [
        ([(False, False)], "either"),
        ([(False, True)], "pay_per_trip"),
    ],
)
def test_pass_advice_loop_with_one_trip(trips, expected):
    pass_price = 100 if expected == "either" else 95
    assert pass_advice(trips, 2, pass_price) == expected


def test_pass_advice_loop_with_multiple_trips():
    trips = [(False, False), (True, True), (False, True)]
    assert pass_advice(trips, 2, 1000) == "pay_per_trip"
