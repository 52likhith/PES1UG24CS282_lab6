import pytest

from highway_toll import pass_advice, toll_charge, toll_for


@pytest.mark.parametrize(
    ("axles", "expected"),
    [
        (2, 100),
        (3, 150),
        (4, 250),
    ],
)
def test_supported_axle_counts(axles, expected):
    assert toll_for(axles, False, False) == expected


def test_more_than_four_axles_uses_default_toll():
    assert toll_for(5, False, False) == 400


def test_invalid_axle_count_is_rejected():
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(1, False, False)


def test_peak_toll_includes_peak_multiplier():
    assert toll_for(3, True, False) == 187.5


def test_non_peak_toll_does_not_include_peak_multiplier():
    assert toll_for(3, False, False) == 150


def test_two_axle_fastag_receives_ten_percent_discount():
    assert toll_for(2, False, True) == 90.0


@pytest.mark.parametrize("axles", [3, 4, 5])
def test_other_axles_receive_five_percent_fastag_discount(axles):
    base_toll = {3: 150, 4: 250, 5: 400}[axles]
    assert toll_for(axles, False, True) == round(base_toll * 0.95, 2)


@pytest.mark.parametrize("vehicle", ["ambulance", "fire_engine"])
def test_exempt_emergency_vehicle_has_no_charge(vehicle):
    assert toll_charge(vehicle, 4, True, True) == 0


def test_regular_vehicle_receives_normal_toll_charge():
    assert toll_charge("car", 3, True, False) == 187.5


def test_pass_advice_recommends_buying_pass_when_trips_cost_more():
    trips = [(True, False), (False, True)]
    assert pass_advice(trips, 2, 180) == "buy_pass"


def test_pass_advice_returns_either_when_trip_cost_equals_pass_price():
    trips = [(False, False)]
    assert pass_advice(trips, 2, 100) == "either"


def test_pass_advice_recommends_pay_per_trip_when_trips_cost_less():
    trips = [(False, False)]
    assert pass_advice(trips, 4, 300) == "pay_per_trip"


def test_pass_advice_handles_empty_trip_list():
    assert pass_advice([], 2, 50) == "pay_per_trip"
