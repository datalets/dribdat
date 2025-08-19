# -*- coding: utf-8 -*-
"""
Additional tests for auth views to increase coverage.
"""
from flask import url_for
from dribdat.user.models import User
from .factories import UserFactory
import dribdat.public.auth

class TestAuthExtra:
    def test_register_disabled(self, user, testapp):
        """Test registration when it's disabled."""
        testapp.app.config['DRIBDAT_NOT_REGISTER'] = True
        res = testapp.get(url_for('auth.register'))
        assert res.status_code == 302
        res = res.follow()
        assert 'Registration currently not possible' in res

    def test_register_first_user_is_admin(self, db, testapp):
        """Test that the first registered user becomes an admin."""
        assert User.query.count() == 0
        res = testapp.get(url_for('auth.register'))
        form = res.forms['registerForm']
        form['username'] = 'firstadmin'
        form['email'] = 'admin@example.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'Administrative user created' in res
        new_user = User.query.filter_by(username='firstadmin').first()
        assert new_user.is_admin

    def test_register_with_user_approval(self, user, testapp):
        """Test registration when user approval is required."""
        testapp.app.config['DRIBDAT_USER_APPROVE'] = True
        testapp.app.config['MAIL_SERVER'] = 'localhost'
        testapp.app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'
        res = testapp.get(url_for('auth.register'))
        form = res.forms['registerForm']
        form['username'] = 'newuser'
        form['email'] = 'newuser@example.com'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'New accounts require activation' in res
        new_user = User.query.filter_by(username='newuser').first()
        assert not new_user.active

    def test_inactive_user_profile_warning(self, db, testapp):
        """Test that an inactive user sees a warning on their profile page."""
        user = UserFactory(active=False, password='password')
        db.session.commit()
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'password'
        res = form.submit().follow()
        res = testapp.get(url_for('auth.user_profile'))
        assert 'This user account is under review' in res

    def test_user_profile_update(self, user, db, testapp):
        """Test that a user can update their profile."""
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        res = form.submit().follow()
        res = testapp.get(url_for('auth.user_profile'))
        form = res.forms['userEdit']
        form['email'] = 'newemail@example.com'
        form['webpage_url'] = 'http://new-web.page'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'Profile updated' in res
        updated_user = User.query.get(user.id)
        assert updated_user.email == 'newemail@example.com'
        assert updated_user.webpage_url == 'http://new-web.page'

    def test_user_profile_update_existing_email(self, user, db, testapp):
        """Test that a user cannot update their email to an existing one."""
        UserFactory(email='existing@example.com')
        db.session.commit()
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        res = form.submit().follow()
        res = testapp.get(url_for('auth.user_profile'))
        form = res.forms['userEdit']
        form['email'] = 'existing@example.com'
        res = form.submit()
        assert 'This e-mail address is already registered' in res

    def test_user_profile_sso_no_password_change(self, user, db, testapp):
        """Test that an SSO user cannot change their password."""
        user.sso_id = 'some_sso_id'
        db.session.commit()
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        res = form.submit().follow()
        res = testapp.get(url_for('auth.user_profile'))
        assert 'password' not in res.forms['userEdit'].fields

    def test_user_story_update(self, user, db, testapp):
        """Test that a user can update their story."""
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        res = form.submit().follow()
        res = testapp.get(url_for('auth.user_story'))
        form = res.forms['userStory']
        form['my_skills'] = 'python, flask'
        form['my_wishes'] = 'javascript, react'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'Story updated' in res
        updated_user = User.query.get(user.id)
        assert updated_user.my_skills == ['python', 'flask']
        assert updated_user.my_wishes == ['javascript', 'react']

    def test_login_inactive_user(self, db, testapp):
        """Test that an inactive user can log in but is warned."""
        user = UserFactory(active=False, password='password')
        db.session.commit()
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'password'
        res = form.submit().follow()
        # The warning is on the user profile page
        res = testapp.get(url_for('auth.user_profile'))
        assert 'This user account is under review' in res

    def test_passwordless_login(self, db, testapp):
        """Test the passwordless login mechanism."""
        user = UserFactory(email='test@example.com')
        db.session.commit()
        testapp.app.config['MAIL_SERVER'] = 'localhost'
        testapp.app.config['MAIL_DEFAULT_SENDER'] = 'test@example.com'
        res = testapp.get(url_for('auth.forgot'))
        form = res.forms['forgotForm']
        form['username'] = 'test@example.com'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'an activation mail' in res

    def test_delete_my_account(self, user, db, testapp):
        """Test that a user can delete their account."""
        res = testapp.get('/login/')
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'myprecious'
        res = form.submit().follow()
        res = testapp.get(url_for('auth.user_profile'))
        # The delete form is the second form on the page
        res = res.forms[1].submit().follow()
        assert res.status_code == 200
        assert 'Your profile has been deleted' in res
        assert User.query.get(user.id) is None
