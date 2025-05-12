# -*- coding: utf-8 -*-
"""Event unit tests."""

from datetime import datetime, timedelta

import pytest
import pytz

from dribdat.user.validators import event_date_check, event_time_check
from dribdat.user.models import Event
from dribdat.admin.forms import EventForm
from dribdat.utils import timesince
from dribdat.settings import Config
from dribdat.aggregation import ProjectActivity
from dribdat.futures import UTC

from .factories import UserFactory, ProjectFactory, EventFactory


@pytest.mark.usefixtures("db")
class TestEvent:
    """Event tests."""

    def is_naive(d):
        return d.tzinfo is None or d.tzinfo.utcoffset(d) is None

    def test_event_validator(self):
        now = datetime.now(UTC)
        event = Event(name="test", starts_at=now)
        event.save()
        form = EventForm(obj=event)
        assert event_time_check(form)
        assert event_date_check(form)

    def test_countdown_10_days(self):
        timezone = pytz.timezone(Config.TIME_ZONE)
        now = datetime.now(UTC)
        event_dt = now + timedelta(days=10)
        event = Event(name="test", starts_at=event_dt)
        event.save()

        assert event.starts_at != event_dt  # store as naive!?
        assert event.name == "test"
        assert event.countdown is not None
        assert event.countdown == event_dt.replace(tzinfo=timezone)
        assert timesince(event.countdown, until=True) == "1 week"

    def test_countdown_24_days(self):
        now = datetime.now(UTC)
        timezone = pytz.timezone(Config.TIME_ZONE)
        event_dt = now + timedelta(days=24)
        event = Event(name="test", starts_at=event_dt)
        event.save()

        assert event.starts_at != event_dt  # store as naive!?
        assert event.name == "test"
        assert event.countdown is not None
        assert event.countdown == event_dt.replace(tzinfo=timezone)
        assert timesince(event.countdown, until=True) == "3 weeks"

    def test_countdown_4_hours(self):
        now = datetime.now(UTC)
        # need to add 10 seconds to avoid timesince to compute 3.9999h
        # formated to 3 by timesince
        event_dt = now + timedelta(hours=4, seconds=10)
        event = Event(name="test", starts_at=event_dt)
        event.save()

        timediff = event_dt - now
        timediff_hours = timediff.total_seconds() // 3600

        assert event.name == "test"
        assert event.countdown is not None
        assert event.countdown == event_dt
        assert timesince(event.countdown, until=True) == "%d hours" % timediff_hours

    def test_event_projects(self):
        event = EventFactory()
        event.save()
        p1 = ProjectFactory()
        p1.event = event
        p1.save()
        p2 = ProjectFactory()
        p2.event = event
        p2.save()
        p3 = ProjectFactory()
        p3.event = event
        p3.is_hidden = True
        p3.save()
        assert event.project_count == 2
        assert p1 in event.current_projects()
        assert p3 not in event.current_projects()

    def test_event_certify(self):
        event = EventFactory()
        user = UserFactory()
        user.save()
        assert user.may_certify() == (False, "projects")
        project = ProjectFactory()
        project.event = event
        project.save()
        ProjectActivity(project, "star", user)
        assert user.may_certify(project) == (False, "projects")
        project.progress = 100
        project.save()
        assert project in user.joined_projects(False)
        assert user.may_certify(project) == (False, "event")
        event.certificate_path = "https://testcert.cc/{username}"
        event.save()
        cert_status, cert_url = user.may_certify(project)
        assert cert_status
        assert "testcert" in cert_url
        assert user.username in cert_url
