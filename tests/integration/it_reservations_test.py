from datetime import datetime

from flask import url_for

import pytest

from timeless.restaurants.models import Reservation, ReservationStatus


@pytest.mark.skip
def test_create_reservation(client):
    """
    @todo #235:30min Find out why form validation is failing for the
     create_reservation test. Fields that are reported to be invalid
     are start_time, end_time and status. Remove skip annotation
     once form validation is fixed.
    """
    comment = "my comment"
    response = client.post(url_for("reservations.create"), data={
        "start_time": datetime.utcnow(),
        "end_time": datetime.utcnow(),
        "comment": comment,
        "num_of_persons": 2,
        "status": ReservationStatus.confirmed
    })
    assert response.location.endswith(url_for("reservations.list_reservations"))
    assert Reservation.query.count() == 1
    assert Reservation.query.get(1).comment == comment


def test_delete_reservation(client, db_session):
    id = 1
    reservation = Reservation(
        id=id,
        start_time=datetime.utcnow(),
        end_time=datetime.utcnow(),
        num_of_persons=2,
        status=ReservationStatus.confirmed,
        comment="test comment"
    )
    db_session.add(reservation)
    db_session.commit()
    response = client.post(url_for('reservations.delete', id=id))
    assert response.location.endswith(url_for("reservations.list_reservations"))
    assert Reservation.query.filter_by(id=id).count() == 0
